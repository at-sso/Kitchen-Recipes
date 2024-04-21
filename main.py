from icecream import install
from src import main
from src.logger import logger
from src.timer import *


if __name__ == "__main__":
    install()
    logger.debug(f"{ main } returned code: { timer(main) }")
