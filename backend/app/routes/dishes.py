from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/dishes", tags=["dishes"])


@router.get("", response_model=list[schemas.DishOut])
def list_dishes(db: Session = Depends(get_db)):
    return [crud.dish_to_schema(dish) for dish in crud.get_dishes(db)]


@router.get("/{dish_id}", response_model=schemas.DishOut)
def get_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = crud.get_dish(db, dish_id)
    if dish is None:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    return crud.dish_to_schema(dish)


@router.post("", response_model=schemas.DishOut, status_code=status.HTTP_201_CREATED)
def add_dish(data: schemas.DishCreate, db: Session = Depends(get_db)):
    try:
        dish = crud.create_dish(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return crud.dish_to_schema(dish)


@router.patch("/{dish_id}", response_model=schemas.DishOut)
def update_dish(dish_id: int, data: schemas.DishUpdate, db: Session = Depends(get_db)):
    dish = crud.get_dish(db, dish_id)
    if dish is None:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    try:
        dish = crud.update_dish(db, dish, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return crud.dish_to_schema(dish)


@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = crud.get_dish(db, dish_id)
    if dish is None:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    crud.delete_dish(db, dish)