from fastapi import FastAPI

from rato_player.routers import colecoes, generos

app = FastAPI()

app.include_router(colecoes.router)
app.include_router(generos.router)


@app.get('/')
def read_root():
    return {'message': 'Hello World'}