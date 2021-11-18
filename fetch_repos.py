#! /usr/bin/env python3

import os.path
import pprint

import yaml
import git

REPO_TARGETS_FNAME = "~/repos/.fetch_targets.yml"
DRY_RUN = False


def fetch_or_clone(git_server_uri, repo_name):
    repo_path = os.path.expanduser("~/repos/{repo_name}".format(repo_name=repo_name))
    exists = os.path.isdir(repo_path)

    repo_url = "{git_server_uri}/{repo_name}.git".format(
        git_server_uri=git_server_uri,
        repo_name=repo_name,
    )


    if exists:
        # Repo already exists locally.
        # Just fetch the latest changes.
        repo = git.Repo(path=repo_path)
        for remote in repo.remotes:
            print("Fetching {repo_name} ...".format(repo_name=repo_name))
            if not DRY_RUN:
                remote.fetch()

    else:
        # Repo does not yet exist, locally.
        # Clone it.
        print("{repo_name} does not exist.".format(repo_name=repo_name))
        print(" -> Cloning {repo_name} ...".format(repo_name=repo_name))
        if not DRY_RUN:
            git.Repo.clone_from(url=repo_url, to_path=repo_path)


def main(targets: str):
    for git_server_uri, repos in targets.items():
        for repo_name in repos:
            fetch_or_clone(git_server_uri, repo_name)


if __name__ == "__main__":
    targets = yaml.load(
        open(os.path.expanduser(REPO_TARGETS_FNAME)),
        Loader=yaml.FullLoader
    )
    main(targets)
