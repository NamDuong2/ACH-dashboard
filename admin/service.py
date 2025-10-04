from auth.schemas import UserInDB
from fastapi import Depends, HTTPException
from .repository import AdminRepository
from auth.utils import get_password_hash
from typing import List, Optional
from .schemas import UserResponse

class AdminService:
    def __init__(self, admin_repository = Depends(AdminRepository)):
        self.admin_repository = admin_repository

    async def create_user(self, user: UserInDB) -> bool:
        try:
            user_exists = await self.admin_repository.get_user_by_username(user.username)
            if user_exists:
                raise HTTPException(status_code=400, detail="User already exists")
            user.password = get_password_hash(user.password)  # Hash password before saving
            success = await self.admin_repository.create_user(user)
            if not success:
                raise HTTPException(status_code=500, detail="Failed to create user")
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_one_user(self, offset: int) -> dict:
        try:
            users = await self.admin_repository.list_users(offset, 1)
            return {"data": [{
                "id": user.id, 
                "username": user.username, 
                "roles": user.roles, 
                "is_active": user.is_active
            } for user in users]}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def list_users(self, page: int, limit: int) -> dict:
        try:
            offset = (page - 1) * limit
            users = await self.admin_repository.list_users(offset, limit)
            total_users = await self.admin_repository.get_total_users()
            total_pages = (total_users + limit - 1) // limit
            return {
                "data": [{
                    "id": user.id, 
                    "username": user.username, 
                    "roles": user.roles, 
                    "is_active": user.is_active
                } for user in users],
                "total_pages": total_pages,
                "total_users": total_users,
                "total_users_in_page": len(users)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        try:
            user = await self.admin_repository.get_user_by_id(user_id)
            if user is None:
                raise HTTPException(status_code=400, detail="User not found")
            return UserResponse(
                id=user.id,
                username=user.username,
                roles=user.roles,
                is_active=user.is_active
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 
    
    async def delete_user(self, user_id: int) -> bool:
        try:
            success = await self.admin_repository.delete_user(user_id)
            if not success:
                raise HTTPException(status_code=400, detail="User not found")
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))