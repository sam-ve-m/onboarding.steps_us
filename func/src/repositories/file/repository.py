from enum import Enum

from etria_logger import Gladsheim

from src.domain.enums.file.selfie_file import UserSelfie
from src.domain.enums.file.term_file import UserTerms
from src.domain.enums.file.user_file import UserDocument
from src.domain.exceptions.model import InvalidFileType
from src.infrastructures.s3.infrastructure import S3Infrastructure


class FileRepository:
    infra = S3Infrastructure

    @classmethod
    async def user_file_exists(
        cls, file_type: Enum, unique_id: str, bucket_name: str
    ) -> bool:
        cls._validate_file_type(file_type=file_type)
        prefix = await cls._resolve_user_path(unique_id=unique_id, file_type=file_type)

        objects = None
        async with cls.infra.get_resource() as s3_resource:
            bucket = await s3_resource.Bucket(bucket_name)
            async for s3_object in bucket.objects.filter(Prefix=prefix):
                objects = s3_object

        exists_selfie = bool(objects)

        return exists_selfie

    @classmethod
    def _validate_file_type(cls, file_type: Enum):
        valid_files = list()
        try:
            for file_enum in [UserDocument, UserTerms, UserSelfie]:
                valid_files += [item.value for item in file_enum]
            if file_type.value not in valid_files:
                raise InvalidFileType("files.error")

        except Exception as ex:
            message = "invalid file type passed to the function"
            Gladsheim.error(error=ex, message=message, file_type=file_type)
            raise InvalidFileType("files.error")

    @staticmethod
    async def _resolve_user_path(unique_id: str, file_type: Enum) -> str:
        return f"{unique_id}/{file_type.value}/"
