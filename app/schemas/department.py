from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import List
from pydantic import ConfigDict

from app.schemas.employee import EmployeeResponse


class DepartmentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    parent_id: int | None = None

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty or whitespace")
        return value


class DepartmentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    parent_id: int | None = None

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str | None):
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value


class DepartmentResponse(BaseModel):
    id: int
    name: str
    parent_id: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DepartmentTreeResponse(BaseModel):
    department: DepartmentResponse
    employees: List[EmployeeResponse] = []
    children: List["DepartmentTreeResponse"] = []


DepartmentTreeResponse.model_rebuild()