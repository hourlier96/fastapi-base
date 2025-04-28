# {{cookiecutter.project_name}}

{{ '=' * cookiecutter.project_name|length }}

## Description

{{cookiecutter.description}}

## Run locally

```sh
uv venv
source .venv/bin/activate
uv pip compile pyproject.toml --extra dev -o requirements.txt
uv pip install -r requirements.txt

# Then run VSCode launcher 
```

## In Container

```sh
devcontainer up --build-no-cache --workspace-folder .

# Then use VSCode launcher to attach debugger to the container
```

## Tests

```sh
python3 -m tests
```

## CI/CD

### CI with Github Actions

[**Enable Github Actions API**](https://github.com/hourlier96/fastapi-base/actions) in your repository

Actions are configured to run linting for every Pull Request on develop, uat and main branches

## Api docs

- [Swagger](http://localhost:8000/api/docs)
