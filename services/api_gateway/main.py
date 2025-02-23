from fastapi import FastAPI
from src.routes import process
from src.config import Config

# Initialize configuration
Config.set_config()
app = FastAPI(title="YouTube Summarization API Gateway")

# Include all routers
app.include_router(process.router, prefix="/process", tags=["Processing"])