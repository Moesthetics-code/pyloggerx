import time
import threading
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from collections import deque


class MetricsCollector:
    """Collect and aggregate logging metrics."""
    
    def __init__(self, window_size: int = 300):
        """
        Initialize metrics collector.
        
        Args:
            window_size: Time window in seconds for metrics aggregation
        """
        self.window_size = window_size
        self._metrics = {
            'logs_per_level': {},
            'logs_per_second': deque(maxlen=window_size),
            'avg_log_size': deque(maxlen=1000),
            'errors': deque(maxlen=100),
        }
        self._lock = threading.Lock()
        self._start_time = time.time()
    
    def record_log(self, level: str, size: int = 0):
        """Record a log entry."""
        with self._lock:
            # Count by level
            if level not in self._metrics['logs_per_level']:
                self._metrics['logs_per_level'][level] = 0
            self._metrics['logs_per_level'][level] += 1
            
            # Record timestamp for rate calculation
            self._metrics['logs_per_second'].append(time.time())
            
            # Record size
            if size > 0:
                self._metrics['avg_log_size'].append(size)
    
    def record_error(self, error: str):
        """Record an error."""
        with self._lock:
            self._metrics['errors'].append({
                'timestamp': datetime.now().isoformat(),
                'error': error
            })
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        with self._lock:
            current_time = time.time()
            
            # Calculate logs per second
            recent_logs = [t for t in self._metrics['logs_per_second'] 
                          if current_time - t < 60]  # Last minute
            logs_per_second = len(recent_logs) / 60 if recent_logs else 0
            
            # Calculate average log size
            avg_size = (sum(self._metrics['avg_log_size']) / len(self._metrics['avg_log_size']) 
                       if self._metrics['avg_log_size'] else 0)
            
            # Calculate uptime
            uptime = current_time - self._start_time
            
            return {
                'uptime_seconds': uptime,
                'logs_per_level': dict(self._metrics['logs_per_level']),
                'logs_per_second': round(logs_per_second, 2),
                'avg_log_size_bytes': round(avg_size, 2),
                'recent_errors': list(self._metrics['errors'])[-10:],  # Last 10 errors
                'total_logs': sum(self._metrics['logs_per_level'].values())
            }
    
    def reset(self):
        """Reset all metrics."""
        with self._lock:
            self._metrics = {
                'logs_per_level': {},
                'logs_per_second': deque(maxlen=self.window_size),
                'avg_log_size': deque(maxlen=1000),
                'errors': deque(maxlen=100),
            }
            self._start_time = time.time()


class AlertManager:
    """Manage alerts based on metrics thresholds."""
    
    def __init__(self):
        self.rules: List[Dict[str, Any]] = []
        self._callbacks: List[Callable] = []
        self._triggered_alerts = {}
        self._lock = threading.Lock()
    
    def add_rule(
        self,
        name: str,
        condition: Callable[[Dict[str, Any]], bool],
        cooldown: int = 300,
        message: Optional[str] = None
    ):
        """
        Add an alert rule.
        
        Args:
            name: Alert name
            condition: Function that takes metrics and returns True if alert should trigger
            cooldown: Minimum seconds between alerts
            message: Custom alert message
        """
        self.rules.append({
            'name': name,
            'condition': condition,
            'cooldown': cooldown,
            'message': message or f"Alert triggered: {name}"
        })
    
    def add_callback(self, callback: Callable[[str, str], None]):
        """
        Add a callback for alerts.
        
        Args:
            callback: Function that takes (alert_name, message) when alert triggers
        """
        self._callbacks.append(callback)
    
    def check_metrics(self, metrics: Dict[str, Any]):
        """Check metrics against all rules."""
        current_time = time.time()
        
        with self._lock:
            for rule in self.rules:
                name = rule['name']
                
                # Check cooldown
                if name in self._triggered_alerts:
                    last_trigger = self._triggered_alerts[name]
                    if current_time - last_trigger < rule['cooldown']:
                        continue
                
                # Check condition
                try:
                    if rule['condition'](metrics):
                        self._trigger_alert(name, rule['message'])
                        self._triggered_alerts[name] = current_time
                except Exception as e:
                    print(f"Error checking alert rule '{name}': {e}")
    
    def _trigger_alert(self, name: str, message: str):
        """Trigger an alert."""
        for callback in self._callbacks:
            try:
                callback(name, message)
            except Exception as e:
                print(f"Error in alert callback: {e}")


