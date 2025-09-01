from datetime import date
from http import HTTPStatus
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from rato_player.databases.mongo import get_mongodb_database
from rato_player.enums import TipoColecaoEnum

router = APIRouter(prefix='/colecoes-mongo', tags=['Coleções MongoDB'])


class ColecaoMongo(BaseModel):
    titulo: str
    tipo: TipoColecaoEnum
    duracao: int
    caminho_capa: str
    data_lancamento: date
    generos_ids: Optional[list[str]] = []


class ColecaoResponse(BaseModel):
    id: str
    titulo: str
    tipo: TipoColecaoEnum
    duracao: int
    caminho_capa: str
    data_lancamento: date
    generos_ids: list[str] = []


@router.post('/', response_model=ColecaoResponse)
async def create_colecao_mongo(colecao: ColecaoMongo):
    """Criar uma nova coleção no MongoDB."""
    try:
        db = await get_mongodb_database()
        collection = db.colecoes

        # Converte para dict e insere
        colecao_dict = colecao.model_dump()
        colecao_dict['data_lancamento'] = colecao_dict['data_lancamento'].isoformat()
        colecao_dict['tipo'] = colecao_dict['tipo'].value

        result = await collection.insert_one(colecao_dict)

        # Busca o documento inserido
        created_colecao = await collection.find_one({'_id': result.inserted_id})

        return ColecaoResponse(
            id=str(created_colecao['_id']),
            titulo=created_colecao['titulo'],
            tipo=created_colecao['tipo'],
            duracao=created_colecao['duracao'],
            caminho_capa=created_colecao['caminho_capa'],
            data_lancamento=created_colecao['data_lancamento'],
            generos_ids=created_colecao.get('generos_ids', []),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro interno: {str(e)}')


@router.get('/', response_model=list[ColecaoResponse])
async def list_colecoes_mongo(limit: int = 10, skip: int = 0):
    """Listar coleções do MongoDB com paginação."""
    try:
        db = await get_mongodb_database()
        collection = db.colecoes

        cursor = collection.find().skip(skip).limit(limit)
        colecoes = await cursor.to_list(length=limit)

        return [
            ColecaoResponse(
                id=str(colecao['_id']),
                titulo=colecao['titulo'],
                tipo=colecao['tipo'],
                duracao=colecao['duracao'],
                caminho_capa=colecao['caminho_capa'],
                data_lancamento=colecao['data_lancamento'],
                generos_ids=colecao.get('generos_ids', []),
            )
            for colecao in colecoes
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro interno: {str(e)}')


@router.get('/{colecao_id}', response_model=ColecaoResponse)
async def get_colecao_mongo(colecao_id: str):
    """Obter uma coleção específica por ID."""
    try:
        if not ObjectId.is_valid(colecao_id):
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='ID inválido')

        db = await get_mongodb_database()
        collection = db.colecoes

        colecao = await collection.find_one({'_id': ObjectId(colecao_id)})
        if not colecao:
            raise HTTPException(status_code=404, detail='Coleção não encontrada')

        return ColecaoResponse(
            id=str(colecao['_id']),
            titulo=colecao['titulo'],
            tipo=colecao['tipo'],
            duracao=colecao['duracao'],
            caminho_capa=colecao['caminho_capa'],
            data_lancamento=colecao['data_lancamento'],
            generos_ids=colecao.get('generos_ids', []),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro interno: {str(e)}')


@router.delete('/{colecao_id}')
async def delete_colecao_mongo(colecao_id: str):
    """Deletar uma coleção por ID."""
    try:
        if not ObjectId.is_valid(colecao_id):
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='ID inválido')

        db = await get_mongodb_database()
        collection = db.colecoes

        result = await collection.delete_one({'_id': ObjectId(colecao_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail='Coleção não encontrada')

        return {'message': 'Coleção deletada com sucesso'}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro interno: {str(e)}')


@router.post('/{colecao_id}/generos/{genero_id}')
async def add_genero_to_colecao_mongo(colecao_id: str, genero_id: str):
    """Adicionar um gênero a uma coleção."""
    try:
        if not ObjectId.is_valid(colecao_id) or not ObjectId.is_valid(genero_id):
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='ID inválido')

        db = await get_mongodb_database()
        colecoes_collection = db.colecoes
        generos_collection = db.generos

        # Verifica se a coleção existe
        colecao = await colecoes_collection.find_one({'_id': ObjectId(colecao_id)})
        if not colecao:
            raise HTTPException(status_code=404, detail='Coleção não encontrada')

        # Verifica se o gênero existe
        genero = await generos_collection.find_one({'_id': ObjectId(genero_id)})
        if not genero:
            raise HTTPException(status_code=404, detail='Gênero não encontrado')

        # Adiciona o gênero se não estiver já associado
        current_generos = colecao.get('generos_ids', [])
        if genero_id not in current_generos:
            await colecoes_collection.update_one(
                {'_id': ObjectId(colecao_id)}, {'$addToSet': {'generos_ids': genero_id}}
            )
            return {'message': 'Gênero adicionado com sucesso'}
        else:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Gênero já está associado à coleção',
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro interno: {str(e)}')


@router.delete('/{colecao_id}/generos/{genero_id}')
async def remove_genero_from_colecao_mongo(colecao_id: str, genero_id: str):
    """Remover um gênero de uma coleção."""
    try:
        if not ObjectId.is_valid(colecao_id) or not ObjectId.is_valid(genero_id):
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='ID inválido')

        db = await get_mongodb_database()
        colecoes_collection = db.colecoes

        # Verifica se a coleção existe
        colecao = await colecoes_collection.find_one({'_id': ObjectId(colecao_id)})
        if not colecao:
            raise HTTPException(status_code=404, detail='Coleção não encontrada')

        # Remove o gênero
        result = await colecoes_collection.update_one(
            {'_id': ObjectId(colecao_id)}, {'$pull': {'generos_ids': genero_id}}
        )

        if result.modified_count > 0:
            return {'message': 'Gênero removido com sucesso'}
        else:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Gênero não estava associado à coleção',
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro interno: {str(e)}')


@router.get('/search/', response_model=list[ColecaoResponse])
async def search_colecoes_mongo(
    titulo: Optional[str] = None,
    tipo: Optional[TipoColecaoEnum] = None,
    ano_inicio: Optional[int] = None,
    ano_fim: Optional[int] = None,
):
    """Buscar coleções por critérios."""
    try:
        db = await get_mongodb_database()
        collection = db.colecoes

        # Constrói o filtro de busca
        filter_query = {}

        if titulo:
            filter_query['titulo'] = {'$regex': titulo, '$options': 'i'}

        if tipo:
            filter_query['tipo'] = tipo.value

        if ano_inicio or ano_fim:
            date_filter = {}
            if ano_inicio:
                date_filter['$gte'] = f'{ano_inicio}-01-01'
            if ano_fim:
                date_filter['$lte'] = f'{ano_fim}-12-31'
            filter_query['data_lancamento'] = date_filter

        cursor = collection.find(filter_query).limit(20)
        colecoes = await cursor.to_list(length=20)

        return [
            ColecaoResponse(
                id=str(colecao['_id']),
                titulo=colecao['titulo'],
                tipo=colecao['tipo'],
                duracao=colecao['duracao'],
                caminho_capa=colecao['caminho_capa'],
                data_lancamento=colecao['data_lancamento'],
                generos_ids=colecao.get('generos_ids', []),
            )
            for colecao in colecoes
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro interno: {str(e)}')
