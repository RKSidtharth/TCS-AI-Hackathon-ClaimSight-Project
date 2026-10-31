from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    email: str
    password: str
    name: str
    role: Optional[str] = "investigator"
    department: Optional[str] = "Motor Claims Investigation"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class UserOut(BaseModel):
    user_id: str
    name: str
    email: str
    role: str
    department: Optional[str] = None

