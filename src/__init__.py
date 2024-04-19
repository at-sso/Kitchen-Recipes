from .logger import *
from .functions import *
from .var import *
from .django import *
from .timer import *


def main() -> int:
    "Main function"
    logger.info("Main function started.")
    logger_specials.was_called(__name__, main.__name__)
    WEBAPP.run(debug=True)
    return 0
