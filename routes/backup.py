from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, HTTPException, status
from zipfile import ZipFile
import os

from core.logging_config import logger


BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
BACKUPS_DIR = STORAGE_DIR / "backups"

router = APIRouter(prefix="/backup", tags=["backup"])


def nome_backup():
    return 'backup_' + str(datetime.now()).replace(" ", "_") + ".zip"


@router.get("", status_code=status.HTTP_200_OK)
def criar_backup():
    backup = nome_backup()
    backup_path = BACKUPS_DIR / backup
    mensagem = ""
    
    try:
        with ZipFile(backup_path, "w") as z:
            for root, dirs, files in os.walk("./storage/"):
                if root == "./storage" or root == "./storage/backups":
                    continue
                for f in files:
                    z.write(root + "/" + f)
                mensagem = f"Backup {backup}, criado com sucesso"
                logger.info(mensagem)
    except Exception as e:
        mensagem = f"Não foi possível criar backup {backup} : {e}"
        logger.error(mensagem)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Não foi possível criar backup {backup} : {e}")

    return {"mensagem": mensagem, "caminho": backup_path}
