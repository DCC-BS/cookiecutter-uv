from typing import Annotated

from dcc_backend_common.logger import get_logger
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
{%- if cookiecutter.use_azure_auth == "y" %}
from fastapi import Security
from fastapi_azure_auth.user import User
{%- endif %}

from {{cookiecutter.project_slug}}.container import Container
from {{cookiecutter.project_slug}}.utils.configuration import Configuration
from {{cookiecutter.project_slug}}.utils.cancel_on_disconnect import CancelOnDisconnect
{%- if cookiecutter.use_azure_auth == "y" %}
from {{cookiecutter.project_slug}}.utils.auth import AuthSchema
from {{cookiecutter.project_slug}}.utils.usage_tracking import get_pseudonymized_user_id
{%- endif %}

logger = get_logger("example_router")


@inject
def create_router(
    config: Configuration = Provide[Container.config],
{%- if cookiecutter.use_azure_auth == "y" %}
    auth_scheme: AuthSchema = Provide[Container.auth_scheme],
{%- endif %}
) -> APIRouter:
    logger.info("Creating example router")
    router: APIRouter = APIRouter(prefix="/example", tags=["example"])
{%- if cookiecutter.use_azure_auth == "y" %}

    @router.get("/foo", dependencies=[Security(auth_scheme)])
    async def get_foo(
        request: Request,
        current_user: Annotated[User, Depends(auth_scheme)],
    ) -> dict[str, str]:
        pseudonymized_user_id = get_pseudonymized_user_id(current_user, config.hmac_secret)
        logger.info(
            "app_event",
            extra={
                "pseudonym_id": pseudonymized_user_id,
                "event": get_foo.__name__,
            },
        )

        # Use CancelOnDisconnect for long-running operations
        async with CancelOnDisconnect(request):
            # Simulate a potentially long operation
            return {"message": f"Example config value is: {config.example}"}
{%- else %}

    @router.get("/foo")
    async def get_foo(
        request: Request,
    ) -> dict[str, str]:
        # Use CancelOnDisconnect for long-running operations
        async with CancelOnDisconnect(request):
            # Simulate a potentially long operation
            return {"message": f"Example config value is: {config.example}"}
{%- endif %}

    logger.info("Example router configured")
    return router
