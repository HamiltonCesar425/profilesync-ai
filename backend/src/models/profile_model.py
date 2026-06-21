from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.session import Base

if TYPE_CHECKING:
    from models.user_model import User
    from models.resume_model import Resume


class ProfileModel(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    full_name: Mapped[str] = mapped_column(String(120))
    professional_title: Mapped[str] = mapped_column(String(120))
    summary: Mapped[str] = mapped_column(Text)

    location: Mapped[str | None] = mapped_column(String(120))
    linkedin_url: Mapped[str | None] = mapped_column(String(255))
    github_url: Mapped[str | None] = mapped_column(String(255))

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="profiles",
    )

    resumes: Mapped[list["Resume"]] = relationship(
        "Resume",
        back_populates="profile",
        cascade="all, delete-orphan",
    )
