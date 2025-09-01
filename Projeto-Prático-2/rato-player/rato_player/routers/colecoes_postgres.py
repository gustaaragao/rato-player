from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, select
from sqlalchemy.orm import Session, selectinload

from rato_player.databases.postgres import get_postgres
from rato_player.models import Colecao, Genero
from rato_player.schemas import (
    ColecaoList,
    ColecaoPublic,
    ColecaoSchema,
    ColecaoSearchFilters,
    ColecaoUpdateSchema,
    FilterPage,
    Mensagem,
)

router = APIRouter(prefix='/postgres/colecoes', tags=['Coleções - Postgres'])

SessionPostgres = Annotated[Session, Depends(get_postgres)]
Pagination = Annotated[FilterPage, Query()]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    summary='Criar uma nova coleção',
    response_model=ColecaoPublic,
)
def create_colecao(colecao_schema: ColecaoSchema, session: SessionPostgres):
    colecao = Colecao(
        titulo=colecao_schema.titulo,
        tipo=colecao_schema.tipo,
        duracao=colecao_schema.duracao,
        caminho_capa=colecao_schema.caminho_capa,
        data_lancamento=colecao_schema.data_lancamento,
    )

    session.add(colecao)
    session.commit()
    session.refresh(colecao)

    return colecao


@router.get(
    '/',
    summary='Listar todas as coleções',
    description='Retorna todas as coleções cadastradas (com suporte a paginação).',
    response_model=ColecaoList,
)
def read_colecoes(session: SessionPostgres, pagination: Pagination):
    colecoes = session.scalars(
        select(Colecao)
        .options(selectinload(Colecao.generos))
        .offset(pagination.offset)
        .limit(pagination.limit)
    ).all()

    return {'colecoes': colecoes}


@router.get(
    '/buscar',
    summary='Buscar coleções por nome e/ou período de lançamento',
    description="""
    Retorna uma lista de coleções cujo **título** contenha o valor informado,
    com suporte a paginação. Também é possível filtrar opcionalmente pelo
    **tipo de coleção** e/ou por período de data de lançamento.

    Exemplos:
    - `/colecoes/buscar?titulo=rock`
    - `/colecoes/buscar?titulo=rock&tipo=CD`
    - `/colecoes/buscar?titulo=rock&data_inicio=2020-01-01&data_fim=2022-12-31`
    """,
    response_model=ColecaoList,
)
def search_colecoes(
    session: SessionPostgres,
    filters: Annotated[ColecaoSearchFilters, Query()],
    pagination: Pagination,
):
    stmt = select(Colecao)

    if filters.titulo:
        stmt = stmt.where(Colecao.titulo.ilike(f'%{filters.titulo}%'))

    if filters.tipo:
        stmt = stmt.where(Colecao.tipo == filters.tipo)

    if filters.data_inicio and filters.data_fim:
        stmt = stmt.where(
            and_(
                Colecao.data_lancamento >= filters.data_inicio,
                Colecao.data_lancamento <= filters.data_fim,
            )
        )
    elif filters.data_inicio:
        stmt = stmt.where(Colecao.data_lancamento >= filters.data_inicio)
    elif filters.data_fim:
        stmt = stmt.where(Colecao.data_lancamento <= filters.data_fim)

    stmt = stmt.offset(pagination.offset).limit(pagination.limit)

    colecoes = (
        session.execute(stmt.options(selectinload(Colecao.generos))).scalars().all()
    )

    return {'colecoes': colecoes}


@router.get(
    '/{id_colecao}',
    summary='Buscar coleção por ID',
    description='Retorna uma coleção específica pelo seu identificador único.',
    response_model=ColecaoPublic,
)
def read_colecao_by_id(id_colecao: int, session: SessionPostgres):
    colecao = session.scalar(
        select(Colecao)
        .options(selectinload(Colecao.generos))
        .where(Colecao.id_colecao == id_colecao)
    )

    if not colecao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'A coleção de ID {id_colecao} não foi encontrada.',
        )

    return colecao


@router.put(
    '/{id_colecao}',
    summary='Atualizar coleção totalmente',
    description='Substitui todos os campos da coleção especificada pelo corpo enviado.',
    response_model=ColecaoPublic,
)
def update_colecao(
    id_colecao: int, colecao_schema: ColecaoSchema, session: SessionPostgres
):
    colecao = session.scalar(select(Colecao).where(Colecao.id_colecao == id_colecao))

    if not colecao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'A coleção de ID {id_colecao} não foi encontrada.',
        )

    colecao_schema = colecao_schema.model_dump()
    for key, value in colecao_schema.items():
        setattr(colecao, key, value)

    session.add(colecao)
    session.commit()
    session.refresh(colecao)

    return colecao


@router.patch(
    '/{id_colecao}',
    summary='Atualizar coleção parcialmente',
    description='Atualiza apenas os campos enviados no corpo da requisição.',
    response_model=ColecaoPublic,
)
def patch_colecao(
    id_colecao: int, colecao_schema: ColecaoUpdateSchema, session: SessionPostgres
):
    colecao = session.scalar(select(Colecao).where(Colecao.id_colecao == id_colecao))

    if not colecao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'A coleção de ID {id_colecao} não foi encontrada.',
        )

    colecao_schema = colecao_schema.model_dump(exclude_unset=True)
    for key, value in colecao_schema.items():
        setattr(colecao, key, value)

    session.add(colecao)
    session.commit()
    session.refresh(colecao)

    return colecao


