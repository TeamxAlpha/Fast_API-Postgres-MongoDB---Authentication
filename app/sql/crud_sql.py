import uuid
from sqlalchemy.orm import Session
from app.schema import schemas
from app.model import models
from passlib.context import CryptContext
import redis

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# redis for session management
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# create user
def create_user_sql(db: Session, user_in: schemas.UserCreate):
    hashed_password = pwd_context.hash(user_in.password)
    user = models.User(
        name=user_in.name,
        email=user_in.email,
        password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# authenticate user
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        return None
    return user

# session management
def create_session(user_id: int):
    token = str(uuid.uuid4())
    r.set(token, user_id, ex=3600)
    return token

def get_user_by_session(token: str):
    user_id = r.get(token)
    return int(user_id) if user_id else None