class HealthMonitor:
    """Monitor logger health and performance."""
    
    def __init__(self, logger, check_interval: int = 60):
        """
        Initialize health monitor.
        
        Args:
            logger: PyLoggerX instance to monitor
            check_interval: Seconds between health checks
        """
        self.logger = logger
        self.check_interval = check_interval
        self.metrics_collector = MetricsCollector()
        self.alert_manager = AlertManager()
        self._running = False
        self._monitor_thread = None
        
        # Setup default alert rules
        self._setup_default_alerts()
    
    def _setup_default_alerts(self):
        """Setup default alert rules."""
        # High error rate
        self.alert_manager.add_rule(
            name="high_error_rate",
            condition=lambda m: m['logs_per_level'].get('ERROR', 0) > 100,
            cooldown=300,
            message="High error rate detected (>100 errors)"
        )
        
        # High log rate
        self.alert_manager.add_rule(
            name="high_log_rate",
            condition=lambda m: m['logs_per_second'] > 100,
            cooldown=300,
            message="High logging rate detected (>100 logs/sec)"
        )
        
        # Exporter circuit breaker open
        def check_circuit_breaker(metrics):
            if 'exporter_metrics' in metrics:
                for name, exp_metrics in metrics['exporter_metrics'].items():
                    if exp_metrics.get('circuit_breaker_open'):
                        return True
            return False
        
        self.alert_manager.add_rule(
            name="exporter_circuit_breaker",
            condition=check_circuit_breaker,
            cooldown=600,
            message="One or more exporters have circuit breaker open"
        )
    
    def start(self):
        """Start monitoring."""
        if self._running:
            return
        
        self._running = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
    
    def stop(self):
        """Stop monitoring."""
        self._running = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self._running:
            try:
                # Collect metrics
                stats = self.logger.get_stats()
                health = self.logger.healthcheck()
                
                # Combine with collector metrics
                metrics = {
                    **self.metrics_collector.get_metrics(),
                    **stats,
                    'health': health
                }
                
                # Check alerts
                self.alert_manager.check_metrics(metrics)
                
            except Exception as e:
                self.metrics_collector.record_error(str(e))
            
            time.sleep(self.check_interval)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current monitoring status."""
        return {
            'running': self._running,
            'metrics': self.metrics_collector.get_metrics(),
            'logger_stats': self.logger.get_stats(),
            'logger_health': self.logger.healthcheck()
        }


def print_dashboard(logger, clear_screen: bool = True):
    """
    Print a monitoring dashboard to console.
    
    Args:
        logger: PyLoggerX instance
        clear_screen: Whether to clear screen before printing
    """
    if clear_screen:
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    stats = logger.get_stats()
    health = logger.healthcheck()
    
    print("=" * 60)
    print("PyLoggerX Monitoring Dashboard")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # General stats
    print("📊 General Statistics:")
    print(f"  Total Logs: {stats['total_logs']}")
    print(f"  Exporters: {stats['exporters']}")
    print(f"  Filters: {stats['filters']}")
    print()
    
    # Rate limiting
    if stats['rate_limit_enabled']:
        print("🚦 Rate Limiting:")
        print(f"  Enabled: Yes")
        print(f"  Max Messages: {stats['rate_limit_messages']}")
        print(f"  Period: {stats['rate_limit_period']}s")
        if 'rate_limit_rejections' in stats:
            print(f"  Rejections: {stats['rate_limit_rejections']}")
        print()
    
    # Exporter health
    print("🏥 Exporter Health:")
    print(f"  Overall Healthy: {'✅ Yes' if health['healthy'] else '❌ No'}")
    for name, is_healthy in health['exporters'].items():
        status = "✅" if is_healthy else "❌"
        print(f"  {status} {name}")
    print()
    
    # Exporter metrics
    if 'exporter_metrics' in stats:
        print("📈 Exporter Metrics:")
        for name, metrics in stats['exporter_metrics'].items():
            print(f"\n  {name}:")
            print(f"    Exported: {metrics['exported_logs']}")
            print(f"    Failed: {metrics['failed_logs']}")
            print(f"    Dropped: {metrics['dropped_logs']}")
            print(f"    Queue: {metrics['queue_size']}")
            if metrics['circuit_breaker_open']:
                print(f"    ⚠️  Circuit Breaker: OPEN (failures: {metrics['consecutive_failures']})")
    
    print()
    print("=" * 60)