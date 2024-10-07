import json
from functools import wraps
from src.init import redis_manager


def custom_cache_decorator(expire=5):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = (
                func.__name__
                + ":"
                + repr({k: v for k, v in kwargs.items() if k != "db"})
            )

            result = await redis_manager.get(key)
            if result:
                return json.loads(result)

            print("ИДУ В БАЗУ ДАННЫХ!")
            result = await func(*args, **kwargs)

            if isinstance(result, (list, tuple)):
                data = [f.model_dump() for f in result]
            else:
                data = result.model_dump()

            await redis_manager.set(key, json.dumps(data), expire=expire)
            return result

        return wrapper

    return decorator
