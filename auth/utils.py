from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi import Depends, HTTPException, status, Security
from typing import List, Optional, Annotated
from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from config import TOKEN_URL
from datetime import datetime, timedelta
import jwt
from .schemas import TokenData

def get_password_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_oauth2_scheme():
    return OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

def get_password_hash(password: str) -> str:
    pwd_context = get_password_context()
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_context = get_password_context()
    return pwd_context.verify(plain_password, hashed_password)

def encode_jwt(user_id: str, username: str, roles: List[str]) -> str:
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES),  # Use utcnow for consistency
            "iat": datetime.utcnow(),  # Use utcnow for consistency
            "sub": {"user_id": user_id, "username": username, "roles": roles},      
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)  # Ensure "secret" is consistent
        return token

def decode_jwt(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]) 
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:  # Capture the specific error
        print(f"Invalid token error: {e}")  # Log the error for debugging
        raise HTTPException(status_code=401, detail="Invalid token")

async def is_token_valid(token: Annotated[str, Depends(get_oauth2_scheme())]):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return {"username": payload["sub"]["username"]}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(get_oauth2_scheme())]):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scopes}"'
    else:
        authenticate_value = "Bearer"
    
    try:
        # Decode the JWT token
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        print("Decoded payload:", payload)  # Debugging line

        # Access the 'sub' field which contains user details
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        username = sub.get("username")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        # Access roles from 'sub'
        token_scopes = sub.get("roles", [])
        print("Token roles:", token_scopes) 
        print("Security scopes:", security_scopes.scopes)
        # Check if the token has the required scopes
        for scope in security_scopes.scopes:
            print("Checking scope:", scope)
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        
        return TokenData(username=username, scopes=token_scopes)

    except jwt.PyJWTError as e:
        print("JWT Error:", e)  # Debugging line
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
