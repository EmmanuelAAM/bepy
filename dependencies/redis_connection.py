import aioredis
from fastapi import HTTPException
from core.config import settings

class RedisSession:
    def __init__(self) -> None:
        self.session_local = aioredis.Redis(host=settings.redis_host, password={settings.redis_password}, encoding="utf-8", decode_responses=True, port=17558)
        self.redis_pool = aioredis.ConnectionPool(connection_class=[self.session_local], port=6379, db=0)
        
    def process_message(self, channel_name: str, message: str):
        try:
            print(message)
            print('Sending msj')
            return self.session_local.publish(channel_name, message)
        except aioredis.RedisError:
            raise HTTPException(status_code=503, detail="Failed to connect to Redis, please try again later.")

# The `get_redis` function is a generator function that is used to provide a database session to
# the caller and ensure that the session is properly closed after its use. Here is a breakdown of
# what the function is doing:
def get_redis():
    redis = RedisSession()
    try:
        # yield is a keyword used in a function like a return statement but it returns a generator. 
        # A generator is an iterator, a kind of iterable you can only iterate over once.
        # In this case, the yield db statement is used within a generator function get_db(). 
        # This function is designed to provide a database session (db) to the caller and ensure that the session is properly closed after its use, even if an error occurs. 
        # This pattern is particularly useful in web applications where you want to ensure that resources like database connections are properly managed and released after use.
        yield redis
    finally:
        redis.close()