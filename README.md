# DevOps Health Checker

A containerized Python service that validates system paths and provides persistent logging. Built as a demonstration of CI/CD, Docker volume management, and secure container practices.

## Quick Start (Web API)

To run the utility with default settings:
```bash
docker run --rm -p 8000:8000 ghcr.io/gixorian/devops-health-check:latest
```
Then visit: `http://localhost:8000/health?path=/etc/passwd`
> [!NOTE]
> The ```--rm``` flag ensures the container is removed after execution to save disk space


## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
|CHECK_PATH|The absolute path inside the container to verify.|```/app```|


## CI/CD Architecture
Every push to the ```main``` branch triggers a GitHub Action that:
1. Lints the code using flake8 with customer linting rules defined in ```.flake8```.
2. Builds a new Docker image.
3. Pushes the versioned image to GitHub Container Registry (GHCR).
