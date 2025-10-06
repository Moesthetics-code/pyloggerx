"""
Production-ready example for PyLoggerX with all advanced features.
"""

import time
import json
from pyloggerx import PyLoggerX
from pyloggerx.config import load_config, save_example_config, EXAMPLE_CONFIGS
from pyloggerx.monitoring import HealthMonitor, print_dashboard, MetricsCollector, AlertManager


def example_1_basic_production():
    """Example 1: Basic production setup with monitoring."""
    print("\n" + "="*60)
    print("Example 1: Basic Production Setup")
    print("="*60)
    
    logger = PyLoggerX(
        name="production_app",
        level="INFO",
        console=True,
        json_file="logs/prod.json",
        text_file="logs/prod.txt",
        
        # Compression enabled
        max_bytes=10 * 1024 * 1024,  # 10MB
        backup_count=5,
        
        # Rate limiting with priority
        enable_rate_limit=True,
        rate_limit_messages=50,
        rate_limit_period=60,
        
        # Performance tracking
        performance_tracking=True,
        include_caller=True,
    )
    
    # Log some events
    logger.info("Application started", version="1.0.0", environment="production")
    logger.warning("High memory usage detected", memory_percent=85.5)
    logger.error("Database connection failed", db_host="db-01", retry_count=3)
    
    # Show stats
    stats = logger.get_stats()
    print(f"\n📊 Stats: {stats['total_logs']} logs processed")
    print(f"🚦 Rate limit: {stats['rate_limit_messages']} msgs/{stats['rate_limit_period']}s")
    
    # Healthcheck
    health = logger.healthcheck()
    print(f"🏥 Health: {'✅ Healthy' if health['healthy'] else '❌ Unhealthy'}")
    
    logger.close()


def example_2_with_monitoring():
    """Example 2: Advanced monitoring with metrics and alerts."""
    print("\n" + "="*60)
    print("Example 2: Advanced Monitoring & Alerting")
    print("="*60)
    
    logger = PyLoggerX(
        name="monitored_service",
        level="INFO",
        console=True,
        json_file="logs/monitored.json",
        enable_rate_limit=True,
        rate_limit_messages=100,
        rate_limit_period=60,
        performance_tracking=True,
    )
    
    # Setup monitoring
    monitor = HealthMonitor(logger, check_interval=2)
    
    # Add custom alert
    def custom_alert_condition(metrics):
        """Alert if more than 5 errors in total."""
        return metrics.get('logs_per_level', {}).get('ERROR', 0) > 5
    
    monitor.alert_manager.add_rule(
        name="custom_error_threshold",
        condition=custom_alert_condition,
        cooldown=10,
        message="⚠️ More than 5 errors detected!"
    )
    
    # Alert callback
    alert_triggered = []
    def alert_handler(name, message):
        alert_triggered.append(f"{name}: {message}")
        print(f"\n🚨 ALERT: {message}")
    
    monitor.alert_manager.add_callback(alert_handler)
    monitor.start()
    
    print("\n🔄 Simulating workload with error spike...")
    
    # Simulate normal operations
    for i in range(5):
        logger.info(f"Processing request {i+1}")
        monitor.metrics_collector.record_log('INFO', 120)
        time.sleep(0.2)
    
    # Simulate error spike (should trigger alert)
    for i in range(8):
        logger.error(f"Error occurred {i+1}", error_code=500)
        monitor.metrics_collector.record_log('ERROR', 200)
        time.sleep(0.2)
    
    # Wait for monitoring to detect
    time.sleep(3)
    
    # Show metrics
    collector_metrics = monitor.metrics_collector.get_metrics()
    print(f"\n📈 Metrics Collector:")
    print(f"  Total logs: {collector_metrics['total_logs']}")
    print(f"  Logs per level: {collector_metrics['logs_per_level']}")
    print(f"  Logs/second: {collector_metrics['logs_per_second']}")
    print(f"  Avg log size: {collector_metrics['avg_log_size_bytes']} bytes")
    
    if alert_triggered:
        print(f"\n🚨 Alerts triggered: {len(alert_triggered)}")
        for alert in alert_triggered:
            print(f"  - {alert}")
    
    monitor.stop()
    logger.close()


