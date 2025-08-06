import os
import yaml

class Config:
    def __init__(self, path="../config/config.yaml"):
        self.data = {}
        if os.path.exists(path):
            with open(path, "r") as f:
                self.data = yaml.safe_load(f) or {}

    def _get_env_or_file(self, env_key, *file_keys, default=None, cast=None):
        """
        Return the environment variable value if set,
        otherwise traverse the nested keys in the config file.
        Optionally cast the value.
        """
        val = os.getenv(env_key)
        if val is not None:
            if cast:
                try:
                    return cast(val)
                except Exception:
                    return default
            return val

        # Traverse nested dict keys
        d = self.data
        for key in file_keys:
            if not isinstance(d, dict):
                return default
            d = d.get(key, None)
            if d is None:
                return default
        return d or default

    @property
    def base_url(self):
        # Remove trailing slash if present
        val = self._get_env_or_file("API_BASE_URL", "api", "base_url", default="http://localhost:8081")
        return val.rstrip("/") if val else val

    @property
    def token(self):
        return self._get_env_or_file("API_TOKEN", "api", "token", default=None)

    @property
    def debug(self):
        def str_to_bool(s):
            return s.lower() in ("true", "1", "yes", "on")
        return self._get_env_or_file("DEBUG", default=False, cast=str_to_bool)

    @property
    def vhost(self):
        return self._get_env_or_file("VHOST", default="default")

    @property
    def app(self):
        return self._get_env_or_file("APP", default="app")
