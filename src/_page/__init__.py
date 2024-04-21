__all__ = ["WEBAPP"]

from flask import (
    Flask,
    Response,
    request,
    render_template,
    jsonify,
)
from typing import (
    Dict,
    Any,
    Tuple,
    Union,
    List,
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

with WEBAPP.app_context():
    NULL_VALUE: ResponseTuple = jsonify({"error": "NULL"}), 500
    NO_DATA_PROVIDED: ResponseTuple = jsonify({"error": "No data provided."}), 400
    NOT_FOUND: ResponseTuple = jsonify({"error": "Not found."}), 404
    MISSING_FIELDS: ResponseTuple = jsonify({"error": "Missing data fields."}), 400
    SUCCESS: ResponseTuple = jsonify({"message": "Updated successfully."}), 200
    __recipes: JSONType = {}
    __response: ResponseTuple = NULL_VALUE

logger_specials.values_returned(__recipes, __response, init=__name__)


@WEBAPP.route("/", methods=["GET", "POST"])
def main_page() -> ShowsRender:
    global __recipes, __response
    logger_specials.was_called(__name__, main_page.__name__)
    if request.method == "POST":
        return add()
    logger_specials.values_returned(__recipes, __response, init=main_page)
    return __render_page()


@WEBAPP.route("/add", methods=["POST"])
def add() -> ShowsRender:
    global __recipes
    logger_specials.was_called(__name__, add.__name__)
    data: Any = request.get_json()
    if not data:
        return __modify_response(NO_DATA_PROVIDED)
    name: str = data["name"]
    ingredients: str = data["ingredients"]
    steps: str = data["steps"]
    recipe_id: str = __generate_recipe_id(__recipes)
    __recipes[recipe_id] = {
        "name": name,
        "ingredients": ingredients,
        "steps": steps,
    }
    logger_specials.values_returned(
        name, ingredients, steps, recipe_id, __recipes, init=add
    )
    return __modify_response(jsonify({"recipe_id": recipe_id}), 200)


@WEBAPP.route("/update", methods=["GET", "POST", "PUT"])
def update() -> ShowsRender:
    global __recipes
    logger_specials.was_called(__name__, update.__name__)
    if request.method == "POST" or request.method == "PUT":
        data: Any = request.get_json()
        if not data:
            return __modify_response(NO_DATA_PROVIDED)
        recipe_id: str | None = data.get("recipe_id")
        if recipe_id not in __recipes:
            return __modify_response(NOT_FOUND)
        required_fields: JSONItems = ["name", "ingredients", "steps"]
        if any(field not in data for field in required_fields):
            return __modify_response(MISSING_FIELDS)
        __recipes[recipe_id].update(
            {
                "name": data["name"],
                "ingredients": data["ingredients"],
                "steps": data["steps"],
            }
        )
        logger_specials.values_returned(
            recipe_id, data, required_fields, __recipes, init=update
        )
        return __modify_response(SUCCESS)
    return __render_page()


@WEBAPP.route("/delete", methods=["GET", "POST", "DELETE"])
def delete() -> ShowsRender:
    global __recipes
    logger_specials.was_called(__name__, delete.__name__)
    if request.method == "POST" or request.method == "DELETE":
        recipe_id: str | None = request.args.get("recipe_id")
        if recipe_id not in __recipes:
            return __modify_response(NOT_FOUND)
        del __recipes[recipe_id]
        logger_specials.values_returned(recipe_id, __recipes, init=delete)
        return __modify_response(SUCCESS)
    return __render_page()


@WEBAPP.route("/view", methods=["GET", "POST"])
def view() -> ShowsRender:
    global __recipes
    logger_specials.was_called(__name__, view.__name__)
    logger_specials.values_returned(__recipes, init=view)
    return __modify_response(jsonify(__recipes), 200)


@WEBAPP.route("/results", methods=["GET"])
def results() -> ResponseTuple:
    global __response
    return __response


@WEBAPP.route("/search", methods=["GET"])
def search() -> ShowsRender:
    global __recipes
    logger_specials.was_called(__name__, search.__name__)
    recipe_id: str | None = request.args.get("recipe_id")
    if recipe_id not in __recipes:
        return __modify_response(NOT_FOUND)
    result: JSONType = {recipe_id: __recipes[recipe_id]}
    logger_specials.values_returned(recipe_id, __recipes[recipe_id], init=search)
    return __modify_response(jsonify(result), 200)


def __render_page() -> ShowsRender:
    return render_template("index.html")


def __generate_recipe_id(r: JSONType) -> str:
    return str(len(r) + random64())


def __modify_response(*val: Any) -> ShowsRender:
    global __response
    __response = val
    return __render_page()
