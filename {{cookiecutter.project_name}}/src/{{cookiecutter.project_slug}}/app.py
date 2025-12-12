from __future__ import annotations

from backend_common.fastapi_error_handling import inject_api_error_handler
from backend_common.fastapi_health_probes import health_probe_router
from backend_common.fastapi_health_probes.router import ServiceDependency
from fastapi import FastAPI

from {{cookiecutter.project_slug}}.routers import example_router

config = {} # TODO load your config here

service_dependencies: list[ServiceDependency] = [
    {"name": "llm", "health_check_url": config.llm_health_check_url, "api_key": config.openai_api_key},
    {
        "name": "language tool",
        "health_check_url": config.language_tool_api_health_check_url,
        "api_key": None,
    },
]


def create_app() -> FastAPI:
    # Initialize FastAPI app
    app = FastAPI()

    # Include health probes
    app.include_router(health_probe_router(service_dependencies))

    # Include API routers
    app.include_router(example_router)

    # Inject error handler
    inject_api_error_handler(app)
