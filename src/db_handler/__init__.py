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

import redis
from typing import Dict, Any

from src.var import *
from src.functions import *
from src.logger import *

RedisType = redis.Redis

# Connect to Redis
redis_client: RedisType = redis.Redis(host="localhost", port=6379, db=0)

# Log values returned by any database.
logger_specials.values_returned(redis_client, init=__name__)


def __generate_recipe_id() -> str:
    return str(var.get_random64())


# Function to add a new recipe
def add_recipe(name: str, ingredients: str, steps: str) -> None:
    new_recipe: Dict[str, str] = {
        "name": name,
        "ingredients": ingredients,
        "steps": steps,
    }

    logger_specials.value_retured("new_recipe", new_recipe, add_recipe)
    recipe_id: str = __generate_recipe_id()
    redis_client.hmset(recipe_id, new_recipe)


# Function to update an existing recipe
def update_recipe(recipe_id: str, name: str, ingredients: str, steps: str) -> None:
    query: Dict[str, str] = {"_id": recipe_id}
    new_values: Dict[str, Dict[str, str]] = {
        "$set": {"name": name, "ingredients": ingredients, "steps": steps}
    }

    logger_specials.values_returned(query, new_values, init=update_recipe)
    redis_client.hmset(recipe_id, new_values)


# Function to delete a recipe
def delete_recipe(recipe_id: str) -> None:
    logger_specials.value_retured("recipe_id", recipe_id, delete_recipe)
    redis_client.delete(recipe_id)


# Function to view all recipes
def view_recipes() -> None:
    recipe_ids: Any = redis_client.keys("*")
    var.reset_extra_message()
    for recipe_id in recipe_ids:
        recipe_details: Any = redis_client.hgetall(recipe_id)
        var.extra_message += accumulate(
            x="",
            y=f"ID: {recipe_id.decode()}, Name: {recipe_details[b'name'].decode()}, "
            f"Ingredients: {recipe_details[b'ingredients'].decode()}, Steps: {recipe_details[b'steps'].decode()}",
            z="\n",
        )


# Function to search for recipes by ingredient
def search_recipe_by_ingredient(ingredient: str) -> None:
    var.reset_extra_message()
    recipe_ids: Any = redis_client.keys("*")
    for recipe_id in recipe_ids:
        recipe_details: Any = redis_client.hgetall(recipe_id)
        if ingredient in recipe_details[b"ingredients"].decode():
            var.extra_message += accumulate(
                x="",
                y=f"ID: {recipe_id.decode()}, Name: {recipe_details[b'name'].decode()}, "
                f"Ingredients: {recipe_details[b'ingredients'].decode()}, Steps: {recipe_details[b'steps'].decode()}",
                z="\n",
            )
