from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/wastage", tags=["wastage"])


@router.get("", response_model=list[schemas.WastageOut])
def list_wastage(db: Session = Depends(get_db)):
    return crud.get_wastage(db)


@router.post("", response_model=schemas.WastageOut, status_code=status.HTTP_201_CREATED)
def add_wastage_entry(data: schemas.WastageCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_wastage_entry(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))