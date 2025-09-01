from http import HTTPStatus
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from rato_player.databases.mongo import get_mongo
from rato_player.schemas import (
    FilterPage,
    GeneroList,
    GeneroPublic,
    GeneroSchema,
    GeneroSearchFilters,
    GeneroUpdateSchema,
    Mensagem,
)

router = APIRouter(prefix='/mongo/generos', tags=['Gêneros - MongoDB'])

MongoDatabase = Annotated[AsyncIOMotorDatabase, HTTPException]
Pagination = Annotated[FilterPage, Query()]


def validate_object_id(obj_id: str) -> ObjectId:
    """Valida e converte string para ObjectId."""
    if not ObjectId.is_valid(obj_id):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='ID inválido.',
        )
    return ObjectId(obj_id)


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    summary='Criar um novo gênero',
    response_model=GeneroPublic,
)
async def create_genero(genero_schema: GeneroSchema):
    try:
        db = await get_mongo()
        collection = db.generos

        # Verifica se já existe um gênero com o mesmo nome
        existing = await collection.find_one({'nome': genero_schema.nome})
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f'O nome "{genero_schema.nome}" já está em uso.',
            )

        # Converte para dict e insere
        genero_dict = genero_schema.model_dump()
        genero_dict['surgiu_em'] = genero_dict['surgiu_em'].isoformat()

        result = await collection.insert_one(genero_dict)

        # Busca o documento inserido
        created_genero = await collection.find_one({'_id': result.inserted_id})

        return GeneroPublic(
            id_genero=str(created_genero['_id']),
            nome=created_genero['nome'],
            surgiu_em=created_genero['surgiu_em'],
            colecoes=[],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.get(
    '/',
    summary='Listar todos os gêneros',
    description='Retorna todos os gêneros cadastrados no MongoDB (com suporte a paginação).',
    response_model=GeneroList,
)
async def read_generos(pagination: Pagination):
    """Lista todos os gêneros com suporte a paginação."""
    try:
        db = await get_mongo()
        collection = db.generos

        cursor = collection.find().skip(pagination.offset).limit(pagination.limit)
        generos = await cursor.to_list(length=pagination.limit)

        generos_response = []
        for genero in generos:
            # Buscar coleções associadas a este gênero
            colecoes_cursor = db.colecoes.find({'generos_ids': str(genero['_id'])})
            colecoes = await colecoes_cursor.to_list(length=None)

            colecoes_data = []
            for colecao in colecoes:
                colecoes_data.append({
                    'id_colecao': str(colecao['_id']),
                    'titulo': colecao['titulo'],
                    'tipo': colecao['tipo'],
                    'duracao': colecao['duracao'],
                    'caminho_capa': colecao['caminho_capa'],
                    'data_lancamento': colecao['data_lancamento'],
                })

            generos_response.append(
                GeneroPublic(
                    id_genero=str(genero['_id']),
                    nome=genero['nome'],
                    surgiu_em=genero['surgiu_em'],
                    colecoes=colecoes_data,
                )
            )

        return GeneroList(generos=generos_response)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.get(
    '/buscar',
    summary='Buscar gêneros por nome e/ou período de surgimento',
    description="""
    Retorna uma lista de gêneros cujo **nome** contenha o valor informado,
    com suporte a paginação. Também é possível filtrar opcionalmente pelo
    período de data de surgimento.

    Exemplos:
    - `/generos/buscar?nome=rock`
    - `/generos/buscar?nome=rock&data_inicio=2020-01-01&data_fim=2022-12-31`
    """,
    response_model=GeneroList,
)
async def search_generos(
    filters: Annotated[GeneroSearchFilters, Query()],
    pagination: Pagination,
):
    try:
        db = await get_mongo()
        collection = db.generos

        # Constrói o filtro de busca
        filter_query = {}

        if filters.nome:
            filter_query['nome'] = {'$regex': filters.nome, '$options': 'i'}

        if filters.data_inicio and filters.data_fim:
            filter_query['surgiu_em'] = {
                '$gte': filters.data_inicio.isoformat(),
                '$lte': filters.data_fim.isoformat(),
            }
        elif filters.data_inicio:
            filter_query['surgiu_em'] = {'$gte': filters.data_inicio.isoformat()}
        elif filters.data_fim:
            filter_query['surgiu_em'] = {'$lte': filters.data_fim.isoformat()}

        cursor = collection.find(filter_query).skip(pagination.offset).limit(pagination.limit)
        generos = await cursor.to_list(length=pagination.limit)

        generos_response = []
        for genero in generos:
            # Buscar coleções associadas a este gênero
            colecoes_cursor = db.colecoes.find({'generos_ids': str(genero['_id'])})
            colecoes = await colecoes_cursor.to_list(length=None)

            colecoes_data = []
            for colecao in colecoes:
                colecoes_data.append({
                    'id_colecao': str(colecao['_id']),
                    'titulo': colecao['titulo'],
                    'tipo': colecao['tipo'],
                    'duracao': colecao['duracao'],
                    'caminho_capa': colecao['caminho_capa'],
                    'data_lancamento': colecao['data_lancamento'],
                })

            generos_response.append(
                GeneroPublic(
                    id_genero=str(genero['_id']),
                    nome=genero['nome'],
                    surgiu_em=genero['surgiu_em'],
                    colecoes=colecoes_data,
                )
            )

        return GeneroList(generos=generos_response)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.get(
    '/{id_genero}',
    summary='Buscar gênero por ID',
    description='Retorna um gênero específico pelo seu identificador único.',
    response_model=GeneroPublic,
)
async def read_genero_by_id(id_genero: str):
    try:
        obj_id = validate_object_id(id_genero)

        db = await get_mongo()
        generos_collection = db.generos
        colecoes_collection = db.colecoes

        genero = await generos_collection.find_one({'_id': obj_id})
        if not genero:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'O gênero de ID {id_genero} não foi encontrado.',
            )

        # Buscar coleções associadas a este gênero
        colecoes_cursor = colecoes_collection.find({'generos_ids': id_genero})
        colecoes = await colecoes_cursor.to_list(length=None)

        colecoes_data = []
        for colecao in colecoes:
            colecoes_data.append({
                'id_colecao': str(colecao['_id']),
                'titulo': colecao['titulo'],
                'tipo': colecao['tipo'],
                'duracao': colecao['duracao'],
                'caminho_capa': colecao['caminho_capa'],
                'data_lancamento': colecao['data_lancamento'],
            })

        return GeneroPublic(
            id_genero=str(genero['_id']),
            nome=genero['nome'],
            surgiu_em=genero['surgiu_em'],
            colecoes=colecoes_data,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.put(
    '/{id_genero}',
    summary='Atualizar gênero totalmente',
    description='Substitui todos os campos do gênero especificado pelo corpo enviado.',
    response_model=GeneroPublic,
)
async def update_genero(id_genero: str, genero_schema: GeneroSchema):
    try:
        obj_id = validate_object_id(id_genero)

        db = await get_mongo()
        collection = db.generos

        # Verifica se o gênero existe
        genero = await collection.find_one({'_id': obj_id})
        if not genero:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'O gênero de ID {id_genero} não foi encontrado.',
            )

        # Verifica se o novo nome não está em uso por outro gênero
        if genero_schema.nome != genero['nome']:
            existing = await collection.find_one({'nome': genero_schema.nome})
            if existing:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail=f'O nome "{genero_schema.nome}" já está em uso.',
                )

        # Atualiza o documento
        update_data = genero_schema.model_dump()
        update_data['surgiu_em'] = update_data['surgiu_em'].isoformat()

        await collection.update_one({'_id': obj_id}, {'$set': update_data})

        # Busca o documento atualizado
        updated_genero = await collection.find_one({'_id': obj_id})

        return GeneroPublic(
            id_genero=str(updated_genero['_id']),
            nome=updated_genero['nome'],
            surgiu_em=updated_genero['surgiu_em'],
            colecoes=[],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.patch(
    '/{id_genero}',
    summary='Atualizar gênero parcialmente',
    description='Atualiza apenas os campos enviados no corpo da requisição.',
    response_model=GeneroPublic,
)
async def patch_genero(id_genero: str, genero_schema: GeneroUpdateSchema):
    try:
        obj_id = validate_object_id(id_genero)

        db = await get_mongo()
        collection = db.generos

        # Verifica se o gênero existe
        genero = await collection.find_one({'_id': obj_id})
        if not genero:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'O gênero de ID {id_genero} não foi encontrado.',
            )

        # Prepara dados para atualização (apenas campos não nulos)
        update_data = genero_schema.model_dump(exclude_unset=True)

        if not update_data:
            # Se não há dados para atualizar, retorna o gênero atual
            return GeneroPublic(
                id_genero=str(genero['_id']),
                nome=genero['nome'],
                surgiu_em=genero['surgiu_em'],
                colecoes=[],
            )

        # Verifica conflito de nome se estiver sendo atualizado
        if 'nome' in update_data and update_data['nome'] != genero['nome']:
            existing = await collection.find_one({'nome': update_data['nome']})
            if existing:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail=f'O nome "{update_data["nome"]}" já está em uso.',
                )

        # Converte data se presente
        if 'surgiu_em' in update_data:
            update_data['surgiu_em'] = update_data['surgiu_em'].isoformat()

        # Atualiza o documento
        await collection.update_one({'_id': obj_id}, {'$set': update_data})

        # Busca o documento atualizado
        updated_genero = await collection.find_one({'_id': obj_id})

        return GeneroPublic(
            id_genero=str(updated_genero['_id']),
            nome=updated_genero['nome'],
            surgiu_em=updated_genero['surgiu_em'],
            colecoes=[],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.delete(
    '/{id_genero}',
    summary='Deletar gênero',
    description='Remove um gênero pelo seu identificador único.',
    response_model=Mensagem,
)
async def delete_genero(id_genero: str):
    try:
        obj_id = validate_object_id(id_genero)

        db = await get_mongo()
        generos_collection = db.generos
        colecoes_collection = db.colecoes

        # Verifica se o gênero existe
        genero = await generos_collection.find_one({'_id': obj_id})
        if not genero:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'O gênero de ID {id_genero} não foi encontrado.',
            )

        # Remove o gênero de todas as coleções que o referenciam
        await colecoes_collection.update_many(
            {'generos_ids': id_genero}, {'$pull': {'generos_ids': id_genero}}
        )

        # Remove o gênero
        await generos_collection.delete_one({'_id': obj_id})

        return Mensagem(mensagem='Gênero deletado com sucesso.')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.get(
    '/{id_genero}/colecoes',
    summary='Listar coleções de um gênero',
    description='Retorna todas as coleções associadas a um gênero específico.',
    response_model=dict,
)
async def get_colecoes_from_genero(id_genero: str):
    try:
        obj_id = validate_object_id(id_genero)

        db = await get_mongo()
        generos_collection = db.generos
        colecoes_collection = db.colecoes

        # Busca o gênero
        genero = await generos_collection.find_one({'_id': obj_id})
        if not genero:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'O gênero de ID {id_genero} não foi encontrado.',
            )

        # Busca coleções associadas a este gênero
        colecoes_cursor = colecoes_collection.find({'generos_ids': id_genero})
        colecoes = await colecoes_cursor.to_list(length=None)

        return {
            'genero': {
                'id_genero': str(genero['_id']),
                'nome': genero['nome'],
                'surgiu_em': genero['surgiu_em'],
            },
            'colecoes': [
                {
                    'id_colecao': str(colecao['_id']),
                    'titulo': colecao['titulo'],
                    'tipo': colecao['tipo'],
                    'duracao': colecao['duracao'],
                    'data_lancamento': colecao['data_lancamento'],
                }
                for colecao in colecoes
            ],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )
