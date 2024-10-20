from fastapi import APIRouter
from fastapi import Depends, Security
from app.utils.common import get_current_user

router = APIRouter()


@router.get("")
def get_company(_=Depends(get_current_user)):
    return "company"


@router.post("")
def post_company():
    return "company"
