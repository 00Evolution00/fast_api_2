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
    # Initialize database models
    await init_models()
    
    # Create logs directory
    os.makedirs('/app/logs', exist_ok=True)
    
    yield


app = create_app()


# Add health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Docker."""
    return {"status": "healthy", "service": "fastapi-backend"}


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
