from datetime import date
from typing import Optional

from pydantic import BaseModel

from enums import TipoColecaoEnum

class Mensagem(BaseModel):
    mensagem: str

class GeneroSchema(BaseModel):
    nome: str
    surgiu_em: date

class GeneroUpdateSchema(BaseModel):
    nome: Optional[str] = None
    surgiu_em: Optional[date] = None

class GeneroBasic(BaseModel):
    id_genero: int
    nome: str
    surgiu_em: date

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

class ColecaoBasic(BaseModel):
    id_colecao: int
    titulo: str
    tipo: str
    duracao: int
    caminho_capa: str
    data_lancamento: date

class GeneroPublic(BaseModel):
    id_genero: int
    nome: str
    surgiu_em: date
    colecoes: list[ColecaoBasic] = []

class ColecaoPublic(BaseModel):
    id_colecao: int
    titulo: str
    tipo: str
    duracao: int
    caminho_capa: str
    data_lancamento: date
    generos: list[GeneroBasic] = []

# Schemas para listas
class GeneroList(BaseModel):
    generos: list[GeneroPublic]
    
class ColecaoList(BaseModel):
    colecoes: list[ColecaoPublic]