@router.delete(
    '/{id_colecao}',
    summary='Deletar coleção',
    description='Remove uma coleção pelo seu identificador único.',
    response_model=Mensagem,
)
def delete_colecao(id_colecao: int, session: SessionPostgres):
    colecao = session.scalar(select(Colecao).where(Colecao.id_colecao == id_colecao))

    if not colecao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'A coleção de ID {id_colecao} não foi encontrada.',
        )

    session.delete(colecao)
    session.commit()

    return {'mensagem': 'Coleção deletada com sucesso.'}


@router.post(
    '/{id_colecao}/generos/{id_genero}',
    summary='Associar gênero a uma coleção',
    description='Adiciona um gênero a uma coleção específica.',
    response_model=Mensagem,
)
def add_genero_to_colecao(id_colecao: int, id_genero: int, session: SessionPostgres):
    # Buscar a coleção
    colecao = session.scalar(select(Colecao).where(Colecao.id_colecao == id_colecao))
    if not colecao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'A coleção de ID {id_colecao} não foi encontrada.',
        )

    # Buscar o gênero
    genero = session.scalar(select(Genero).where(Genero.id_genero == id_genero))
    if not genero:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'O gênero de ID {id_genero} não foi encontrado.',
        )

    # Verificar se a associação já existe
    if genero in colecao.generos:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=(
                f'O gênero "{genero.nome}" já está associado à '
                f'coleção "{colecao.titulo}".'
            ),
        )

    # Adicionar o gênero à coleção
    colecao.generos.append(genero)
    session.commit()

    return {
        'mensagem': (
            f'Gênero "{genero.nome}" associado à '
            f'coleção "{colecao.titulo}" com sucesso.'
        )
    }


@router.delete(
    '/{id_colecao}/generos/{id_genero}',
    summary='Desassociar gênero de uma coleção',
    description='Remove um gênero de uma coleção específica.',
    response_model=Mensagem,
)
def remove_genero_from_colecao(
    id_colecao: int, id_genero: int, session: SessionPostgres
):
    # Buscar a coleção
    colecao = session.scalar(select(Colecao).where(Colecao.id_colecao == id_colecao))
    if not colecao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'A coleção de ID {id_colecao} não foi encontrada.',
        )

    # Buscar o gênero
    genero = session.scalar(select(Genero).where(Genero.id_genero == id_genero))
    if not genero:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'O gênero de ID {id_genero} não foi encontrado.',
        )

    # Verificar se a associação existe
    if genero not in colecao.generos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=(
                f'O gênero "{genero.nome}" não está associado à '
                f'coleção "{colecao.titulo}".'
            ),
        )

    # Remover o gênero da coleção
    colecao.generos.remove(genero)
    session.commit()

    return {
        'mensagem': (
            f'Gênero "{genero.nome}" desassociado da '
            f'coleção "{colecao.titulo}" com sucesso.'
        )
    }


@router.get(
    '/{id_colecao}/generos',
    summary='Listar gêneros de uma coleção',
    description='Retorna todos os gêneros associados a uma coleção específica.',
    response_model=dict,
)
def get_generos_from_colecao(id_colecao: int, session: SessionPostgres):
    # Buscar a coleção com os gêneros carregados
    colecao = session.scalar(select(Colecao).where(Colecao.id_colecao == id_colecao))
    if not colecao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'A coleção de ID {id_colecao} não foi encontrada.',
        )

    return {
        'colecao': {'id_colecao': colecao.id_colecao, 'titulo': colecao.titulo},
        'generos': [
            {
                'id_genero': genero.id_genero,
                'nome': genero.nome,
                'surgiu_em': genero.surgiu_em,
            }
            for genero in colecao.generos
        ],
    }


@router.put(
    '/{id_colecao}/generos',
    summary='Definir gêneros de uma coleção',
    description='Substitui todos os gêneros de uma coleção pelos IDs fornecidos.',
    response_model=Mensagem,
)
def set_generos_to_colecao(
    id_colecao: int, generos_ids: list[int], session: SessionPostgres
):
    # Buscar a coleção
    colecao = session.scalar(select(Colecao).where(Colecao.id_colecao == id_colecao))
    if not colecao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'A coleção de ID {id_colecao} não foi encontrada.',
        )

    # Buscar todos os gêneros pelos IDs
    generos = session.scalars(
        select(Genero).where(Genero.id_genero.in_(generos_ids))
    ).all()

    # Verificar se todos os gêneros foram encontrados
    if len(generos) != len(generos_ids):
        generos_encontrados = [g.id_genero for g in generos]
        generos_nao_encontrados = [
            id for id in generos_ids if id not in generos_encontrados
        ]
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Gêneros não encontrados: {generos_nao_encontrados}',
        )

    # Substituir todos os gêneros da coleção
    colecao.generos.clear()
    colecao.generos.extend(generos)
    session.commit()

    generos_nomes = [g.nome for g in generos]
    return {
        'mensagem': (
            f'Gêneros da coleção "{colecao.titulo}" definidos como: '
            f'{", ".join(generos_nomes)}'
        )
    }
