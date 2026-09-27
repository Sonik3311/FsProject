"""Операции с данными и бизнес-логика (расчёт себестоимости, матрица аллергенов)."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


class ConflictError(Exception):
    """Запись не может быть изменена/удалена из-за конфликта связей."""


def _apply_updates(obj, data) -> None:
    """Переносит на объект только те поля схемы, которые переданы (не None)."""
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)


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


def update_ingredient(
    db: Session,
    ingredient: models.Ingredient,
    data: schemas.IngredientUpdate,
) -> models.Ingredient:
    _apply_updates(ingredient, data)
    db.commit()
    db.refresh(ingredient)
    return ingredient


def delete_ingredient(db: Session, ingredient: models.Ingredient) -> None:
    in_dishes = db.scalar(
        select(models.DishIngredient).where(models.DishIngredient.ingredient_id == ingredient.id)
    )
    in_wastage = db.scalar(
        select(models.WastageEntry).where(models.WastageEntry.ingredient_id == ingredient.id)
    )
    if in_dishes or in_wastage:
        raise ConflictError(
            f"Ингредиент «{ingredient.name}» используется в блюдах или списаниях и не может быть удалён"
        )
    db.delete(ingredient)
    db.commit()


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


def _set_dish_ingredients(
    db: Session,
    dish: models.Dish,
    items: list[schemas.DishIngredientIn],
) -> None:
    """Заменяет состав блюда целиком (старые позиции удаляются).

    Сначала удаляются старые строки (flush), и только потом вставляются новые —
    иначе новые строки конфликтуют с уникальным ограничением (dish_id, ingredient_id).
    """
    dish.ingredients = []
    db.flush()
    for item in items:
        ingredient = db.get(models.Ingredient, item.ingredient_id)
        if ingredient is None:
            raise ValueError(f"Ингредиент {item.ingredient_id} не найден")
        dish.ingredients.append(
            models.DishIngredient(ingredient=ingredient, qty=item.qty)
        )


def create_dish(db: Session, data: schemas.DishCreate) -> models.Dish:
    dish = models.Dish(name=data.name)
    _set_dish_ingredients(db, dish, data.ingredients)
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish


def update_dish(db: Session, dish: models.Dish, data: schemas.DishUpdate) -> models.Dish:
    if data.name is not None:
        dish.name = data.name
    if data.ingredients is not None:
        _set_dish_ingredients(db, dish, data.ingredients)
    db.commit()
    db.refresh(dish)
    return dish


def delete_dish(db: Session, dish: models.Dish) -> None:
    db.delete(dish)
    db.commit()


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


def get_wastage_entry(db: Session, entry_id: int) -> models.WastageEntry | None:
    return db.get(models.WastageEntry, entry_id)


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


def update_wastage_entry(
    db: Session,
    entry: models.WastageEntry,
    data: schemas.WastageUpdate,
) -> models.WastageEntry:
    if data.ingredient_id is not None:
        ingredient = db.get(models.Ingredient, data.ingredient_id)
        if ingredient is None:
            raise ValueError(f"Ингредиент {data.ingredient_id} не найден")
        entry.ingredient = ingredient
        entry.unit = ingredient.unit
    for field in ("qty", "reason", "date"):
        value = getattr(data, field)
        if value is not None:
            setattr(entry, field, value)
    db.commit()
    db.refresh(entry)
    return entry


def delete_wastage_entry(db: Session, entry: models.WastageEntry) -> None:
    db.delete(entry)
    db.commit()