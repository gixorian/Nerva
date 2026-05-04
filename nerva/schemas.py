from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    id: int
    status: str
    result: Optional[dict] = None
    task_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
