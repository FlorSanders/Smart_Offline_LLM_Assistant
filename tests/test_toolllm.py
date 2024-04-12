import typer
import pyaudio
import os
import sys

# Add main dir to system path
main_dir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.append(main_dir)
from pipeline.utils import get_config, get_logger
from pipeline.toolllm import ToolLLM
from pipeline.llm import LLM


def main(
    config_path: str = os.path.join(main_dir, "config.json"),
    log_level: str = "DEBUG",
    test_algebra: bool = False,
    test_weather: bool = False,
    test_search: bool = False,
):
    """
    LLM Interaction test script
    """

    # Initialize program
    config = get_config(config_path)
    logger = get_logger(log_level=log_level)
    logger.info("Program Initialized")

    # Intialize llm
    llm = LLM(config)

    # Initialize tool llm
    toollm = ToolLLM(config, llm)

    # Test algebra
    if test_algebra:
        logger.info("Testing algebra")
        prompt = "What is three multiplied by four minus seven?"
        logger.info(f"Prompt: {prompt}")
        result = toollm(prompt)
        logger.info(f"Result: {result}")

    # Test weather
    if test_weather:
        logger.info("Testing weather")
        prompt = "What is the weather in Halle, Belgium?"
        logger.info(f"Prompt: {prompt}")
        result = toollm(prompt)
        logger.info(f"Result: {result}")

    # Test search
    if test_search:
        logger.info("Testing search")
        prompt = "What can you tell me about the Eiffel Tower?"
        logger.info(f"Prompt: {prompt}")
        result = toollm(prompt)
        logger.info(f"Result: {result}")


if __name__ == "__main__":
    typer.run(main)
