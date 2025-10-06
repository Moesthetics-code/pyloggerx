import os
from logging.handlers import RotatingFileHandler as BaseRotatingFileHandler
from logging.handlers import TimedRotatingFileHandler as BaseTimedRotatingFileHandler


class RotatingFileHandler(BaseRotatingFileHandler):
    """Enhanced rotating file handler with better error handling."""
    
    def __init__(self, *args, **kwargs):
        # Ensure directory exists
        filename = args[0] if args else kwargs.get('filename')
        if filename:
            os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        super().__init__(*args, **kwargs)


class TimedRotatingHandler(BaseTimedRotatingFileHandler):
    """Enhanced timed rotating file handler with better error handling."""
    
    def __init__(self, *args, **kwargs):
        # Ensure directory exists
        filename = args[0] if args else kwargs.get('filename')
        if filename:
            os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        super().__init__(*args, **kwargs)