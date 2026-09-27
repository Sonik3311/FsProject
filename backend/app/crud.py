"""Операции с данными и бизнес-логика (расчёт себестоимости, матрица аллергенов)."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


# ---------- Ингредиенты ----------

def get_ingredients(db: Session) -> list[models.Ingredient]:
    return list(db.scalars(select(models.Ingredient).order_by(models.Ingredient.name)))


def get_ingredient(db: Session, ingredient_id: int) -> models.Ingredient | None:
    return db.get(models.Ingredient, ingredient_id)


def create_ingredient(db: Session, data: schemas.IngredientCreate) -> models.Ingredient:
    ingredient = models.Ingredient(**data.model_dump())
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient


# ---------- Блюда ----------

def _ingredient_cost(ingredient: models.Ingredient, qty: float) -> float:
    return round(ingredient.price_per_unit * qty, 2)


def get_dishes(db: Session) -> list[models.Dish]:
    return list(db.scalars(select(models.Dish).order_by(models.Dish.name)))


def get_dish(db: Session, dish_id: int) -> models.Dish | None:
    return db.get(models.Dish, dish_id)


def compute_dish_cost(dish: models.Dish) -> float:
    return round(sum(_ingredient_cost(di.ingredient, di.qty) for di in dish.ingredients), 2)


def compute_dish_allergens(dish: models.Dish) -> list[str]:
    allergens: set[str] = set()
    for di in dish.ingredients:
        allergens.update(di.ingredient.allergens)
    return sorted(allergens)


def dish_to_schema(dish: models.Dish) -> schemas.DishOut:
    return schemas.DishOut(
        id=dish.id,
        name=dish.name,
        cost=compute_dish_cost(dish),
        allergens=compute_dish_allergens(dish),
        ingredients=[
            schemas.DishIngredientOut(
                ingredient_id=di.ingredient_id,
                name=di.ingredient.name,
                unit=di.ingredient.unit,
                qty=di.qty,
                cost=_ingredient_cost(di.ingredient, di.qty),
            )
            for di in dish.ingredients
        ],
    )


def create_dish(db: Session, data: schemas.DishCreate) -> models.Dish:
    dish = models.Dish(name=data.name)
    for item in data.ingredients:
        ingredient = db.get(models.Ingredient, item.ingredient_id)
        if ingredient is None:
            raise ValueError(f"Ингредиент {item.ingredient_id} не найден")
        dish.ingredients.append(
            models.DishIngredient(ingredient=ingredient, qty=item.qty)
        )
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish


# ---------- Матрица аллергенов ----------

def allergen_matrix(db: Session) -> list[dict]:
    dishes = get_dishes(db)
    return [
        {"dish_id": dish.id, "dish_name": dish.name, "allergens": compute_dish_allergens(dish)}
        for dish in dishes
    ]


# ---------- Списания ----------

def get_wastage(db: Session) -> list[models.WastageEntry]:
    return list(db.scalars(select(models.WastageEntry).order_by(models.WastageEntry.date.desc())))


def create_wastage_entry(db: Session, data: schemas.WastageCreate) -> models.WastageEntry:
    ingredient = db.get(models.Ingredient, data.ingredient_id)
    if ingredient is None:
        raise ValueError(f"Ингредиент {data.ingredient_id} не найден")
    entry = models.WastageEntry(
        ingredient=ingredient,
        qty=data.qty,
        unit=ingredient.unit,
        reason=data.reason,
        date=data.date or date.today(),
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry