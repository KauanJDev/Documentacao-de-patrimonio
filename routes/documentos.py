import hashlib
import uuid
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

DOCUMENTOS_FILE = Path(settings["storage"]["diretorio_metadados"]) / "documentos.json"
ARQUIVOS_DIR = Path(settings["storage"]["diretorio_arquivos"])

router = APIRouter(
    prefix="/documentos",
    tags=["documentos"],
)

""" F02 e F07 - Listar e Filtrar documentos- liz """
@router.get("", response_model=list[Documento])
def listar_documentos(
    extensao: str | None = None,
    numero_patrimonial: str |None = None,
    setor: str | None = None,
    categoria: str | None = None,
    situacao: str | None = None
):
    documentos = ler_json(DOCUMENTOS_FILE)

    if extensao:
        documentos = [
            doc for doc in documentos if (
                doc["extensao"].lower() == extensao.lower()
            )
        ]

    if numero_patrimonial:
        documentos = [
            doc for doc in documentos if (
                doc["numero_patrimonial"].lower() == numero_patrimonial.lower()
            )
        ]

    if setor:
        documentos = [
            doc for doc in documentos if (
                doc["setor"].lower() == setor.lower()
            )
        ]

    if categoria:
        documentos = [
            doc for doc in documentos if (
                doc["categoria"].lower() == categoria.lower()
            )
        ]

    if situacao:
        documentos = [
            doc for doc in documentos if (
                doc["situacao"].lower() == situacao.lower()
            )
        ]

    logger.info(
        "Listagem de documentos: %d registros"
        "Filtros: extensao=%s, n.patrimonial=%s, setor=%s, categoria=%s, situacao=%s", 
        len(documentos), extensao, numero_patrimonial, setor, categoria, situacao
    )

    return documentos

@router.get("/estatisticas", status_code=status.HTTP_200_OK)
def obter_estatisticas():
    documentos = ler_json(DOCUMENTOS_FILE)

    estatisticas = {
        "total_documentos": len(documentos),
        "tamanho_bytes": 0,
        "por_extensao": {},
        "por_categoria": {},
        "por_setor": {},
        "por_situacao": {},
    }

    for doc in documentos:

        if "tamanho" in doc:
            estatisticas["tamanho_bytes"] += doc["tamanho"]

        if "categoria" in doc:
            categoria = doc["categoria"]
        else:
            categoria = "nao informado"

        if categoria in estatisticas["por_categoria"]:
            estatisticas["por_categoria"][categoria] += 1
        else:
            estatisticas["por_categoria"][categoria] = 1

        if "setor" in doc:
            setor = doc["setor"]
        else:
            setor = "nao informado"

        if setor in estatisticas["por_setor"]:
            estatisticas["por_setor"][setor] += 1
        else:
            estatisticas["por_setor"][setor] = 1

        if "situacao" in doc:
            situacao = doc["situacao"]
        else:
            situacao = "nao informado"

        if situacao in estatisticas["por_situacao"]:
            estatisticas["por_situacao"][situacao] += 1
        else:
            estatisticas["por_situacao"][situacao] = 1

        if "extensao" in doc:
            extensao = doc["extensao"]
        else:
            extensao = "nao informado"

        if extensao in estatisticas["por_extensao"]:
            estatisticas["por_extensao"][extensao] += 1
        else:
            estatisticas["por_extensao"][extensao] = 1

    logger.info("Consulta realizada para obter estatisticas dos documentos.")
    return estatisticas


""" F03 - Procurar por id - liz """
@router.get("/{documento_id}", response_model=Documento)
def obter_documento(documento_id: str):
    documento = buscar_por_id(DOCUMENTOS_FILE, documento_id)

    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento nao encontrado"
        )

    logger.info(
        "Consulta de documento: id = %s", 
        documento_id
    )

    return documento

