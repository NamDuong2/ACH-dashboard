from pydantic import BaseModel
from typing import List

class UserResponse(BaseModel):
    username: str
    roles: List[str]
    is_active: bool

