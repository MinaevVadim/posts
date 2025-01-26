import aiohttp

from env_config import settings
from log_config import add_logger

logger = add_logger(__name__)


class CommunicateClient:
    """A class for communication between a media service"""

    @classmethod
    async def response_image(cls, idd: int) -> "":
        """The method of sending the image"""
        logger.info(
            "Request for sending back a file with %s id to the media service",
            idd,
        )
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as cli:
            response = await cli.get(
                f"http://{settings.media.host_name}:{settings.media.host_port}/media/{idd}"
            )
            return await response.read()
