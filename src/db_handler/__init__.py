__all__ = [
    "conn",
    "add_recipe",
    "update_recipe",
    "delete_recipe",
    "view_recipes",
    "search_recipe_by_ingredient",
]

import sqlite3

from src.const import *

# Connect to the database.
conn: sqlite3.Connection = sqlite3.connect(DATABASE_FILE)


# Function to create the recipe table if it doesn't exist
def __create_table() -> None:
    conn.execute(
        """CREATE TABLE IF NOT EXISTS recipes
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             ingredients TEXT NOT NULL,
             steps TEXT NOT NULL);"""
    )
    conn.commit()


# Function to add a new recipe
def add_recipe(name: str, ingredients: str, steps: str) -> None:
    conn.execute(
        "INSERT INTO recipes (name, ingredients, steps) VALUES (?, ?, ?);",
        (name, ingredients, steps),
    )
    conn.commit()


# Function to update an existing recipe
def update_recipe(recipe_id: int, name: str, ingredients: str, steps: str) -> None:
    conn.execute(
        "UPDATE recipes SET name=?, ingredients=?, steps=? WHERE id=?;",
        (name, ingredients, steps, recipe_id),
    )
    conn.commit()


# Function to delete a recipe
def delete_recipe(recipe_id: int) -> None:
    conn.execute("DELETE FROM recipes WHERE id=?;", (recipe_id,))
    conn.commit()


# Function to view all recipes
def view_recipes() -> None:
    cursor: sqlite3.Cursor = conn.execute("SELECT * FROM recipes;")
    for row in cursor:
        print(f"ID: {row[0]}, Name: {row[1]}, Ingredients: {row[2]}, Steps: {row[3]}")


# Function to search for recipes by ingredient
def search_recipe_by_ingredient(ingredient: str) -> None:
    cursor: sqlite3.Cursor = conn.execute(
        "SELECT * FROM recipes WHERE ingredients LIKE ?;", ("%" + ingredient + "%",)
    )
    for row in cursor:
        print(f"ID: {row[0]}, Name: {row[1]}, Ingredients: {row[2]}, Steps: {row[3]}")


__create_table()
