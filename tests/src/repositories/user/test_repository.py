from unittest.mock import patch, AsyncMock

from etria_logger import Gladsheim
from pytest import mark, raises

from func.src.domain.user.model import User
from func.src.repositories.user.repository import UserRepository


@mark.asyncio
@patch.object(UserRepository, "_UserRepository__get_collection")
async def test_find_user(get_collection_mock):
    find_one_result_dummy = {"user": "data"}
    collection_mock = AsyncMock()
    collection_mock.find_one.return_value = find_one_result_dummy
    get_collection_mock.return_value = collection_mock
    result = await UserRepository.find_user({})
    assert isinstance(result, User)


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserRepository, "_UserRepository__get_collection")
async def test_find_user_when_exception_happens(get_collection_mock, etria_error_mock):
    get_collection_mock.side_effect = Exception()
    with raises(Exception):
        result = await UserRepository.find_user({})
    etria_error_mock.assert_called()
