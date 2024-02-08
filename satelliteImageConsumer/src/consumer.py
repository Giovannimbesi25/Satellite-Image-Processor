import pika
from image_processor import ImageProcessor

class Consumer:
        
    HOST = 'rabbitmq'
    PORT = 5672
    USER = 'guest'
    PASSWORD = 'guest'
    QUEUE_NAME = 'satellite_image_queue'

    def start_consumer(self):
        connection_params = pika.ConnectionParameters(
            host=Consumer.HOST,
            port=Consumer.PORT,
            credentials=pika.PlainCredentials(Consumer.USER, Consumer.PASSWORD),
        )

        with pika.BlockingConnection(connection_params) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=Consumer.QUEUE_NAME)

            try:
                while True:
                    print(" [*] Waiting for subimages. Press CTRL+C to interrupt")
                    channel.basic_consume(queue=Consumer.QUEUE_NAME, on_message_callback=ImageProcessor().process_subimage)
                    channel.start_consuming()
            except KeyboardInterrupt:
                print(" [x] Interrupted. Closing the consumer.")




