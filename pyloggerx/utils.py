import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, TYPE_CHECKING

# Import conditionnel pour éviter la dépendance circulaire
if TYPE_CHECKING:
    from .core import PyLoggerX

def ensure_directory(filepath: str):
    """Ensure directory exists for the given filepath."""
    directory = os.path.dirname(os.path.abspath(filepath))
    os.makedirs(directory, exist_ok=True)


def setup_logger(
    name: str,
    level: str = "INFO",
    console: bool = True,
    json_file: Optional[str] = None,
    **kwargs
) -> 'PyLoggerX':
    """Quick setup function for creating a logger."""
    # Import local pour éviter la dépendance circulaire
    from .core import PyLoggerX
    
    return PyLoggerX(
        name=name,
        level=level,
        console=console,
        json_file=json_file,
        **kwargs
    )


def configure_logging(config: Dict[str, Any]) -> 'PyLoggerX':
    """Configure logger from dictionary."""
    # Import local pour éviter la dépendance circulaire
    from .core import PyLoggerX
    
    return PyLoggerX(**config)


def get_caller_info():
    """Get caller information for debugging."""
    import inspect
    frame = inspect.currentframe()
    try:
        caller_frame = frame.f_back.f_back
        return {
            'filename': caller_frame.f_code.co_filename,
            'function': caller_frame.f_code.co_name,
            'line': caller_frame.f_lineno
        }
    finally:
        del frame