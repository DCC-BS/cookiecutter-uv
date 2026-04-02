from dependency_injector import containers, providers

from {{cookiecutter.project_slug}}.utils.configuration import Configuration
{%- if cookiecutter.use_azure_auth == "y" %}
from {{cookiecutter.project_slug}}.services.azure_service import AzureService
from {{cookiecutter.project_slug}}.utils.auth import AuthSchema, create_auth_scheme
from {{cookiecutter.project_slug}}.utils.auth_settings import AuthSettings
{%- endif %}


class Container(containers.DeclarativeContainer):
    config: providers.Object[Configuration] = providers.Object(Configuration.from_env())
{%- if cookiecutter.use_azure_auth == "y" %}

    auth_settings: providers.Singleton[AuthSettings] = providers.Singleton(AuthSettings, config=config)
    azure_service: providers.Singleton[AzureService] = providers.Singleton(AzureService, auth_settings=auth_settings)
    auth_scheme: providers.Singleton[AuthSchema] = providers.Singleton(
        create_auth_scheme,
        azure_scheme=azure_service.provided.azure_scheme,
        disable_auth=config.provided.disable_auth,
    )
{%- endif %}
