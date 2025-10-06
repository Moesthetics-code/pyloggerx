import json
import threading
import time
import atexit
from typing import Dict, Any, List, Optional
from datetime import datetime
from queue import Queue, Empty, Full
import sys


class BaseExporter:
    """Base class for all exporters with production-ready features."""
    
    def __init__(
        self, 
        batch_size: int = 100, 
        batch_timeout: int = 5,
        max_queue_size: int = 10000,
        circuit_breaker_threshold: int = 10,
        circuit_breaker_timeout: int = 60
    ):
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.max_queue_size = max_queue_size
        
        # Queue with size limit
        self._queue = Queue(maxsize=max_queue_size)
        self._batch = []
        self._last_flush = time.time()
        self._running = True
        self._lock = threading.Lock()
        
        # Metrics
        self._total_logs = 0
        self._dropped_logs = 0
        self._exported_logs = 0
        self._failed_logs = 0
        
        # Circuit breaker
        self._consecutive_failures = 0
        self._circuit_breaker_threshold = circuit_breaker_threshold
        self._circuit_breaker_timeout = circuit_breaker_timeout
        self._circuit_open = False
        self._circuit_opened_at = None
        
        # Non-daemon thread for graceful shutdown
        self._worker_thread = threading.Thread(target=self._worker, daemon=False)
        self._worker_thread.start()
        
        # Register cleanup on exit
        atexit.register(self.close)
    
    def export(self, log_data: Dict[str, Any]):
        """Add log to export queue with overflow handling."""
        self._total_logs += 1
        
        try:
            self._queue.put_nowait(log_data)
        except Full:
            self._dropped_logs += 1
            # Alert every 100 dropped logs
            if self._dropped_logs % 100 == 0:
                print(
                    f"Warning: {self.__class__.__name__} dropped {self._dropped_logs} logs "
                    f"(queue full: {self.max_queue_size})",
                    file=sys.stderr
                )
    
    def _check_circuit_breaker(self) -> bool:
        """Check if circuit breaker is open."""
        if not self._circuit_open:
            return True
        
        # Check if timeout has passed
        if time.time() - self._circuit_opened_at > self._circuit_breaker_timeout:
            print(f"Circuit breaker for {self.__class__.__name__} attempting to close", file=sys.stderr)
            self._circuit_open = False
            self._consecutive_failures = 0
            return True
        
        return False
    
    def _record_success(self):
        """Record successful batch send."""
        self._consecutive_failures = 0
        if self._circuit_open:
            print(f"Circuit breaker for {self.__class__.__name__} closed (recovered)", file=sys.stderr)
            self._circuit_open = False
    
    def _record_failure(self):
        """Record failed batch send and check circuit breaker."""
        self._consecutive_failures += 1
        
        if self._consecutive_failures >= self._circuit_breaker_threshold and not self._circuit_open:
            self._circuit_open = True
            self._circuit_opened_at = time.time()
            print(
                f"Circuit breaker OPEN for {self.__class__.__name__} "
                f"after {self._consecutive_failures} failures. "
                f"Will retry in {self._circuit_breaker_timeout}s",
                file=sys.stderr
            )
    
    def _worker(self):
        """Background worker for batching."""
        while self._running:
            try:
                # Get log with timeout
                log_data = self._queue.get(timeout=1)
                
                with self._lock:
                    self._batch.append(log_data)
                    
                    # Check if should flush
                    if (len(self._batch) >= self.batch_size or 
                        time.time() - self._last_flush >= self.batch_timeout):
                        self.flush()
                    
            except Empty:
                # Check timeout
                with self._lock:
                    if self._batch and time.time() - self._last_flush >= self.batch_timeout:
                        self.flush()
    
    def flush(self):
        """Flush batch to remote service."""
        with self._lock:
            if not self._batch:
                return
            
            # Check circuit breaker
            if not self._check_circuit_breaker():
                # Circuit is open, drop batch
                self._failed_logs += len(self._batch)
                self._batch.clear()
                return
            
            batch_copy = self._batch.copy()
            
            try:
                self._send_batch(batch_copy)
                self._exported_logs += len(batch_copy)
                self._record_success()
                self._batch.clear()
                self._last_flush = time.time()
            except Exception as e:
                self._failed_logs += len(batch_copy)
                self._record_failure()
                print(f"Failed to flush batch in {self.__class__.__name__}: {e}", file=sys.stderr)
                # Don't clear batch on failure for potential retry
                # But clear after circuit breaker opens to prevent memory leak
                if self._circuit_open:
                    self._batch.clear()
    
    def _send_batch(self, batch: List[Dict[str, Any]]):
        """Send batch to remote service. Override in subclasses."""
        raise NotImplementedError
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get exporter metrics."""
        return {
            'total_logs': self._total_logs,
            'exported_logs': self._exported_logs,
            'dropped_logs': self._dropped_logs,
            'failed_logs': self._failed_logs,
            'queue_size': self._queue.qsize(),
            'circuit_breaker_open': self._circuit_open,
            'consecutive_failures': self._consecutive_failures
        }
    
    def healthcheck(self) -> bool:
        """Check if exporter is healthy."""
        return not self._circuit_open and self._queue.qsize() < self.max_queue_size * 0.9
    
    def close(self):
        """Close exporter and flush remaining logs."""
        self._running = False
        self.flush()
        if self._worker_thread.is_alive():
            self._worker_thread.join(timeout=5)


class ElasticsearchExporter(BaseExporter):
    """Export logs to Elasticsearch."""
    
    def __init__(
        self,
        url: str,
        index: str = "pyloggerx",
        username: Optional[str] = None,
        password: Optional[str] = None,
        batch_size: int = 100,
        batch_timeout: int = 5,
        timeout: int = 10
    ):
        self.url = url.rstrip('/')
        self.index = index
        self.username = username
        self.password = password
        self.timeout = timeout
        super().__init__(batch_size, batch_timeout)
    
    def _send_batch(self, batch: List[Dict[str, Any]]):
        """Send batch to Elasticsearch using bulk API."""
        try:
            import requests
        except ImportError:
            raise ImportError("requests library required. Install: pip install requests")
        
        # Build bulk request
        bulk_data = []
        for log in batch:
            bulk_data.append(json.dumps({"index": {"_index": self.index}}))
            bulk_data.append(json.dumps(log))
        
        body = '\n'.join(bulk_data) + '\n'
        
        auth = None
        if self.username and self.password:
            auth = (self.username, self.password)
        
        response = requests.post(
            f"{self.url}/_bulk",
            data=body,
            headers={"Content-Type": "application/x-ndjson"},
            auth=auth,
            timeout=self.timeout
        )
        response.raise_for_status()


class LokiExporter(BaseExporter):
    """Export logs to Grafana Loki."""
    
    def __init__(
        self,
        url: str,
        labels: Optional[Dict[str, str]] = None,
        batch_size: int = 100,
        batch_timeout: int = 5,
        timeout: int = 10
    ):
        self.url = url.rstrip('/')
        self.labels = labels or {"job": "pyloggerx"}
        self.timeout = timeout
        super().__init__(batch_size, batch_timeout)
    
    def _send_batch(self, batch: List[Dict[str, Any]]):
        """Send batch to Loki."""
        try:
            import requests
        except ImportError:
            raise ImportError("requests library required. Install: pip install requests")
        
        streams = {}
        
        for log in batch:
            label_set = {**self.labels}
            if 'level' in log:
                label_set['level'] = log['level']
            
            label_str = '{' + ','.join(f'{k}="{v}"' for k, v in sorted(label_set.items())) + '}'
            
            if label_str not in streams:
                streams[label_str] = []
            
            timestamp = log.get('timestamp', datetime.now().isoformat())
            try:
                timestamp_ns = str(int(datetime.fromisoformat(timestamp).timestamp() * 1e9))
            except:
                timestamp_ns = str(int(time.time() * 1e9))
                
            log_line = json.dumps(log)
            streams[label_str].append([timestamp_ns, log_line])
        
        loki_streams = []
        for label_str, values in streams.items():
            stream_labels = {}
            label_content = label_str.strip('{}')
            if label_content:
                for pair in label_content.split(','):
                    if '=' in pair:
                        k, v = pair.split('=', 1)
                        stream_labels[k] = v.strip('"')
            
            loki_streams.append({
                "stream": stream_labels,
                "values": values
            })
        
        response = requests.post(
            f"{self.url}/loki/api/v1/push",
            json={"streams": loki_streams},
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )
        response.raise_for_status()


class SentryExporter(BaseExporter):
    """Export errors to Sentry."""
    
    def __init__(
        self,
        dsn: str,
        environment: str = "production",
        batch_size: int = 1,
        batch_timeout: int = 1
    ):
        self.dsn = dsn
        self.environment = environment
        self._sentry_sdk = None
        self._init_sentry()
        super().__init__(batch_size, batch_timeout)
    
    def _init_sentry(self):
        """Initialize Sentry SDK."""
        try:
            import sentry_sdk
            
            # Validate DSN format before initializing
            if not self.dsn or self.dsn == "https://your-sentry-dsn":
                print("Warning: Invalid or placeholder Sentry DSN. Sentry logging disabled.", file=sys.stderr)
                return
            
            sentry_sdk.init(
                dsn=self.dsn,
                environment=self.environment,
                traces_sample_rate=0.1
            )
            self._sentry_sdk = sentry_sdk
        except ImportError:
            raise ImportError("sentry-sdk required. Install: pip install sentry-sdk")
        except Exception as e:
            print(f"Warning: Failed to initialize Sentry: {e}. Sentry logging disabled.", file=sys.stderr)
            self._sentry_sdk = None
    
    def _send_batch(self, batch: List[Dict[str, Any]]):
        """Send batch to Sentry."""
        if not self._sentry_sdk:
            return
        
        for log in batch:
            level = log.get('level', 'INFO').lower()
            
            if level not in ['error', 'critical', 'exception']:
                continue
            
            with self._sentry_sdk.push_scope() as scope:
                for key, value in log.items():
                    if key not in ['timestamp', 'level', 'message']:
                        scope.set_extra(key, value)
                
                scope.level = level
                
                if 'exception' in log:
                    self._sentry_sdk.capture_exception(Exception(log.get('message', 'Error')))
                else:
                    self._sentry_sdk.capture_message(log.get('message', 'Error'))


class DatadogExporter(BaseExporter):
    """Export logs to Datadog."""
    
    def __init__(
        self,
        api_key: str,
        site: str = "datadoghq.com",
        service: str = "pyloggerx",
        batch_size: int = 100,
        batch_timeout: int = 5,
        timeout: int = 10
    ):
        self.api_key = api_key
        self.site = site
        self.service = service
        self.timeout = timeout
        super().__init__(batch_size, batch_timeout)
    
    def _send_batch(self, batch: List[Dict[str, Any]]):
        """Send batch to Datadog."""
        try:
            import requests
        except ImportError:
            raise ImportError("requests library required. Install: pip install requests")
        
        dd_logs = []
        for log in batch:
            dd_log = {
                "ddsource": "python",
                "ddtags": f"service:{self.service}",
                "hostname": log.get('hostname', 'unknown'),
                "message": log.get('message', ''),
                "status": log.get('level', 'INFO').lower(),
                "timestamp": log.get('timestamp', datetime.now().isoformat()),
            }
            for k, v in log.items():
                if k not in ['message', 'level', 'timestamp', 'hostname']:
                    dd_log[k] = v
            dd_logs.append(dd_log)
        
        response = requests.post(
            f"https://http-intake.logs.{self.site}/v1/input",
            json=dd_logs,
            headers={
                "DD-API-KEY": self.api_key,
                "Content-Type": "application/json"
            },
            timeout=self.timeout
        )
        response.raise_for_status()


class SlackExporter(BaseExporter):
    """Export logs to Slack."""
    
    def __init__(
        self,
        webhook_url: str,
        channel: Optional[str] = None,
        username: str = "PyLoggerX",
        min_level: str = "WARNING",
        batch_size: int = 1,
        batch_timeout: int = 1,
        timeout: int = 10
    ):
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username
        self.min_level = min_level.upper()
        self.timeout = timeout
        self._level_order = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3, 'CRITICAL': 4}
        self._min_level_value = self._level_order.get(self.min_level, 2)
        super().__init__(batch_size, batch_timeout)
    
    def _send_batch(self, batch: List[Dict[str, Any]]):
        """Send batch to Slack."""
        try:
            import requests
        except ImportError:
            raise ImportError("requests library required. Install: pip install requests")
        
        for log in batch:
            level = log.get('level', 'INFO').upper()
            level_value = self._level_order.get(level, 1)
            
            if level_value < self._min_level_value:
                continue
            
            color_map = {
                'DEBUG': '#808080',
                'INFO': '#36a64f',
                'WARNING': '#ff9900',
                'ERROR': '#ff0000',
                'CRITICAL': '#8b0000'
            }
            color = color_map.get(level, '#808080')
            
            message = {
                "username": self.username,
                "attachments": [{
                    "color": color,
                    "title": f"{level}: {log.get('message', 'No message')}",
                    "text": json.dumps({k: v for k, v in log.items() if k != 'message'}, indent=2),
                    "footer": "PyLoggerX",
                    "ts": int(datetime.now().timestamp())
                }]
            }
            
            if self.channel:
                message["channel"] = self.channel
            
            response = requests.post(
                self.webhook_url,
                json=message,
                timeout=self.timeout
            )
            response.raise_for_status()


class WebhookExporter(BaseExporter):
    """Export logs to generic webhook."""
    
    def __init__(
        self,
        url: str,
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        batch_size: int = 100,
        batch_timeout: int = 5,
        timeout: int = 10
    ):
        self.url = url
        self.method = method.upper()
        self.headers = headers or {"Content-Type": "application/json"}
        self.timeout = timeout
        super().__init__(batch_size, batch_timeout)
    
    def _send_batch(self, batch: List[Dict[str, Any]]):
        """Send batch to webhook."""
        try:
            import requests
        except ImportError:
            raise ImportError("requests library required. Install: pip install requests")
        
        payload = {
            "logs": batch,
            "count": len(batch),
            "timestamp": datetime.now().isoformat()
        }
        
        response = requests.request(
            method=self.method,
            url=self.url,
            json=payload,
            headers=self.headers,
            timeout=self.timeout
        )
        response.raise_for_status()