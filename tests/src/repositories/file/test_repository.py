from enum import Enum
from unittest.mock import AsyncMock

import pytest
from pytest import mark

from src.domain.enums.file.user_file import UserFileType
from src.domain.exceptions.model import InternalServerError
from src.infrastructures.s3.infrastructure import S3Infrastructure
from src.repositories.file.repository import FileRepository

user_file_type_stub = UserFileType.SELFIE
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
    with pytest.raises(InternalServerError):
        result = await FileRepository.user_file_exists(
            file_type=user_file_type_stub, unique_id="", bucket_name=bucket_name_stub
        )


def test__get_file_extension_by_type():
    enum_dummy = UserFileType.SELFIE
    result = FileRepository._get_file_extension_by_type(enum_dummy)
    expected_result = ".jpg"
    assert result == expected_result


def test__get_file_extension_by_type_exception():
    class EnumDummy(Enum):
        DUMMY = "dummy"

    with pytest.raises(InternalServerError):
        result = FileRepository._get_file_extension_by_type(EnumDummy.DUMMY)


@mark.asyncio
async def test__resolve_user_path():
    result = await FileRepository._resolve_user_path("testeid", UserFileType.SELFIE)
    expected_result = "testeid/user_selfie/"
    assert result == expected_result
