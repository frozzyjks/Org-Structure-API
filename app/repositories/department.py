from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.department import Department
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select


class DepartmentRepository:

    async def get_by_name_and_parent(
            self,
            db: AsyncSession,
            name: str,
            parent_id: int | None,
    ):
        result = await db.execute(
            select(Department).where(
                Department.name == name,
                Department.parent_id == parent_id,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, name: str, parent_id: int | None):
        department = Department(name=name, parent_id=parent_id)
        db.add(department)
        try:
            await db.commit()
            await db.refresh(department)
            return department
        except IntegrityError:
            await db.rollback()
            raise ValueError("Department name must be unique within the same parent")

    async def get_by_id(self, db: AsyncSession, department_id: int):
        result = await db.execute(
            select(Department).where(Department.id == department_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Department))
        return result.scalars().all()

    async def update(
        self,
        db: AsyncSession,
        department_id: int,
        name: str | None,
        parent_id: int | None,
    ):
        department = await self.get_by_id(db, department_id)
        if not department:
            return None

        if name is not None:
            department.name = name

        department.parent_id = parent_id

        try:
            await db.commit()
            await db.refresh(department)
            return department
        except IntegrityError:
            await db.rollback()
            raise ValueError("Department name must be unique within the same parent")

    async def delete(self, db: AsyncSession, department_id: int):
        department = await self.get_by_id(db, department_id)
        if not department:
            return None

        await db.delete(department)
        await db.commit()
        return department