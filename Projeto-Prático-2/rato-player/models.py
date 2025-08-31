from datetime import date

from sqlalchemy.orm import Mapped, registry, mapped_column, relationship
from sqlalchemy import Column, Table, ForeignKey, Integer, String, Date, Enum

from enums import TipoColecaoEnum

table_registry = registry()

genero_colecao = Table(
    "genero_colecao",
    table_registry.metadata,
    Column("id_genero", ForeignKey("genero.id_genero"), primary_key=True),
    Column("id_colecao", ForeignKey("colecao.id_colecao"), primary_key=True),
)

@table_registry.mapped_as_dataclass
class Genero:
    __tablename__ = 'genero'

    id_genero: Mapped[int] = mapped_column(Integer, init=False, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    surgiu_em: Mapped[date] = mapped_column(Date, nullable=False)

    colecoes = relationship(
        "Colecao",
        secondary=genero_colecao,
        back_populates="generos"
    )

@table_registry.mapped_as_dataclass
class Colecao:
    __tablename__ = 'colecao'

    id_colecao: Mapped[int] = mapped_column(Integer, init=False, primary_key=True, autoincrement=True)
    caminho_capa: Mapped[str] = mapped_column(String(500), unique=False, nullable=False)
    duracao: Mapped[int] = mapped_column(Integer, nullable=False)
    data_lancamento: Mapped[date] = mapped_column(Date, nullable=False)
    titulo: Mapped[str] = mapped_column(String(90), nullable=False)
    tipo: Mapped[TipoColecaoEnum] = mapped_column(Enum(TipoColecaoEnum), nullable=False)

    generos = relationship(
        "Genero",
        secondary=genero_colecao,
        back_populates="colecoes"
    )