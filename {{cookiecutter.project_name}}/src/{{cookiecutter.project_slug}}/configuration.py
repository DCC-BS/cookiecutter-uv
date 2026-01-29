from __future__ import annotations

from typing import override

from dcc_backend_common.config import get_env_or_throw, log_secret
from dcc_backend_common.config.app_config import AbstractAppConfig
from pydantic import Field


class Configuration(AbstractAppConfig):
    example: str = Field(description="This is a example", default="default value")
    example_secret: str = Field(description="This is a secret example")

    @override
    @classmethod
    def from_env(cls) -> "AbstractAppConfig":
        return cls(
            example=get_env_or_throw("EXAMPLE_ENV_VAR"), example_secret=get_env_or_throw("EXAMPLE_SECRET_ENV_VAR")
        )

    @override
    def __str__(self) -> str:
        return f"""
        Configuration(
            example={self.example},
            exaple_secret={log_secret(self.example_secret)},
        )
        """
