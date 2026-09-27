from datetime import date

from sqlalchemy import Date, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"
    __table_args__ = (UniqueConstraint("name", name="uq_ingredient_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    unit: Mapped[str] = mapped_column(String(10))
    price_per_unit: Mapped[float] = mapped_column(Float)
    allergens: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)

    dishes: Mapped[list["DishIngredient"]] = relationship(back_populates="ingredient")


class Dish(Base):
    __tablename__ = "dishes"
    __table_args__ = (UniqueConstraint("name", name="uq_dish_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    ingredients: Mapped[list["DishIngredient"]] = relationship(
        back_populates="dish",
        cascade="all, delete-orphan",
    )


class DishIngredient(Base):
    __tablename__ = "dish_ingredients"
    __table_args__ = (UniqueConstraint("dish_id", "ingredient_id", name="uq_dish_ingredient"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    dish_id: Mapped[int] = mapped_column(ForeignKey("dishes.id", ondelete="CASCADE"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    qty: Mapped[float] = mapped_column(Float)

    dish: Mapped[Dish] = relationship(back_populates="ingredients")
    ingredient: Mapped[Ingredient] = relationship(back_populates="dishes")


class WastageEntry(Base):
    __tablename__ = "wastage"

    id: Mapped[int] = mapped_column(primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    qty: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(10))
    reason: Mapped[str] = mapped_column(String(200))
    date: Mapped[date] = mapped_column(Date)

    ingredient: Mapped[Ingredient] = relationship()