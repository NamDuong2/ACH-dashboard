from database import get_async_session
from sqlalchemy import select, delete, func
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import Depends
from auth.schemas import UserInDB
from models import User
from typing import Optional, List

class AdminRepository:
    def __init__(self, session: Session = Depends(get_async_session)):
        self.session = session

    async def create_user(self, user_in: UserInDB) -> bool:
        try:
            user = User(
                username=user_in.username,
                email=user_in.email,
                password=user_in.password,
                is_active=user_in.is_active,
                roles=user_in.roles
            )
            async with self.session.begin():
                self.session.add(user)
                await self.session.commit()
            return True
        except Exception as e:
            return False

    async def list_users(self, offset: int, limit: int) -> List[dict]:
        try:
            async with self.session.begin():
                sql = select(User.id, User.username, User.roles, User.is_active).limit(limit).offset(offset)
                result = await self.session.execute(sql)
            return result.fetchall()
        except Exception as e:
            return []

    async def get_total_users(self) -> int:
        try:
            async with self.session.begin():
                sql = select(func.count(User.id))
                result = await self.session.execute(sql)
            return result.scalar_one_or_none()
        except Exception as e:
            return 0
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        try:
            async with self.session.begin():
                sql = select(User).where(User.username == username)
                result = await self.session.execute(sql)
            return result.scalar_one_or_none()
        except Exception as e:
            return None

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        try:
            async with self.session.begin():
                sql = select(User).where(User.id == user_id)
                result = await self.session.execute(sql)
            return result.scalar_one_or_none()
        except Exception as e:
            return None
    
    async def delete_user(self, user_id: int) -> bool:
        try:
            async with self.session.begin():
                sql  = delete(User).where(User.id == user_id)
                await self.session.execute(sql)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

