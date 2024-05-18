from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from functools import wraps
from pydantic import BaseModel
from typing import Dict, List
import asyncio
import json

app_with_socket = FastAPI()
connected_clients: List[WebSocket] = []

channels: Dict[str, List[WebSocket]] = {}

async def connect_to_channel(websocket: WebSocket, channel_name: str):
    if channel_name not in channels:
        channels[channel_name] = []
    channels[channel_name].append(websocket)
    try:
        while True:
            # Here, we could handle incoming messages or simply keep the connection open
            await websocket.receive_text()
    except WebSocketDisconnect:
        channels[channel_name].remove(websocket)
        if not channels[channel_name]:  # Clean up empty channel
            del channels[channel_name]

async def broadcast_websocket_clients(message: str, channel_name: str="crud"):
    if channel_name in channels:
        disconnected_clients = []
        for websocket in channels[channel_name]:
            try:
                await websocket.send_text(message)
            except WebSocketDisconnect:
                disconnected_clients.append(websocket)
        for websocket in disconnected_clients:
            channels[channel_name].remove(websocket)
        if not channels[channel_name]:  # Clean up empty channel
            del channels[channel_name]

def notify_websocket_clients(action, masterdata_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result: BaseModel = func(*args, **kwargs)
            message = {
                "type": action,
                "masterdata_name": masterdata_name,
                "performed_by": kwargs.get('updated_by', 'Unknown'),  # Ensure updated_by is provided or default
                "item": result.model_dump_json()
            }
            #To-do: check permissions.
            asyncio.create_task(broadcast_websocket_clients(json.dumps(message)))
            return result
        return wrapper
    return decorator