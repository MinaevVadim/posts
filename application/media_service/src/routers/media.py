import base64

from fastapi import APIRouter
from starlette import status

from client import client
from communicate.media import CommunicateClient
from schemas.media import MediaSchema, MediaCreateSchema

router = APIRouter(prefix="/media", tags=["media"])


@router.get(
    "/{idd}",
    status_code=status.HTTP_200_OK,
    response_model=MediaSchema,
)
async def get_media(idd: str) -> MediaSchema:
    link = await client.get_file(idd)
    return MediaSchema(link=link)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MediaSchema)
async def create_media(data: MediaCreateSchema) -> MediaSchema:
    encoded_image = data.file.encode("utf-8")
    image = base64.b64decode(encoded_image)
    idd = await client.upload_file(image)
    return await CommunicateClient().response_image(idd)
