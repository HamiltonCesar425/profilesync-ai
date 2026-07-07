from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.session import Base

if TYPE_CHECKING:
    from models.job_model import JobModel
    from models.profile_model import ProfileModel
    from models.resume_model import Resume


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    profiles: Mapped[list["ProfileModel"]] = relationship(
        "ProfileModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    resumes: Mapped[list["Resume"]] = relationship(
        "Resume",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    jobs: Mapped[list["JobModel"]] = relationship(
        "JobModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )

