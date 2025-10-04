from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from models import User
from .schemas import UserOutDB
from database import get_async_session
from fastapi import Depends

class UserRepository:
    def __init__(self, session: Session = Depends(get_async_session)):
        self.session : Session = session

    async def get_user_by_username(self, username: str) -> Optional[UserOutDB]:
        try:
            async with self.session.begin():
                sql = select(User).where(User.username == username)
                result = await self.session.execute(sql)
            return result.scalar_one_or_none()
        except Exception as e:
            return None