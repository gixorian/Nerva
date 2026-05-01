from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime, timezone


class TaskRecord(Base):
    __tablename__ = "task_records"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    result = Column(String, nullable=True)
