import os
import time
from celery import Celery
from nerva.database import SessionLocal
from nerva.models import TaskRecord
from nerva.registry import TASK_REGISTRY, register_task

redis_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery_app = Celery("nerva", broker=redis_url, backend=redis_url)


@celery_app.task(bind=True)
def nerva_worker(self, task_id: int):
    db = SessionLocal()
    try:
        task = db.query(TaskRecord).filter(TaskRecord.id == task_id).first()
        if not task:
            return f"Task {task_id} not found"

        task.status = "WORKING"  # type: ignore
        db.commit()

        logic_func = TASK_REGISTRY.get(task.task_type)

        if logic_func:
            execution_result = logic_func(task.payload)
            task.result = execution_result
            task.status = "COMPLETED"  # type: ignore
        else:
            task.status = "FAILED"  # type: ignore
            task.result = {"error": f"No logic registered for {task.task_type}"}  # type: ignore

        db.commit()
        return f"Task {task_id} finished with status: {task.status}"

    except Exception as e:
        db.rollback()
        task = db.query(TaskRecord).filter(TaskRecord.id == task_id).first()
        if task:
            task.status = "FAILED"  # type: ignore
            task.result = {"error": str(e)}  # type: ignore
            db.commit()
        raise e
    finally:
        db.close()


def perform_debug_sleep(payload: dict):
    seconds = payload.get("seconds", 10)
    time.sleep(seconds)
    return {"message": "Sleep finished", "slept_for": seconds}


register_task("DEBUG_SLEEP", perform_debug_sleep)
