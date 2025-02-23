import pika
from src.config import Config

def send_to_queue(queue_name, message):
    """Send a message to RabbitMQ"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.get_corpus("rabbitmq", "host")))
    channel = connection.channel()
    # channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    connection.close()