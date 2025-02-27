from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import pika, json, time
from src.config import Config
import asyncio

router = APIRouter()
active_connections = {}

async def broadcast_notification(message: str, msg_task_id: str):
    """Send a notification to all connected clients"""
    disconnected_clients = set()
    # wait for active connection
    while len(active_connections) <= 0:    
        await asyncio.sleep(0.1)

    for task_id ,connection in active_connections.items():
        try:
            if task_id == msg_task_id:
                await connection.send_text(message)
        except:
            disconnected_clients.add(connection)
    
    # Remove disconnected clients
    for client in disconnected_clients:
        active_connections.remove(client)

def rabbitmq_consumer():
    """RabbitMQ Consumer: Listens for messages and sends them to WebSocket."""
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.get_corpus("rabbitmq", "host")))
    channel = connection.channel()
    channel.queue_declare(queue=Config.get_corpus("rabbitmq", "status_queue"), durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode("utf-8"))
        msg_task_id, progress_msg = message['video_id'], message['status']  # Extract task_id from message
        time.sleep(1)
        asyncio.run(broadcast_notification(progress_msg, msg_task_id))  # Send to WebSocket clients
        
    channel.basic_consume(queue=Config.get_corpus("rabbitmq", "status_queue"), on_message_callback=callback, auto_ack=True)
    
    try:
        channel.start_consuming()  # Keep consuming messages in a separate thread
    except Exception:
        channel.stop_consuming()
    finally:
        connection.close()
    


@router.websocket("/status/{task_id}")
async def process_video(websocket: WebSocket, task_id: str):
    await websocket.accept()
    active_connections[task_id] = websocket
    try:
        while True:
            await websocket.receive_text()  # Keep WebSocket open
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for task: {task_id}")
    finally:
        active_connections.pop(task_id, None) 
    
    print(active_connections)



