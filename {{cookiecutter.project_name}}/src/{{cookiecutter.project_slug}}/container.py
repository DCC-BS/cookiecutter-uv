from dcc_backend_common.usage_tracking import UsageTrackingService
from dependency_injector import containers, providers

from {{cookiecutter.project_slug}}.utils.app_config import AppConfig
{%- if cookiecutter.use_azure_auth == "y" %}
from {{cookiecutter.project_slug}}.services.azure_service import AzureService
from {{cookiecutter.project_slug}}.utils.auth import AuthSchema, create_auth_scheme
from {{cookiecutter.project_slug}}.utils.auth_settings import AuthSettings
{%- endif %}


class Container(containers.DeclarativeContainer):
    app_config: providers.Object[AppConfig] = providers.Object(AppConfig.from_env())

    usage_tracking_service: providers.Singleton[UsageTrackingService] = providers.Singleton(
        UsageTrackingService,
        hmac_secret=app_config.provided.hmac_secret,
    )
{%- if cookiecutter.use_azure_auth == "y" %}

    auth_settings: providers.Singleton[AuthSettings] = providers.Singleton(AuthSettings, config=app_config)
    azure_service: providers.Singleton[AzureService] = providers.Singleton(AzureService, auth_settings=auth_settings)
    auth_scheme: providers.Singleton[AuthSchema] = providers.Singleton(
        create_auth_scheme,
        azure_scheme=azure_service.provided.azure_scheme,
        disable_auth=app_config.provided.disable_auth,
    )
{%- endif %}
