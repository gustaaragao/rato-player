from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_session
from models import Colecao
from schemas.colecao import ColecaoList, ColecaoPublic, ColecaoSchema, ColecaoUpdateSchema
from schemas.mensagem import Mensagem
from enums import TipoColecaoEnum

router = APIRouter(prefix='/colecoes', tags=['Coleções'])


@router.post(
    '/', 
    status_code=HTTPStatus.CREATED, 
    summary='Criar uma nova coleção',
    response_model=ColecaoPublic
)
def create_colecao(
    colecao_schema: ColecaoSchema,
    session: Session = Depends(get_session)
):
    colecao = Colecao(
        titulo=colecao_schema.titulo,
        tipo=colecao_schema.tipo,
        duracao=colecao_schema.duracao,
        caminho_capa=colecao_schema.caminho_capa,
        data_lancamento=colecao_schema.data_lancamento
    )

    session.add(colecao)
    session.commit()
    session.refresh(colecao)

    return colecao

@router.get(
    '/',
    summary='Listar todas as coleções',
    description='Retorna todas as coleções cadastradas, com suporte a paginação e filtro por tipo.',
    response_model=ColecaoList
)
def read_colecoes(
    skip: int = 0,
    limit: int = 10,
    tipo: TipoColecaoEnum | None = Query(None, description="Filtrar por tipo de coleção"),
    session: Session = Depends(get_session)
):
    stmt = select(Colecao)
    if tipo:
        stmt = stmt.where(Colecao.tipo == tipo)

    stmt = stmt.offset(skip).limit(limit)

    colecoes = session.execute(stmt).scalars().all()

    return {'colecoes': colecoes}

@router.get(
    '/buscar',
    summary='Buscar coleções por nome',
    description='''
    Retorna uma lista de coleções cujo **nome da capa** contenha o valor informado, com suporte a paginação.
    Também é possível filtrar opcionalmente pelo **tipo de coleção**.
    
    Exemplos:
    - `/colecoes/buscar?nome=rock`
    - `/colecoes/buscar?nome=rock&tipo=CD`
    '''
)
def search_colecoes(
    titulo: str = Query(..., description='Parte do título da coleção a ser buscada'),
    tipo: TipoColecaoEnum | None = Query(None, description='Filtrar por tipo de coleção (ex: "Album", "EP", "Single", "Compilacao")'),
    session: Session = Depends(get_session)
):
    stmt = select(Colecao).where(Colecao.titulo.ilike(f"%{titulo}%"))

    if tipo:
        stmt = stmt.where(Colecao.tipo == tipo)
    
    colecoes = session.execute(stmt).scalars().all() 

    return {'colecoes': colecoes}

@router.get(
    '/{id_colecao}',
    summary='Buscar coleção por ID',
    description='Retorna uma coleção específica pelo seu identificador único.',
    response_model=ColecaoPublic
)
def read_colecao_by_id(
    id_colecao: int,
    session: Session = Depends(get_session)
):
    colecao = session.scalar(select(Colecao).where(Colecao.id_colecao == id_colecao))

    if not colecao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'A coleção de ID {id_colecao} não foi encontrada.'
        )
    
    return colecao

@router.put(
    '/{id_colecao}',
    summary='Atualizar coleção totalmente',
    description='Substitui todos os campos da coleção especificada pelo corpo enviado.',
    response_model=ColecaoPublic
)
def update_colecao(
    id_colecao: int,
    colecao_schema: ColecaoSchema,
    session: Session = Depends(get_session)
):
    colecao = session.scalar(select(Colecao).where(Colecao.id_colecao == id_colecao))

    if not colecao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'A coleção de ID {id_colecao} não foi encontrada.'
        )

    colecao_schema = colecao_schema.model_dump(exclude_unset=True)
    for key, value in colecao_schema.items():
        setattr(colecao, key, value)

    session.add(colecao)
    session.commit()
    session.refresh(colecao)

    return colecao

@router.patch(
    '/{id_colecao}',
    summary='Atualizar coleção parcialmente',
    description='Atualiza apenas os campos enviados no corpo da requisição.'
)
def patch_colecao(
    id_colecao: int,
    colecao_schema: ColecaoUpdateSchema,
    session: Session = Depends(get_session)
):
    colecao = session.scalar(select(Colecao).where(Colecao.id_colecao == id_colecao))

    if not colecao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'A coleção de ID {id_colecao} não foi encontrada.'
        )

    colecao_schema = colecao_schema.model_dump(exclude_unset=True)
    for key, value in colecao_schema.items():
        setattr(colecao, key, value)
    
    session.add(colecao)
    session.commit()
    session.refresh(colecao)

    return colecao

@router.delete(
    "/{id_colecao}",
    summary="Deletar coleção",
    description="Remove uma coleção pelo seu identificador único.",
    response_model=Mensagem
)
def delete_colecao(
    id_colecao: int,
    session: Session = Depends(get_session)
):
    colecao = session.scalar(select(Colecao).where(Colecao.id_colecao == id_colecao))

    if not colecao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'A coleção de ID {id_colecao} não foi encontrada.'
        )
    
    session.delete(colecao)
    session.commit()

    return {'mensagem': 'Coleção deletada com sucesso.'}