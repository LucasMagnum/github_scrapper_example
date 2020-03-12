import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api import init_app
from db import Base, init_db


class Config:
    DB_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
    return create_engine(Config.DB_URL)


@pytest.yield_fixture
def dbsession(engine):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    Base.metadata.create_all(engine)

    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=engine)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
async def api_client(loop, test_client):
    def create_app(loop):
        return init_app(Config, loop)

    return loop.run_until_complete(test_client(create_app))
