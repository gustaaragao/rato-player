from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from settings import Settings

settings = Settings()

POSTGRES_URL = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB_NAME}"
)

engine = create_engine(POSTGRES_URL)

def get_postgres():
    with Session(engine) as session:
        yield session