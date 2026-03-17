from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# we inherit from BaseModel
class TaskModel(BaseModel):
    # this must be a string ( `TYPE HINTING` )
    title: str = Field(..., min_length=3, max_length=50)
    # this must be a string BUT is optional
    description: str | None = None
    # default state is False
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "First task",
                "description": "Complete your first task",
                "completed": False
            }
        }