from pydantic import BaseModel


class ColecaoSchema(BaseModel):
    ...

class ColecaoPublic(BaseModel):
    ...

class ColecaoList(BaseModel):
    colecoes: list[ColecaoPublic]