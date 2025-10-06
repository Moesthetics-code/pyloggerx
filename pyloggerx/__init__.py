"""
PyLoggerX - Modern, colorful and production-ready logging for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PyLoggerX provides a simple, modern interface for Python logging with:
- Colorful console output
- JSON export capabilities
- Automatic log rotation with compression
- Multiple output formats
- Minimal configuration required
- Remote logging (Elasticsearch, Loki, Sentry, etc.)
- Production-ready features (circuit breakers, rate limiting, health monitoring)

Basic usage:
    >>> from pyloggerx import log
    >>> log.info("Hello, world!")
    >>> log.warning("This is a warning")
    >>> log.error("Something went wrong")

Advanced usage with all production features:
    >>> from pyloggerx import PyLoggerX
    >>> from pyloggerx.monitoring import HealthMonitor
    >>> from pyloggerx.config import load_config
    >>> 
    >>> # Load from config file
    >>> config = load_config("config.json", from_env=True)
    >>> logger = PyLoggerX(**config)
    >>> 
    >>> # Start monitoring
    >>> monitor = HealthMonitor(logger)
    >>> monitor.start()
    >>> 
    >>> # Use logger
    >>> logger.info("Application started")
    >>> 
    >>> # Check health
    >>> health = logger.healthcheck()
    >>> stats = logger.get_stats()
"""

__version__ = "1.0.0"
__author__ = "Mohamed NDIAYE"
__email__ = "mintok2000@gmail.com"
__license__ = "MIT"
__description__ = "Modern, colorful and production-ready logging for Python"
__url__ = "https://github.com/Moesthetics-code/pyloggerx"

# Core components
from .core import PyLoggerX, log, LogTimer

# Formatters
from .formatters import ColorFormatter, JSONFormatter

# Handlers with compression support
from .handlers import (
    RotatingFileHandler,
    TimedRotatingHandler,
    AsyncFileHandler
)

# Remote exporters with circuit breakers
from .exporters import (
    BaseExporter,
    ElasticsearchExporter,
    LokiExporter,
    SentryExporter,
    DatadogExporter,
    SlackExporter,
    WebhookExporter
)

# Filters
from .filters import (
    LevelFilter,
    MessageFilter,
    RateLimitFilter,
    SamplingFilter
)

# Adapters for compatibility
from .adapters import StructlogAdapter, LoguruAdapter

# Configuration system
from .config import (
    ConfigLoader,
    ConfigValidator,
    load_config,
    save_example_config,
    EXAMPLE_CONFIGS
)

# Monitoring and metrics
from .monitoring import (
    MetricsCollector,
    AlertManager,
    HealthMonitor,
    print_dashboard
)

# Utilities
from .utils import (
    setup_logger,
    configure_logging,
    ensure_directory,
    get_caller_info
)

__all__ = [
    # Core
    'PyLoggerX',
    'log',
    'LogTimer',
    
    # Formatters
    'ColorFormatter',
    'JSONFormatter',
    
    # Handlers
    'RotatingFileHandler',
    'TimedRotatingHandler',
    'AsyncFileHandler',
    
    # Exporters
    'BaseExporter',
    'ElasticsearchExporter',
    'LokiExporter',
    'SentryExporter',
    'DatadogExporter',
    'SlackExporter',
    'WebhookExporter',
    
    # Filters
    'LevelFilter',
    'MessageFilter',
    'RateLimitFilter',
    'SamplingFilter',
    
    # Adapters
    'StructlogAdapter',
    'LoguruAdapter',
    
    # Configuration
    'ConfigLoader',
    'ConfigValidator',
    'load_config',
    'save_example_config',
    'EXAMPLE_CONFIGS',
    
    # Monitoring
    'MetricsCollector',
    'AlertManager',
    'HealthMonitor',
    'print_dashboard',
    
    # Utilities
    'setup_logger',
    'configure_logging',
    'ensure_directory',
    'get_caller_info',
]

# Version info
VERSION = __version__
VERSION_INFO = tuple(int(x) for x in __version__.split('.'))