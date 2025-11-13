from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    def password_length(cls, v):
        if len(v) > 72:
            raise ValueError("Password ideally can be between 72 characters")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def password_length(cls, v):
        if len(v) > 72:
            raise ValueError("Password ideally can be between 72 characters")
        return v

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