""" F06 - Exclusao de documento - liz """
@router.delete("/{documento_id}")
def excluir_documento(documento_id = str):
    if not deletar(DOCUMENTOS_FILE, documento_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento nao encontrado"
        )

    logger.info(
        "Documento removido: %s",
        documento_id
    )

    return{
        "mensgem": "Documento removido com sucesso :)"
    }

def calcular_sha256(conteudo: bytes) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(conteudo)
    return sha256_hash.hexdigest()

def salvar_arquivo(conteudo: bytes, nome_armazenado: str) -> None:
    caminho_arquivo = ARQUIVOS_DIR / nome_armazenado
    caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho_arquivo, "wb") as f:
        f.write(conteudo)
    logger.info(f"Arquivo fisico salvo em {caminho_arquivo}.")

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
        logger.warning(f"Conflito de nome: {nome_armazenado}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ja existe um arquivo armazenado com esse ID.",
        )

    try:
        salvar_arquivo(conteudo, nome_armazenado)
    except Exception as e:
        logger.error(f"Erro ao salvar arquivo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao salvar arquivo fisicamente.",
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
    
    documento_json = jsonable_encoder(documento)
    
    documentos.append(documento_json)
    escrever_json(DOCUMENTOS_FILE, documentos)

    logger.info(f"Documento com ID {documento.id} criado com sucesso.")
    return documento

@router.get("/{documento_id}/integridade", status_code=status.HTTP_200_OK)
def verificar_integridade(documento_id: str):
    documento = buscar_por_id(DOCUMENTOS_FILE, documento_id)

    if not documento:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    try:
        caminho_arquivo = ARQUIVOS_DIR / documento["nome_armazenado"]
        if not caminho_arquivo.exists():
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        with open(caminho_arquivo, mode="rb") as file:
            conteudo = file.read()

        hash_atual = calcular_sha256(conteudo)
        integro = documento["sha256"] == hash_atual

        return {
            "id" : documento["id"],
            "nome" : documento["nome_original"],
            "hash_orginal" : documento["sha256"],
            "hash_atual" : hash_atual,
            "íntegro" : integro
        }
    except Exception as e:
        logger.error(f"Erro ao verificar integridade : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao verificar integradade"
        )

@router.get("/{documento_id}/download",status_code=status.HTTP_200_OK)
def baixar_documento(documento_id: str):
    documento = buscar_por_id(DOCUMENTOS_FILE, documento_id)

    if not documento:
        logger.warning(f"Documento com ID {documento_id} nao encontrado para download.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento nao encontrado.",
        )

    try:
        caminho_arquivo = ARQUIVOS_DIR / documento["nome_armazenado"]
        if not caminho_arquivo.exists():
            logger.error(f"Arquivo físico nao encontrado para o documento ID {documento_id}.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo físico nao encontrado.",
            )
        logger.info(f"Documento com ID {documento_id} baixado com sucesso.")
        return FileResponse(
            path=caminho_arquivo,
            media_type=documento["tipo_mime"],
            filename=documento["nome_original"],
        )
    except Exception as e:
        logger.error(f"Erro ao baixar documento com ID {documento_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao baixar o documento.",
        )

@router.put("/{documento_id}", response_model=Documento, status_code=status.HTTP_200_OK)
def atualizar_metadados(documento_id: str, categoria: str = Form(...),
                        descricao: str = Form(default=""), 
                        numero_patrimonial: str = Form(...), 
                        setor: str = Form(...), 
                        situacao: str = Form(...)):
    
    documento = buscar_por_id(DOCUMENTOS_FILE, documento_id)

    if not documento:
        logger.warning(f"Documento com ID {documento_id} nao encontrado para atualizacao.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento nao encontrado.",
        )

    try:
        documento["categoria"] = categoria
        documento["descricao"] = descricao
        documento["numero_patrimonial"] = numero_patrimonial
        documento["setor"] = setor
        documento["situacao"] = situacao

        atualizar(DOCUMENTOS_FILE, documento_id, documento)
        
    except Exception as e:
        logger.error(f"Erro ao atualizar documento com ID {documento_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar o documento.",
        )
