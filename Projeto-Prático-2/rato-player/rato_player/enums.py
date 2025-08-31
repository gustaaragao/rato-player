from enum import Enum


class TipoColecaoEnum(str, Enum):
    Album = 'Album'
    EP = 'EP'
    Single = 'Single'
    Compilacao = 'Compilacao'
