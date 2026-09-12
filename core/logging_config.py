import logging
import logging.config
import importlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOGGING_CONFIG_FILE = BASE_DIR / "logging.yaml"

with open(LOGGING_CONFIG_FILE, "r") as file:
    yaml = importlib.import_module("yaml")
    config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

config["handlers"]["file"]["filename"] = str(BASE_DIR / "app.log")

logger = logging.getLogger(__name__)
logger.info("Sistema de logging configurado com sucesso.")