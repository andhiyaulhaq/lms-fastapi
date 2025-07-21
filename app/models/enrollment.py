from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from app.database import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "course_id", name="_user_course_uc"),)
