"""
Log filters for PyLoggerX .

Supports:
- Level-based filtering
- Message pattern filtering
- Rate limiting
- Custom filters
"""

import logging
import re
import time
from typing import Optional, Pattern


class LevelFilter(logging.Filter):
    """Filter logs by level."""
    
    def __init__(self, min_level: str = "INFO", max_level: str = "CRITICAL"):
        super().__init__()
        self.min_level = getattr(logging, min_level.upper())
        self.max_level = getattr(logging, max_level.upper())
    
    def filter(self, record):
        return self.min_level <= record.levelno <= self.max_level


class MessageFilter(logging.Filter):
    """Filter logs by message pattern."""
    
    def __init__(self, pattern: str, exclude: bool = False):
        super().__init__()
        self.pattern = re.compile(pattern)
        self.exclude = exclude
    
    def filter(self, record):
        matches = bool(self.pattern.search(record.getMessage()))
        return not matches if self.exclude else matches


class RateLimitFilter(logging.Filter):
    """Rate limit logs."""
    
    def __init__(self, max_logs: int = 100, period: int = 60):
        super().__init__()
        self.max_logs = max_logs
        self.period = period
        self._log_times = []
    
    def filter(self, record):
        current_time = time.time()
        
        # Remove old entries
        self._log_times = [t for t in self._log_times if current_time - t < self.period]
        
        # Check limit
        if len(self._log_times) >= self.max_logs:
            return False
        
        self._log_times.append(current_time)
        return True


class SamplingFilter(logging.Filter):
    """Sample logs (keep only a percentage)."""
    
    def __init__(self, rate: float = 0.1):
        super().__init__()
        self.rate = max(0.0, min(1.0, rate))
        self._counter = 0
    
    def filter(self, record):
        self._counter += 1
        return (self._counter % int(1 / self.rate)) == 0 if self.rate > 0 else False