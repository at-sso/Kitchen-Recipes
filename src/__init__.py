from .logger import *
from ._page import *


def main() -> int:
    "Main function"
    logger.info("Main function started.")
    logger_specials.was_called(__name__, main.__name__)
    WEBAPP.run(debug=True, host="0.0.0.0")
    return 0
