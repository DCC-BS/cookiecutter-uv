{%- if cookiecutter.use_azure_auth == "y" -%}
from {{cookiecutter.project_slug}}.services.azure_service import AzureService

__all__ = ["AzureService"]
{%- endif %}
