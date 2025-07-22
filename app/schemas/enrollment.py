from datetime import datetime

from pydantic import BaseModel


class EnrollmentOut(BaseModel):
    user_id: int
    course_id: int
    enrollment_date: datetime

    class Config:
        from_attributes = True


class EnrollmentPostResponse(BaseModel):
    user_id: int
    course_id: int
    enrollment_date: datetime
    message: str

    class Config:
        from_attributes = True
