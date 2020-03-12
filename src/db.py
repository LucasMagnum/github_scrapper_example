from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, nullable=False, unique=True)

    name = Column(String(255), nullable=False)
    imported_at = Column("imported_at", DateTime, nullable=False)

    def __repr__(self):
        return f"<User(name={self.name})>"


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, nullable=False, unique=True)

    name = Column(String(255), nullable=False)
    languages = Column(String(50), nullable=False)
    imported_at = Column(DateTime, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User")

    def __repr__(self):
        return f"<Repository(name={self.name})>"


async def init_db(app):
    engine = create_engine(app["config"].DB_URL)
    session = sessionmaker(bind=engine)
    app["db"] = session()


async def close_db(app):
    app["db"].close()
