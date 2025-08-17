from http import HTTPStatus
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from database import get_session

router = APIRouter(prefix='/colecoes', tags=['Coleções'])


@router.post('/', status_code=HTTPStatus.CREATED, summary='Criar uma nova coleção')
def create_colecao(
    session: Session = Depends(get_session)
):
    ...

@router.get(
    '/',
    summary='Listar todas as coleções',
    description='Retorna todas as coleções cadastradas, com suporte a paginação e filtro por tipo.'
)
def read_colecoes(
    session: Session = Depends(get_session)
):
    ...

@router.get(
    '/{id_colecao}',
    summary='Buscar coleção por ID',
    description='Retorna uma coleção específica pelo seu identificador único.'
)
def read_colecao_by_id(
    id_colecao: int,
    session: Session = Depends(get_session)
):
    ...

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
    nome: str = Query(..., description='Parte do nome da capa a ser buscada'),
    tipo: str | None = Query(None, description='Filtrar por tipo de coleção (ex: "Album", "EP", "Single", "Compilacao")'),
    session: Session = Depends(get_session)
):
    ...

@router.put(
    "/{id_colecao}",
    summary="Atualizar coleção totalmente",
    description="Substitui todos os campos da coleção especificada pelo corpo enviado."
)
def update_colecao(
    id_colecao: int,
    session: Session = Depends(get_session)
):
    ...

@router.patch(
    '/{id_colecao}',
    summary='Atualizar coleção parcialmente',
    description='Atualiza apenas os campos enviados no corpo da requisição.'
)
def patch_colecao(
    id_colecao: int,
    session: Session = Depends(get_session)
):
    ...

@router.delete(
    "/{id_colecao}",
    summary="Deletar coleção",
    description="Remove uma coleção pelo seu identificador único."
)
def delete_colecao(
    id_colecao: int,
    session: Session = Depends(get_session)
):
    ...