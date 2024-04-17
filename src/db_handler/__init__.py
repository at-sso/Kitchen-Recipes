__all__ = [
    "add_recipe",
    "update_recipe",
    "delete_recipe",
    "view_recipes",
    "search_recipe_by_ingredient",
]

from typing import Any, List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.var import *
from src.functions import *
from src.const import DATABASE_FILE

# Create SQLAlchemy engine and session
engine = create_engine(f"sqlite:///{DATABASE_FILE}")
Session = sessionmaker(bind=engine)
session = Session()

Base: Any = declarative_base()


# Define the Recipe model
class Recipe(Base):
    __tablename__: str = "recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ingredients = Column(String, nullable=False)
    steps = Column(String, nullable=False)


# Create tables
Base.metadata.create_all(engine)


# Function to add a new recipe
def add_recipe(name: str, ingredients: str, steps: str) -> None:
    new_recipe = Recipe(name=name, ingredients=ingredients, steps=steps)
    session.add(new_recipe)
    session.commit()


# Function to update an existing recipe
def update_recipe(recipe_id: int, name: str, ingredients: str, steps: str) -> None:
    recipe: Any | None = session.query(Recipe).get(recipe_id)
    if recipe:
        recipe.name = name
        recipe.ingredients = ingredients
        recipe.steps = steps
        session.commit()


# Function to delete a recipe
def delete_recipe(recipe_id: int) -> None:
    recipe: Any | None = session.query(Recipe).get(recipe_id)
    if recipe:
        session.delete(recipe)
        session.commit()


# Function to view all recipes
def view_recipes() -> None:
    recipes: List[Recipe] = session.query(Recipe).all()
    var.reset_extra_message()
    for recipe in recipes:
        var.extra_message += accumulate(
            x="",
            y=f"ID: {recipe.id}, Name: {recipe.name}, "
            f"Ingredients: {recipe.ingredients}, Steps: {recipe.steps}",
            z="\n",
        )


# Function to search for recipes by ingredient
def search_recipe_by_ingredient(ingredient: str) -> None:
    recipes: List[Recipe] = (
        session.query(Recipe).filter(Recipe.ingredients.like(f"%{ingredient}%")).all()
    )
    var.reset_extra_message()
    for recipe in recipes:
        var.extra_message += accumulate(
            x="",
            y=f"ID: {recipe.id}, Name: {recipe.name}, "
            f"Ingredients: {recipe.ingredients}, Steps: {recipe.steps}",
            z="\n",
        )
