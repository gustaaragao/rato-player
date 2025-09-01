from http import HTTPStatus
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query

from rato_player.databases.mongo import get_mongo
from rato_player.schemas import (
    ColecaoList,
    ColecaoPublic,
    ColecaoSchema,
    ColecaoSearchFilters,
    ColecaoUpdateSchema,
    FilterPage,
    Mensagem,
)

router = APIRouter(prefix='/mongo/colecoes', tags=['Coleções - MongoDB'])

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
    summary='Criar uma nova coleção',
    response_model=ColecaoPublic,
)
async def create_colecao(colecao_schema: ColecaoSchema):
    try:
        db = await get_mongo()
        collection = db.colecoes

        # Converte para dict e insere
        colecao_dict = colecao_schema.model_dump()
        colecao_dict['data_lancamento'] = colecao_dict['data_lancamento'].isoformat()
        colecao_dict['tipo'] = colecao_dict['tipo'].value
        colecao_dict['generos_ids'] = []  # Inicializa com lista vazia

        result = await collection.insert_one(colecao_dict)

        # Busca o documento inserido
        created_colecao = await collection.find_one({'_id': result.inserted_id})

        return ColecaoPublic(
            id_colecao=str(created_colecao['_id']),
            titulo=created_colecao['titulo'],
            tipo=created_colecao['tipo'],
            duracao=created_colecao['duracao'],
            caminho_capa=created_colecao['caminho_capa'],
            data_lancamento=created_colecao['data_lancamento'],
            generos=[],
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.get(
    '/',
    summary='Listar todas as coleções',
    description='Retorna todas as coleções cadastradas no MongoDB (com suporte a paginação).',
    response_model=ColecaoList,
)
async def read_colecoes(pagination: Pagination):
    try:
        db = await get_mongo()
        colecoes_collection = db.colecoes
        generos_collection = db.generos

        cursor = colecoes_collection.find().skip(pagination.offset).limit(pagination.limit)
        colecoes = await cursor.to_list(length=pagination.limit)

        colecoes_response = []
        for colecao in colecoes:
            # Buscar gêneros associados a esta coleção
            generos_ids = colecao.get('generos_ids', [])
            generos_data = []

            if generos_ids:
                generos_cursor = generos_collection.find({
                    '_id': {'$in': [ObjectId(gid) for gid in generos_ids if ObjectId.is_valid(gid)]}
                })
                generos = await generos_cursor.to_list(length=None)

                for genero in generos:
                    generos_data.append({
                        'id_genero': str(genero['_id']),
                        'nome': genero['nome'],
                        'surgiu_em': genero['surgiu_em'],
                    })

            colecoes_response.append(
                ColecaoPublic(
                    id_colecao=str(colecao['_id']),
                    titulo=colecao['titulo'],
                    tipo=colecao['tipo'],
                    duracao=colecao['duracao'],
                    caminho_capa=colecao['caminho_capa'],
                    data_lancamento=colecao['data_lancamento'],
                    generos=generos_data,
                )
            )

        return ColecaoList(colecoes=colecoes_response)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


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
async def search_colecoes(
    filters: Annotated[ColecaoSearchFilters, Query()],
    pagination: Pagination,
):
    try:
        db = await get_mongo()
        colecoes_collection = db.colecoes
        generos_collection = db.generos

        # Constrói o filtro de busca
        filter_query = {}

        if filters.titulo:
            filter_query['titulo'] = {'$regex': filters.titulo, '$options': 'i'}

        if filters.tipo:
            filter_query['tipo'] = filters.tipo.value

        if filters.data_inicio and filters.data_fim:
            filter_query['data_lancamento'] = {
                '$gte': filters.data_inicio.isoformat(),
                '$lte': filters.data_fim.isoformat(),
            }
        elif filters.data_inicio:
            filter_query['data_lancamento'] = {'$gte': filters.data_inicio.isoformat()}
        elif filters.data_fim:
            filter_query['data_lancamento'] = {'$lte': filters.data_fim.isoformat()}

        cursor = colecoes_collection.find(filter_query).skip(pagination.offset).limit(pagination.limit)
        colecoes = await cursor.to_list(length=pagination.limit)

        colecoes_response = []
        for colecao in colecoes:
            # Buscar gêneros associados a esta coleção
            generos_ids = colecao.get('generos_ids', [])
            generos_data = []

            if generos_ids:
                generos_cursor = generos_collection.find({
                    '_id': {'$in': [ObjectId(gid) for gid in generos_ids if ObjectId.is_valid(gid)]}
                })
                generos = await generos_cursor.to_list(length=None)

                for genero in generos:
                    generos_data.append({
                        'id_genero': str(genero['_id']),
                        'nome': genero['nome'],
                        'surgiu_em': genero['surgiu_em'],
                    })

            colecoes_response.append(
                ColecaoPublic(
                    id_colecao=str(colecao['_id']),
                    titulo=colecao['titulo'],
                    tipo=colecao['tipo'],
                    duracao=colecao['duracao'],
                    caminho_capa=colecao['caminho_capa'],
                    data_lancamento=colecao['data_lancamento'],
                    generos=generos_data,
                )
            )

        return ColecaoList(colecoes=colecoes_response)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.get(
    '/{id_colecao}',
    summary='Buscar coleção por ID',
    description='Retorna uma coleção específica pelo seu identificador único.',
    response_model=ColecaoPublic,
)
async def read_colecao_by_id(id_colecao: str):
    try:
        obj_id = validate_object_id(id_colecao)

        db = await get_mongo()
        colecoes_collection = db.colecoes
        generos_collection = db.generos

        colecao = await colecoes_collection.find_one({'_id': obj_id})
        if not colecao:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'A coleção de ID {id_colecao} não foi encontrada.',
            )

        # Buscar gêneros associados a esta coleção
        generos_ids = colecao.get('generos_ids', [])
        generos_data = []

        if generos_ids:
            generos_cursor = generos_collection.find({
                '_id': {'$in': [ObjectId(gid) for gid in generos_ids if ObjectId.is_valid(gid)]}
            })
            generos = await generos_cursor.to_list(length=None)

            for genero in generos:
                generos_data.append({
                    'id_genero': str(genero['_id']),
                    'nome': genero['nome'],
                    'surgiu_em': genero['surgiu_em'],
                })

        return ColecaoPublic(
            id_colecao=str(colecao['_id']),
            titulo=colecao['titulo'],
            tipo=colecao['tipo'],
            duracao=colecao['duracao'],
            caminho_capa=colecao['caminho_capa'],
            data_lancamento=colecao['data_lancamento'],
            generos=generos_data,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.put(
    '/{id_colecao}',
    summary='Atualizar coleção totalmente',
    description='Substitui todos os campos da coleção especificada pelo corpo enviado.',
    response_model=ColecaoPublic,
)
async def update_colecao(id_colecao: str, colecao_schema: ColecaoSchema):
    try:
        obj_id = validate_object_id(id_colecao)

        db = await get_mongo()
        collection = db.colecoes

        # Verifica se a coleção existe
        colecao = await collection.find_one({'_id': obj_id})
        if not colecao:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'A coleção de ID {id_colecao} não foi encontrada.',
            )

        # Atualiza o documento
        update_data = colecao_schema.model_dump()
        update_data['data_lancamento'] = update_data['data_lancamento'].isoformat()
        update_data['tipo'] = update_data['tipo'].value

        await collection.update_one({'_id': obj_id}, {'$set': update_data})

        # Busca o documento atualizado
        updated_colecao = await collection.find_one({'_id': obj_id})

        return ColecaoPublic(
            id_colecao=str(updated_colecao['_id']),
            titulo=updated_colecao['titulo'],
            tipo=updated_colecao['tipo'],
            duracao=updated_colecao['duracao'],
            caminho_capa=updated_colecao['caminho_capa'],
            data_lancamento=updated_colecao['data_lancamento'],
            generos=[],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.patch(
    '/{id_colecao}',
    summary='Atualizar coleção parcialmente',
    description='Atualiza apenas os campos enviados no corpo da requisição.',
    response_model=ColecaoPublic,
)
async def patch_colecao(id_colecao: str, colecao_schema: ColecaoUpdateSchema):
    try:
        obj_id = validate_object_id(id_colecao)

        db = await get_mongo()
        collection = db.colecoes

        # Verifica se a coleção existe
        colecao = await collection.find_one({'_id': obj_id})
        if not colecao:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'A coleção de ID {id_colecao} não foi encontrada.',
            )

        # Prepara dados para atualização (apenas campos não nulos)
        update_data = colecao_schema.model_dump(exclude_unset=True)

        if not update_data:
            # Se não há dados para atualizar, retorna a coleção atual
            return ColecaoPublic(
                id_colecao=str(colecao['_id']),
                titulo=colecao['titulo'],
                tipo=colecao['tipo'],
                duracao=colecao['duracao'],
                caminho_capa=colecao['caminho_capa'],
                data_lancamento=colecao['data_lancamento'],
                generos=[],
            )

        # Converte campos especiais se presentes
        if 'data_lancamento' in update_data:
            update_data['data_lancamento'] = update_data['data_lancamento'].isoformat()
        if 'tipo' in update_data:
            update_data['tipo'] = update_data['tipo'].value

        # Atualiza o documento
        await collection.update_one({'_id': obj_id}, {'$set': update_data})

        # Busca o documento atualizado
        updated_colecao = await collection.find_one({'_id': obj_id})

        return ColecaoPublic(
            id_colecao=str(updated_colecao['_id']),
            titulo=updated_colecao['titulo'],
            tipo=updated_colecao['tipo'],
            duracao=updated_colecao['duracao'],
            caminho_capa=updated_colecao['caminho_capa'],
            data_lancamento=updated_colecao['data_lancamento'],
            generos=[],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.delete(
    '/{id_colecao}',
    summary='Deletar coleção',
    description='Remove uma coleção pelo seu identificador único.',
    response_model=Mensagem,
)
async def delete_colecao(id_colecao: str):
    try:
        obj_id = validate_object_id(id_colecao)

        db = await get_mongo()
        collection = db.colecoes

        # Verifica se a coleção existe
        colecao = await collection.find_one({'_id': obj_id})
        if not colecao:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'A coleção de ID {id_colecao} não foi encontrada.',
            )

        # Remove a coleção
        await collection.delete_one({'_id': obj_id})

        return Mensagem(mensagem='Coleção deletada com sucesso.')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.post(
    '/{id_colecao}/generos/{id_genero}',
    summary='Associar gênero a uma coleção',
    description='Adiciona um gênero a uma coleção específica.',
    response_model=Mensagem,
)
async def add_genero_to_colecao(id_colecao: str, id_genero: str):
    try:
        colecao_obj_id = validate_object_id(id_colecao)
        genero_obj_id = validate_object_id(id_genero)

        db = await get_mongo()
        colecoes_collection = db.colecoes
        generos_collection = db.generos

        # Buscar a coleção
        colecao = await colecoes_collection.find_one({'_id': colecao_obj_id})
        if not colecao:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'A coleção de ID {id_colecao} não foi encontrada.',
            )

        # Buscar o gênero
        genero = await generos_collection.find_one({'_id': genero_obj_id})
        if not genero:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'O gênero de ID {id_genero} não foi encontrado.',
            )

        # Verificar se a associação já existe
        current_generos = colecao.get('generos_ids', [])
        if id_genero in current_generos:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=(f'O gênero "{genero["nome"]}" já está associado à coleção "{colecao["titulo"]}".'),
            )

        # Adicionar o gênero à coleção
        await colecoes_collection.update_one(
            {'_id': colecao_obj_id}, {'$addToSet': {'generos_ids': id_genero}}
        )

        return Mensagem(
            mensagem=(f'Gênero "{genero["nome"]}" associado à coleção "{colecao["titulo"]}" com sucesso.')
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.delete(
    '/{id_colecao}/generos/{id_genero}',
    summary='Desassociar gênero de uma coleção',
    description='Remove um gênero de uma coleção específica.',
    response_model=Mensagem,
)
async def remove_genero_from_colecao(id_colecao: str, id_genero: str):
    try:
        colecao_obj_id = validate_object_id(id_colecao)
        genero_obj_id = validate_object_id(id_genero)

        db = await get_mongo()
        colecoes_collection = db.colecoes
        generos_collection = db.generos

        # Buscar a coleção
        colecao = await colecoes_collection.find_one({'_id': colecao_obj_id})
        if not colecao:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'A coleção de ID {id_colecao} não foi encontrada.',
            )

        # Buscar o gênero
        genero = await generos_collection.find_one({'_id': genero_obj_id})
        if not genero:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'O gênero de ID {id_genero} não foi encontrado.',
            )

        # Verificar se a associação existe
        current_generos = colecao.get('generos_ids', [])
        if id_genero not in current_generos:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=(f'O gênero "{genero["nome"]}" não está associado à coleção "{colecao["titulo"]}".'),
            )

        # Remover o gênero da coleção
        await colecoes_collection.update_one({'_id': colecao_obj_id}, {'$pull': {'generos_ids': id_genero}})

        return Mensagem(
            mensagem=(f'Gênero "{genero["nome"]}" desassociado da coleção "{colecao["titulo"]}" com sucesso.')
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.get(
    '/{id_colecao}/generos',
    summary='Listar gêneros de uma coleção',
    description='Retorna todos os gêneros associados a uma coleção específica.',
    response_model=dict,
)
async def get_generos_from_colecao(id_colecao: str):
    try:
        obj_id = validate_object_id(id_colecao)

        db = await get_mongo()
        colecoes_collection = db.colecoes
        generos_collection = db.generos

        # Buscar a coleção
        colecao = await colecoes_collection.find_one({'_id': obj_id})
        if not colecao:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'A coleção de ID {id_colecao} não foi encontrada.',
            )

        # Buscar gêneros associados
        generos_ids = colecao.get('generos_ids', [])
        generos_data = []

        if generos_ids:
            generos_cursor = generos_collection.find({
                '_id': {'$in': [ObjectId(gid) for gid in generos_ids if ObjectId.is_valid(gid)]}
            })
            generos = await generos_cursor.to_list(length=None)

            for genero in generos:
                generos_data.append({
                    'id_genero': str(genero['_id']),
                    'nome': genero['nome'],
                    'surgiu_em': genero['surgiu_em'],
                })

        return {
            'colecao': {'id_colecao': str(colecao['_id']), 'titulo': colecao['titulo']},
            'generos': generos_data,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )


