# DevOps Health Checker

A containerized Python service that validates system paths and provides persistent logging. Built as a demonstration of CI/CD, Docker volume management, and secure container practices.

## Quick Start

To run the utility with default settings:
```bash
docker run --rm ghcr.io/gixorian/devops-health-check:latest
```

## Advanced Usage (Persistance)

To map local logs and check a specific path, use the following command.
> [!NOTE]
> The --rm flag ensures the container is removed after execution to save disk space
```bash
mkdir -p logs
docker run --rm \
-u $(id -u):$(id -g) \
-v $(pwd)/logs:/app/logs \
-e CHECK_PATH=/etc/passwd \
ghcr.io/gixorian/devops-health-check:latest
```
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
|CHECK_PATH|The absolute path inside the container to verify.|```/app```
