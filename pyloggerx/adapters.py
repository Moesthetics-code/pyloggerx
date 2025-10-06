from typing import Any, Dict


class StructlogAdapter:
    """Adapter for structlog compatibility."""
    
    def __init__(self, logger):
        self.logger = logger
    
    def msg(self, event: str, **kwargs):
        """structlog-style logging."""
        self.logger.info(event, **kwargs)
    
    def debug(self, event: str, **kwargs):
        self.logger.debug(event, **kwargs)
    
    def info(self, event: str, **kwargs):
        self.logger.info(event, **kwargs)
    
    def warning(self, event: str, **kwargs):
        self.logger.warning(event, **kwargs)
    
    def error(self, event: str, **kwargs):
        self.logger.error(event, **kwargs)
    
    def bind(self, **kwargs):
        """Bind context data."""
        self.logger.add_enrichment(**kwargs)
        return self


class LoguruAdapter:
    """Adapter for loguru-style logging."""
    
    def __init__(self, logger):
        self.logger = logger
    
    def trace(self, message: str, **kwargs):
        self.logger.debug(message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs):
        self.logger.info(message, **kwargs)
    
    def success(self, message: str, **kwargs):
        self.logger.info(f"✓ {message}", **kwargs)
    
    def warning(self, message: str, **kwargs):
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        self.logger.critical(message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        self.logger.exception(message, **kwargs)