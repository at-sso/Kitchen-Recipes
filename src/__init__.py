from .logger import *
from .functions import *
from .var import *
from .db_handler import *
from .timer import *


def main() -> int:
    "Main function"
    logger.info("Main function started.")
    logger_specials.was_called(__name__, main.__name__)

    while True:
        clear_terminal()
        prt(
            "Kitchen Recipes [Tests version]\n"
            "1) Add new recipe.\n"
            "2) Update existing recipe.\n"
            "3) Delete existing recipe.\n"
            "4) View list of recipes.\n"
            "5) Search for recipes by ingredient.\n"
            "6) Quit.\n",
            i=f"{var.extra_message}\n",
        )

        option: str = inp("Select an option.").lower()

        try:
            match option:
                case "1":
                    name = inp("Enter recipe name.")
                    ingredients = inp("Enter ingredients (comma separated).")
                    steps = inp("Enter steps.")
                    timer(add_recipe, name, ingredients, steps)
                    var.extra_message = "Recipe added successfully!"

                case "2":
                    recipe_id = inp("Enter recipe ID to update.")
                    name = inp("Enter updated recipe name.")
                    ingredients = inp("Enter updated ingredients (comma separated).")
                    steps = inp("Enter updated steps.")
                    timer(update_recipe, recipe_id, name, ingredients, steps)
                    var.extra_message = "Recipe updated successfully!"

                case "3":
                    recipe_id = inp("Enter recipe ID to delete.")
                    timer(delete_recipe, recipe_id)
                    var.extra_message = "Recipe deleted successfully!"

                case "4":
                    timer(view_recipes)

                case "5":
                    ingredient = inp("Enter ingredient to search.")
                    timer(search_recipe_by_ingredient, ingredient)

                case "6":
                    prt("Exiting...")
                    break

                case _:
                    var.extra_message = "Invalid option. Please choose again."
        except Exception:
            return 1

    return 0
