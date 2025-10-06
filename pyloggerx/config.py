import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigLoader:
    """Load configuration from various sources."""
    
    @staticmethod
    def from_json(filepath: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def from_yaml(filepath: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            import yaml
            with open(filepath, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except ImportError:
            raise ImportError("PyYAML required for YAML config. Install: pip install pyyaml")
    
    @staticmethod
    def from_env(prefix: str = "PYLOGGERX_") -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {}
        
        # Map environment variables to config keys
        env_mapping = {
            f"{prefix}LEVEL": "level",
            f"{prefix}JSON_FILE": "json_file",
            f"{prefix}TEXT_FILE": "text_file",
            f"{prefix}CONSOLE": "console",
            f"{prefix}COLORS": "colors",
            f"{prefix}RATE_LIMIT_ENABLED": "enable_rate_limit",
            f"{prefix}RATE_LIMIT_MESSAGES": "rate_limit_messages",
            f"{prefix}RATE_LIMIT_PERIOD": "rate_limit_period",
            f"{prefix}ELASTICSEARCH_URL": "elasticsearch_url",
            f"{prefix}LOKI_URL": "loki_url",
            f"{prefix}SENTRY_DSN": "sentry_dsn",
            f"{prefix}DATADOG_API_KEY": "datadog_api_key",
            f"{prefix}SLACK_WEBHOOK": "slack_webhook",
        }
        
        for env_var, config_key in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert boolean strings
                if value.lower() in ['true', 'yes', '1']:
                    value = True
                elif value.lower() in ['false', 'no', '0']:
                    value = False
                # Convert numeric strings
                elif value.isdigit():
                    value = int(value)
                
                config[config_key] = value
        
        return config
    
    @staticmethod
    def from_file(filepath: str) -> Dict[str, Any]:
        """Auto-detect file type and load configuration."""
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")
        
        suffix = path.suffix.lower()
        
        if suffix == '.json':
            return ConfigLoader.from_json(filepath)
        elif suffix in ['.yaml', '.yml']:
            return ConfigLoader.from_yaml(filepath)
        else:
            raise ValueError(f"Unsupported config file format: {suffix}")
    
    @staticmethod
    def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
        """Merge multiple configurations. Later configs override earlier ones."""
        merged = {}
        for config in configs:
            merged.update(config)
        return merged


class ConfigValidator:
    """Validate configuration values."""
    
    VALID_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    
    @staticmethod
    def validate(config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate configuration.
        Returns (is_valid, error_message).
        """
        # Validate level
        if 'level' in config:
            level = config['level'].upper()
            if level not in ConfigValidator.VALID_LEVELS:
                return False, f"Invalid level: {level}. Must be one of {ConfigValidator.VALID_LEVELS}"
        
        # Validate rate limiting
        if config.get('enable_rate_limit'):
            if 'rate_limit_messages' in config:
                if not isinstance(config['rate_limit_messages'], int) or config['rate_limit_messages'] < 1:
                    return False, "rate_limit_messages must be a positive integer"
            
            if 'rate_limit_period' in config:
                if not isinstance(config['rate_limit_period'], (int, float)) or config['rate_limit_period'] <= 0:
                    return False, "rate_limit_period must be a positive number"
        
        # Validate sampling
        if config.get('enable_sampling'):
            if 'sampling_rate' in config:
                rate = config['sampling_rate']
                if not isinstance(rate, (int, float)) or not (0.0 <= rate <= 1.0):
                    return False, "sampling_rate must be between 0.0 and 1.0"
        
        # Validate URLs
        url_fields = ['elasticsearch_url', 'loki_url', 'webhook_url']
        for field in url_fields:
            if field in config and config[field]:
                if not isinstance(config[field], str) or not config[field].startswith('http'):
                    return False, f"{field} must be a valid HTTP(S) URL"
        
        return True, None


def load_config(
    config_file: Optional[str] = None,
    from_env: bool = True,
    defaults: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Load configuration from multiple sources with priority:
    1. Environment variables (highest priority)
    2. Config file
    3. Defaults (lowest priority)
    
    Args:
        config_file: Path to configuration file (JSON or YAML)
        from_env: Whether to load from environment variables
        defaults: Default configuration dict
    
    Returns:
        Merged configuration dictionary
    
    Raises:
        FileNotFoundError: If config_file doesn't exist
        ValueError: If configuration is invalid
    """
    configs = []
    
    # Add defaults
    if defaults:
        configs.append(defaults)
    
    # Add file config
    if config_file:
        file_config = ConfigLoader.from_file(config_file)
        configs.append(file_config)
    
    # Add env config
    if from_env:
        env_config = ConfigLoader.from_env()
        if env_config:
            configs.append(env_config)
    
    # Merge all configs
    merged = ConfigLoader.merge_configs(*configs)
    
    # Validate
    is_valid, error = ConfigValidator.validate(merged)
    if not is_valid:
        raise ValueError(f"Invalid configuration: {error}")
    
    return merged


# Example configuration templates
EXAMPLE_CONFIGS = {
    "basic": {
        "name": "myapp",
        "level": "INFO",
        "console": True,
        "colors": True,
        "json_file": "logs/app.json",
        "text_file": "logs/app.txt"
    },
    
    "production": {
        "name": "myapp",
        "level": "WARNING",
        "console": False,
        "colors": False,
        "json_file": "/var/log/myapp/app.json",
        "text_file": "/var/log/myapp/app.txt",
        "max_bytes": 50 * 1024 * 1024,  # 50MB
        "backup_count": 10,
        "enable_rate_limit": True,
        "rate_limit_messages": 100,
        "rate_limit_period": 60,
        "performance_tracking": True,
        #"elasticsearch_url": "http://elasticsearch:9200",
        #"sentry_dsn": "https://your-sentry-dsn"
    },
    
    "development": {
        "name": "myapp-dev",
        "level": "DEBUG",
        "console": True,
        "colors": True,
        "include_caller": True,
        "json_file": "logs/dev.json",
        "enable_rate_limit": False,
        "performance_tracking": True
    }
}


def save_example_config(config_type: str = "basic", filepath: str = "pyloggerx.json"):
    """Save an example configuration to a file."""
    if config_type not in EXAMPLE_CONFIGS:
        raise ValueError(f"Unknown config type: {config_type}. Available: {list(EXAMPLE_CONFIGS.keys())}")
    
    config = EXAMPLE_CONFIGS[config_type]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    print(f"Example '{config_type}' configuration saved to {filepath}")