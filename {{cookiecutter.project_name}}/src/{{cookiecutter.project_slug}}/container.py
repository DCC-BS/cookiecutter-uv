from dependency_injector import containers, providers
from {{ cookiecutter.project_slug }}.config import Configuration


class Container(containers.DeclarativeContainer):
    config: providers.Object[Configuration] = providers.Object(Configuration.from_env())
