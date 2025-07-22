from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud import enrollment as crud
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.enrollment import EnrollmentOut, EnrollmentPostResponse

router = APIRouter(prefix="/courses", tags=["Enrollments"])


@router.post(
    "/{course_id}/enroll",
    response_model=EnrollmentPostResponse,
    status_code=status.HTTP_201_CREATED,
)
def enroll(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.create_enrollment(db, current_user, course_id)


@router.delete("/{course_id}/enroll", status_code=status.HTTP_204_NO_CONTENT)
def unenroll(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    crud.delete_enrollment(db, current_user, course_id)
    return


@router.get("/{course_id}/enrollments", response_model=list[EnrollmentOut])
def list_course_enrollments(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.get_course_enrollments(db, course_id, instructor_id=current_user.id)


# @router.get("/me/enrollments", response_model=list[EnrollmentOut])
# def list_my_enrollments(
#     db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
# ):
#     return crud.get_user_enrollments(db, current_user.id)
