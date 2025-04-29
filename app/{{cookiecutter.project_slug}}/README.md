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
pre-commit install

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
