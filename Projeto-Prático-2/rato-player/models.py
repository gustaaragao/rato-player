from datetime import date

from sqlalchemy.orm import Mapped, registry, mapped_column
from sqlalchemy import ForeignKey, Integer, String, Date, Enum

from enums import TipoColecaoEnum

table_registry = registry()


@table_registry.mapped_as_dataclass
class Genero:
    __tablename__ = 'genero'

    id_genero: Mapped[int] = mapped_column(Integer, init=False, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    surgiu_em: Mapped[date] = mapped_column(Date, nullable=False)

@table_registry.mapped_as_dataclass
class Colecao:
    __tablename__ = 'colecao'

    id_colecao: Mapped[int] = mapped_column(Integer, init=False, primary_key=True, autoincrement=True)
    caminho_capa: Mapped[str] = mapped_column(String(500), unique=False, nullable=False)
    duracao: Mapped[int] = mapped_column(Integer, nullable=False)
    data_lancamento: Mapped[date] = mapped_column(Date, nullable=False)
    titulo: Mapped[str] = mapped_column(String(90), nullable=False)
    tipo: Mapped[TipoColecaoEnum] = mapped_column(Enum(TipoColecaoEnum), nullable=False)

@table_registry.mapped_as_dataclass
class GeneroColecao:
    __tablename__ = 'Genero_Colecao'
    
    nome_genero: Mapped[str] = mapped_column(ForeignKey("Genero.nome"), primary_key=True)
    id_colecao: Mapped[int] = mapped_column(ForeignKey("Colecao.id_colecao"), primary_key=True)