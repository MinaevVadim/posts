import json

import pika

from log_config import add_logger
from utils import SenderEmail


logger = add_logger(__name__)


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

    def callback(self, ch, method, properties, body) -> None:
        """A method that generates and sends data to the mail"""
        pass

    def consume_basic(self, queue: str | dict, auto_ack: bool = True) -> None:
        """A method that allows you to await a message from a queue"""
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(
            queue=queue,
            on_message_callback=self.callback,
            auto_ack=auto_ack,
        )
        logger.info(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()


class SendEmailClient(RabbitMQClient):
    """A class that allows you to send notifications by mail"""

    def callback(self, ch, method, properties, body) -> None:
        """A method that generates and sends data to the mail"""
        data = json.loads(body)
        user = data.get("user_id")
        post = data.get("post_id")
        emails = data.get("emails")
        sender_email = SenderEmail(
            message=f"User {user} has added a new post № {post}",
            email_from="admin@email.com",
            email_to=emails,
            subject="Hello my friend!",
        )
        sender_email.login_user("password")
        sender_email.send_message()
