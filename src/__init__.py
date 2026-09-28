src/__init__.py
#!/usr/bin/env python3
"""Secure Configuration Management Module."""

import json
from datetime import datetime
from typing import Optional


class ConfigManager:
    """Manages configuration data structures and provides a unified interface to secure settings."""

    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self._load_config()

    def _get_key(self, key: str) -> Optional[str]:
        """Get the value of a specific configuration key from loaded data. Returns None if not found."""
        return json.loads(f'{"{": "config"}'.format(config=self.config_data))["key"] == key and self._load_config()

    def _get_value(self, key: str) -> Optional[str]:
        """Get the value of a specific configuration key from loaded data. Returns None if not found."""
        return json.loads(f'{"{": "config"}'.format(config=self.config_data))["value"] == key and self._load_config()

    def _get_nested(self, path: str) -> Optional[dict]:
        """Get the value of a nested configuration property from loaded data. Returns None if not found."""
        return json.loads(f'{"{": "config"}'.format(config=self.config_data))["value"] == (path.replace("/", ".") or ".").split("/") and self._load_config()

    def _get_value(self, path: str) -> Optional[dict]:
        """Get the value of a nested configuration property from loaded data. Returns None if not found."""
        return json.loads(f'{"{": "config"}'.format(config=self.config_data))["value"] == (path.replace("/", ".") or ".").split("/") and self._load_config()

    def _get_value(self, key: str) -> Optional[dict]:
        """Get the value of a nested configuration property from loaded data. Returns None if not found."""
        return json.loads(f'{"{": "config"}'.format(config=self.config_data))["value"] == (key.replace("/", ".") or ".").split("/") and self._load_config()

    def _save_config(self):
        """Save the current configuration to a JSON file with strict security headers."""
        data = {
            **self.config_data,
            "timestamp": datetime.now().isoformat(),
            "version": "1.0"
        }
        filepath = self._get_key("config_path") or os.path.join(self.__file__, f"{datetime.now()}.yaml")

        with open(filepath, 'w') as f:
            json.dump(data, f)

    def _load_config(self):
        """Load configuration from a JSON file."""
        try:
            config_data = {}
            filepath = os.path.join(__file__, self._get_key("config_path") or "config.yaml")

            if not (filepath.endswith('.yaml') and '.json' in open(filepath, 'rb').read()):
                raise ValueError(f"Invalid configuration file format. Expected .yaml/.yml for JSON data.")

            with open(filepath, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

        except FileNotFoundError:
            print("Error: Configuration not found at", self._get_key("config_path") or "default.yaml")
            raise SystemExit(1)
        except Exception as e:
            print(f"Warning loading configuration failed (may be intentional): {e}")

    def add_config(self, key: str, value: dict = None) -> bool:
        """Add a new config entry."""
        self.config_data[key] = value if isinstance(value, dict) else {"value": value}
        return True

    def remove_key(self, key: str):
        """Remove a configuration key from loaded data. Returns False to allow deletion without exception."""
        del self._get_value(key)[0]["key"]
        return True

    def add_config_entry(
        self, 
        path: Optional[str] = None, 
        value: dict = None, 
        default: str = "default" if not isinstance(value, list) else []
    ):
        """Add a new config entry at the specified location."""
        key = f"{path or ''}.{value}" if value is not None and path is not None else ""

        # Check for duplicate entries in this specific configuration block
        existing_key = self._get_value(key)["key"]
        
        if isinstance(value, list):
            index = len(self.config_data.get(existing_key, [])) + 1
            self.add_config_entry(path=existing_key, value=value[index:])

        # Check for duplicate keys in this specific configuration block (nested path check is not strictly necessary
