from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.department import DepartmentRepository
from app.repositories.employee import EmployeeRepository
from app.models.department import Department
from sqlalchemy import select


class DepartmentService:

    def __init__(self):
        self.repo = DepartmentRepository()
        self.employee_repo = EmployeeRepository()

    async def create(self, db: AsyncSession, name: str, parent_id: int | None):

        if parent_id:
            parent = await self.repo.get_by_id(db, parent_id)
            if not parent:
                raise ValueError("Parent department not found")

        existing = await self.repo.get_by_name_and_parent(
            db,
            name,
            parent_id,
        )

        if existing:
            raise ValueError(
                "Department name must be unique within the same parent"
            )

        return await self.repo.create(db, name, parent_id)

    async def update(
        self,
        db: AsyncSession,
        department_id: int,
        name: str | None,
        parent_id: int | None,
    ):
        department = await self.repo.get_by_id(db, department_id)
        if not department:
            raise ValueError("Department not found")

        if parent_id == department_id:
            raise ValueError("Department cannot be parent of itself")

        if parent_id:
            parent = await self.repo.get_by_id(db, parent_id)
            if not parent:
                raise ValueError("Parent department not found")

            if await self._is_descendant(db, parent_id, department_id):
                raise ValueError("Cycle detected")

        existing = await self.repo.get_by_name_and_parent(
            db,
            name,
            parent_id,
        )

        if existing and existing.id != department_id:
            raise ValueError(
                "Department name must be unique within the same parent"
            )

        return await self.repo.update(db, department_id, name, parent_id)

    async def delete(self, db: AsyncSession, department_id: int):
        department = await self.repo.get_by_id(db, department_id)
        if not department:
            raise ValueError("Department not found")

        return await self.repo.delete(db, department_id)

    async def get_tree(
        self,
        db: AsyncSession,
        department_id: int,
        depth: int = 3,
        include_employees: bool = False,
    ):
        if depth < 1 or depth > 5:
            raise ValueError("Depth must be between 1 and 5")

        department = await self.repo.get_by_id(db, department_id)
        if not department:
            raise ValueError("Department not found")

        return await self._build_tree(
            db,
            department,
            depth,
            include_employees,
        )

    async def _is_descendant(
        self,
        db: AsyncSession,
        parent_id: int,
        target_id: int,
    ):
        current = await self.repo.get_by_id(db, parent_id)

        while current:
            if current.parent_id == target_id:
                return True
            if not current.parent_id:
                return False
            current = await self.repo.get_by_id(db, current.parent_id)

        return False

    async def _build_tree(
            self,
            db: AsyncSession,
            department: Department,
            depth: int,
            include_employees: bool,
    ):
        if depth == 0:
            return None

        employees = []
        if include_employees:
            employees = await self.employee_repo.get_by_department(
                db,
                department.id,
            )

        result = await db.execute(
            select(Department).where(Department.parent_id == department.id)
        )
        children_departments = result.scalars().all()

        children = []
        for child in children_departments:
            subtree = await self._build_tree(
                db,
                child,
                depth - 1,
                include_employees,
            )
            if subtree:
                children.append(subtree)

        return {
            "department": department,
            "employees": employees,
            "children": children,
        }