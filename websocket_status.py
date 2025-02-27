import asyncio
import websockets

async def receive_updates(task_id):
    """Connect to WebSocket and receive progress updates."""
    uri = f"ws://localhost:8000/ws/status/{task_id}"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to WebSocket for Task ID: {task_id}")

            while True:
                message = await websocket.recv()
                print(f"Received: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    task_id = input("Enter Task ID: ")  # Enter the task ID received from /start_ocr/
    asyncio.run(receive_updates(task_id))
