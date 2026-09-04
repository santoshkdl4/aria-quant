from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection established. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        # Broadcast standard JSON events to all connected clients
        text = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(text)
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {e}")
                
manager = ConnectionManager()

@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive commands from terminal
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                
                # Acknowledge receipt
                await manager.broadcast({
                    "type": "terminal_response",
                    "sender": "aria",
                    "text": f"Command received: \"{msg.get('text', '')}\". I am routing this request to the agent pipeline."
                })
                
                # In the future, this is where we would trigger actual agent tasks or trade executions
            except json.JSONDecodeError:
                logger.warning("Received invalid JSON from WebSocket client")
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
