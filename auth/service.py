from typing import Optional, List
from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from .schemas import UserInDB, UserOutDB
from .repository import UserRepository
from .utils import verify_password, encode_jwt
import jwt
import datetime
from fastapi.security import OAuth2PasswordRequestForm
from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:
    def __init__(self, user_repository = Depends(UserRepository)):
        self.user_repository = user_repository
        
    async def authenticate_user(self, form_data: OAuth2PasswordRequestForm = Depends()) -> Optional[JSONResponse]:
        user = await self.user_repository.get_user_by_username(form_data.username)
        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        token = encode_jwt(user.id, user.username, user.roles)
        response = JSONResponse(status_code=200, content={"token": token})
        return response

    """ async def get_current_user(self, token: str = Depends(get_oauth2_scheme())) -> Optional[UserOutDB]:
        try:
            if isinstance(token, str):
                payload = self._decode_jwt(token)
                username = payload.get("username")
                if username is None:
                    raise HTTPException(
                        status_code=401,
                        detail="Invalid authentication credentials",
                    )
            else:
                raise HTTPException(status_code=401, detail="Invalid token format")
        except Exception as e:
            print(f"Error in get_current_user: {e}")
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            ) 
        
        user = await self.user_repository.get_user_by_username(username)
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user """
    
    async def get_user_by_username(self, username: str) -> Optional[UserOutDB]:
        return await self.user_repository.get_user_by_username(username)

