import json
from aioredis import from_url, Redis
from dependency_injector import containers, providers, wiring
from fastapi import Depends, HTTPException
from functools import wraps
from pydantic import BaseModel
from typing import AsyncIterator
import aioredis
import asyncio

async def init_redis_pool(host: str, password: str) -> AsyncIterator[Redis]:
    session = from_url(host, password={password}, encoding="utf-8", decode_responses=True, port=17558)

    yield session
    session.close()
    await session.wait_closed()

class Service:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def process(self, channel_name: str, message: str) -> str:
        try:
            await self._redis.publish(channel_name, message)
        except aioredis.RedisError:
            raise HTTPException(status_code=503, detail="Failed to connect to Redis, please try again later.")

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    redis_pool = providers.Resource(
        init_redis_pool,
        host=config.redis_host,
        password=config.redis_password,
    )

    service = providers.Factory(
        Service,
        redis=redis_pool,
    )

@wiring.inject
async def send_msj(message, service: Service = Depends(wiring.Provide[Container.service])):
    await service.process("crud", json.dumps(message))

def notify_redis_clients(action, masterdata_name):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result: BaseModel = func(*args, **kwargs)
            print(action)
            print(masterdata_name)
            #To-do: check permissions.
            message = {
                "type": action,
                "masterdata_name": masterdata_name,
                "performed_by": kwargs.get('updated_by', 'Unknown'),  # Ensure updated_by is provided or default
                "item": result.model_dump_json()
            }
            asyncio.create_task(send_msj(message=message))
            return message
        return wrapper
    return decorator