<p align="center">
  <img width="600" src="https://raw.githubusercontent.com/fpgmaas/cookiecutter-uv/main/docs/static/cookiecutter.svg">
</p style = "margin-bottom: 2rem;">

---

[![Build status](https://img.shields.io/github/actions/workflow/status/DCC-BS/cookiecutter-uv/main.yml?branch=main)](https://github.com/DCC-BS/cookiecutter-uv/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/badge/python-3.10_%7C_3.11_%7C_3.12_%7C_3.13-blue?labelColor=grey&color=blue)](https://github.com/DCC-BS/cookiecutter-uv/blob/main/pyproject.toml)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://dcc-bs.github.io/cookiecutter-uv/)
[![License](https://img.shields.io/github/license/DCC-BS/cookiecutter-uv)](https://img.shields.io/github/license/DCC-BS/cookiecutter-uv)


This is a modern Cookiecutter template that can be used to initiate a Python project with all the necessary tools for development, testing, and deployment. It supports the following features:

- [uv](https://docs.astral.sh/uv/) for dependency management
- CI/CD with [GitHub Actions](https://github.com/features/actions)
- Pre-commit hooks with [pre-commit](https://pre-commit.com/)
- Code quality with [ruff](https://github.com/charliermarsh/ruff), [basedpyright](https://docs.basedpyright.com) and [deptry](https://github.com/fpgmaas/deptry/)
- Publishing to [PyPI](https://pypi.org) by creating a new release on GitHub
- Testing and coverage with [pytest](https://docs.pytest.org/en/7.1.x/) and [codecov](https://about.codecov.io/)
- Documentation with [MkDocs](https://www.mkdocs.org/)
- Compatibility testing for multiple versions of Python with [tox-uv](https://github.com/tox-dev/tox-uv)
- Containerization with [Docker](https://www.docker.com/)
- Development environment with [VSCode devcontainers](https://code.visualstudio.com/docs/devcontainers/containers)

---

<p align="center">
  <a href="https://dcc-bs.github.io/cookiecutter-uv/">Documentation</a> - <a href="https://github.com/DCC-BS/example-project">Example</a>
</p>

---

## Prerequisites

Install [astral uv](https://docs.astral.sh/uv/getting-started/installation/) on your local device.

For winodws you additionaly need those installations:
- Install [Scoop](https://scoop.sh/)
- Install make: `scoop install make`

## Quickstart

On your local machine, navigate to the directory in which you want to
create a project directory, and run the following command:

```bash
uvx cookiecutter https://github.com/DCC-BS/cookiecutter-uv
```

Follow the prompts to configure your project. Once completed, a new directory containing your project will be created. Then navigate into your newly created project directory and follow the instructions in the `README.md` to complete the setup of your project.

## Acknowledgements

This project is partially based on [Audrey
Feldroy\'s](https://github.com/audreyfeldroy)\'s great
[cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) and this [uv cookiecutter fork](https://github.com/fpgmaas/cookiecutter-uv)
repository.
