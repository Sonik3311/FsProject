from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/wastage", tags=["wastage"])


@router.get("", response_model=list[schemas.WastageOut])
def list_wastage(db: Session = Depends(get_db)):
    return crud.get_wastage(db)


@router.get("/{entry_id}", response_model=schemas.WastageOut)
def get_wastage_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = crud.get_wastage_entry(db, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Запись списания не найдена")
    return entry


@router.post("", response_model=schemas.WastageOut, status_code=status.HTTP_201_CREATED)
def add_wastage_entry(data: schemas.WastageCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_wastage_entry(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.patch("/{entry_id}", response_model=schemas.WastageOut)
def update_wastage_entry(entry_id: int, data: schemas.WastageUpdate, db: Session = Depends(get_db)):
    entry = crud.get_wastage_entry(db, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Запись списания не найдена")
    try:
        return crud.update_wastage_entry(db, entry, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wastage_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = crud.get_wastage_entry(db, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Запись списания не найдена")
    crud.delete_wastage_entry(db, entry)