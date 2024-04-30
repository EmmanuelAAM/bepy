from auth import authRouter
from auth.auth_middleware import AuthMiddleware
from crud import crudRouter
from dependencies.socket import app_with_socket
from dependencies.redis_connection import Container
from core.config import settings

app = app_with_socket
app.add_middleware(AuthMiddleware)
app.include_router(authRouter)
app.include_router(crudRouter)

@app.on_event("startup")
async def on_startup():
    from dependencies.database import init_db
    # from dependencies.redis_connection import init_redis_conection
    init_db()
    # await init_redis_conection()

# @app.on_event("shutdown")
# async def on_shotdown():
#     await app.state.redis.close()
container = Container()
container.config.redis_host.from_value(settings.redis_host)
container.config.redis_password.from_value(settings.redis_password)
container.wire(modules=[__name__])