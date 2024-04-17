from .logger import *
from .functions import *
from .var import *
from .db_handler import *


def main() -> int:
    "Main function"
    logger.info("Main function started.")
    logger_specials.was_called(__name__, main.__name__)

    while True:
        prt(
            "Kitchen Recipes [Tests version]\n"
            "1) Add new recipe\n"
            "2) Update existing recipe\n"
            "3) Delete existing recipe\n"
            "4) View list of recipes\n"
            "5) Search for recipes by ingredient\n"
            "6) Quit\n"
        )

        option = inp("Select an option.").lower()

        if option == "1":
            name = inp("Enter recipe name.")
            ingredients = inp("Enter ingredients (comma separated).")
            steps = inp("Enter steps.")
            add_recipe(name, ingredients, steps)
            prt("Recipe added successfully!")
        elif option == "2":
            recipe_id = int(inp("Enter recipe ID to update."))
            name = inp("Enter updated recipe name.")
            ingredients = inp("Enter updated ingredients (comma separated).")
            steps = inp("Enter updated steps.")
            update_recipe(recipe_id, name, ingredients, steps)
            prt("Recipe updated successfully!")
        elif option == "3":
            recipe_id = int(inp("Enter recipe ID to delete."))
            delete_recipe(recipe_id)
            prt("Recipe deleted successfully!")
        elif option == "4":
            view_recipes()
        elif option == "5":
            ingredient = inp("Enter ingredient to search.")
            search_recipe_by_ingredient(ingredient)
        elif option == "6":
            prt("Exiting...")
            break
        else:
            prt("Invalid option. Please choose again.")

    return 0
