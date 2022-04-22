#! /usr/bin/env python3

import os.path
import pprint
import argparse

import yaml
import git

REPO_TARGETS_FNAME = "~/repos/.fetch_targets.yml"
DRY_RUN = False
DEBUG = False


def fetch_or_clone(git_server_uri: str, repo_name: str, fetch: bool=True, clone: bool=True):
    repo_path = os.path.expanduser("~/repos/{repo_name}".format(repo_name=repo_name))
    exists = os.path.isdir(repo_path)

    repo_url = "{git_server_uri}/{repo_name}.git".format(
        git_server_uri=git_server_uri,
        repo_name=repo_name,
    )


    if exists: # Source tree for repo already exists, locally. Fetch it.
        if fetch:
            # Repo already exists locally.
            # Just fetch the latest changes.

            print("Fetching {repo_name} ...".format(repo_name=repo_name))
            if not DRY_RUN:
                repo = git.Repo(path=repo_path)
                for remote in repo.remotes:
                    remote.fetch()

        else:
            if DEBUG: print("( Skipping fetch for {repo_name} )".format(repo_name=repo_name))

    else: # Source tree for repo does not yet exist, locally. Clone it.
        if clone:
            # Repo does not yet exist, locally.
            # Clone it.
            print("{repo_name} does not exist.".format(repo_name=repo_name))
            print(" -> Cloning {repo_name} ...".format(repo_name=repo_name))
            if not DRY_RUN:
                git.Repo.clone_from(url=repo_url, to_path=repo_path)

        else:
            if DEBUG: print("( Skipping clone for {repo_name} )".format(repo_name=repo_name))


def main(targets: str, fetch: bool=True, clone: bool=True):
    for git_server_uri, repos in targets.items():
        for repo_name in repos:
            fetch_or_clone(
                git_server_uri=git_server_uri,
                repo_name=repo_name,
                fetch=fetch,
                clone=clone,
            )


if __name__ == "__main__":
    targets = yaml.load(
        open(os.path.expanduser(REPO_TARGETS_FNAME)),
        Loader=yaml.FullLoader
    )

    # Parse arguments. Support options such as:
    # - Fetch-only: i.e. do not clone any repos that don't yet exist locally
    # - Clone-only: i.e. do not fetch existing repos

    ap = argparse.ArgumentParser()
    ap.add_argument('--fetch-only', action='store_true')
    ap.add_argument('--clone-only', action='store_true')
    args = ap.parse_args()
    assert not (args.fetch_only and args.clone_only), \
        "Arguments --fetch-only and --clone-only are mutually exclusive. Provide one or the other, not both."

    # Run the main functionality
    main(
        targets = targets,
        fetch = args.fetch_only or not args.clone_only,
        clone = args.clone_only or not args.fetch_only,
    )
