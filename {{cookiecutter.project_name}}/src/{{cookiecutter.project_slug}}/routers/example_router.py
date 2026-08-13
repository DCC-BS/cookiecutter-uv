from collections.abc import AsyncGenerator
from contextlib import aclosing

from dcc_backend_common.logger import get_logger
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Request
{%- if cookiecutter.use_azure_auth == "y" %}
from fastapi import Security
from fastapi_azure_auth.user import User
from typing import Annotated
from fastapi import Depends
{%- endif %}

from {{cookiecutter.project_slug}}.container import Container
from {{cookiecutter.project_slug}}.utils.app_config import AppConfig
{%- if cookiecutter.use_azure_auth == "y" %}
from {{cookiecutter.project_slug}}.utils.auth import AuthSchema
from {{cookiecutter.project_slug}}.utils.usage_tracking import get_pseudonymized_user_id
{%- endif %}

logger = get_logger("example_router")


@inject
def create_router(
    config: AppConfig = Provide[Container.app_config],
{%- if cookiecutter.use_azure_auth == "y" %}
    auth_scheme: AuthSchema = Provide[Container.auth_scheme],
{%- endif %}
) -> APIRouter:
    logger.info("Creating example router")
    router: APIRouter = APIRouter(prefix="/example", tags=["example"])

    async def do_something() -> AsyncGenerator[str]:
        yield "test"
{% if cookiecutter.use_azure_auth == "y" %}
    @router.get("/foo", dependencies=[Security(auth_scheme)])
    async def get_foo(
        request: Request,
        current_user: Annotated[User, Depends(auth_scheme)],
    ) -> AsyncGenerator[str]:
        pseudonymized_user_id = get_pseudonymized_user_id(current_user, config.hmac_secret)
        logger.info(
            "app_event",
            extra={
                "pseudonym_id": pseudonymized_user_id,
                "event": get_foo.__name__,
            },
        )

        # aclosing: on disconnect the service generator must be closed here,
        # inside the request context, so its cleanup (llm_call usage logging)
        # runs deterministically instead of at garbage collection.
        async with aclosing(do_something()) as chunks:
            async for chunk in chunks:
                if await request.is_disconnected():
                    logger.info("Client disconnected, stopping translation stream")
                    break
                yield chunk
{%- else %}
    @router.get("/foo")
    async def get_foo(
        request: Request,
    ) -> AsyncGenerator[str]:
        # aclosing: on disconnect the service generator must be closed here,
        # inside the request context, so its cleanup (llm_call usage logging)
        # runs deterministically instead of at garbage collection.
        async with aclosing(do_something()) as chunks:
            async for chunk in chunks:
                if await request.is_disconnected():
                    logger.info("Client disconnected, stopping translation stream")
                    break
                yield chunk
{%- endif %}

    logger.info("Example router configured")
    return router
