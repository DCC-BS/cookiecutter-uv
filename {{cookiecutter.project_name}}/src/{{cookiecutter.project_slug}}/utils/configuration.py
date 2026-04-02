from __future__ import annotations

import os
from typing import override

from dcc_backend_common.config import get_env_or_throw, log_secret
from dcc_backend_common.config.app_config import LlmConfig
from pydantic import Field


class Configuration(LlmConfig):
    """Application configuration loaded from environment variables."""

    client_url: str = Field(description="The URL for client application", default="http://localhost:3000")
    environment: str = Field(description="The application environment", default="development")
    llm_health_check_url: str = Field(
        description="The URL for LLM health check API", default="http://localhost:8001/health"
    )

    # Example configuration field (remove in production)
    example: str = Field(description="Example configuration value", default="default value")
{%- if cookiecutter.use_azure_auth == "y" %}

    # Azure AD Authentication
    azure_client_id: str = Field(description="The client ID for Azure AD application")
    azure_tenant_id: str = Field(description="The tenant ID for Azure AD application")
    azure_frontend_client_id: str = Field(description="The client ID for Azure AD frontend application")
    azure_scope_description: str = Field(
        description="The scope description for Azure AD authentication", default="user_impersonation"
    )
    disable_auth: bool = Field(description="Flag to disable authentication", default=True)

    # HMAC secret for pseudonymization
    hmac_secret: str = Field(description="Used to pseudonymize user id. Create with openssl rand 32 | base64")
{%- endif %}

    @classmethod
    @override
    def from_env(cls) -> "Configuration":
{%- if cookiecutter.use_azure_auth == "y" %}
        disable_auth = os.getenv("AUTH_MODE", "none").lower().strip() == "none"
{%- endif %}

        llm_api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not llm_api_key:
            raise ValueError("LLM_API_KEY environment variable must be set")

        return cls(
            client_url=get_env_or_throw("CLIENT_URL"),
            llm_api_key=llm_api_key,
            llm_url=get_env_or_throw("LLM_URL"),
            llm_model=get_env_or_throw("LLM_MODEL"),
            llm_health_check_url=get_env_or_throw("LLM_HEALTH_CHECK_URL"),
{%- if cookiecutter.use_azure_auth == "y" %}
            azure_client_id="" if disable_auth else get_env_or_throw("AZURE_CLIENT_ID"),
            azure_tenant_id="" if disable_auth else get_env_or_throw("AZURE_TENANT_ID"),
            azure_frontend_client_id="" if disable_auth else get_env_or_throw("AZURE_FRONTEND_CLIENT_ID"),
            azure_scope_description="" if disable_auth else get_env_or_throw("AZURE_SCOPE_DESCRIPTION"),
            hmac_secret=get_env_or_throw("HMAC_SECRET"),
            disable_auth=disable_auth,
{%- endif %}
            environment=os.getenv("ENVIRONMENT", "production"),
        )

    @override
    def __str__(self) -> str:
        return f"""
        Configuration(
            client_url={self.client_url},
            llm_api_key={log_secret(self.llm_api_key)},
            llm_url={self.llm_url},
            llm_model={self.llm_model},
            llm_health_check_url={self.llm_health_check_url},
{%- if cookiecutter.use_azure_auth == "y" %}
            azure_client_id={log_secret(self.azure_client_id)},
            azure_tenant_id={log_secret(self.azure_tenant_id)},
            azure_frontend_client_id={log_secret(self.azure_frontend_client_id)},
            azure_scope_description={self.azure_scope_description},
            hmac_secret={log_secret(self.hmac_secret)},
            disable_auth={self.disable_auth},
{%- endif %}
            environment={self.environment}
        )
        """
