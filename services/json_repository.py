import json
from pathlib import Path
from typing import Any

from core.logging_config import logger

def garantir_arquivo(arquivo: Path) -> None:
    arquivo.parent.mkdir(parents=True, exist_ok=True)

    if not arquivo.exists(): 
        with open(arquivo, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

        logger.info(f"Arquivo {arquivo} criado com sucesso.")

def ler_json(arquivo: Path) -> list[Any]:
    garantir_arquivo(arquivo)

    with open(arquivo, "r", encoding="utf-8") as file:
        garantir_arquivo(arquivo)

        try:
            with open(arquivo, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as erro:
            logger.error(
                f"Erro ao ler o arquivo {arquivo}: {erro}. O arquivo será reiniciado.",
                arquivo.name,
                erro
            )
def escrever_json(arquivo: Path, dados: list[Any]) -> None:
    garantir_arquivo(arquivo)

    with open(arquivo, "w", encoding="utf-8") as file:
        json.dump(dados, file, ensure_ascii=False, indent=4)
        logger.info(f"Dados escritos com sucesso no arquivo {arquivo}.")
    logger.debug(
        f"Dados escritos no arquivo {arquivo}: {json.dumps(dados, ensure_ascii=False, indent=4)}"
    )

def buscar_por_id(arquivo: Path, id: int) -> Any:
    dados = ler_json(arquivo)
    for item in dados:
        if item.get("id") == id:
            return item
    logger.warning(f"Item com ID {id} não encontrado no arquivo {arquivo}.")
    return None

def atualizar(arquivo: Path, id: int, novos_dados: dict[str, Any]) -> bool:
    dados = ler_json(arquivo)
    for index, item in enumerate(dados):
        if item.get("id") == id:
            novos_dados["id"] = id
            dados[index] = novos_dados
            escrever_json(arquivo, dados)
            logger.info(f"Item com ID {id} atualizado com sucesso no arquivo {arquivo}.")
            return True
    logger.warning(f"Item com ID {id} não encontrado para atualização no arquivo {arquivo}.")
    return False

def deletar(arquivo: Path, id: int) -> bool:
    dados = ler_json(arquivo)

    nova_lista = [
        item for item in dados if item.get("id") != id
    ]

    if len(dados) == 0:
        logger.warning(f"Nenhum item encontrado no arquivo {arquivo} para deletar.")
        return False

    escrever_json(arquivo, nova_lista)
    logger.info(f"Item com ID {id} deletado com sucesso do arquivo {arquivo}.")

    return True