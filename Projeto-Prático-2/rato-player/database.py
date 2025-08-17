from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from settings import Settings

DATABASE_URL = (
    f"postgresql+psycopg2://{Settings().POSTGRES_USER}:"
    f"{Settings().POSTGRES_PASSWORD}@{Settings().POSTGRES_HOST}:"
    f"{Settings().POSTGRES_PORT}/{Settings().POSTGRES_DB_NAME}"
)

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session