import typer
from pipeline import run_pipeline


def main(config_path: str = "./config.json", log_level: str = "DEBUG"):
    """
    Local-First LLM Voice Assistant
    """

    # Run voice assistant pipeline
    run_pipeline(config_path, log_level)


if __name__ == "__main__":
    typer.run(main)
