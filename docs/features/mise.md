# Task runner (mise)

The generated repository uses [mise](https://mise.jdx.dev/) both for managing the
tool versions (`python`, `uv`, etc., pinned in `mise.toml`) and as the single
entry point for development tasks.

A list of all available tasks can be obtained by running `mise tasks` in the
terminal. Initially, if all features are selected, the following tasks are
available (run with `mise run <task>`):

```
install              Create the virtual environment and install the pre-commit hooks
dev                  Run the FastAPI dev server with auto-reload
run                  Run the production ASGI server (uvicorn)
check                Verify lockfile, format code, lint, and type-check
test                 Run the test suite (including doctests)
ci                   Run all CI checks (lock, format, lint, types, tests)
build                Build the wheel file
docs                 Build and serve the MkDocs documentation   (mkdocs only)
docs:deploy          Deploy the docs to GitHub Pages             (mkdocs only)
deptry               Check for obsolete dependencies            (deptry only)
docker:up            Start docker compose services
docker:down          Stop docker compose containers
```

Secrets are loaded through `varlock` via the `env-check` task, which depends on
`pass-login` (provided by the `.mise-tasks/` scripts). The `postinstall` and
`enter` hooks run `install` and a login check automatically when you enter the
project directory.
