# ================================
# examples/async_logging_example.py
# ================================
"""
Example: Async logging with PyLoggerX v3
"""

import asyncio
from pyloggerx import PyLoggerX
import time

async def async_operation(logger, operation_id):
    """Simulate async operation."""
    logger.info(f"Starting async operation {operation_id}")
    
    # Simulate async work
    await asyncio.sleep(0.5)
    
    logger.info(f"Async operation {operation_id} completed")

async def main():
    # Initialize logger
    logger = PyLoggerX(
        name="async_app",
        level="INFO",
        console=True,
        json_file="logs/async.json",
        performance_tracking=True,
        elasticsearch_url="http://localhost:9200"
    )
    
    logger.info("Async application started")
    
    # Create multiple concurrent tasks
    tasks = [async_operation(logger, i) for i in range(10)]
    
    # Run all tasks concurrently
    with logger.timer("all_async_operations"):
        await asyncio.gather(*tasks)
    
    # Show performance stats
    stats = logger.get_performance_stats()
    logger.info("All async operations completed", **stats)
    
    logger.flush()
    print("\n✅ Async operations logged successfully")

if __name__ == "__main__":
    asyncio.run(main())
