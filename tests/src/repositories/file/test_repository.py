from enum import Enum
from unittest.mock import AsyncMock, patch

import pytest
from etria_logger import Gladsheim
from pytest import mark

from func.src.domain.enums.file.user_file import UserDocument
from func.src.domain.exceptions.model import InvalidFileType
from func.src.infrastructures.s3.infrastructure import S3Infrastructure
from func.src.repositories.file.repository import FileRepository

user_file_type_stub = UserDocument.DOCUMENT_BACK
unique_id_stub = "uniqueid"
bucket_name_stub = "bucket_name"


class FilterMock:
    iteration_return = "document"
    iteration = 0

    def __aiter__(self):
        return self

    def __anext__(self):
        if self.iteration > 1:
            raise StopAsyncIteration
        else:
            self.iteration += 1

            async def get_item():
                return self.iteration_return

            return get_item()


class InfraMock:
    async def __aenter__(self):
        class Object(AsyncMock):
            def filter(self, Prefix=None):
                filter_mock = FilterMock()
                return filter_mock

        class Bucket_:
            async def __call__(self, *args, **kwargs):
                return Bucket_()

            objects = Object()

        class GetResource:
            Bucket = Bucket_()

        return GetResource()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return


@mark.asyncio
async def test_user_file_exists_when_file_exists(monkeypatch):
    monkeypatch.setattr(S3Infrastructure, "get_resource", InfraMock)
    result = await FileRepository.user_file_exists(
        file_type=user_file_type_stub,
        unique_id=unique_id_stub,
        bucket_name=bucket_name_stub,
    )
    assert result is True


@mark.asyncio
async def test_user_file_exists_when_file_not_exists(monkeypatch):
    monkeypatch.setattr(FilterMock, "iteration_return", None)
    monkeypatch.setattr(S3Infrastructure, "get_resource", InfraMock)
    result = await FileRepository.user_file_exists(
        file_type=user_file_type_stub,
        unique_id=unique_id_stub,
        bucket_name=bucket_name_stub,
    )
    assert result is False


@mark.asyncio
async def test_user_file_exists_exception(monkeypatch):
    with pytest.raises(Exception):
        result = await FileRepository.user_file_exists(
            file_type=user_file_type_stub, unique_id="", bucket_name=bucket_name_stub
        )


def test_validate_file_type():
    enum_dummy = UserDocument.DOCUMENT_BACK
    result = FileRepository._validate_file_type(enum_dummy)
    assert result is None


@patch.object(Gladsheim, "error")
def test_validate_file_type_exception(etria_mock):
    class EnumDummy(Enum):
        DUMMY = "dummy"

    with pytest.raises(InvalidFileType):
        result = FileRepository._validate_file_type(EnumDummy.DUMMY)
    assert etria_mock.called


@mark.asyncio
async def test__resolve_user_path():
    result = await FileRepository._resolve_user_path(
        "testeid", UserDocument.DOCUMENT_FRONT
    )
    expected_result = "testeid/document_front/"
    assert result == expected_result
