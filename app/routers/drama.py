from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from typing import List, Optional

from app import schemas

router = APIRouter(prefix='/dramas', tags=['Dramas'])

@router.get('/', response_model=List[schemas.Drama])
