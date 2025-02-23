#!/usr/bin/env python
import pika
import uuid
import json


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


for i in range(1):
    data = {
    "video_url": "https://www.youtube.com/watch?v=_dfLOzuIg2o",
    "video_id": str(uuid.uuid4())
    }



    channel.basic_publish(exchange='',
                        routing_key='video_to_audio_queue',
                        body=json.dumps(data))

    print(" [x] Sent 'Hello World!'")