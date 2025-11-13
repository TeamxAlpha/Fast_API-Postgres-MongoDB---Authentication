from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.sql import crud_sql, db_sql
from app.schema import schemas
from app.model import models

router = APIRouter(prefix="/sql/users", tags=["SQL Users"])

@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(db_sql.get_db)):
    return crud_sql.create_user_sql(db, user_in)

@router.post("/login")
def login(user_in: schemas.UserLogin, db: Session = Depends(db_sql.get_db)):
    user = crud_sql.authenticate_user(db, user_in.email, user_in.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = crud_sql.create_session(user.id)
    return {"session_token": token}

@router.get("/me", response_model=schemas.UserOut)
def get_me(session_token: str, db: Session = Depends(db_sql.get_db)):
    user_id = crud_sql.get_user_by_session(session_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid session")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user
