
from motor.motor_asyncio import AsyncIOMotorClient
from settings import Settings

settings = Settings()

MONGODB_URL = (
    f"mongodb://{settings.MONGODB_USER}:{settings.MONGODB_PASSWORD}" 
    f"@{settings.MONGODB_HOST}:{settings.MONGODB_PORT}/?authSource={settings.MONGODB_DB_NAME}"
)

client = AsyncIOMotorClient(MONGODB_URL)
db = client[settings.MONGODB_DB_NAME]

def get_mongodb():
    return db