"""LLM 配置管理模块。

从 YAML 文件加载并验证大语言模型（LLM）的配置参数。
支持通过环境变量覆盖 API 密钥。
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


SUPPORTED_PROVIDERS = {"openai", "anthropic", "google", "ollama"}

# 环境变量名映射：provider -> env var
_PROVIDER_ENV_KEYS: dict[str, str] = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_API_KEY",
}


class LLMConfig:
    """从 YAML 配置文件加载 LLM 参数，并支持环境变量覆盖。

    用法::

        cfg = LLMConfig("config/default.yaml")
        print(cfg.provider)     # e.g. "openai"
        print(cfg.model_name)   # e.g. "gpt-4o"
        print(cfg.api_key)      # 优先读取环境变量
    """

    def __init__(self, config_path: str | Path) -> None:
        self._path = Path(config_path)
        if not self._path.exists():
            raise FileNotFoundError(f"配置文件不存在：{self._path}")

        with self._path.open("r", encoding="utf-8") as f:
            raw: dict[str, Any] = yaml.safe_load(f) or {}

        model_cfg = raw.get("model", {})
        request_cfg = raw.get("request", {})
        logging_cfg = raw.get("logging", {})

        self.provider: str = model_cfg.get("provider", "openai").lower()
        if self.provider not in SUPPORTED_PROVIDERS:
            raise ValueError(
                f"不支持的提供商 '{self.provider}'，"
                f"可选值：{sorted(SUPPORTED_PROVIDERS)}"
            )

        self.model_name: str = model_cfg.get("name", "")
        self.temperature: float = float(model_cfg.get("temperature", 0.7))
        self.max_tokens: int = int(model_cfg.get("max_tokens", 2048))

        # API key：环境变量 > 配置文件
        env_key = _PROVIDER_ENV_KEYS.get(self.provider)
        file_key: str = model_cfg.get("api_key", "")
        if env_key:
            self.api_key: str = os.getenv(env_key, "") or file_key
        else:
            self.api_key = file_key

        self.timeout: int = int(request_cfg.get("timeout", 60))
        self.max_retries: int = int(request_cfg.get("max_retries", 3))
        self.log_level: str = logging_cfg.get("level", "INFO").upper()

    def to_dict(self) -> dict[str, Any]:
        """以字典形式返回配置（不含 API 密钥）。"""
        return {
            "provider": self.provider,
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "log_level": self.log_level,
        }

    def __repr__(self) -> str:
        return (
            f"LLMConfig(provider={self.provider!r}, "
            f"model={self.model_name!r}, "
            f"temperature={self.temperature}, "
            f"max_tokens={self.max_tokens})"
        )
