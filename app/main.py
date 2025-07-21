from fastapi import FastAPI

from app.database import engine
from app.models import course, enrollment, user
from app.routers import users

user.Base.metadata.create_all(bind=engine)
course.Base.metadata.create_all(bind=engine)
enrollment.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the LMS API"}
