import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import DB_URL
from src.db import Base, Repository, User


def create_tables(engine):
    Base.metadata.create_all(engine)


def sample_data(engine):
    session = sessionmaker(bind=engine)()
    session.add_all(
        [
            User(
                external_id=1, name="Owner First", imported_at=datetime.datetime.now()
            ),
            User(
                external_id=2, name="Owner second", imported_at=datetime.datetime.now()
            ),
            User(
                external_id=3, name="owner THIRD", imported_at=datetime.datetime.now()
            ),
        ]
    )

    session.add_all(
        [
            Repository(
                external_id=1,
                name="repos/repo",
                owner_id=1,
                languages="python",
                imported_at=datetime.datetime.now(),
            ),
            Repository(
                external_id=2,
                name="repos/repo_2",
                owner_id=2,
                languages="ruby",
                imported_at=datetime.datetime.now(),
            ),
            Repository(
                external_id=3,
                name="repos/repo_3",
                owner_id=3,
                languages="golang",
                imported_at=datetime.datetime.now(),
            ),
        ]
    )
    session.commit()
    session.close()


if __name__ == "__main__":
    engine = create_engine(DB_URL)

    create_tables(engine)
    sample_data(engine)
