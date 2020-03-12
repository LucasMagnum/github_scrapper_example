import asyncio

from aiohttp import ClientSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from db import init_db
from repositories import Repository, User


async def scrap_github(repository: Repository, user: User):
    print("Collecting data...")
    latest_repo = await repository.get_latest_by_external_id()

    since = latest_repo["id"] if latest_repo else 0
    url = config.GITHUB_API_URL.format(since=since)

    async with ClientSession() as session:
        response = await fetch_data(url, session)

        for repo in response:
            owner = await user.get_or_create(
                external_id=repo["owner"]["id"], name=repo["owner"]["login"]
            )

            # Extract language from
            languages = await fetch_data(repo["languages_url"], session)
            languages = ", ".join(languages)

            await repository.get_or_create(
                external_id=repo["id"],
                name=repo["full_name"],
                languages=languages,
                owner_id=owner.id,
            )

    # Waiting a bit to avoid too much requests
    print("Waiting 1 second before next request")
    await asyncio.sleep(1)


async def fetch_data(url, session):
    async with session.get(url) as response:
        if response.status == 403:
            raise ValueError("API limit exceeded")
        return await response.json()


if __name__ == "__main__":
    engine = create_engine(config.DB_URL)
    session = sessionmaker(bind=engine)()

    repository = Repository(session)
    user = User(session)

    asyncio.run(scrap_github(repository, user))
