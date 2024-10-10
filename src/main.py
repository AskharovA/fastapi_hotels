from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

import logging
import sys
from pathlib import Path

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.DEBUG)

from src.api.auth import router as router_users  # noqa: E402
from src.api.hotels import router as router_hotels  # noqa: E402
from src.api.rooms import router as router_rooms  # noqa: E402
from src.api.bookings import router as router_bookings  # noqa: E402
from src.api.facilities import router as router_facilities  # noqa: E402
from src.init import redis_manager  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0")
