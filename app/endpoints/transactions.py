from fastapi import APIRouter, Depends
from ..users import fastapi_users

from ..storage.schemas import UserDB

router = APIRouter()

@router.get('/transactions')
def transactions(user: UserDB = Depends(fastapi_users.get_current_active_user)):
    return f"Hello, {user.email}"