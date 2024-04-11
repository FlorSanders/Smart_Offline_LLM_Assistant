import typer
import pyaudio
import os
import sys

# Add main dir to system path
main_dir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.append(main_dir)
from pipeline.utils import get_config, get_logger
from pipeline.tools import Weather, Search, Algebra, ToolError


def main(
    log_level: str = "DEBUG",
    test_algebra: bool = False,
    test_weather: bool = False,
    test_search: bool = False,
):
    logger = get_logger(log_level="DEBUG")
    logger.info("Program Initialized")

    # Test algebra
    if test_algebra:
        logger.info("Testing algebra")
        algebra_tool = Algebra()
        equation = "3 * 4 + 2 * 6"
        try:
            algebra_tool(equation)
        except ToolError as e:
            logger.error(e)

    # Test weather
    if test_weather:
        logger.info("Getting weather for NY")
        weather_tool = Weather()
        result = weather_tool("Columbia University in New York")
        logger.info("Weather for NY retrieved")
        logger.debug(result)

    # Test search
    if test_search:
        logger.info("Searching for Columbia University")
        search_tool = Search()
        result = search_tool("Eiffel Tower")
        logger.info("Search for Columbia University retrieved")
        logger.debug(result)


if __name__ == "__main__":
    typer.run(main)
