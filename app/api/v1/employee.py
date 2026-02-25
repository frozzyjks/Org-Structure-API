from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.schemas.employee import EmployeeCreate, EmployeeResponse
from app.services.department import DepartmentService
from app.repositories.employee import EmployeeRepository
from app.repositories.department import DepartmentRepository

router = APIRouter(prefix="/employees", tags=["Employees"])

employee_repo = EmployeeRepository()
department_repo = DepartmentRepository()


@router.post("/{department_id}", response_model=EmployeeResponse)
async def create_employee(
    department_id: int,
    data: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
):
    department = await department_repo.get_by_id(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    employee = await employee_repo.create(
        db,
        department_id,
        data.full_name,
        data.position,
        data.hired_at,
    )
    return employee


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
):
    employee = await employee_repo.delete(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"message": "Employee deleted"}