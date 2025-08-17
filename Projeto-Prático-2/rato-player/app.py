from fastapi import FastAPI

from routers import colecoes, generos

app = FastAPI()

app.include_router(colecoes.router)
app.include_router(generos.router)