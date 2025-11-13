from fastapi import APIRouter, HTTPException, Depends
from app.nosql import crud_nosql, db_nosql
from app.schema import schemas
from bson.errors import InvalidId
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/nosql/users", tags=["NoSQL Users"])
security = HTTPBearer()

@router.post("/register")
def register(user_in: schemas.UserCreate):
    if db_nosql.get_user_by_email(user_in.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash password with Argon2
    user_data = {
        "name": user_in.name,
        "email": user_in.email,
        "password": crud_nosql.hash_password(user_in.password)
    }
    db_nosql.users_collection.insert_one(user_data)
    return {"msg": "User registered"}

@router.post("/login")
def login(user_in: schemas.UserLogin):
    user = db_nosql.get_user_by_email(user_in.email)
    if not user or not crud_nosql.verify_password(user_in.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT token
    token = crud_nosql.create_access_token({"user_id": str(user["_id"])})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get current logged-in user info.
    use HTTPbearer to auto parse authentication token bearer.
    """
    token = credentials.credentials

    user_id = crud_nosql.verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    try:
        user = db_nosql.get_user_by_id(user_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID in token")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}