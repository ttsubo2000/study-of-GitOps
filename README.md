# Study GitOps using Github Actions

This repository introduced how to practice GitOps using Github Actions with Docker container

## Prerequisites

- Docker Hub account
- Predefined Github Action Secrets:

        secrets.DOCKER_HUB_USERNAME
        secrets.DOCKER_HUB_TOKEN

## Technical commentary

### Get Version from Git

This step:

    - name: Extract version from git tag (if applicable)
      id: extract_version
      run: |
        GIT_TAG=$(git describe --tags --abbrev=0 --exact-match 2>/dev/null || true)
        if [ -n "$GIT_TAG" ]; then
          echo "VERSION=${GIT_TAG#v}" >> $GITHUB_ENV
          echo "IS_TAG=true" >> $GITHUB_ENV
        else
          COMMIT_SHA=$(git rev-parse --short "$GITHUB_SHA")
          echo "VERSION=0.0.0-$COMMIT_SHA" >> $GITHUB_ENV
          echo "IS_TAG=false" >> $GITHUB_ENV
        fi

This step will extract the version from the git tag, if available, and store it in the `VERSION` environment variable. If there's no git tag, it will create a version using the short commit SHA.

`GIT_TAG` will hold the tag name if the current commit is an exact match for a tag. If there's no tag, `GIT_TAG` will remain empty.

The `echo "VERSION=${GIT_TAG#v}" >> $GITHUB_ENV` line will remove the "v" prefix (if present)

## Build and Push Docker image

This step:

    - name: Build and push Docker image
      uses: docker/build-push-action@v2
      with:
        context: .
      push: true
      tags: |
        ${{ secrets.DOCKER_HUB_USERNAME }}/study_gitops:${{ env.VERSION }}
        ${{ secrets.DOCKER_HUB_USERNAME }}/study_gitops:latest
      build-args: |
        VERSION=${{ env.VERSION }}

This step will build the Docker image from the Dockerfile in the root of the repository (specified by `context: .`), push it to Docker Hub, and tag it with the version extracted from the git tag (`${{ env.VERSION }}`) and the `latest` tag.

The `build-args` parameter allows you to pass build arguments to the Dockerfile. In this case, we're passing the `VERSION` argument, which can be used in the Dockerfile for setting the version of your application.
