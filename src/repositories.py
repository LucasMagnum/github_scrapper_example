import datetime

from sqlalchemy.sql.expression import func

from db import Repository as RepositoryTable
from db import User as UserTable


class User:
    """
    A user interface that interacts direct with the database.
    """

    def __init__(self, db):
        self.db = db
        self.table = UserTable

    async def search(self, query: dict):
        queryset = await self.apply_filters(query)
        return queryset

    async def apply_filters(self, query: dict):
        queryset = self.db.query(self.table)

        if name := query.get("name"):
            queryset = queryset.filter(self.table.name.ilike(f"%{name}%"))

        return [self.serialize(obj) for obj in queryset.all()]

    async def get_or_create(self, external_id: int, name: str):
        queryset = self.db.query(self.table)
        if found := queryset.filter(self.table.external_id == external_id).all():
            return found[0]

        user = self.table(
            external_id=external_id, name=name, imported_at=datetime.datetime.now()
        )

        self.db.add(user)
        self.db.commit()

        return user

    def serialize(self, user_obj: UserTable):
        return {
            "id": user_obj.id,
            "name": user_obj.name,
            "imported_at": user_obj.imported_at.isoformat(),
        }


class Repository:
    """
    A repository interface that interacts directly with the database.
    """

    def __init__(self, db):
        self.db = db
        self.table = RepositoryTable

    async def search(self, query: dict):
        queryset = await self.apply_filters(query)
        return queryset

    async def apply_filters(self, query: dict):
        queryset = self.db.query(self.table)

        if name := query.get("name"):
            queryset = queryset.filter(self.table.name.ilike(f"%{name}%"))

        if languages := query.get("languages"):
            queryset = queryset.filter(self.table.languages.ilike(f"%{languages}%"))

        if author := query.get("author"):
            queryset = queryset.join(self.table.owner).filter(UserTable.name == author)

        return [self.serialize(obj) for obj in queryset.all()]

    async def get_or_create(
        self, external_id: int, name: str, languages: str, owner_id: int
    ):
        queryset = self.db.query(self.table)
        if found := queryset.filter(self.table.external_id == external_id).all():
            return found[0]

        repo = self.table(
            name=name,
            languages=languages,
            owner_id=owner_id,
            external_id=external_id,
            imported_at=datetime.datetime.now(),
        )

        self.db.add(repo)
        self.db.commit()

        return repo

    async def get_latest_by_external_id(self):
        max_external_id = self.db.query(func.max(self.table.external_id)).scalar()

        if max_external_id:
            obj = (
                self.db.query(self.table)
                .filter(self.table.external_id == max_external_id)
                .scalar()
            )
            return self.serialize(obj)

        return

    def serialize(self, repo: RepositoryTable):
        return {
            "id": repo.id,
            "name": repo.name,
            "languages": repo.languages,
            "external_id": repo.external_id,
            "owner": {"id": repo.owner.id, "name": repo.owner.name},
            "imported_at": repo.imported_at.isoformat(),
        }
