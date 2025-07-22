from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.database import engine
from app.models import course, enrollment, user
from app.routers import courses, enrollments, users

user.Base.metadata.create_all(bind=engine)
course.Base.metadata.create_all(bind=engine)
enrollment.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(courses.router)
app.include_router(enrollments.router)

for route in app.routes:
    if isinstance(route, APIRoute):
        print(f"{route.path} -> {route.methods}")


@app.get("/")
def read_root():
    return {"message": "Welcome to the LMS API"}