def example_3_config_management():
    """Example 3: Configuration management."""
    print("\n" + "="*60)
    print("Example 3: Configuration Management")
    print("="*60)
    
    # 1. Create custom config
    custom_config = {
        "name": "config_demo",
        "level": "INFO",
        "console": True,
        "json_file": "logs/config_demo.json",
        "enable_rate_limit": True,
        "rate_limit_messages": 10,
        "rate_limit_period": 5,
        "performance_tracking": True
    }
    
    # Save to file
    with open("custom_config.json", "w") as f:
        json.dump(custom_config, f, indent=2)
    print("✅ Custom config saved to custom_config.json")
    
    # 2. Load and use config
    config = load_config(
        config_file="custom_config.json",
        from_env=False,  # Don't override with env vars for this demo
        defaults={"backup_count": 3}
    )
    
    print(f"\n📝 Loaded configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    # 3. Create logger from config
    logger = PyLoggerX(**config)
    logger.info("Logger created from config file")
    
    # 4. Show all available config templates
    print(f"\n📚 Available config templates:")
    for template_name in EXAMPLE_CONFIGS.keys():
        print(f"  - {template_name}")
    
    logger.close()


def example_4_rate_limiting_detailed():
    """Example 4: Detailed rate limiting behavior."""
    print("\n" + "="*60)
    print("Example 4: Rate Limiting Detailed Behavior")
    print("="*60)
    
    logger = PyLoggerX(
        name="rate_limit_detailed",
        level="DEBUG",
        console=True,
        enable_rate_limit=True,
        rate_limit_messages=3,
        rate_limit_period=5
    )
    
    print("\n🚦 Configuration: 3 messages per 5 seconds")
    print("Priority: ERROR and CRITICAL are NEVER rate limited\n")
    
    # Test 1: INFO messages (will be limited)
    print("Test 1: Sending 10 INFO messages")
    for i in range(10):
        logger.info(f"INFO {i+1}")
        time.sleep(0.1)
    
    stats = logger.get_stats()
    print(f"✅ Processed: {stats['total_logs']} (expected: 3)")
    if 'rate_limit_rejections' in stats:
        print(f"❌ Rejected: {stats['rate_limit_rejections']}")
    
    # Wait for period reset
    print("\n⏳ Waiting 5s for rate limit reset...")
    time.sleep(5)
    
    # Test 2: Mixed levels
    print("\nTest 2: Sending mixed levels (INFO + ERROR)")
    logger.info("INFO 1")
    logger.info("INFO 2")
    logger.info("INFO 3")
    logger.info("INFO 4 - should be blocked")
    logger.error("ERROR 1 - should ALWAYS pass")
    logger.error("ERROR 2 - should ALWAYS pass")
    logger.critical("CRITICAL 1 - should ALWAYS pass")
    
    stats = logger.get_stats()
    print(f"\n📊 Final stats: {stats['total_logs']} total logs")
    
    logger.close()


def example_5_performance_advanced():
    """Example 5: Advanced performance tracking."""
    print("\n" + "="*60)
    print("Example 5: Advanced Performance Tracking")
    print("="*60)
    
    logger = PyLoggerX(
        name="perf_advanced",
        level="INFO",
        console=True,
        performance_tracking=True
    )
    
    operations = [
        ("Fast Operation", 0.05),
        ("Medium Operation", 0.15),
        ("Slow Operation", 0.3),
        ("Database Query", 0.1),
        ("API Call", 0.2),
        ("Cache Lookup", 0.02)
    ]
    
    print("\n⏱️ Executing operations...")
    
    for op_name, duration in operations:
        with logger.timer(op_name):
            time.sleep(duration)
    
    # Get detailed stats
    perf_stats = logger.get_performance_stats()
    
    print(f"\n📊 Performance Summary:")
    print(f"  Operations: {perf_stats['total_operations']}")
    print(f"  Average: {perf_stats['avg_duration']:.3f}s")
    print(f"  Fastest: {perf_stats['min_duration']:.3f}s")
    print(f"  Slowest: {perf_stats['max_duration']:.3f}s")
    
    print(f"\n📋 Operations ranked by duration:")
    sorted_ops = sorted(
        perf_stats['operations'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    for i, (op, duration) in enumerate(sorted_ops, 1):
        print(f"  {i}. {op}: {duration:.3f}s")
    
    logger.close()


def example_6_dashboard_monitoring():
    """Example 6: Live dashboard monitoring."""
    print("\n" + "="*60)
    print("Example 6: Live Dashboard Monitoring")
    print("="*60)
    
    logger = PyLoggerX(
        name="dashboard_demo",
        level="INFO",
        console=False,  # Disable console to keep dashboard clean
        json_file="logs/dashboard.json",
        enable_rate_limit=True,
        rate_limit_messages=20,
        rate_limit_period=10,
        performance_tracking=True
    )
    
    print("\n🔄 Running workload... (dashboard will show final state)")
    
    # Simulate varied workload
    for i in range(30):
        if i % 5 == 0:
            logger.warning(f"Warning {i}")
        elif i % 7 == 0:
            logger.error(f"Error {i}")
        else:
            logger.info(f"Info {i}")
        time.sleep(0.05)
    
    # Show dashboard
    print("\n" + "="*60)
    print_dashboard(logger, clear_screen=False)
    
    logger.close()


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("PyLoggerX Production-Ready Examples")
    print("="*70)
    print("\nThese examples demonstrate:")
    print("  ✅ Circuit breakers")
    print("  ✅ Rate limiting with priorities")
    print("  ✅ Health monitoring & alerts")
    print("  ✅ Configuration management")
    print("  ✅ Metrics collection")
    print("  ✅ Performance tracking")
    print("  ✅ Live dashboards")
    
    try:
        example_1_basic_production()
        time.sleep(1)
        
        example_2_with_monitoring()
        time.sleep(1)
        
        example_3_config_management()
        time.sleep(1)
        
        example_4_rate_limiting_detailed()
        time.sleep(1)
        
        example_5_performance_advanced()
        time.sleep(1)
        
        example_6_dashboard_monitoring()
        
        print("\n" + "="*70)
        print("✅ All examples completed successfully!")
        print("="*70)
        print("\n📁 Check the logs/ directory for generated log files")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Examples interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()