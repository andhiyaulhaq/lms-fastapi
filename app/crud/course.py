from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


def create_course(db: Session, course_data: CourseCreate, instructor_id: int):
    course = Course(**course_data.dict(), instructor_id=instructor_id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get_all_courses(db: Session):
    return db.query(Course).all()


def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()


def update_course(db: Session, course: Course, update_data: CourseUpdate):
    for field, value in update_data.dict().items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course: Course):
    db.delete(course)
    db.commit()
