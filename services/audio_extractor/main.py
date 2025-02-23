import json
import logging
import pika
from contextlib import contextmanager
from src.config import Config
from src.extractor import download_audio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize configuration
Config.set_config()

@contextmanager
def rabbitmq_connection():
    """Context manager for RabbitMQ connection."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.get_corpus("rabbitmq", "host"))
    )
    channel = connection.channel()
    try:
        yield channel
    finally:
        connection.close()


def setup_queues(channel):
    """Declare required queues."""
    channel.queue_declare(queue=Config.get_corpus("rabbitmq", "input_queue"), durable=True)
    channel.queue_declare(queue=Config.get_corpus("rabbitmq", "output_queue"), durable=True)


def callback(ch, method, properties, body):
    """Process incoming RabbitMQ messages."""
    try:
        data = json.loads(body.decode("utf-8"))
        logging.info(f"Received message: {data}")

        if 'video_url' not in data or 'video_id' not in data:
            logging.error("Invalid message format. Missing required fields.")
            return

        audio_path = download_audio(data['video_url'], data['video_id'])
        response_data = {
            "video_id": data['video_id'],
            "audio_file_path": audio_path
        }

        ch.basic_publish(
            exchange='',
            routing_key=Config.get_corpus("rabbitmq", "output_queue"),
            body=json.dumps(response_data)
        )
        logging.info(f"Published response: {response_data}")
    
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON: {e}")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")


def main():
    with rabbitmq_connection() as channel:
        setup_queues(channel)
        logging.info("Waiting for messages. To exit press CTRL+C")
        
        channel.basic_consume(
            queue=Config.get_corpus("rabbitmq", "input_queue"),
            on_message_callback=callback,
            auto_ack=True
        )
        
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            logging.info("Shutting down consumer gracefully.")


if __name__ == "__main__":
    main()
