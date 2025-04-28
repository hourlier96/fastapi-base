import json

import git
import requests


def checkRepositoryNameOption(repo_name):
    """
    Check if repository_name is empty,
    if not init & fill empty git repo
    """
    if not repo_name:
        return

    g = git.cmd.Git(repo_name)
    g.init()
    g.remote("add", "origin", f"git@github.com:{repo_name}.git")
    g.add(".")
    g.commit("-m", "Commit made by cookiecutter")
    g.branch("-M", "main")

    g.branch("develop")
    g.merge("develop")

    g.branch("uat")
    g.merge("uat")

    g.config("init.defaultBranch", "develop")

    g.push("-u", "origin", "--all")
    print(f"Pushed to remote repository: https://github.com/{repo_name}")


def enableBranchesProtection(repo_name, github_token):
    """
    Use GITHUB_TOKEN to enable & set branches protection
    """
    owner = repo_name.split("/")[0]
    repo = repo_name.split("/")[1]
    base_url = f"https://api.github.com/repos/{owner}/{repo}/branches"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
    }

    # https://docs.github.com/en/rest/branches/branch-protection?apiVersion=2022-11-28#update-branch-protection
    # Update the config according to your needs
    body = json.dumps(json.load(open("./hooks_modules/branch_protection.json")))

    branches = ["develop", "uat", "main"]
    for branch in branches:
        url = f"{base_url}/{branch}/protection"
        response = requests.put(url, body, headers=headers)
        if response.status_code != 200:
            print(f"Failed to activate protection for branch {branch}:")
            print(response.json())
            break
