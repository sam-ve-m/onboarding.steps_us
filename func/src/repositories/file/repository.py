from enum import Enum
from typing import Optional

from src.domain.enums.file.term_file import TermsFileType
from src.domain.enums.file.user_file import UserFileType
from src.domain.exceptions.model import InternalServerError
from src.infrastructures.s3.infrastructure import S3Infrastructure


class FileRepository:
    infra = S3Infrastructure

    _file_extension_by_file_type = {
        "user_selfie": ".jpg",
        "document_front": ".jpg",
        "document_back": ".jpg",
        "term_application": ".pdf",
        "term_open_account": ".pdf",
        "term_refusal": ".pdf",
        "term_non_compliance": ".pdf",
        "term_retail_liquid_provider": ".pdf",
        "term_open_account_dw": ".pdf",
        "term_application_dw": ".pdf",
        "term_and_privacy_policy_data_sharing_policy_dw": ".pdf",
        "term_disclosures_and_disclaimers": ".pdf",
        "term_money_corp": ".pdf",
        "term_gringo_world": ".pdf",
        "term_gringo_world_general_advices": ".pdf",
    }

    @classmethod
    async def user_file_exists(
        cls, file_type: UserFileType, unique_id: str, bucket_name: str
    ):
        prefix = await cls._resolve_user_path(unique_id=unique_id, file_type=file_type)
        file_name = file_type.value
        file_extension = cls._get_file_extension_by_type(file_type=file_type)
        if not prefix or not file_name or not file_extension:
            raise InternalServerError("files.error")

        objects = None
        async with cls.infra.get_resource() as s3_resource:
            bucket = await s3_resource.Bucket(bucket_name)
            async for s3_object in bucket.objects.filter(Prefix=prefix):
                objects = s3_object

        if not objects:
            exists_selfie = False
        else:
            exists_selfie = True

        return exists_selfie

    @classmethod
    def _get_file_extension_by_type(cls, file_type: Enum) -> Optional[str]:
        valid_files = list()
        for file_enum in [UserFileType, TermsFileType]:
            valid_files += [item.value for item in file_enum]
        if file_type.value not in valid_files:
            raise InternalServerError("files.error")
        return cls._file_extension_by_file_type.get(file_type.value)

    @staticmethod
    async def _resolve_user_path(unique_id: str, file_type: UserFileType) -> str:
        return f"{unique_id}/{file_type.value}/"
