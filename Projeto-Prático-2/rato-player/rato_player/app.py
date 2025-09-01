from fastapi import FastAPI

from rato_player.routers import (
    colecoes_mongo,
    colecoes_postgres,
    generos_mongo,
    generos_postgres,
)

app = FastAPI(
    title='Rato Player API',
    description='API do Aplicativo de Música "Rato Player"',
    version='0.1.0',
)

# Routers PostgreSQL
app.include_router(colecoes_postgres.router)
app.include_router(generos_postgres.router)

# Routers MongoDB
app.include_router(colecoes_mongo.router)
app.include_router(generos_mongo.router)
