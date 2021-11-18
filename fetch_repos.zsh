#! /usr/bin/env zsh

echo "Fetching the following repos..."

REPOS_DIR="${HOME}/repos"
FETCH_TARGETS="${REPOS_DIR}/.fetch_targets"


for repo in $( cat "${FETCH_TARGETS}" | grep -v '^#' ) ; do
    echo " -> ${repo}"

    ## For dev workflow
    #rm -rf "${HOME}/repos/${repo}"
    #git clone "git@gitlab.oracledatacloud.com:moat/${repo}.git"

    git -C "${HOME}/repos/${repo}" \
        fetch
done
