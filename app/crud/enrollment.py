from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User


def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()


def is_user_enrolled(db: Session, user_id: int, course_id: int):
    return db.query(Enrollment).filter_by(user_id=user_id, course_id=course_id).first()


def create_enrollment(db: Session, user: User, course_id: int):
    course = get_course(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
        )

    if is_user_enrolled(db, user.id, course_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already enrolled in this course",
        )

    enrollment = Enrollment(user_id=user.id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return {
        "user_id": enrollment.user_id,
        "course_id": enrollment.course_id,
        "enrollment_date": enrollment.enrollment_date,
        "message": "User successfully enrolled",
    }


def delete_enrollment(db: Session, user: User, course_id: int):
    enrollment = is_user_enrolled(db, user.id, course_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not enrolled in this course",
        )

    db.delete(enrollment)
    db.commit()


def get_course_enrollments(db: Session, course_id: int, instructor_id: int):
    course = get_course(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
        )
    if course.instructor_id != instructor_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the course instructor can view enrollments",
        )

    return db.query(Enrollment).filter(Enrollment.course_id == course_id).all()


def get_user_enrollments(db: Session, user_id: int):
    return db.query(Enrollment).filter(Enrollment.user_id == user_id).all()
