import hashlib
import os
import uuid
import datetime
from pathlib import Path
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from core.logging_config import logger
from models.Documento import Documento
from services.json_repository import (
    garantir_arquivo,
    ler_json,
    escrever_json,
    buscar_por_id,
    atualizar
)

BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTOS_FILE = BASE_DIR / "data" / "documentos.json"

router = APIRouter(
    prefix="/documentos",
    tags=["documentos"],
    responses={404: {"description": "não encontrado"}},
)

def calcular_sha256(conteudo: bytes) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(conteudo)
    return sha256_hash.hexdigest()

def salvar_arquivo(conteudo: bytes, nome_armazenado: str) -> None:
    caminho_arquivo = BASE_DIR / "uploads" / nome_armazenado
    caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho_arquivo, "wb") as f:
        f.write(conteudo)
    logger.info(f"Arquivo salvo em {caminho_arquivo}")

@router.post("/", response_model=Documento, status_code=status.HTTP_201_CREATED)
def criar_documento(
    arquivo: UploadFile = File(...),
    categoria: str = Form(...),
    descricao: str = Form(default=""),
    funcionario: str = Form(...),
    setor: str = Form(...),
    tipo_funcionario: str = Form(...),
    competencias: str = Form(...),
):
    garantir_arquivo(DOCUMENTOS_FILE)

    documento_id = str(uuid.uuid4())
    nome_original = arquivo.filename
    extensao = Path(nome_original).suffix.lower()
    tipo_mime = arquivo.content_type or "application/octet-stream"
    conteudo = arquivo.file.read()
    tamanho = len(conteudo)
    sha256 = calcular_sha256(conteudo)

    nome_armazenado = f"{documento_id}{extensao}"
    caminho_arquivo = os.path.join(BASE_DIR, "uploads", nome_armazenado)

    if os.path.exists(caminho_arquivo):
        logger.warning(f"Conflito de nome de armazenamento: {nome_armazenado}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um arquivo armazenado com esse identificador.",
        )

    try:
        salvar_arquivo(conteudo, nome_armazenado)
    except Exception as e:
        logger.error(f"Erro ao salvar o arquivo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao salvar o arquivo.",
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
        data_upload=datetime.datetime.now().isoformat(),
        sha256=sha256,
        funcionario=funcionario,
        setor=setor,
        tipo_funcionario=tipo_funcionario,
        competencias=competencias,
    )

    documentos = ler_json(DOCUMENTOS_FILE)
    documentos.append(documento.dict())
    escrever_json(DOCUMENTOS_FILE, documentos)

    logger.info(f"Documento com ID {documento.id} criado com sucesso.")
    return documento