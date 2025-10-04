from sqlalchemy import Column, Integer, String, Boolean, ARRAY  
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    roles = Column(ARRAY(String), default=["uploader"])  # Roles can be: admin, uploader, approver

 