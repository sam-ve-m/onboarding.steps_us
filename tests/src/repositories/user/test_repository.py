from unittest.mock import patch, AsyncMock

from etria_logger import Gladsheim
from pytest import mark, raises

from src.repositories.user.repository import UserRepository


@mark.asyncio
@patch.object(UserRepository, "_UserRepository__get_collection")
async def test_find_user(get_collection_mock):
    expected_result = {"user": "data"}
    collection_mock = AsyncMock()
    collection_mock.find_one.return_value = expected_result
    get_collection_mock.return_value = collection_mock
    result = await UserRepository.find_user({})
    assert result == expected_result


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserRepository, "_UserRepository__get_collection")
async def test_find_user_when_exception_happens(get_collection_mock, etria_error_mock):
    get_collection_mock.side_effect = Exception()
    with raises(Exception):
        result = await UserRepository.find_user({})
    etria_error_mock.assert_called()
