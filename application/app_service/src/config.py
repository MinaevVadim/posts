import pika


class RabbitMQClient:
    """The rabbitmq class that helps you exchange data efficiently and reliably"""

    def __init__(self, host: str, port: int, **kwargs) -> None:
        self.parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            **kwargs,
        )
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def public_basic(
        self, queue: str, exchange: str, route_key: str, body: str | bytes
    ) -> None:
        """A method that allows you to put a message in a queue"""
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=route_key,
            body=body,
        )
        self.close()

    def close(self):
        """Connection closing method"""
        self.connection.close()
