from datetime import date
from typing import Optional, Union

from pydantic import BaseModel, Field

from rato_player.enums import TipoColecaoEnum


class FilterPage(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(1, ge=1)


class ColecaoSearchFilters(BaseModel):
    titulo: Optional[str] = None
    tipo: Optional[TipoColecaoEnum] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None


class GeneroSearchFilters(BaseModel):
    nome: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None


class Mensagem(BaseModel):
    mensagem: str


# Schemas de entrada/edição (comuns para PostgreSQL e MongoDB)
class GeneroSchema(BaseModel):
    nome: str
    surgiu_em: date


class GeneroUpdateSchema(BaseModel):
    nome: Optional[str] = None
    surgiu_em: Optional[date] = None


class ColecaoSchema(BaseModel):
    titulo: str
    tipo: TipoColecaoEnum
    duracao: int
    caminho_capa: str
    data_lancamento: date


class ColecaoUpdateSchema(BaseModel):
    titulo: Optional[str] = None
    tipo: Optional[TipoColecaoEnum] = None
    duracao: Optional[int] = None
    caminho_capa: Optional[str] = None
    data_lancamento: Optional[date] = None


# Schemas básicos (flexíveis para PostgreSQL e MongoDB)
class GeneroBasic(BaseModel):
    id_genero: Union[int, str]  # int para PostgreSQL, str para MongoDB
    nome: str
    surgiu_em: date


class ColecaoBasic(BaseModel):
    id_colecao: Union[int, str]  # int para PostgreSQL, str para MongoDB
    titulo: str
    tipo: str
    duracao: int
    caminho_capa: str
    data_lancamento: date


# Schemas públicos (flexíveis para PostgreSQL e MongoDB)
class GeneroPublic(BaseModel):
    id_genero: Union[int, str]  # int para PostgreSQL, str para MongoDB
    nome: str
    surgiu_em: date
    colecoes: list[ColecaoBasic] = []


class ColecaoPublic(BaseModel):
    id_colecao: Union[int, str]  # int para PostgreSQL, str para MongoDB
    titulo: str
    tipo: str
    duracao: int
    caminho_capa: str
    data_lancamento: date
    generos: list[GeneroBasic] = []


# Schemas para listas (reutilizáveis para PostgreSQL e MongoDB)
class GeneroList(BaseModel):
    generos: list[GeneroPublic]


class ColecaoList(BaseModel):
    colecoes: list[ColecaoPublic]
