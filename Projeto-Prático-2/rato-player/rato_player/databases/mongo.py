from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from rato_player.settings import Settings

settings = Settings()

# URL para conexão local do MongoDB
MONGODB_URL = f'mongodb://{settings.MONGODB_USER}:{settings.MONGODB_PASSWORD}@{settings.MONGODB_HOST}:{settings.MONGODB_PORT}/'

DB_NAME = settings.MONGODB_DB_NAME


async def get_mongo():
    client: AsyncIOMotorClient = None
    if client is None:
        try:
            client = AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
            # Testa a conexão
            await client.admin.command('ping')
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            raise e

    return client[DB_NAME]
