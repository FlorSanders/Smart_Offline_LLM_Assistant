import json
import logging
import sys

logger = None


def get_config(config_path):
    """
    Load configuration from file
    ---
    Args:
    - config_path: Configuration file path

    Returns:
    - config: Configuration dictionary
    """
    with open(config_path, "r") as f:
        config = json.load(f)
    return config


def get_logger(log_level="INFO"):
    """
    Get logger
    ---
    Args:
    - log_level (default = "INFO"): Logger level

    Returns
    - logger: Logger instance
    """

    global logger
    # Figure out where script was called from
    name = sys.argv[0].replace(".py", "")
    if logger is None:
        logger = logging.getLogger(name)
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(f"{name}.log"), logging.StreamHandler()],
        )
    return logger
