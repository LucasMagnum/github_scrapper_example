import datetime

import pytest

from repositories import Repository, User


@pytest.fixture
def user(dbsession):
    return User(dbsession)


@pytest.fixture
def repository(dbsession):
    return Repository(dbsession)


@pytest.mark.asyncio
async def test_user_should_not_create_duplicate_user_with_same_external_id(user):
    first_user = await user.get_or_create(external_id=1, name="Lucas")
    second_user = await user.get_or_create(external_id=1, name="Lucas Magnum")
    assert first_user.id == second_user.id


@pytest.mark.asyncio
async def test_user_search_should_return_all_data_when_filters_are_not_given(user):
    results = await user.search({})
    assert not results

    await user.get_or_create(external_id=1, name="New user")

    results = await user.search({})
    assert results[0]["id"] == 1
    assert results[0]["name"] == "New user"


@pytest.mark.asyncio
async def test_user_search_by_name_should_return_matching_users(user):
    await user.get_or_create(external_id=1, name="First user")
    await user.get_or_create(external_id=2, name="Second user")

    assert len(await user.search({})) == 2
    assert len(await user.search({"name": "first"})) == 1
    assert len(await user.search({"name": "second"})) == 1


@pytest.mark.asyncio
async def test_user_should_ignore_invalid_filters(user):
    await user.get_or_create(external_id=1, name="First user")
    await user.get_or_create(external_id=2, name="Second user")

    assert len(await user.search({})) == 2
    assert len(await user.search({"invalid_name": "first"})) == 2
    assert len(await user.search({"name": None})) == 2


@pytest.mark.asyncio
async def test_repository_should_not_create_duplicate_repo_with_same_external_id(
    repository, user
):
    user = await user.get_or_create(external_id=1, name="owner")

    first_repo = await repository.get_or_create(
        name="repos/repo_01", languages="Python", owner_id=user.id, external_id=1
    )

    second_repo = await repository.get_or_create(
        name="repos/repo_02", languages="Python", owner_id=user.id, external_id=1
    )

    assert first_repo.id == second_repo.id


@pytest.mark.asyncio
async def test_repository_search_should_return_all_data_when_filters_are_not_given(
    repository, user
):
    results = await repository.search({})
    assert not results

    user = await user.get_or_create(external_id=1, name="owner")
    await repository.get_or_create(
        name="repos/repo_01", languages="Python", owner_id=user.id, external_id=1
    )

    results = await repository.search({})
    response = results[0]

    assert response["id"] == 1
    assert response["name"] == "repos/repo_01"
    assert response["languages"] == "Python"


@pytest.mark.asyncio
async def test_repository_search_by_name_should_return_matching_repos(repository, user):
    user = await user.get_or_create(external_id=1, name="owner")

    await repository.get_or_create(
        name="repos/repo_01", languages="Python", owner_id=user.id, external_id=1
    )
    await repository.get_or_create(
        name="repos/repo_02", languages="Ruby", owner_id=user.id, external_id=2
    )

    assert len(await repository.search({})) == 2
    assert len(await repository.search({"name": "repo_01"})) == 1
    assert len(await repository.search({"name": "repo_02"})) == 1


@pytest.mark.asyncio
async def test_repository_search_by_name_should_ignore_invalid_filters(
    repository, user
):
    user = await user.get_or_create(external_id=1, name="owner")
    await repository.get_or_create(
        name="repos/repo_01", languages="Python", owner_id=user.id, external_id=1
    )
    await repository.get_or_create(
        name="repos/repo_02", languages="Ruby", owner_id=user.id, external_id=2
    )

    assert len(await repository.search({})) == 2
    assert len(await repository.search({"invalid": "repo_01"})) == 2
    assert len(await repository.search({"name": ""})) == 2


@pytest.mark.asyncio
async def test_repository_search_by_name_languages_and_owner(repository, user):
    user_01 = await user.get_or_create(external_id=1, name="owner")
    user_02 = await user.get_or_create(external_id=2, name="second owner")

    await repository.get_or_create(
        name="repos/repo_01", languages="Python", owner_id=user_01.id, external_id=1
    )
    await repository.get_or_create(
        name="repos/repo_02", languages="Ruby", owner_id=user_02.id, external_id=2
    )
    await repository.get_or_create(
        name="repos/repo_03", languages="Golang", owner_id=user_01.id, external_id=3
    )

    assert len(await repository.search({})) == 3
    assert len(await repository.search({"author": "second owner"})) == 1
    assert len(await repository.search({"languages": "golang"})) == 1
    assert len(await repository.search({"name": "repo_01", "languages": "python"})) == 1
    assert len(await repository.search({"author": "owner", "languages": "python"})) == 1

    results = await repository.search({"author": "second owner"})
    response = results[0]

    assert response["id"] == 2
    assert response["name"] == "repos/repo_02"
    assert response["languages"] == "Ruby"
    assert response["owner"]["name"] == "second owner"


@pytest.mark.asyncio
async def test_repository_get_latest_by_external_id_return_correct_repo(
    repository, user
):
    user_01 = await user.get_or_create(external_id=1, name="owner")

    await repository.get_or_create(
        name="repos/repo_01", languages="Python", owner_id=user_01.id, external_id=7
    )
    await repository.get_or_create(
        name="repos/repo_02", languages="Ruby", owner_id=user_01.id, external_id=2
    )
    await repository.get_or_create(
        name="repos/repo_03", languages="Python", owner_id=user_01.id, external_id=1
    )
    await repository.get_or_create(
        name="repos/repo_04", languages="Python", owner_id=user_01.id, external_id=5
    )

    response = await repository.get_latest_by_external_id()

    assert response["external_id"] == 7
    assert response["name"] == "repos/repo_01"
