from fastapi import APIRouter, Depends, HTTPException, Body, Security, Query
from auth.schemas import UserInDB
from .service import AdminService
from auth.utils import get_current_user
from auth.schemas import TokenData

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/user")
async def create_user(user: UserInDB = Body(...), admin_service = Depends(AdminService), current_user: TokenData = Security(get_current_user, scopes=["admin"])):
    try:    
        response = await admin_service.create_user(user)
        if response:
            return response
        else:
            raise HTTPException(status_code=400, detail="User already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/one")
async def get_one_user(offset: int = Query(0, ge=0), admin_service = Depends(AdminService), current_user: TokenData = Security(get_current_user, scopes=["admin"])):
    response = await admin_service.get_one_user(offset)
    return response

@router.get("/users")
async def list_users(page: int = Query(1, ge=1), limit: int = Query(10, ge=1), admin_service = Depends(AdminService), current_user: TokenData = Security(get_current_user, scopes=["admin"])):
    response = await admin_service.list_users(page, limit)
    return response

@router.get("/users/{id}")
async def get_user_by_id(id: int, admin_service = Depends(AdminService), current_user: TokenData = Security(get_current_user, scopes=["admin"])):
    response = await admin_service.get_user_by_id(id)
    return response

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, admin_service = Depends(AdminService), current_user: TokenData = Security(get_current_user, scopes=["admin"])):
    try:
        response = await admin_service.delete_user(user_id)
        if response:
            return response
        else:
            raise HTTPException(status_code=400, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@router.put("/update-user")
async def update_user(user_id: int = Body(...), user: UserInDB = Body(...), admin_service = Depends(AdminService), current_user: TokenData = Security(get_current_user, scopes=["admin"])):
    try:
        response = await admin_service.update_user(user_id, user)
        if response:
            return response
        else:
            raise HTTPException(status_code=400, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user")
async def get_user(user_id: int = Body(...), admin_service = Depends(AdminService), current_user: TokenData = Security(get_current_user, scopes=["admin"])):
    try:
        response = await admin_service.get_user_by_id(user_id)
        if response:
            return response
        else:
            raise HTTPException(status_code=400, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

