import logging
import json
import sys
import os
from datetime import datetime
from typing import Optional, Union, Dict, Any, List
from pathlib import Path

from .formatters import ColorFormatter, JSONFormatter
from .handlers import RotatingFileHandler, TimedRotatingHandler
from .utils import ensure_directory


class PyLoggerX:
    """
    Modern logging wrapper with colors, JSON export, rotation, and remote logging.
    
    Version 1.0.0 Features:
    - Remote logging to Elasticsearch, Loki, Sentry, Datadog, etc.
    - Advanced filtering capabilities
    - Rate limiting for logs
    - Batch processing for remote exports
    - Async logging support
    - Log sampling for high-volume scenarios
    - Custom metadata enrichment
    """
    
    LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    EMOJIS = {
        'DEBUG': '🐞',
        'INFO': '✅',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '💀'
    }
    
    def __init__(
        self,
        name: str = "PyLoggerX",
        level: str = "INFO",
        console: bool = True,
        colors: bool = True,
        json_file: Optional[str] = None,
        text_file: Optional[str] = None,
        max_bytes: int = 10 * 1024 * 1024,
        backup_count: int = 5,
        rotation_when: str = "midnight",
        rotation_interval: int = 1,
        format_string: Optional[str] = None,
        include_caller: bool = False,
        performance_tracking: bool = False,
        elasticsearch_url: Optional[str] = None,
        elasticsearch_index: str = "pyloggerx",
        elasticsearch_username: Optional[str] = None,
        elasticsearch_password: Optional[str] = None,
        loki_url: Optional[str] = None,
        loki_labels: Optional[Dict[str, str]] = None,
        sentry_dsn: Optional[str] = None,
        sentry_environment: str = "production",
        datadog_api_key: Optional[str] = None,
        datadog_site: str = "datadoghq.com",
        slack_webhook: Optional[str] = None,
        slack_channel: Optional[str] = None,
        webhook_url: Optional[str] = None,
        webhook_method: str = "POST",
        enable_sampling: bool = False,
        sampling_rate: float = 1.0,
        enable_rate_limit: bool = False,
        rate_limit_messages: int = 100,
        rate_limit_period: int = 60,
        batch_size: int = 100,
        batch_timeout: int = 5,
        enrichment_data: Optional[Dict[str, Any]] = None,
        filters: Optional[List[Any]] = None
    ):
        """Initialize the PyLoggerX instance."""
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.LEVELS.get(level.upper(), logging.INFO))
        self.colors = colors
        self.include_caller = include_caller
        self.performance_tracking = performance_tracking
        self._performance_data = {}
        
        # Version 3 - New attributes with proper initialization
        self.enable_sampling = enable_sampling
        self.sampling_rate = sampling_rate
        self.enable_rate_limit = enable_rate_limit
        self.rate_limit_messages = rate_limit_messages
        self.rate_limit_period = rate_limit_period
        self.enrichment_data = enrichment_data or {}
        self._exporters = []
        self._filters = filters or []
        self._log_count = 0
        self._rate_limit_data = {}
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Setup handlers
        if console:
            self._setup_console_handler(format_string)
        
        if json_file:
            self._setup_json_handler(json_file, max_bytes, backup_count)
        
        if text_file:
            self._setup_text_handler(text_file, max_bytes, backup_count)
        
        self._setup_exporters(
            elasticsearch_url=elasticsearch_url,
            elasticsearch_index=elasticsearch_index,
            elasticsearch_username=elasticsearch_username,
            elasticsearch_password=elasticsearch_password,
            loki_url=loki_url,
            loki_labels=loki_labels,
            sentry_dsn=sentry_dsn,
            sentry_environment=sentry_environment,
            datadog_api_key=datadog_api_key,
            datadog_site=datadog_site,
            slack_webhook=slack_webhook,
            slack_channel=slack_channel,
            webhook_url=webhook_url,
            webhook_method=webhook_method,
            batch_size=batch_size,
            batch_timeout=batch_timeout
        )
        
        # Apply filters
        for filter_obj in self._filters:
            self.logger.addFilter(filter_obj)
    
    def _setup_console_handler(self, format_string: Optional[str] = None):
        """Setup colorful console handler."""
        handler = logging.StreamHandler(sys.stdout)
        formatter = ColorFormatter(
            colors=self.colors,
            format_string=format_string,
            include_caller=self.include_caller
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def _setup_json_handler(self, filepath: str, max_bytes: int, backup_count: int):
        """Setup JSON file handler with rotation."""
        ensure_directory(filepath)
        handler = RotatingFileHandler(
            filename=filepath,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        formatter = JSONFormatter(include_caller=self.include_caller)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def _setup_text_handler(self, filepath: str, max_bytes: int, backup_count: int):
        """Setup text file handler with rotation."""
        ensure_directory(filepath)
        handler = RotatingFileHandler(
            filename=filepath,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)-8s : %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def _setup_exporters(self, **kwargs):
        """Setup remote exporters (v3)."""
        from .exporters import (
            ElasticsearchExporter, LokiExporter, SentryExporter,
            DatadogExporter, SlackExporter, WebhookExporter
        )
        
        # Elasticsearch
        if kwargs.get('elasticsearch_url'):
            exporter = ElasticsearchExporter(
                url=kwargs['elasticsearch_url'],
                index=kwargs.get('elasticsearch_index', 'pyloggerx'),
                username=kwargs.get('elasticsearch_username'),
                password=kwargs.get('elasticsearch_password'),
                batch_size=kwargs.get('batch_size', 100),
                batch_timeout=kwargs.get('batch_timeout', 5)
            )
            self._exporters.append(exporter)
        
        # Loki
        if kwargs.get('loki_url'):
            exporter = LokiExporter(
                url=kwargs['loki_url'],
                labels=kwargs.get('loki_labels', {}),
                batch_size=kwargs.get('batch_size', 100),
                batch_timeout=kwargs.get('batch_timeout', 5)
            )
            self._exporters.append(exporter)
        
        # Sentry
        if kwargs.get('sentry_dsn'):
            exporter = SentryExporter(
                dsn=kwargs['sentry_dsn'],
                environment=kwargs.get('sentry_environment', 'production')
            )
            self._exporters.append(exporter)
        
        # Datadog
        if kwargs.get('datadog_api_key'):
            exporter = DatadogExporter(
                api_key=kwargs['datadog_api_key'],
                site=kwargs.get('datadog_site', 'datadoghq.com'),
                batch_size=kwargs.get('batch_size', 100),
                batch_timeout=kwargs.get('batch_timeout', 5)
            )
            self._exporters.append(exporter)
        
        # Slack
        if kwargs.get('slack_webhook'):
            exporter = SlackExporter(
                webhook_url=kwargs['slack_webhook'],
                channel=kwargs.get('slack_channel')
            )
            self._exporters.append(exporter)
        
        # Generic Webhook
        if kwargs.get('webhook_url'):
            exporter = WebhookExporter(
                url=kwargs['webhook_url'],
                method=kwargs.get('webhook_method', 'POST')
            )
            self._exporters.append(exporter)
    
    def _should_log(self, level: str, message: str) -> bool:
        """Check if log should be processed (v3 - sampling & rate limiting)."""
        import random
        import time
        
        # Sampling
        if self.enable_sampling and random.random() > self.sampling_rate:
            return False
        
        # Rate limiting with priority - NEVER limit ERROR and CRITICAL
        if self.enable_rate_limit:
            # Priority: ERROR and CRITICAL always pass
            if level in ['ERROR', 'CRITICAL']:
                return True
            
            current_time = time.time()
            
            # Optimization: Use level directly as key
            if level not in self._rate_limit_data:
                self._rate_limit_data[level] = [0, current_time, 0]  # [count, start_time, rejected_count]
            
            data = self._rate_limit_data[level]
            
            # Reset if period expired
            if current_time - data[1] > self.rate_limit_period:
                # Log rejected count before reset
                if data[2] > 0:
                    print(
                        f"Rate limit: {data[2]} {level} logs rejected in last period",
                        file=sys.stderr
                    )
                data[0] = 0
                data[1] = current_time
                data[2] = 0
            
            # Check limit BEFORE incrementing
            if data[0] >= self.rate_limit_messages:
                data[2] += 1  # Track rejected logs
                return False
            
            data[0] += 1
        
        return True
    
    def _export_to_remote(self, log_data: Dict[str, Any]):
        """Export log to remote services (v3)."""
        for exporter in self._exporters:
            try:
                exporter.export(log_data)
            except Exception as e:
                # Don't fail if remote logging fails
                print(f"Failed to export to {exporter.__class__.__name__}: {e}", file=sys.stderr)
    
    def _log_with_context(self, level: str, message: str, **kwargs):
        """Log message with additional context."""
        # Check if should log (v3)
        if not self._should_log(level, message):
            return
        
        # Increment log count
        self._log_count += 1
        
        # Merge enrichment data
        log_data = {
            'emoji': self.EMOJIS.get(level, ''),
            **self.enrichment_data,
            **kwargs
        }
        
        if self.performance_tracking and 'duration' in kwargs:
            self._performance_data[message] = kwargs['duration']
        
        # Log locally
        getattr(self.logger, level.lower())(message, extra=log_data)
        
        # Export to remote services (v3)
        if self._exporters:
            remote_log_data = {
                'timestamp': datetime.now().isoformat(),
                'level': level,
                'logger': self.name,
                'message': message,
                **log_data
            }
            self._export_to_remote(remote_log_data)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self._log_with_context('DEBUG', message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self._log_with_context('INFO', message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self._log_with_context('WARNING', message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self._log_with_context('ERROR', message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self._log_with_context('CRITICAL', message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback."""
        self.logger.exception(message, extra={'emoji': self.EMOJIS['ERROR'], **kwargs})
    
    def set_level(self, level: str):
        """Change logging level."""
        self.logger.setLevel(self.LEVELS.get(level.upper(), logging.INFO))
    
    def add_context(self, **kwargs):
        """Add context to all future logs."""
        for handler in self.logger.handlers:
            if hasattr(handler.formatter, 'add_context'):
                handler.formatter.add_context(**kwargs)
    
    def add_enrichment(self, **kwargs):
        """Add enrichment data to all logs (v3)."""
        self.enrichment_data.update(kwargs)
    
    def add_filter(self, filter_obj):
        """Add a log filter (v3)."""
        self._filters.append(filter_obj)
        self.logger.addFilter(filter_obj)
    
    def timer(self, operation_name: str):
        """Context manager for timing operations."""
        return LogTimer(self, operation_name)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        if not self.performance_tracking:
            return {}
        
        stats = {}
        if self._performance_data:
            durations = list(self._performance_data.values())
            stats = {
                'total_operations': len(durations),
                'avg_duration': sum(durations) / len(durations),
                'max_duration': max(durations),
                'min_duration': min(durations),
                'operations': dict(self._performance_data)
            }
        
        return stats
    
    def get_stats(self) -> Dict[str, Any]:
        """Get general logging statistics (v3)."""
        return {
            'total_logs': self._log_count,
            'exporters': len(self._exporters),
            'filters': len(self._filters),
            'sampling_enabled': self.enable_sampling,
            'sampling_rate': self.sampling_rate if self.enable_sampling else None,
            'rate_limit_enabled': self.enable_rate_limit,
            'rate_limit_messages': self.rate_limit_messages if self.enable_rate_limit else None,
            'rate_limit_period': self.rate_limit_period if self.enable_rate_limit else None
        }
        
    def healthcheck(self) -> Dict[str, Any]:
        """Check health of logger and all exporters."""
        health = {
            'healthy': True,
            'exporters': {}
        }
        
        for exporter in self._exporters:
            name = exporter.__class__.__name__
            if hasattr(exporter, 'healthcheck'):
                is_healthy = exporter.healthcheck()
                health['exporters'][name] = is_healthy
                if not is_healthy:
                    health['healthy'] = False
        
        return health
    
    def clear_performance_stats(self):
        """Clear performance statistics."""
        self._performance_data.clear()
    
    def flush(self):
        """Flush all exporters (v3)."""
        for exporter in self._exporters:
            if hasattr(exporter, 'flush'):
                exporter.flush()
    
    def close(self):
        """Close all handlers and exporters (v3)."""
        self.flush()
        for handler in self.logger.handlers:
            handler.close()
        for exporter in self._exporters:
            if hasattr(exporter, 'close'):
                exporter.close()


class LogTimer:
    """Context manager for timing operations."""
    
    def __init__(self, logger: PyLoggerX, operation_name: str):
        self.logger = logger
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.debug(f"Starting {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            
            # CORRECTION: Utiliser le nom d'opération comme clé pour les stats
            if self.logger.performance_tracking:
                self.logger._performance_data[self.operation_name] = duration
            
            if exc_type:
                self.logger.error(
                    f"{self.operation_name} failed after {duration:.3f}s",
                    duration=duration,
                    error_type=exc_type.__name__ if exc_type else None
                )
            else:
                self.logger.info(
                    f"{self.operation_name} completed in {duration:.3f}s",
                    duration=duration
                )


# Global default logger instance
log = PyLoggerX()