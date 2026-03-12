import asyncio
import os
import sys
from contextlib import asynccontextmanager

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

import uvicorn

from src.app import create_app
from src.core.db import init_models


@asynccontextmanager
async def lifespan(app):
    await init_models()
    yield


app = create_app()


async def run() -> None:
    config = uvicorn.Config(
        "src.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )
    server = uvicorn.Server(config=config)
    tasks = (asyncio.create_task(server.serve()),)

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
