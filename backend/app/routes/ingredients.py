from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("", response_model=list[schemas.IngredientOut])
def list_ingredients(db: Session = Depends(get_db)):
    return crud.get_ingredients(db)


@router.get("/{ingredient_id}", response_model=schemas.IngredientOut)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = crud.get_ingredient(db, ingredient_id)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ингредиент не найден")
    return ingredient


@router.post("", response_model=schemas.IngredientOut, status_code=status.HTTP_201_CREATED)
def add_ingredient(data: schemas.IngredientCreate, db: Session = Depends(get_db)):
    return crud.create_ingredient(db, data)


@router.patch("/{ingredient_id}", response_model=schemas.IngredientOut)
def update_ingredient(ingredient_id: int, data: schemas.IngredientUpdate, db: Session = Depends(get_db)):
    ingredient = crud.get_ingredient(db, ingredient_id)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ингредиент не найден")
    return crud.update_ingredient(db, ingredient, data)


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = crud.get_ingredient(db, ingredient_id)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ингредиент не найден")
    crud.delete_ingredient(db, ingredient)