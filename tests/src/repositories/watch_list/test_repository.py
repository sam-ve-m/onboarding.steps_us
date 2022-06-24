from unittest.mock import patch, AsyncMock

import pytest
from etria_logger import Gladsheim
from nidavellir import Sindri
from pytest import mark

from src.domain.request.model import WatchListSymbols
from src.domain.watch_list.model import WatchListSymbolModel
from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure
from src.repositories.user.repository import OnboardingStepsRepository

dummy_symbols_to_insert = {
    "symbols": [
        {"symbol": "PETR4", "region": "BR"},
        {"symbol": "AAPL", "region": "US"},
        {"symbol": "JBSS3", "region": "BR"},
    ]
}

dummy_watch_list_symbols_model = [
    WatchListSymbolModel(symbol, "test_id")
    for symbol in WatchListSymbols(**dummy_symbols_to_insert).symbols
]
dummy_insert = [
    str(Sindri.dict_to_primitive_types(x.to_dict()))
    for x in dummy_watch_list_symbols_model
]


@mark.asyncio
@patch.object(OnboardingStepsRepository, "_WatchListRepository__get_collection")
async def test_insert_all_symbols_in_watch_list(get_collection_mock, monkeypatch):
    class TransactionMock:
        async def __aenter__(self):
            return AsyncMock()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return

    class ActuallySessionMock:
        def start_transaction(self):
            return TransactionMock()

        async def __aenter__(self):
            return AsyncMock()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    class SessionMock:
        session = ActuallySessionMock()

        async def __aenter__(self):
            return self.session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    class ClientMock:
        session = SessionMock()

        async def start_session(self):
            return self.session

        async def __aenter__(self):
            pass

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    def get_client_mock():
        return ClientMock()

    collection_mock = AsyncMock()
    collection_mock.update_one.return_value = True
    get_collection_mock.return_value = collection_mock

    monkeypatch.setattr(MongoDBInfrastructure, "get_client", get_client_mock)

    await OnboardingStepsRepository.insert_all_symbols_in_watch_list(
        dummy_watch_list_symbols_model
    )
    get_collection_mock.assert_called_once_with()
    assert collection_mock.update_one.call_count == len(dummy_watch_list_symbols_model)


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(OnboardingStepsRepository, "_WatchListRepository__get_collection")
async def test_insert_all_symbols_in_watch_list_exception(
    get_collection_mock, etria_error_mock, monkeypatch
):
    class ActuallySessionMock:
        def start_transaction(self):
            raise Exception("ERROR")

        async def __aenter__(self):
            return AsyncMock()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    class SessionMock:
        session = ActuallySessionMock()

        async def __aenter__(self):
            return self.session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    class ClientMock:
        session = SessionMock()

        async def start_session(self):
            return self.session

        async def __aenter__(self):
            pass

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    def get_client_mock():
        return ClientMock()

    collection_mock = AsyncMock()
    collection_mock.update_one.return_value = True
    get_collection_mock.return_value = collection_mock

    monkeypatch.setattr(MongoDBInfrastructure, "get_client", get_client_mock)

    with pytest.raises(Exception):
        await OnboardingStepsRepository.insert_all_symbols_in_watch_list(
            dummy_watch_list_symbols_model
        )

        get_collection_mock.assert_called_once_with()
        get_collection_mock.assert_called_once_with()
        collection_mock.update_one.assert_not_called()
        collection_mock.update_one.assert_not_awaited()
        etria_error_mock.assert_called()
