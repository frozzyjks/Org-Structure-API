from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    DepartmentTreeResponse,
)
from app.services.department import DepartmentService

router = APIRouter(prefix="/departments", tags=["Departments"])
service = DepartmentService()


@router.post("/", response_model=DepartmentResponse)
async def create_department(
    data: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        department = await service.create(db, data.name, data.parent_id)
        return department
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: int,
    data: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        department = await service.update(
            db,
            department_id,
            data.name,
            data.parent_id,
        )
        return department
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{department_id}")
async def delete_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        await service.delete(db, department_id)
        return {"message": "Department deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{department_id}/tree", response_model=DepartmentTreeResponse)
async def get_department_tree(
    department_id: int,
    depth: int = Query(default=3, ge=1, le=5),
    include_employees: bool = False,
    db: AsyncSession = Depends(get_db),
):
    try:
        tree = await service.get_tree(
            db,
            department_id,
            depth,
            include_employees,
        )
        return tree
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))