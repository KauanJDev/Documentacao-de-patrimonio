import json
from pathlib import Path
from typing import Any, Optional
import tempfile
from core.logging_config import logger

def garantir_arquivo(arquivo: Path) -> None:
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    if not arquivo.exists(): 
        with open(arquivo, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)
        logger.info(f"Arquivo {arquivo} criado com sucesso.")

def ler_json(arquivo: Path) -> list[Any]:
    garantir_arquivo(arquivo)
    try:
        with open(arquivo, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as erro:
        logger.error(f"Erro ao ler o arquivo {arquivo}: {erro}. Reiniciando estrutura.")
        with open(arquivo, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)
        return []

def escrever_json(arquivo: Path, dados: list[Any]) -> None:
    garantir_arquivo(arquivo)
    dir_destino = arquivo.parent
    with tempfile.NamedTemporaryFile("w", dir=dir_destino, delete=False, encoding="utf-8", suffix=".tmp") as tmp:
        json.dump(dados, tmp, ensure_ascii=False, indent=4)
        caminho_temp = Path(tmp.name)
    caminho_temp.replace(arquivo)
    logger.info(f"Dados escritos com sucesso no arquivo {arquivo}.")

def buscar_por_id(arquivo: Path, id: str) -> Optional[dict[str, Any]]:
    dados = ler_json(arquivo)
    for item in dados:
        if item.get("id") == id:
            return item
    logger.warning(f"Item com ID {id} não encontrado no arquivo {arquivo}.")
    return None

def atualizar(arquivo: Path, id: str, novos_dados: dict[str, Any]) -> bool:
    dados = ler_json(arquivo)
    for index, item in enumerate(dados):
        if item.get("id") == id:
            novos_dados["id"] = id
            dados[index] = novos_dados
            escrever_json(arquivo, dados)
            logger.info(f"Item com ID {id} atualizado com sucesso no arquivo {arquivo}.")
            return True
    logger.warning(f"Item com ID {id} não encontrado para atualização.")
    return False

def deletar(arquivo: Path, id: str) -> bool:
    dados = ler_json(arquivo)
    nova_lista = [item for item in dados if item.get("id") != id]

    if len(nova_lista) == len(dados):
        logger.warning(f"Nenhum item com ID {id} foi encontrado para deletar.")
        return False

    escrever_json(arquivo, nova_lista)
    logger.info(f"Registro do item ID {id} deletado com sucesso do JSON.")
    return True