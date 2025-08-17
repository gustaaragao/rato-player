from http import HTTPStatus
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from database import get_session

router = APIRouter(prefix='/generos', tags=['Gêneros'])


@router.post('/', status_code=HTTPStatus.CREATED)
def create_genero(
    session: Session = Depends(get_session)
):
    ...

@router.get('/')
def read_generos(
    session: Session = Depends(get_session)
):
    ...

@router.get('/{id_genero}')
def read_genero_by_id(
    id_genero: int,
    session: Session = Depends(get_session)
):
    ...

@router.get('/buscar')
def search_generos(
    session: Session = Depends(get_session)
):
    ...

@router.put('/{id_genero}')
def update_genero(
    id_genero: int,
    session: Session = Depends(get_session)
):
    ...

@router.delete('/{id_genero}')
def delete_genero(
    id_genero: int,
    session: Session = Depends(get_session)
):
    ...
