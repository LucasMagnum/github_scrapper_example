import functools

from aiohttp import web

import config
from db import close_db, init_db
from repositories import Repository, User


async def search_handler(request, repository_class):
    repository = repository_class(db=request.app["db"])
    data = await repository.search(query=request.query)

    return web.json_response(data)


def init_app(config):
    app = web.Application()
    app["config"] = config

    app.add_routes(
        [
            web.get(
                "/users/_search",
                functools.partial(search_handler, repository_class=User),
            ),
            web.get(
                "/repositories/_search",
                functools.partial(search_handler, repository_class=Repository),
            ),
        ]
    )

    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    return app


if __name__ == "__main__":
    app = init_app(config)
    web.run_app(app, port=8002)
