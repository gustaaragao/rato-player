from datetime import date
from typing import Optional

from pydantic import BaseModel

from enums import TipoColecaoEnum

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

class ColecaoPublic(BaseModel):
    id_colecao: int
    titulo: str
    tipo: str
    duracao: int
    caminho_capa: str
    data_lancamento: date

class ColecaoList(BaseModel):
    colecoes: list[ColecaoPublic]