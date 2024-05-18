from auth import authRouter
from auth.auth_middleware import AuthMiddleware
from crud import crudRouter
from dependencies.socket import app_with_socket, connect_to_channel
from fastapi import WebSocket

app = app_with_socket

@app.on_event("startup")
async def on_startup():
    from dependencies.database import init_db
    init_db()

app.add_middleware(AuthMiddleware)
app.include_router(authRouter)
app.include_router(crudRouter)
"""to-do: move to its own router, it will probably require arch changes."""
@app.websocket("/ws/{channel_name}")
async def websocket_endpoint(websocket: WebSocket, channel_name: str):
    await websocket.accept()
    await connect_to_channel(websocket, channel_name)