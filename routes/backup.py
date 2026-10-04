from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, HTTPException, status
from zipfile import ZipFile
import os

from core.logging_config import BASE_DIR, logger
from core.archive_config import settings

STORAGE_DIR = Path(settings["storage"].get("diretorio_storage", BASE_DIR / "storage"))
BACKUPS_DIR = Path(settings["storage"]["diretorio_backups"])

router = APIRouter(prefix="/backup", tags=["backup"])

def nome_backup():
    data_formatada = datetime.now().strftime("%Y-%m-%d_%H%M")
    return f"backup_{data_formatada}.zip"

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_backup():
    backup = nome_backup()
    
    if not BACKUPS_DIR.exists():
        BACKUPS_DIR.mkdir(parents=True)
        logger.info(f"Pasta de backups criada em: {BACKUPS_DIR}")

    backup_path = BACKUPS_DIR / backup
    
    try:
        with ZipFile(backup_path, "w") as z:
            for root, dirs, files in os.walk(STORAGE_DIR):
                caminho_atual = Path(root).resolve()
                
                if BACKUPS_DIR in caminho_atual.parents or caminho_atual == BACKUPS_DIR:
                    continue
                    
                for f in files:
                    caminho_completo = caminho_atual / f
                    if caminho_completo == backup_path.resolve():
                        continue

                    nome_no_zip = caminho_completo.relative_to(STORAGE_DIR)
                    z.write(caminho_completo, arcname=nome_no_zip)
                    
        mensagem = f"Backup {backup} criado com sucesso"
        logger.info(mensagem)
        
    except Exception as e:
        mensagem = f"Nao foi possivel criar backup {backup} : {e}"
        logger.error(mensagem)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=mensagem
        )

    return {"mensagem": mensagem, "caminho": backup_path}