@router.put(
    '/{id_colecao}/generos',
    summary='Definir gêneros de uma coleção',
    description='Substitui todos os gêneros de uma coleção pelos IDs fornecidos.',
    response_model=Mensagem,
)
async def set_generos_to_colecao(id_colecao: str, generos_ids: list[str]):
    try:
        obj_id = validate_object_id(id_colecao)

        db = await get_mongo()
        colecoes_collection = db.colecoes
        generos_collection = db.generos

        # Buscar a coleção
        colecao = await colecoes_collection.find_one({'_id': obj_id})
        if not colecao:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'A coleção de ID {id_colecao} não foi encontrada.',
            )

        # Validar todos os IDs de gêneros
        generos_obj_ids = []
        for gid in generos_ids:
            try:
                generos_obj_ids.append(validate_object_id(gid))
            except HTTPException:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f'ID de gênero inválido: {gid}',
                )

        # Buscar todos os gêneros pelos IDs
        generos_cursor = generos_collection.find({'_id': {'$in': generos_obj_ids}})
        generos = await generos_cursor.to_list(length=None)

        # Verificar se todos os gêneros foram encontrados
        if len(generos) != len(generos_ids):
            generos_encontrados = [str(g['_id']) for g in generos]
            generos_nao_encontrados = [gid for gid in generos_ids if gid not in generos_encontrados]
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Gêneros não encontrados: {generos_nao_encontrados}',
            )

        # Substituir todos os gêneros da coleção
        await colecoes_collection.update_one({'_id': obj_id}, {'$set': {'generos_ids': generos_ids}})

        generos_nomes = [g['nome'] for g in generos]
        return Mensagem(
            mensagem=(f'Gêneros da coleção "{colecao["titulo"]}" definidos como: {", ".join(generos_nomes)}')
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {str(e)}',
        )
