from fastapi import APIRouter, HTTPException, Depends
import uuid
import json
from src.services.rabbitmq_service import send_to_queue
from src.utils.middleware import rate_limitting

router = APIRouter(dependencies=[Depends(rate_limitting)])

@router.post("/")
async def process_video(youtube_url: str):
    """Start processing a YouTube video"""
    if not youtube_url:
        raise HTTPException(status_code=400, detail="Missing YouTube URL")

    video_id = str(uuid.uuid4())  # Generate unique job ID
    # Send to RabbitMQ queue
    message = json.dumps({"video_url": youtube_url, "video_id": video_id})
    send_to_queue("video_to_audio_queue", message)

    return {"video_id": video_id, "status": "Processing"}
