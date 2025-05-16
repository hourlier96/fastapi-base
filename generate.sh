#!/bin/bash

echo -e "\n==========================="
echo "|    FastAPI Generator    |"
echo "|                         |"
echo "|    by @hourlier96       |"
echo -e "===========================\n"
echo "This script will generate a new folder"
echo -e "Ensure the project slug you gonna choose is available at '$(realpath ../)'\n"

CLONE_DIR="fastapi-base"
VENV_DIR=".venv"

if ! [ -d "../$CLONE_DIR" ]; then
  echo "Directory $CLONE_DIR doesn't exists. You probably cloned the repository with a different name. Change the CLONE_DIR variable in generate.sh"
  exit 1
fi


if ! command -v uv &> /dev/null; then
  echo "❌ Error: uv not installed. Please install it first."
  exit 1
fi

# Delete old virtual environment if it exists
if [ -d "$VENV_DIR" ]; then
  rm -rf "$VENV_DIR"
  exit 1
fi

uv venv "$VENV_DIR" > /dev/null 2>&1
source "$VENV_DIR/bin/activate" > /dev/null 2>&1

uv pip install -r requirements.txt > /dev/null 2>&1

# GITHUB_TOKEN passed as parameter
if [ -n "$1" ]; then
  if [ ! -f "app/{{cookiecutter.project_slug}}/.env" ]; then
      touch "app/{{cookiecutter.project_slug}}/.env"
  fi
  echo "$1" > "app/{{cookiecutter.project_slug}}/.env"
fi

cd ..

echo -e "------------------------------------------------------"
if ! cookiecutter "$CLONE_DIR"/app; then
  rm -rf "$CLONE_DIR"/"$VENV_DIR"
  exit 1
fi
rm -rf "$CLONE_DIR"/"$VENV_DIR"
echo -e "\n----------------------------------------------------"

