from fastapi import FastAPI

from rato_player.routers import colecoes_postgres, generos_postgres

app = FastAPI()

app.include_router(colecoes_postgres.router)
app.include_router(generos_postgres.router)


@app.get('/')
def read_root():
    return {'message': 'Hello World'}
