import sys

from config import SendEmailClient
from env_config import settings


def main():
    """The main function of the service is to send notifications"""
    client = SendEmailClient(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
    )
    client.consume_basic(queue="email")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
