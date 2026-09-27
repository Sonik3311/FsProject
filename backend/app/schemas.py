import datetime

from pydantic import BaseModel, ConfigDict, Field


class IngredientBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    unit: str = Field(min_length=1, max_length=10)
    price_per_unit: float = Field(gt=0)
    allergens: list[str] = Field(default_factory=list)


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(BaseModel):
    """Все поля опциональны — обновляются только переданные."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    unit: str | None = Field(default=None, min_length=1, max_length=10)
    price_per_unit: float | None = Field(default=None, gt=0)
    allergens: list[str] | None = None


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


class DishUpdate(BaseModel):
    """Все поля опциональны. Если ingredients передан — состав заменяется целиком."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    ingredients: list[DishIngredientIn] | None = None


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


class WastageUpdate(BaseModel):
    """Все поля опциональны — обновляются только переданные. unit пересчитывается из ингредиента."""

    ingredient_id: int | None = None
    qty: float | None = Field(default=None, gt=0)
    reason: str | None = Field(default=None, min_length=1, max_length=200)
    date: datetime.date | None = None


class WastageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ingredient_id: int
    qty: float
    unit: str
    reason: str
    date: datetime.date