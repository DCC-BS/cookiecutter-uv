from {{cookiecutter.project_slug}}.utils.configuration import Configuration
{%- if cookiecutter.use_azure_auth == "y" %}
from {{cookiecutter.project_slug}}.utils.auth import AuthSchema, create_auth_scheme
from {{cookiecutter.project_slug}}.utils.auth_settings import AuthSettings
{%- endif %}

__all__ = [
    "Configuration",
{%- if cookiecutter.use_azure_auth == "y" %}
    "AuthSchema",
    "create_auth_scheme",
    "AuthSettings",
{%- endif %}
]
