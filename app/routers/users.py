from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.user import (  # get_user_by_id,
    create_user,
    get_user_by_email,
    get_user_by_username,
    update_user,
    verify_password,
)
from app.dependencies import get_current_user, get_db
from app.schemas.user import Token, UserCreate, UserLogin, UserOut, UserUpdate
from app.utils.auth import create_access_token

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    try:
        return create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, credentials.username)
    if not db_user or not verify_password(
        credentials.password, db_user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def get_profile(current_user: UserOut = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut)
def update_profile(
    updates: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return update_user(db, current_user.id, updates)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Username or email already taken"
        ) from e
