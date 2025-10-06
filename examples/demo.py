# ================================
# examples/demo.py
# ================================
"""
Demo script for PyLoggerX - shows all major features
"""
import time
import random
from pyloggerx import PyLoggerX, log

def basic_demo():
    """Demonstrate basic logging features."""
    print("\n🎯 Basic Logging Demo")
    print("=" * 50)
    
    log.info("Application started successfully")
    log.warning("This is a warning message")
    log.error("An error occurred")
    log.debug("Debug information (might not be visible depending on level)")
    
    # With context
    log.info("User action", user_id=123, action="login", ip="192.168.1.1")
    
    # Exception logging
    try:
        result = 1 / 0
    except ZeroDivisionError:
        log.exception("Division by zero error occurred")

def advanced_demo():
    """Demonstrate advanced features."""
    print("\n⚡ Advanced Features Demo")
    print("=" * 50)
    
    # Create custom logger with multiple outputs
    logger = PyLoggerX(
        name="demo_advanced",
        level="DEBUG",
        json_file="demo_logs.json",
        text_file="demo_logs.txt",
        performance_tracking=True,
        include_caller=True,
        enable_rate_limit=True,
        rate_limit_messages=2,
        rate_limit_period=10
    )
    
    # Add persistent context
    logger.add_context(session_id="demo_session_123", version="2.0.0")
    
    # Performance tracking
    with logger.timer("Data Processing"):
        logger.info("Starting data processing")
        time.sleep(0.5)  # Simulate work
        logger.debug("Processing intermediate step")
        time.sleep(0.3)  # More work
        logger.info("Data processing completed")
    
    # Multiple operations for statistics
    operations = ["Database Query", "API Call", "File Processing", "Cache Update"]
    
    for operation in operations:
        with logger.timer(operation):
            # Simulate variable processing time
            time.sleep(random.uniform(0.1, 0.5))
            if random.choice([True, False, True]):  # 66% success rate
                logger.info(f"{operation} completed successfully")
            else:
                logger.warning(f"{operation} completed with warnings")
    
    # Show performance statistics
    stats = logger.get_performance_stats()
    logger.info("Performance Summary", **stats)
    
    # Simulate spam
    print("\n🚫 Spam Logging Test (rate_limit_messages=2, period=10s)")
    print("📝 Expected: Only 2 messages should appear, then blocking for 10s")
    
    for i in range(10):
        logger.warning(f"🔁 Attempt {i+1}/10: This is a spammy warning message!")
        time.sleep(0.1)  # very short delay between logs
    
    # Show stats
    general_stats = logger.get_stats()
    
    print(f"\n✅ Logs written to: demo_logs.txt and demo_logs.json")
    print(f"📊 Total operations tracked: {stats.get('total_operations', 0)}")
    print(f"⏱️  Average duration: {stats.get('avg_duration', 0):.3f}s")
    print(f"🚦 Rate limiting: {general_stats['rate_limit_enabled']}")
    print(f"   - Max messages: {general_stats['rate_limit_messages']}")
    print(f"   - Period: {general_stats['rate_limit_period']}s")
    print(f"   - Total logs processed: {general_stats['total_logs']}")

def error_handling_demo():
    """Demonstrate error handling and logging."""
    print("\n🚨 Error Handling Demo")
    print("=" * 50)
    
    logger = PyLoggerX(name="error_demo")
    
    # Simulate different types of errors
    errors = [
        ("Network Error", ConnectionError("Failed to connect to server")),
        ("File Not Found", FileNotFoundError("config.yaml not found")),
        ("Permission Error", PermissionError("Access denied to /var/log/")),
        ("Value Error", ValueError("Invalid input: expected integer, got string"))
    ]
    
    for error_name, error in errors:
        try:
            raise error
        except Exception as e:
            logger.error(f"{error_name} occurred",
                        error_type=type(e).__name__,
                        error_message=str(e),
                        severity="high" if "Permission" in error_name else "medium")

def json_logging_demo():
    """Demonstrate JSON structured logging."""
    print("\n📄 JSON Logging Demo")
    print("=" * 50)
    
    logger = PyLoggerX(
        name="json_demo",
        console=True,  # Also show in console
        json_file="structured_demo.json"
    )
    
    # Simulate web application logs
    web_events = [
        {"event": "user_login", "user_id": 12345, "ip": "192.168.1.100", "user_agent": "Chrome/91.0"},
        {"event": "page_view", "user_id": 12345, "page": "/dashboard", "load_time": 0.23},
        {"event": "api_call", "user_id": 12345, "endpoint": "/api/users", "method": "GET", "status": 200},
        {"event": "user_logout", "user_id": 12345, "session_duration": 1847}
    ]
    
    logger.info("Web application started", server="web-01", port=8080)
    
    for event_data in web_events:
        event_type = event_data.pop("event")
        logger.info(f"Event: {event_type}", **event_data)
    
    logger.info("Demo completed", events_processed=len(web_events))
    print("✅ Structured logs written to: structured_demo.json")

def rate_limit_detailed_demo():
    """Demonstrate rate limiting in detail."""
    print("\n🚦 Detailed Rate Limiting Demo")
    print("=" * 50)
    
    logger = PyLoggerX(
        name="rate_limit_demo",
        enable_rate_limit=True,
        rate_limit_messages=3,
        rate_limit_period=5
    )
    
    print("Testing: 3 messages max per 5 seconds")
    print("-" * 50)
    
    # First burst - should show 3 messages
    print("\n📤 Burst 1: Sending 5 messages rapidly...")
    for i in range(5):
        logger.info(f"Message {i+1}/5 from burst 1")
        time.sleep(0.1)
    
    # Wait for period to reset
    print("\n⏳ Waiting 5 seconds for rate limit reset...")
    time.sleep(5)
    
    # Second burst - should show 3 messages again
    print("\n📤 Burst 2: Sending 5 messages rapidly...")
    for i in range(5):
        logger.info(f"Message {i+1}/5 from burst 2")
        time.sleep(0.1)
    
    stats = logger.get_stats()
    print(f"\n📊 Total messages processed: {stats['total_logs']} out of 10 attempted")

def main():
    """Run all demos."""
    print("🚀 PyLoggerX Demo")
    print("=" * 60)
    print("This demo showcases all major features of PyLoggerX")
    
    # Run all demos
    basic_demo()
    time.sleep(1)
    
    advanced_demo()
    time.sleep(1)
    
    error_handling_demo()
    time.sleep(1)
    
    json_logging_demo()
    time.sleep(1)
    
    rate_limit_detailed_demo()
    
    print("\n🎉 Demo completed!")
    print("Check the generated log files to see the structured output.")
    print("\nFiles created:")
    print("- demo_logs.txt (human-readable logs)")
    print("- demo_logs.json (structured JSON logs)")
    print("- structured_demo.json (web app simulation logs)")

def demo():
    """Entry point for console script."""
    main()

if __name__ == "__main__":
    main()