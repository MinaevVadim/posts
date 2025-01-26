import base64
from typing import Optional

import aiohttp
from fastapi import UploadFile

from env_config import settings
from log_config import add_logger


logger = add_logger(__name__)


class CommunicateClient:
    """A class for communication between this service and a media service"""

    @classmethod
    async def send_image(cls, file: Optional[UploadFile], idd: int) -> "":
        """A method for sending a file to a media service"""
        if file:
            encoded_file = base64.b64encode(file.file.read())
            decoded_file = encoded_file.decode("utf-8")
            logger.info("File %s was sent to media service", file.filename)
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(10)
            ) as client:
                async with client.post(
                    f"http://{settings.media.media_host}:{settings.media.media_port}/media",
                    json={
                        "idd": idd,
                        "file": decoded_file,
                    },
                ) as response:
                    link_image = await response.read()
                    return link_image.decode()

    @classmethod
    async def get_image(cls, idd: int) -> "":
        """A method for getting a file to a media service"""
        logger.info(
            "Sending a request for getting a file with %s id to the media service",
            idd,
        )
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as client:
            async with client.get(
                f"http://{settings.media.media_host}:{settings.media.media_port}/media/{idd}"
            ) as response:
                link_image = await response.read()
                return link_image.decode()
