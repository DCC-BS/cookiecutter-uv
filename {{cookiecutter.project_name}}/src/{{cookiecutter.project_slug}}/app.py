from dcc_backend_common.fastapi_error_handling import inject_api_error_handler
from dcc_backend_common.fastapi_health_probes import health_probe_router
from dcc_backend_common.fastapi_health_probes.router import ServiceDependency
from dcc_backend_common.logger import get_logger, init_logger
from fastapi import FastAPI
from structlog.stdlib import BoundLogger

from {{ cookiecutter.project_slug }}.container import Container
from {{ cookiecutter.project_slug}}.routers.example_router
form {{ cookiecutter.project_slug}}.routers import example_router

def create_app() -> FastAPI:
    init_logger()

    logger: BoundLogger = get_logger("app")
    logger.info("Starting {{ cookiecuter.project_name }} API application")

    # Set up dependency injection container
    logger.debug("Configuring dependency injection container")
    container = Container()
    container.wire(modules=[example_router])
    container.check_dependencies()
    logger.info("Dependency injection configured")

    config = container.config()
    logger.info(f"Running with configuration: {config}")

{% if cookiecutter.use_pydantic_ai == "y" %}
    # only in development mode, enable pydantic_ai logfire instrumentation
    if config.environment == "development":
        import logfire

        logfire.configure()
        logfire.instrument_pydantic_ai()
{% endif %}

    service_dependencies: list[ServiceDependency] = [
        {"name": "llm", "health_check_url": "TODO", "api_key": "TODO"},
    ]

    app = FastAPI(
        title="{{ cookiecutter.project_name }}",
        description="TODO",
        version="0.1.0",
    )

    app.include_router(health_probe_router(service_dependencies))
    inject_api_error_handler(app)

    # Configure CORS
    logger.debug("Setting up CORS middleware")
    app.add_middleware(
        allow_origins=[config.client_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS configured with origin: {config.client_url}")

    # Include routers
    logger.debug("Registering API routers")
    app.include_router(example_router.create_router())
    logger.info("All routers registered")

    logger.info("API setup complete")
    return app


app = create_app()
