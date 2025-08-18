from datetime import date
from http import HTTPStatus
from typing import Optional
from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query, HTTPException
from database import get_session
from models import Genero
from schemas.mensagem import Mensagem
from schemas.genero import GeneroSchema, GeneroList, GeneroPublic, GeneroUpdateSchema

router = APIRouter(prefix='/generos', tags=['Gêneros'])


@router.post(
    '/', 
    status_code=HTTPStatus.CREATED, 
    summary='Criar uma novo gênero',
    response_model=GeneroPublic
)
def create_genero(
    genero_schema: GeneroSchema,
    session: Session = Depends(get_session)
):
    db_genero = session.scalar(select(Genero).where(Genero.nome == genero_schema.nome))

    if db_genero:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f'O nome "{genero_schema.nome}" já está em uso.'
        )

    genero = Genero(nome=genero_schema.nome, surgiu_em=genero_schema.surgiu_em)

    session.add(genero)
    session.commit()
    session.refresh(genero)

    return genero

@router.get(
    '/',
    summary='Listar todos os gêneros',
    description='Retorna todos os gêneros cadastrados (com suporte a paginação).',
    response_model=GeneroList
)
def read_generos(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    generos = session.scalars(select(Genero).offset(skip).limit(limit)).all()

    return {'generos': generos}

@router.get(
    '/buscar',
    summary='Buscar gêneros por nome e/ou período de surgimento',
    description='''
    Retorna uma lista de gêneros cujo **nome** contenha o valor informado, 
    com suporte a paginação. Também é possível filtrar opcionalmente pelo 
    período de data de surgimento.

    Exemplos:
    - `/generos/buscar?nome=rock`
    - `/generos/buscar?nome=rock&data_inicio=2020-01-01&data_fim=2022-12-31`
    ''',
    response_model=GeneroList
)
def search_generos(
    nome: str | None = Query(None, description='Parte do nome do gênero a ser buscado'),
    data_inicio: Optional[date] = Query(None, description='Data mínima de surgimento (Formato: YYYY-MM-DD)'),
    data_fim: Optional[date] = Query(None, description='Data máxima de surgimento (Formato: YYYY-MM-DD)'),
    skip: int = 0, 
    limit: int = 10,
    session: Session = Depends(get_session)
):
    stmt = select(Genero)

    if nome:
        stmt = stmt.where(Genero.nome.ilike(f"%{nome}%"))

    if data_inicio and data_fim:
        stmt = stmt.where(and_(Genero.surgiu_em >= data_inicio, Genero.surgiu_em <= data_fim))
    elif data_inicio:
        stmt = stmt.where(Genero.surgiu_em >= data_inicio)
    elif data_fim:
        stmt = stmt.where(Genero.surgiu_em <= data_fim)
    
    stmt = stmt.offset(skip).limit(limit)

    generos = session.execute(stmt).scalars().all() 

    return {'generos': generos}

@router.get(
    '/{id_genero}',
    summary='Buscar gênero por ID',
    description='Retorna um gênero específico pelo seu identificador único.',
    response_model=GeneroPublic
)
def read_genero_by_id(
    id_genero: int,
    session: Session = Depends(get_session)
):
    db_genero = session.scalar(select(Genero).where(Genero.id_genero == id_genero))

    if not db_genero:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'O gênero de ID {id_genero} não foi encontrado.'
        )
    
    return db_genero

@router.put(
    '/{id_genero}',
    summary='Atualizar gênero totalmente',
    description='Substitui todos os campos do gênero especificado pelo corpo enviado.',
    response_model=GeneroPublic
)
def update_genero(
    id_genero: int,
    genero_schema: GeneroSchema,
    session: Session = Depends(get_session)
):
    genero = session.scalar(select(Genero).where(Genero.id_genero == id_genero))

    if not genero:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'O gênero de ID {id_genero} não foi encontrado.'
        )

    genero_schema = genero_schema.model_dump()
    for key, value in genero_schema.items():
        setattr(genero, key, value)
    
    session.add(genero)
    session.commit()
    session.refresh(genero)

    return genero

@router.patch(
    '/{id_genero}',
    summary='Atualizar gênero parcialmente',
    description='Atualiza apenas os campos enviados no corpo da requisição.',
    response_model=GeneroPublic
)
def patch_genero(
    id_genero: int,
    genero_schema: GeneroUpdateSchema,
    session: Session = Depends(get_session)
):
    genero = session.scalar(select(Genero).where(Genero.id_genero == id_genero))

    if not genero:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'O gênero de ID {id_genero} não foi encontrado.'
        )

    genero_schema = genero_schema.model_dump(exclude_unset=True)
    for key, value in genero_schema.items():
        setattr(genero, key, value)
    
    session.add(genero)
    session.commit()
    session.refresh(genero)

    return genero

@router.delete(
    '/{id_genero}', 
    summary="Deletar gênero",
    description="Remove um gênero pelo seu identificador único.",
    response_model=Mensagem
)
def delete_genero(
    id_genero: int,
    session: Session = Depends(get_session)
):
    colecao = session.scalar(select(Genero).where(Genero.id_genero == id_genero))

    if not colecao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'A coleção de ID {id_genero} não foi encontrada.'
        )
    
    session.delete(colecao)
    session.commit()

    return {'mensagem': 'Gênero deletado com sucesso.'}