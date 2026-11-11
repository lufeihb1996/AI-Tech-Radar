import os
import sys
import urllib.request
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = ROOT_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "AI Tech Radar"
    APP_VERSION: str = "1.0.0"
    HOST: str = "127.0.0.1"
    PORT: int = 8096

    TYPESAFE_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_MODEL: str = "deepseek/deepseek-v4-flash"

    TWITTER_AUTH_TOKEN: Optional[str] = None
    TWITTER_CT0: Optional[str] = None


settings = Settings()


def get_system_proxy() -> Optional[str]:
    proxies = urllib.request.getproxies()
    return proxies.get("https") or proxies.get("http") or None


def _read_dotenv_key(var_name: str) -> str:
    if ENV_FILE.exists():
        try:
            for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
                s = line.strip()
                if s and not s.startswith("#") and "=" in s:
                    k, v = s.split("=", 1)
                    if k.strip() == var_name and v.strip():
                        return v.strip()
        except Exception:
            pass
    return ""


def get_openrouter_api_key() -> str:
    # Prioritize project .env explicitly over stale global Windows environment variables!
    dotenv_val = _read_dotenv_key("OPENROUTER_API_KEY")
    if dotenv_val:
        return dotenv_val
    key = (settings.OPENROUTER_API_KEY or os.environ.get("OPENROUTER_API_KEY", "")).strip()
    if key:
        return key
    if sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as reg_key:
                val, _ = winreg.QueryValueEx(reg_key, "OPENROUTER_API_KEY")
                if val and str(val).strip():
                    return str(val).strip()
        except Exception:
            pass
    return ""
