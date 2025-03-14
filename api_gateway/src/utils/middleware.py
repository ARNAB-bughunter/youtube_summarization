from fastapi import Request, HTTPException
import time

rate_limit_record = {}

async def rate_limitting(request: Request):
    client_ip = request.client.host
    currenttime = time.time()
    if client_ip in rate_limit_record and currenttime - rate_limit_record[client_ip] < 120:
        raise HTTPException(status_code=429, detail="Rate Limit Exceeded")
    
    rate_limit_record[client_ip] = currenttime