from pydantic import BaseModel, Field
from pydantic import EmailStr
from typing import Optional, List

class UserInDB(BaseModel):
    username: str
    email: EmailStr
    password: str
    roles: List[str]  # "admin", "uploader", "approver"
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True


class UserOutDB(BaseModel):
    id: str = Field(..., alias='id')
    username: str = Field(..., alias='username')
    password: str = Field(..., alias='password')
    roles: List[str] = Field(..., alias='roles')

class TokenData(BaseModel):
    username: str
    scopes: List[str]

