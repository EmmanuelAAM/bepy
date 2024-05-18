from functools import wraps
import json
from fastapi import Depends
from dependencies.redis_connection import RedisSession, get_redis
from pydantic import BaseModel

def send_msj(message: str, redis: RedisSession):
    print('Send Msj')
    redis.process_message("crud", message)

def notify_redis_clients(action, masterdata_name, redis: RedisSession=Depends(get_redis)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(__name__)
            result: BaseModel = func(*args, **kwargs)
            message = {
                "type": action,
                "masterdata_name": masterdata_name,
                "performed_by": kwargs.get('updated_by', 'Unknown'),  # Ensure updated_by is provided or default
                "item": result.model_dump_json()
            }
            print(json.dumps(message))
            #To-do: check permissions.
            send_msj(message=json.dumps(message), redis= redis)
            return result
        return wrapper
    return decorator