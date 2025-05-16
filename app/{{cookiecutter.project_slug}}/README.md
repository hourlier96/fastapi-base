# {{cookiecutter.project_name}}

{{ '=' * cookiecutter.project_name|length }}

## Description

{{cookiecutter.description}}

## Installation

You can run the application locally, or use Dev Container benefits

### Local

```sh
uv venv
source .venv/bin/activate
uv pip compile pyproject.toml --extra dev -o requirements.txt
uv pip install -r requirements.txt
pre-commit install  # Optional: requires git repository

# Then use VSCode launcher to run the app
```

### Dev container

```sh
devcontainer up --build-no-cache --workspace-folder .

# Then use VSCode launcher to attach debugger to the container
```

## Tests

```sh
python3 -m pytest
```

## CI/CD

### CI with Github Actions

[**Enable Github Actions API**](https://github.com/hourlier96/fastapi-base/actions) in your repository

Actions are configured to run linting for every Pull Request on 'develop', 'next' and 'main' branches

## Api docs

- [Swagger](http://localhost:8000/api/docs)

## Quickstart

1. Copy the example environment file and adapt values if needed:

```sh
cp .env.example .env
```

1. Run in a Dev Container (recommended for development):

```sh
# Start the devcontainer and run the `app` service.
devcontainer up --build-no-cache --workspace-folder .
```

This repository includes a `devcontainer` configuration that will:

- start the `app` service from `docker-compose.yml`,
- run a small setup script to install dev dependencies, and
- launch `uvicorn app.main:app --reload` inside the container.

1. Run locally (alternative):

```sh
# create venv and install deps (example)
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open the docs at `http://localhost:8000/api/docs`.
