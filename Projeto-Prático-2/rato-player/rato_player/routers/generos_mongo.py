from datetime import date
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from rato_player.databases.mongo import get_mongodb_database

router = APIRouter(prefix='/generos-mongo', tags=['Gêneros MongoDB'])


class GeneroMongo(BaseModel):
    nome: str
    surgiu_em: date


class GeneroResponse(BaseModel):
    id: str
    nome: str
    surgiu_em: date


@router.post('/', response_model=GeneroResponse)
async def create_genero_mongo(genero: GeneroMongo):
    """Criar um novo gênero no MongoDB."""
    try:
        db = await get_mongodb_database()
        collection = db.generos

        # Verifica se já existe um gênero com o mesmo nome
        existing = await collection.find_one({'nome': genero.nome})
        if existing:
            raise HTTPException(status_code=400, detail='Gênero já existe')

        # Converte para dict e insere
        genero_dict = genero.model_dump()
        genero_dict['surgiu_em'] = genero_dict['surgiu_em'].isoformat()

        result = await collection.insert_one(genero_dict)

        # Busca o documento inserido
        created_genero = await collection.find_one({'_id': result.inserted_id})

        return GeneroResponse(
            id=str(created_genero['_id']),
            nome=created_genero['nome'],
            surgiu_em=created_genero['surgiu_em'],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro interno: {str(e)}')


@router.get('/', response_model=list[GeneroResponse])
async def list_generos_mongo(limit: int = 10, skip: int = 0):
    """Listar gêneros do MongoDB com paginação."""
    try:
        db = await get_mongodb_database()
        collection = db.generos

        cursor = collection.find().skip(skip).limit(limit)
        generos = await cursor.to_list(length=limit)

        return [
            GeneroResponse(
                id=str(genero['_id']),
                nome=genero['nome'],
                surgiu_em=genero['surgiu_em'],
            )
            for genero in generos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro interno: {str(e)}')


@router.get('/{genero_id}', response_model=GeneroResponse)
async def get_genero_mongo(genero_id: str):
    """Obter um gênero específico por ID."""
    try:
        if not ObjectId.is_valid(genero_id):
            raise HTTPException(status_code=400, detail='ID inválido')

        db = await get_mongodb_database()
        collection = db.generos

        genero = await collection.find_one({'_id': ObjectId(genero_id)})
        if not genero:
            raise HTTPException(status_code=404, detail='Gênero não encontrado')

        return GeneroResponse(
            id=str(genero['_id']), nome=genero['nome'], surgiu_em=genero['surgiu_em']
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro interno: {str(e)}')


@router.delete('/{genero_id}')
async def delete_genero_mongo(genero_id: str):
    """Deletar um gênero por ID."""
    try:
        if not ObjectId.is_valid(genero_id):
            raise HTTPException(status_code=400, detail='ID inválido')

        db = await get_mongodb_database()
        collection = db.generos

        result = await collection.delete_one({'_id': ObjectId(genero_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail='Gênero não encontrado')

        return {'message': 'Gênero deletado com sucesso'}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro interno: {str(e)}')


@router.get('/search/', response_model=list[GeneroResponse])
async def search_generos_mongo(
    nome: Optional[str] = None,
    ano_inicio: Optional[int] = None,
    ano_fim: Optional[int] = None,
):
    try:
        db = await get_mongodb_database()
        collection = db.generos

        # Constrói o filtro de busca
        filter_query = {}

        if nome:
            filter_query['nome'] = {'$regex': nome, '$options': 'i'}  # Case insensitive

        if ano_inicio or ano_fim:
            date_filter = {}
            if ano_inicio:
                date_filter['$gte'] = f'{ano_inicio}-01-01'
            if ano_fim:
                date_filter['$lte'] = f'{ano_fim}-12-31'
            filter_query['surgiu_em'] = date_filter

        cursor = collection.find(filter_query).limit(20)
        generos = await cursor.to_list(length=20)

        return [
            GeneroResponse(
                id=str(genero['_id']),
                nome=genero['nome'],
                surgiu_em=genero['surgiu_em'],
            )
            for genero in generos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro interno: {str(e)}')
