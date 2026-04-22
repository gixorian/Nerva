from fastapi import FastAPI, Response, status
from health_check import check_path
import os

app = FastAPI()


@app.get("/health", status_code=200)
def health_endpoint(response: Response, path: str = ""):
    query_path = ""

    if path == "":
        query_path = os.getenv("CHECK_PATH", "/app")
    else:
        query_path = path

    if check_path(query_path):
        response.status_code = status.HTTP_200_OK
        return {"status": "healthy"}
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unhealthy", "reason": "Path not found"}
