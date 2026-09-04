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
                
from app.research.agent import execute_agent_query

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
                command_text = msg.get('text', '')
                
                # Acknowledge receipt
                await manager.broadcast({
                    "type": "terminal_response",
                    "sender": "aria",
                    "text": f"Analyzing request: \"{command_text}\". Running strategy agent pipeline..."
                })
                
                # Trigger Agent Pipeline
                agent_result = await execute_agent_query(command_text)
                
                if agent_result["status"] == "success":
                    await manager.broadcast({
                        "type": "terminal_response",
                        "sender": "aria",
                        "text": f"Backtest Complete.\nWin Rate: {agent_result['metrics']['win_rate']:.2%}\nReturn: {agent_result['metrics']['total_return']:.2%}\nSharpe: {agent_result['metrics']['sharpe_ratio']:.2f}"
                    })
                    await manager.broadcast({
                        "type": "agent_code",
                        "code": agent_result['code']
                    })
                    await manager.broadcast({
                        "type": "backtest_metrics",
                        "metrics": agent_result['metrics']
                    })
                else:
                    await manager.broadcast({
                        "type": "terminal_response",
                        "sender": "aria",
                        "text": f"Agent failed: {agent_result['message']}"
                    })
                    
            except json.JSONDecodeError:
                logger.warning("Received invalid JSON from WebSocket client")
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
