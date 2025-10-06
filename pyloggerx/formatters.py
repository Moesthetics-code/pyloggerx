import logging
import json
import inspect
from datetime import datetime
from typing import Optional, Dict, Any


class ColorFormatter(logging.Formatter):
    """Colorful console formatter with emojis."""
    
    COLORS = {
        'DEBUG': '\033[94m',    # Blue
        'INFO': '\033[92m',     # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',    # Red
        'CRITICAL': '\033[95m', # Magenta
        'RESET': '\033[0m'
    }
    
    def __init__(
        self,
        colors: bool = True,
        format_string: Optional[str] = None,
        include_caller: bool = False
    ):
        self.colors = colors
        self.include_caller = include_caller
        self.context = {}
        
        if format_string is None:
            if include_caller:
                format_string = '[%(asctime)s] %(emoji)s %(levelname)-8s [%(filename)s:%(lineno)d] : %(message)s'
            else:
                format_string = '[%(asctime)s] %(emoji)s %(levelname)-8s : %(message)s'
        
        super().__init__(format_string, datefmt='%Y-%m-%d %H:%M:%S')
    
    def format(self, record):
        # Add context to record
        for key, value in self.context.items():
            setattr(record, key, value)
        
        # Add emoji if not present
        if not hasattr(record, 'emoji'):
            record.emoji = ''
        
        # Format the message
        formatted = super().format(record)
        
        # Apply colors
        if self.colors:
            color = self.COLORS.get(record.levelname, '')
            reset = self.COLORS['RESET']
            formatted = f"{color}{formatted}{reset}"
        
        return formatted
    
    def add_context(self, **kwargs):
        """Add persistent context to all log messages."""
        self.context.update(kwargs)


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def __init__(self, include_caller: bool = False):
        self.include_caller = include_caller
        self.context = {}
        super().__init__()
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
        }
        
        # Add caller information if requested
        if self.include_caller:
            log_entry.update({
                'filename': record.filename,
                'line_number': record.lineno,
                'pathname': record.pathname
            })
        
        # Add exception information if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Add any extra fields from the record
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                          'filename', 'module', 'exc_info', 'exc_text', 'stack_info',
                          'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
                          'thread', 'threadName', 'processName', 'process', 'message',
                          'emoji']:
                log_entry[key] = value
        
        # Add persistent context
        log_entry.update(self.context)
        
        return json.dumps(log_entry, ensure_ascii=False)
    
    def add_context(self, **kwargs):
        """Add persistent context to all log messages."""
        self.context.update(kwargs)