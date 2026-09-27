import datetime

from pydantic import BaseModel, ConfigDict, Field


class IngredientBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    unit: str = Field(min_length=1, max_length=10)
    price_per_unit: float = Field(gt=0)
    allergens: list[str] = Field(default_factory=list)


class IngredientCreate(IngredientBase):
    pass


class IngredientOut(IngredientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class DishIngredientIn(BaseModel):
    ingredient_id: int
    qty: float = Field(gt=0)


class DishIngredientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ingredient_id: int
    name: str
    unit: str
    qty: float
    cost: float


class DishCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    ingredients: list[DishIngredientIn] = Field(default_factory=list)


class DishOut(BaseModel):
    id: int
    name: str
    cost: float
    allergens: list[str]
    ingredients: list[DishIngredientOut]


class WastageCreate(BaseModel):
    ingredient_id: int
    qty: float = Field(gt=0)
    reason: str = Field(min_length=1, max_length=200)
    date: datetime.date | None = None


class WastageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ingredient_id: int
    qty: float
    unit: str
    reason: str
    date: datetime.date