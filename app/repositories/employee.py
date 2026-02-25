from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employee import Employee


class EmployeeRepository:

    async def create(
        self,
        db: AsyncSession,
        department_id: int,
        full_name: str,
        position: str,
        hired_at,
    ):
        employee = Employee(
            department_id=department_id,
            full_name=full_name,
            position=position,
            hired_at=hired_at,
        )
        db.add(employee)
        await db.commit()
        await db.refresh(employee)
        return employee

    async def get_by_id(self, db: AsyncSession, employee_id: int):
        result = await db.execute(
            select(Employee).where(Employee.id == employee_id)
        )
        return result.scalar_one_or_none()

    async def get_by_department(self, db: AsyncSession, department_id: int):
        result = await db.execute(
            select(Employee).where(Employee.department_id == department_id)
        )
        return result.scalars().all()

    async def delete(self, db: AsyncSession, employee_id: int):
        employee = await self.get_by_id(db, employee_id)
        if not employee:
            return None

        await db.delete(employee)
        await db.commit()
        return employee