from fastapi import FastAPI

from rato_player.routers import (
    colecoes_mongo,
    colecoes_postgres,
    generos_mongo,
    generos_postgres,
)

app = FastAPI(
    title='Rato Player API',
    description='API para gerenciamento de coleções musicais.',
    version='1.0.0',
)

# Routers PostgreSQL
app.include_router(colecoes_postgres.router)
app.include_router(generos_postgres.router)

# Routers MongoDB
app.include_router(colecoes_mongo.router)
app.include_router(generos_mongo.router)
