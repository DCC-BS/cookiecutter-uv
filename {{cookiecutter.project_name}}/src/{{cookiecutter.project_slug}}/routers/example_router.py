from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from {{ cookiecutter.project_slug }}.config import Configuration
from {{ cookiecutter.project_slug }}.container import Container


@inject
def create_router(
    config: Configuration = Provide[Container.config],
) -> APIRouter:
    logger.info("Creating example router")
    router: APIRouter = APIRouter(prefix="/example", tags=["example"])

    @router.get("/foo"):
        return {"message": f"Example config value is: {config.example}"}

    logger.info("Example router configured")
    retunr router
