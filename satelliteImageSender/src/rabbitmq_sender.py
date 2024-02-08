import pika

class RabbitMQSender:
    HOST = 'rabbitmq'
    PORT = 5672
    USER = 'guest'
    PASSWORD = 'guest'
    QUEUE_NAME = 'satellite_image_queue'

    def __init__(self):
        self.connection_params = pika.ConnectionParameters(
            host=RabbitMQSender.HOST,
            port=RabbitMQSender.PORT,
            credentials=pika.PlainCredentials(RabbitMQSender.USER, RabbitMQSender.PASSWORD)
        )
        self.queue_name = RabbitMQSender.QUEUE_NAME

    def send_image(self, image_id, image_data, is_subimage=False, index=None):
        with pika.BlockingConnection(self.connection_params) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=self.queue_name)

            properties = pika.BasicProperties(
                headers={'image_id': image_id}
            )

            channel.basic_publish(exchange='',
                                  routing_key=self.queue_name,
                                  body=image_data,
                                  properties=properties)

            if is_subimage:
                print(f" [x] Subimage {index} sent to RabbitMQ with ID: {image_id}")
            else:
                print(f" [x] Image sent to RabbitMQ with ID: {image_id}")
