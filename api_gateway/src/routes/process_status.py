from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import pika, json, time
from src.config import Config
import asyncio

router = APIRouter()
active_connections = {}

async def broadcast_notification(progress: str, summary: str, msg_task_id: str, thumbnail_url: str):
    """Send a notification to all connected clients"""
    disconnected_clients = set()
    # wait for active connection
    while len(active_connections) <= 0:    
        await asyncio.sleep(0.1)
    
    final_message = json.dumps({"progress": progress, "summary": summary, "thumbnail_url": thumbnail_url})

    for task_id ,connection in active_connections.items():
        try:
            if task_id == msg_task_id:
                await connection.send_text(final_message)
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
        print(f"Received message: {message}")
        msg_task_id, progress, summary, thumbnail_url = message['video_id'], message['progress'], message['summary'], message['thumbnail_url']
        time.sleep(1)
        if msg_task_id in active_connections:
            asyncio.run(broadcast_notification(progress, summary, msg_task_id, thumbnail_url))  # Send to WebSocket clients
            ch.basic_ack(method.delivery_tag)  # Acknowledge successful processing
        else:
            ch.basic_nack(method.delivery_tag, requeue=True)  # Requeue if client is offline
        
    channel.basic_consume(queue=Config.get_corpus("rabbitmq", "status_queue"), on_message_callback=callback, auto_ack=False)
    
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



