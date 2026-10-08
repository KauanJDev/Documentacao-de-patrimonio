import hashlib
import uuid
import csv
import json
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse

from core.logging_config import logger
from core.archive_config import settings
from models.Documento import Documento
from services.json_repository import (
    garantir_arquivo,
    ler_json,
    escrever_json,
    buscar_por_id,
    atualizar,
    deletar,
)

METADATA = Path(settings["storage"]["diretorio_metadados"])
DOCUMENTOS_FILE = Path(settings["storage"]["diretorio_metadados"]) / "documentos.json"
DOCUMENTOS_CSV = Path(settings["storage"]["diretorio_metadados"]) / "documentos.csv"


router = APIRouter(
    prefix="/exportar",
    tags=["exportar"],
)


@router.get("/csv", status_code=status.HTTP_200_OK)
def exportar_csv():
    documentos = ler_json(DOCUMENTOS_FILE)

    try:
        if not DOCUMENTOS_FILE.exists():
            logger.error(f"Arquivo JSON não encontrado")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo JSON não encontrado"
            )
        with open(DOCUMENTOS_CSV, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = []

            for key in documentos[0].keys():
                fieldnames.append(key)

            writer = csv.DictWriter(file, fieldnames)
            writer.writeheader()

            for doc in documentos:
                writer.writerow(doc)

        return FileResponse(
            path=DOCUMENTOS_CSV,
            media_type="text/csv",
            filename="documentos"
        )
    except Exception as e:
        logger.error(f"Erro ao baixar CSV: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao baixar arquivo CSV"
        )
