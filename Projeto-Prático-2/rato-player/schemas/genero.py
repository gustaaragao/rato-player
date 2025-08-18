from datetime import date
from typing import Optional

from pydantic import BaseModel


class GeneroSchema(BaseModel):
    nome: str
    surgiu_em: date

class GeneroPublic(BaseModel):
    id_genero: int
    nome: str
    surgiu_em: date

class GeneroUpdateSchema(BaseModel):
    nome: Optional[str] = None
    surgiu_em: Optional[date] = None
    
class GeneroList(BaseModel):
    generos: list[GeneroPublic]