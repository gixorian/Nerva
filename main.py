from fastapi import FastAPI, Response, status
from health_check import check_path
import os
import redis

app = FastAPI()

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True
)


@app.get("/stats", status_code=200)
def stats_endpoint(response: Response):
    response.status_code = status.HTTP_200_OK
    return {
        "total": r.get("total_checks") or 0,
        "healthy": r.get("healthy_count") or 0,
        "unhealthy": r.get("unhealthy_count") or 0,
    }


@app.get("/health", status_code=200)
def health_endpoint(response: Response, path: str = ""):
    query_path = ""

    if path == "":
        query_path = os.getenv("CHECK_PATH", "/app")
    else:
        query_path = path

    r.incr("total_checks")
    if check_path(query_path):
        r.incr("healthy_count")
        response.status_code = status.HTTP_200_OK
        return {"status": "healthy"}
    else:
        r.incr("unhealthy_count")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unhealthy", "reason": "Path not found"}
