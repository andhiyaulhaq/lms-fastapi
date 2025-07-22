from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    instructor = relationship("User", back_populates="courses")
    enrollments = relationship(
        "Enrollment", back_populates="course", cascade="all, delete-orphan"
    )
