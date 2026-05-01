import os
import redis
from fastapi import FastAPI, HTTPException, Response, status, Depends
from health_check import check_path
from tasks import process
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import TaskRecord

app = FastAPI()

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True
)

Base.metadata.create_all(bind=engine)


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


@app.get("/process", status_code=202)
def process_endpoint(response: Response, db: Session = Depends(get_db)):
    new_task = TaskRecord(status="PENDING")
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    process.delay(new_task.id)  # type: ignore
    response.status_code = status.HTTP_202_ACCEPTED
    return {"status": "working", "task_id": new_task.id}


@app.get("/status/{task_id}", status_code=200)
def task_status_endpoint(task_id, db: Session = Depends(get_db)):
    task = db.query(TaskRecord).filter(TaskRecord.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found"
        )

    return {"task_id": task.id, "status": task.status}
