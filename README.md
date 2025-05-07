# FastAPI Template Generator

A duplicable [FastAPI](https://fastapi.tiangolo.com/) code base:

[See ReadMe](app/{{cookiecutter.project_slug}}/README.md)

## Features

New project generation with [cookiecutter](https://github.com/cookiecutter/cookiecutter)

- Automated push on empty repository
- [devcontainer](https://code.visualstudio.com/docs/remote/containers) environment
- Linting & Formatter with [ruff](https://github.com/charliermarsh/ruff) & [mypy](https://github.com/python/mypy)
- Precommit hooks with [precommit](https://pre-commit.com)
- [Github Actions](https://github.com/features/actions) CI/CD pipeline

## Generation

Clone this repository and install dependencies

```bash
cd fastapi-base
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

(Optional): Add a github access token to .env file if you want the branch protection to be automated at generation

```bash
# .env content ...
GITHUB_ACCESS_TOKEN="<PERSONAL_ACCESS_TOKEN>"
```

Generate the code base

```bash
cookiecutter fastapi-base/app   # Will ask your needs from cookiecutter.json
```

### Options

- **'repository_name'** allows you to specify an empty-existing Git repository to push the template on.

  ```bash
  <github_username>/<repo_name>  # Required format

  # 1. Ensure you have corrects SSH rights & access

  # 2. This will also set branch protection if you specified GITHUB_ACCESS_TOKEN variable in .env
  # Change settings as your convenience in hooks_modules/branch_protection.json
  ```

- **'project_name'** is the name on the top of ReadMe.

- **'project_slug'** is the name of the generated folder

- **'description'** will be added under the project name in the ReadMe.

- **'database'** will add selected async dependencies to the pyproject.toml

## CI

The generation is tested to ensure the template is working as expected.

Test locally with [act](https://github.com/nektos/act):

```sh
act -j <job_name> --rm -W .github/workflows/template-generation.yaml
```
