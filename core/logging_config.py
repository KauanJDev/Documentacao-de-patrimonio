import logging
import logging.config
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOGGING_CONFIG_FILE = BASE_DIR / "logging.yaml"
LOG_DIR = BASE_DIR / "storage" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

with open(LOGGING_CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)

    config["handlers"]["file"]["filename"] = str(LOG_DIR / "sistema.log")
    
    logging.config.dictConfig(config)

logger = logging.getLogger("documento_patrimonio")
logger.info("Sistema de logging configurado com sucesso na pasta storage/logs.")