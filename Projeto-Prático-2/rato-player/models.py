from datetime import date
from enum import Enum

from sqlalchemy.orm import Mapped, registry

table_registry = registry()

class TipoColecaoEnum(str, Enum):
    Album = "Album"
    EP = "EP"
    Single = "Single"
    Compilacao = "Compilacao"

@table_registry.mapped_as_dataclass
class Genero:
    __tablename__ = 'Genero'

    nome: Mapped[str]
    surgiu_em: Mapped[date]

@table_registry.mapped_as_dataclass
class Colecao:
    __tablename__ = 'Colecao'

    id_colecao: Mapped[int]
    caminho_capa: Mapped[str]
    duracao: Mapped[int]
    data_lancamento: Mapped[date]
    titulo: Mapped[str]
    tipo_colecao: Mapped[TipoColecaoEnum]

@table_registry.mapped_as_dataclass
class GeneroColecao:
    __tablename__ = 'Genero_Colecao'
    
    nome_genero: Mapped[str]
    id_colecao: Mapped[int]