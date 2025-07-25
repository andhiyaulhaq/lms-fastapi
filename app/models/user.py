from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # Relationships
    courses = relationship(
        "Course", back_populates="instructor"
    )  # if this user can create courses
    enrollments = relationship(
        "Enrollment", back_populates="user", cascade="all, delete-orphan"
    )
