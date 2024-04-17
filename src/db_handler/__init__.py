"""Note: Every function should have a logger that informs the developer (not "debugged") 
when the function is called or a value is created. Database failures should not be caused by invalid values.
The main function calls the timer function to handle errors and log the execution time of each called function.
The `logger_special` formatters will come in hand while logging every value created (or returned) by anything."""

__all__ = [
    "add_recipe",
    "update_recipe",
    "delete_recipe",
    "view_recipes",
    "search_recipe_by_ingredient",
]

from pymongo import database, collection, cursor
from pymongo import MongoClient
from typing import Any, Dict

from src.var import *
from src.functions import *
from src.logger import *

MongoDBType = MongoClient[Any]
DatabaseType = database.Database[Any]  # type: ignore[misc]
CollectionType = collection.Collection[Any]  # type: ignore[misc]
CursorType = cursor.Cursor[Any]

# Connect to MongoDB
client: MongoDBType = MongoClient("mongodb://localhost:27017/")
db: DatabaseType = client["recipes_db"]
collections: CollectionType = db["recipes"]

# Schema isn't necessary in MongoDB but can be helpful for consistency.
# In this case, it's just for illustrative purposes.
recipe_schema: Dict[str, str] = {"name": "", "ingredients": "", "steps": ""}

# Log values returned by any database.
logger_specials.values_returned(client, db, collections, recipe_schema, init=__name__)


# Function to add a new recipe
def add_recipe(name: str, ingredients: str, steps: str) -> None:
    new_recipe: Dict[str, str] = {
        "name": name,
        "ingredients": ingredients,
        "steps": steps,
    }

    logger_specials.value_retured("new_recipe", new_recipe, add_recipe)
    collections.insert_one(new_recipe)


# Function to update an existing recipe
def update_recipe(recipe_id: str, name: str, ingredients: str, steps: str) -> None:
    query: Dict[str, str] = {"_id": recipe_id}
    new_values: Dict[str, Dict[str, str]] = {
        "$set": {"name": name, "ingredients": ingredients, "steps": steps}
    }

    logger_specials.values_returned(query, new_values, init=update_recipe)
    collections.update_one(query, new_values)


# Function to delete a recipe
def delete_recipe(recipe_id: str) -> None:
    query: Dict[str, str] = {"_id": recipe_id}

    logger_specials.value_retured("query", query, delete_recipe)
    collections.delete_one(query)


# Function to view all recipes
def view_recipes() -> None:
    recipes: CursorType = collections.find()
    logger_specials.value_retured("recipes", recipes, view_recipes)

    var.reset_extra_message()
    for recipe in recipes:
        var.extra_message += accumulate(
            x="",
            y=f"ID: {recipe['_id']}, Name: {recipe['name']}, "
            f"Ingredients: {recipe['ingredients']}, Steps: {recipe['steps']}",
            z="\n",
        )


# Function to search for recipes by ingredient
def search_recipe_by_ingredient(ingredient: str) -> None:
    recipes: CursorType = collections.find({"ingredients": {"$regex": ingredient}})
    logger_specials.value_retured("recipes", recipes, search_recipe_by_ingredient)

    var.reset_extra_message()
    for recipe in recipes:
        var.extra_message += accumulate(
            x="",
            y=f"ID: {recipe['_id']}, Name: {recipe['name']}, "
            f"Ingredients: {recipe['ingredients']}, Steps: {recipe['steps']}",
            z="\n",
        )
