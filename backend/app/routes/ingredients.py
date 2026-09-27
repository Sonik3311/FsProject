from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("", response_model=list[schemas.IngredientOut])
def list_ingredients(db: Session = Depends(get_db)):
    return crud.get_ingredients(db)


@router.post("", response_model=schemas.IngredientOut, status_code=status.HTTP_201_CREATED)
def add_ingredient(data: schemas.IngredientCreate, db: Session = Depends(get_db)):
    return crud.create_ingredient(db, data)