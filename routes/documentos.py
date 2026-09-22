import hashlib
import uuid
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder

from core.logging_config import logger
from models.Documento import Documento
from services.json_repository import (
    garantir_arquivo,
    ler_json,
    escrever_json
)

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
DOCUMENTOS_FILE = STORAGE_DIR / "metadata" / "documentos.json"
ARQUIVOS_DIR = STORAGE_DIR / "arquivos"

router = APIRouter(
    prefix="/documentos",
    tags=["documentos"],
)

def calcular_sha256(conteudo: bytes) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(conteudo)
    return sha256_hash.hexdigest()

def salvar_arquivo(conteudo: bytes, nome_armazenado: str) -> None:
    caminho_arquivo = ARQUIVOS_DIR / nome_armazenado
    caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho_arquivo, "wb") as f:
        f.write(conteudo)
    logger.info(f"Arquivo fisico salvo em {caminho_arquivo}")

@router.post("/", response_model=Documento, status_code=status.HTTP_201_CREATED)
def criar_documento(
    arquivo: UploadFile = File(...),
    categoria: str = Form(...),
    descricao: str = Form(default=""),
    numero_patrimonial: str = Form(...),
    setor: str = Form(...),
    situacao: str = Form(...),
):
    garantir_arquivo(DOCUMENTOS_FILE)

    documento_id = str(uuid.uuid4())
    nome_original = arquivo.filename
    extensao = Path(nome_original).suffix.lower() if nome_original else ""
    tipo_mime = arquivo.content_type or "application/octet-stream"
    conteudo = arquivo.file.read()
    tamanho = len(conteudo)
    sha256 = calcular_sha256(conteudo)

    nome_armazenado = f"{documento_id}{extensao}"
    caminho_arquivo = ARQUIVOS_DIR / nome_armazenado

    if caminho_arquivo.exists():
        logger.warning(f"Conflito de nome de armazenamento: {nome_armazenado}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ja existe um arquivo armazenado com esse identificador.",
        )

    try:
        salvar_arquivo(conteudo, nome_armazenado)
    except Exception as e:
        logger.error(f"Erro ao salvar o arquivo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao salvar o arquivo fisicamente.",
        )

    documento = Documento(
        id=documento_id,
        nome_original=nome_original,
        nome_armazenado=nome_armazenado,
        extensao=extensao,
        tipo_mime=tipo_mime,
        tamanho=tamanho,
        categoria=categoria,
        descricao=descricao,
        data_upload=datetime.now().isoformat(),
        sha256=sha256,
        numero_patrimonial=numero_patrimonial,
        setor=setor,
        situacao=situacao,
    )

    documentos = ler_json(DOCUMENTOS_FILE)
    
    documento_seguro_para_json = jsonable_encoder(documento)
    
    documentos.append(documento_seguro_para_json)
    escrever_json(DOCUMENTOS_FILE, documentos)

    logger.info(f"Documento com ID {documento.id} criado com sucesso.")
    return documento