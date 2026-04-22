# DevOps Health Checker

A production-ready health monitoring agent featuring a FastAPI web service, internal logging, and Redis persistence. This project demonstrates a multi-container architecture orchestrated with Docker Compose.

## 🚀 Features
- **FastAPI Interface:** High-performance asynchronous API for health monitoring.
- **Persistence:** Tracks success/failure metrics using a **Redis 8** backend.
- **Dynamic Probes:** Check any system path via query parameters.
- **Observability:** Structured logging with volume mapping for host-side analysis.
- **Orchestration:** Seamless multi-container management via Docker Compose.
- **CI/CD:** Automated linting and container builds via GitHub Actions.

## 🏗 Architecture
The system follows a Three-Tier architecture pattern:
1. **Client Tier:** Consumes the API via `curl` or browser.
2. **Application Tier:** FastAPI service running on Python 3.14-alpine.
3. **Data Tier:** Redis 8 (Alpine) for in-memory metrics storage with named volume persistence.

## 🛠 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/gixorian/devops-health-check
cd devops-health-check
```

### 2. Configure Environment
To handle local file permissions correctly, copy the template and set your User/Group IDs:
```bash
cp .env.example .env
```
> [!NOTE]
> Run ```id -u``` and ```id -g``` in your terminal to find your IDs and update the ```.env``` file.

### 3. Launch the Stack
```bash
docker compose up -d
```

## 📊 API Endpoints

### Health Check
Check the existence of a file path. Defaults to /app.
- **URL:** ```GET /health?path=/etc/passwd```
- **Success:** ```200 OK```
- **Failure:** ```503 Service Unavailable```

### Metrics Stats
Retrieve cumulative statistics stored in Redis.
- **URL:** ```GET /stats```
- **Response Example:**
  ```json
  {
    "total": "10",
    "healthy": "8",
    "unhealthy": "2"
  }
  ```

## 🪵 Logging & Volume Mapping

The application is configured to persist logs to the host machine, ensuring that log data is not lost when the container stops.

- **Host Path:** `./logs/health.log`
- **Container Path:** `/app/logs/health.log`
- **Volume Type:** Bind Mount

This allows you to monitor the application logs in real-time from your host terminal:
```bash
tail -f logs/health.log
```

## 💾 Persistence Note

This project uses a named Docker volume (```redis_data```). This means your statistics will survive a ```docker compose down```. To completely wipe the database, run:
```bash 
docker compose down -v
```

## 🤖 CI/CD Architecture

On every push to main, GitHub Actions will:

1. Install dependencies from requirements.txt.
2. Lint the code using flake8 with custom linting rules defined in ```.flake8```.
3. Build and push a new Docker image to GHCR (GitHub Container Registry).
