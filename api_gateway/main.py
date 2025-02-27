from fastapi import FastAPI
from src.routes import process, process_status
from src.config import Config
import threading

# Initialize configuration
Config.set_config()
app = FastAPI(title="YouTube Summarization API Gateway")

# Include all routers
app.include_router(process.router, prefix="/process")
app.include_router(process_status.router, prefix="/ws")




@app.on_event("startup")
def startup_event():
    """Start RabbitMQ listener in a separate thread"""
    threading.Thread(target=process_status.rabbitmq_consumer, daemon=True).start()

