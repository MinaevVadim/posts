from contextlib import asynccontextmanager

import aiofiles
from aiobotocore.session import get_session

from env_config import settings


class S3Client:
    """S3 Storage class"""

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ) -> None:
        self._config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self._bucket_name = bucket_name
        self._session = get_session()

    @asynccontextmanager
    async def _get_client(self) -> None:
        """Contextual manager for creating a storage client"""
        async with self._session.create_client("s3", **self._config) as s3_client:
            yield s3_client

    async def upload_file(self, file_path: str) -> str:
        """The method of uploading a file to the storage"""
        object_name = file_path.split("/")[-1]
        async with self._get_client() as s3_client:
            async with aiofiles.open(file_path, "rb") as file:
                await s3_client.put_object(
                    Bucket=self._bucket_name,
                    Key=object_name,
                    Body=file,
                )
            return object_name

    async def get_file(self, key: str) -> str:
        """Method of getting a file from storage"""
        async with self._get_client() as s3_client:
            response = await s3_client.get_object(
                Bucket=self._bucket_name,
                Key=key,
            )
            async with response["Body"] as stream:
                return await stream.read()

    async def delete_file(self, key: str) -> None:
        """Method of removing a file from storage"""
        async with self._get_client() as s3_client:
            await s3_client.delete_object(Bucket=self._bucket_name, Key=key)


client = S3Client(
    access_key=settings.s3storage.access_key,
    secret_key=settings.s3storage.secret_key,
    endpoint_url=settings.s3storage.endpoint_url,
    bucket_name=settings.s3storage.bucket_name,
)
