from sqlalchemy import String, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.core.database import Base


class Department(Base):
    __tablename__ = "departments"

    __table_args__ = (
        UniqueConstraint("parent_id", "name", name="uq_department_parent_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    parent = relationship(
        "Department",
        remote_side=[id],
        backref="children",
    )

    employees = relationship(
        "Employee",
        back_populates="department",
        cascade="all, delete",
    )