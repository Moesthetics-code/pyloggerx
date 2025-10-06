# ================================
# examples/multi_export_example.py
# ================================
"""
Example: Logging to multiple services simultaneously
"""

from pyloggerx import PyLoggerX
import time

def main():
    # Initialize logger with multiple exporters
    logger = PyLoggerX(
        name="multi_export_app",
        level="INFO",
        console=True,
        json_file="logs/app.json",
        text_file="logs/app.log",
        # Multiple remote services
        elasticsearch_url="http://localhost:9200",
        elasticsearch_index="multi-app-logs",
        loki_url="http://localhost:3100",
        loki_labels={"app": "multi-service"},
        sentry_dsn="https://your-sentry-dsn@sentry.io/project-id",
        slack_webhook="https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
        # Configuration
        batch_size=30,
        batch_timeout=5,
        enrichment_data={
            "service": "api-gateway",
            "datacenter": "us-east-1",
            "version": "4.1.0"
        }
    )
    
    logger.info("Multi-export service started")
    
    # Simulate various events
    events = [
        ("info", "User authentication successful", {"user": "john@example.com"}),
        ("info", "Database connection established", {"db": "postgres", "host": "db-01"}),
        ("warning", "High memory usage detected", {"memory_pct": 85}),
        ("error", "API rate limit exceeded", {"ip": "192.168.1.100", "endpoint": "/api/data"}),
        ("critical", "Database connection lost", {"db": "postgres", "retry_count": 3}),
    ]
    
    for level, message, context in events:
        log_func = getattr(logger, level)
        log_func(message, **context)
        time.sleep(1)
    
    # Get statistics
    stats = logger.get_stats()
    logger.info("Service statistics", **stats)
    
    logger.flush()
    
    print("\n✅ Logs sent to all configured services:")
    print("   - Console (colored)")
    print("   - Local files (JSON + text)")
    print("   - Elasticsearch")
    print("   - Grafana Loki")
    print("   - Sentry")
    print("   - Slack")

if __name__ == "__main__":
    main()


# ================================
# examples/advanced_filtering_example.py
# ================================
"""
Example: Advanced filtering and sampling with PyLoggerX v3
"""

from pyloggerx import PyLoggerX
from pyloggerx.filters import LevelFilter, MessageFilter, RateLimitFilter, SamplingFilter
import time
import random

def main():
    # Create filters
    # 1. Only log WARNING and above
    level_filter = LevelFilter(min_level="WARNING")
    
    # 2. Exclude logs containing "debug"
    message_filter = MessageFilter(pattern="debug", exclude=True)
    
    # 3. Rate limit: max 50 logs per minute
    rate_limit_filter = RateLimitFilter(max_logs=50, period=60)
    
    # Initialize logger with filters
    logger = PyLoggerX(
        name="filtered_app",
        level="DEBUG",
        console=True,
        json_file="logs/filtered.json",
        # Apply filters
        filters=[level_filter, message_filter, rate_limit_filter],
        # Enable sampling (keep 50% of logs)
        enable_sampling=True,
        sampling_rate=0.5,
        # Enable rate limiting
        enable_rate_limit=True,
        rate_limit_messages=100,
        rate_limit_period=60
    )
    
    logger.info("Application with filters started")
    
    # Generate many logs
    for i in range(100):
        level = random.choice(['debug', 'info', 'warning', 'error'])
        message = f"Log message {i} with {level} level"
        
        log_func = getattr(logger, level)
        log_func(message, iteration=i, random_value=random.random())
        
        time.sleep(0.1)
    
    # Print statistics
    stats = logger.get_stats()
    print(f"\n📊 Statistics:")
    print(f"   Total logs processed: {stats['total_logs']}")
    print(f"   Sampling enabled: {stats['sampling_enabled']}")
    print(f"   Sampling rate: {stats['sampling_rate']}")
    print(f"   Filters applied: {stats['filters']}")
    
    logger.flush()

if __name__ == "__main__":
    main()
