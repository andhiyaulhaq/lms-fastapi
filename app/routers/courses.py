from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import course as course_crud
from app.dependencies import get_current_user, get_db
from app.schemas.course import CourseCreate, CourseOut, CourseUpdate

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("/", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "instructor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors can create courses",
        )
    return course_crud.create_course(db, course_data, instructor_id=user.id)


@router.get("/", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return course_crud.get_all_courses(db)


@router.get("/{course_id}", response_model=CourseOut)
def retrieve(course_id: int, db: Session = Depends(get_db)):
    course = course_crud.get_course(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
        )
    return course


@router.put("/{course_id}", response_model=CourseOut)
def update(
    course_id: int,
    update_data: CourseUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    course = course_crud.get_course(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
        )
    if course.instructor_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the course instructor can update this course",
        )
    return course_crud.update_course(db, course, update_data)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    course_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    course = course_crud.get_course(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
        )
    if course.instructor_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the course instructor can delete this course",
        )
    course_crud.delete_course(db, course)
    return None
