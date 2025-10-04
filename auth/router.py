from fastapi import APIRouter, Request, Body, Depends, HTTPException
from .service import AuthService
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from fastapi import status, Security
from fastapi.security import SecurityScopes
from config import JWT_SECRET_KEY, JWT_ALGORITHM
import jwt
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from .schemas import TokenData
from .utils import get_current_user, is_token_valid

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/verify")
async def verify(token_info: dict = Depends(is_token_valid)):
    return {"success": True, "username": token_info["username"]}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service = Depends(AuthService)):
    response = await auth_service.authenticate_user(form_data)
    if response:
        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@router.post("/logout")
async def logout(auth_service = Depends(AuthService)):
    # Implement logout logic if needed (e.g., token invalidation)
    return {"message": "Logged out successfully"}
