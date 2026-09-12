from datetime import datetime

from pydantic import BaseModel,Field

class Documento(BaseModel):
    id: int = Field(gt=0, description="ID do documento")
    nome_original: str = Field(
        min_length=1, max_length=255, description="Nome original do documento"
    )
    nome_armazenado: str = Field(
        min_length=1, max_length=255, description="Nome armazenado do documento"
    )
    extensao: str = Field(
        min_length=1, max_length=10, description="Extensão do documento"
    )
    tipo_mime: str = Field(
        min_length=1, max_length=50, description="Tipo MIME do documento"
    )
    tamanho: int = Field(gt=0, description="Tamanho do documento em bytes")
    categoria: str = Field(
        min_length=1, max_length=50, description="Categoria do documento"
    )
    descricao: str = Field(
        min_length=1, max_length=500, description="Descrição do documento"
    )
    data_upload: datetime = Field(
        description="Data e hora do upload do documento"
    )
    sha256: str = Field(
        min_length=64, max_length=64, description="Hash SHA-256 do documento"
    )

class Funcionario(BaseModel):
    id: int = Field(gt=0, description="ID do funcionário")
    nome: str = Field(
        min_length=1, max_length=255, description="Nome do funcionário"
    )
    setor: str = Field(
        min_length=1, max_length=100, description="Setor do funcionário"
    )
    tipo: str = Field(
        min_length=1, max_length=50, description="Tipo do funcionário"
    )
    competencias: list[str] = Field(
        min_items=1, description="Lista de competências do funcionário"
    )