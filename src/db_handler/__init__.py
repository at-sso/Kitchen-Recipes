"""Note: Every function should have a logger that informs the developer when the function is called or a 
value is created. Database failures should not be caused by invalid values. The main function calls the timer
function to handle errors and log the execution time of each called function. The `logger_special` formatters
will come in hand while logging every value created (or returned) by anything."""

__all__ = ["WEBAPP"]

from flask import (
    Flask,
    Response,
    request,
    render_template,
    jsonify,
)
from typing import (
    Callable,
    Dict,
    Any,
    Tuple,
    Union,
    List,
    overload,
)

from src.var import *
from src.logger import *
from src.const import *

ShowsRender = str
ResponseTuple = Tuple[Response, int]
ShowsRenderOrResponse = Union[ShowsRender, ResponseTuple]

JSONType = Dict[Any, Any]
JSONItems = List[Any]

WEBAPP = Flask(__name__)


class RecipeApp:
    def __init__(self) -> None:
        self._recipes: JSONType = {}
        self._response: ResponseTuple
        self._render_page: Callable[[], ShowsRender] = lambda: render_template(
            "index.html"
        )

        logger_specials.values_returned(
            self._recipes, self.__generate_recipe_id, self._render_page, init=__name__
        )

    @WEBAPP.route("/", methods=["GET", "POST"])
    def main_page(self) -> ShowsRender:
        logger_specials.was_called(__name__, self.main_page.__name__)
        if request.method == "POST":
            return self.add()
        return self._render_page()

    @WEBAPP.route("/add", methods=["POST"])
    def add(self) -> ShowsRender:
        data: Any = request.get_json()
        if not data:
            return self.__modify_response(NO_DATA_PROVIDED)
        name: str = data["name"]
        ingredients: str = data["ingredients"]
        steps: str = data["steps"]
        recipe_id: str = self.__generate_recipe_id()
        self._recipes[recipe_id] = {
            "name": name,
            "ingredients": ingredients,
            "steps": steps,
        }
        logger_specials.values_returned(
            name, ingredients, steps, recipe_id, self._recipes, init=self.add
        )
        return self.__modify_response(jsonify({"recipe_id": recipe_id}), 200)

    @WEBAPP.route("/update", methods=["GET", "POST", "PUT"])
    def update(self) -> ShowsRender:
        if request.method == "POST" or request.method == "PUT":
            data: Any = request.get_json()
            if not data:
                return self.__modify_response(NO_DATA_PROVIDED)
            recipe_id: str | None = data.get("recipe_id")
            if recipe_id not in self._recipes:
                return self.__modify_response(NOT_FOUND)
            required_fields: JSONItems = ["name", "ingredients", "steps"]
            if any(field not in data for field in required_fields):
                return self.__modify_response(MISSING_FIELDS)
            self._recipes[recipe_id].update(
                {
                    "name": data["name"],
                    "ingredients": data["ingredients"],
                    "steps": data["steps"],
                }
            )
            logger_specials.values_returned(
                recipe_id, data, required_fields, self._recipes, init=self.update
            )
            return self.__modify_response(SUCCESS)
        return self._render_page()

    @WEBAPP.route("/delete", methods=["GET", "POST", "DELETE"])
    def delete(self) -> ShowsRender:
        if request.method == "POST" or request.method == "DELETE":
            recipe_id: str | None = request.args.get("recipe_id")
            if recipe_id not in self._recipes:
                return self.__modify_response(
                    jsonify({"error": "Recipe not found"}), 404
                )
            del self._recipes[recipe_id]
            logger_specials.values_returned(recipe_id, self._recipes, init=self.delete)
            return self.__modify_response(SUCCESS)
        return self._render_page()

    @WEBAPP.route("/view", methods=["GET", "POST"])
    def view(self) -> ShowsRender:
        logger_specials.was_called(__name__, self.view.__name__)
        logger_specials.values_returned(self._recipes, init=self.view)
        return self.__modify_response(jsonify(self._recipes), 200)

    @WEBAPP.route("/search", methods=["GET"])
    def search(self) -> ShowsRender:
        logger_specials.was_called(__name__, self.search.__name__)
        recipe_id: str | None = request.args.get("recipe_id")
        if recipe_id not in self._recipes:
            return self.__modify_response(jsonify({"error": "Recipe not found"}), 404)
        result: JSONType = {recipe_id: self._recipes[recipe_id]}
        logger_specials.values_returned(
            recipe_id, self._recipes[recipe_id], init=self.search
        )
        self.__modify_response(jsonify(result), 200)
        return self._render_page()

    @overload
    def __modify_response(self, args: Tuple[Response, int]) -> ShowsRender: ...

    @overload
    def __modify_response(self, response: Response, request: int) -> ShowsRender: ...

    def __modify_response(self, *args: Any) -> ShowsRender:  # type: ignore[misc]
        if len(args) == 1:
            # Case where a tuple is provided
            logger_specials.was_called(__name__, self.__modify_response.__name__)
            self._response = args[0]
            logger_specials.value_retured(
                "_response", self._response, self.__modify_response
            )
        elif len(args) == 2:
            # Case where specific values are provided
            logger_specials.was_called(__name__, self.__modify_response.__name__)
            self._response = args[0], args[1]
            logger_specials.value_retured(
                "_response", self._response, self.__modify_response
            )
        return self._render_page()

    def __generate_recipe_id(self) -> str:
        return str(len(self._recipes) + var.get_random64())


recipe_app = RecipeApp()
