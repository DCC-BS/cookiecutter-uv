from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dcc_backend_common.fastapi_error_handling import inject_api_error_handler
from dcc_backend_common.fastapi_health_probes import health_probe_router
from dcc_backend_common.fastapi_health_probes.router import ServiceDependency
from dcc_backend_common.logger import get_logger, init_logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from structlog.stdlib import BoundLogger

from {{cookiecutter.project_slug}}.container import Container
from {{cookiecutter.project_slug}}.routers import example_router
from {{cookiecutter.project_slug}}.utils.configuration import Configuration
from {{cookiecutter.project_slug}}.utils.middleware import add_logging_middleware
{%- if cookiecutter.use_azure_auth == "y" %}
from {{cookiecutter.project_slug}}.utils.auth import AuthSchema
{%- endif %}


def create_app() -> FastAPI:
    init_logger()

    logger: BoundLogger = get_logger("app")
    logger.info("Starting {{cookiecutter.project_name}} API application")

    # Set up dependency injection container
    logger.debug("Configuring dependency injection container")
    container = Container()
    container.wire(modules=["{{cookiecutter.project_slug}}.routers.example_router"])
    container.check_dependencies()
    logger.info("Dependency injection configured")

    config: Configuration = container.config()
    logger.info(f"Running with configuration: {config}")
{%- if cookiecutter.use_pydantic_ai == "y" %}

    # only in development mode, enable pydantic_ai logfire instrumentation
    if config.environment == "development":
        import os

        import logfire

        # Only configure logfire if token is available (avoids interactive prompts)
        if os.getenv("LOGFIRE_TOKEN"):
            logfire.configure()
            logfire.instrument_pydantic_ai()
{%- endif %}

    service_dependencies: list[ServiceDependency] = [
        {"name": "llm", "health_check_url": config.llm_health_check_url, "api_key": config.llm_api_key},
    ]

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
        """
        Application lifecycle context manager.

        Use this for startup/shutdown tasks like:
        - Loading auth configuration
        - Warming up connections
        - Initializing resources
        """
{%- if cookiecutter.use_azure_auth == "y" %}

        if not config.disable_auth:
            await container.azure_service().load_config()
{%- endif %}
        yield

    app = FastAPI(
        title="{{cookiecutter.project_name}}",
        description="{{cookiecutter.project_description}}",
        version="0.1.0",
{%- if cookiecutter.use_azure_auth == "y" %}
        swagger_ui_oauth2_redirect_url="/oauth2-redirect",
        swagger_ui_init_oauth={
            "usePkceWithAuthorizationCodeGrant": True,
            "clientId": config.azure_frontend_client_id,
        },
{%- endif %}
        lifespan=lifespan,
    )

    app.include_router(health_probe_router(service_dependencies))
    inject_api_error_handler(app)

    # Configure CORS
    logger.debug("Setting up CORS middleware")
    app.add_middleware(
        CORSMiddleware,  # ty:ignore[invalid-argument-type]
        allow_origins=[config.client_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS configured with origin: {config.client_url}")

    # Add logging middleware
    add_logging_middleware(app)

    # Include routers
    logger.debug("Registering API routers")
    app.include_router(example_router.create_router())
    logger.info("All routers registered")

    logger.info("API setup complete")
    return app


app = create_app()
