import logging
import redis.asyncio as redis


class RedisManager:
    redis_: redis.Redis

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def connect(self):
        logging.info("Connecting to Redis...")
        self.redis_ = await redis.Redis(host=self.host, port=self.port)
        logging.info("Successfully connected to Redis")

    async def set(self, key: str, value: str, expire: int = 0):
        if expire:
            await self.redis_.set(key, value, ex=expire)
        else:
            await self.redis_.set(key, value)

    async def get(self, key: str):
        return await self.redis_.get(key)

    async def delete(self, key: str):
        await self.redis_.delete(key)

    async def close(self):
        if self.redis_:
            await self.redis_.close()
