from sqlalchemy import Column, Integer, String, Text

from database.session import Base


class ProfileModel(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    professional_title = Column(String(120), nullable=False)
    summary = Column(Text, nullable=False)
    location = Column(String(120), nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    github_url = Column(String(255), nullable=True)
