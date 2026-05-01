from celery import Celery
import time
import os
from database import SessionLocal
from models import TaskRecord

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
app = Celery("tasks", broker=broker_url)


@app.task
def process(task_id: int):
    db = SessionLocal()

    try:
        task = db.query(TaskRecord).filter(TaskRecord.id == task_id).first()

        if task:
            task.status = "PROCESSING"  # type: ignore
            db.commit()

            time.sleep(10)

            task.status = "COMPLETED"  # type: ignore
            db.commit()

    except Exception as e:
        print(f"Error occured: {e}")

        db.rollback()
        task.status = "FAILED"  # type: ignore
        db.commit()

    finally:
        db.close()
