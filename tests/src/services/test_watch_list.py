from unittest.mock import patch

from pytest import mark

from src.domain.request.model import WatchListSymbols
from src.domain.watch_list.model import WatchListSymbolModel
from src.repositories.user.repository import OnboardingStepsRepository
from src.services.onboarding_steps import OnboardingSteps

dummy_symbols_to_register = {
    "symbols": [
        {"symbol": "PETR4", "region": "BR"},
        {"symbol": "AAPL", "region": "US"},
        {"symbol": "JBSS3", "region": "BR"},
    ]
}

dummy_watch_list_symbols = WatchListSymbols(**dummy_symbols_to_register)


@mark.asyncio
@patch.object(OnboardingStepsRepository, "insert_all_symbols_in_watch_list")
async def test_register_symbols(insert_all_symbols_in_watch_list_mock):
    result = await OnboardingSteps.onboarding_user_current_step_us(
        dummy_watch_list_symbols, "test-id"
    )
    assert insert_all_symbols_in_watch_list_mock.call_count == 1
    for call in insert_all_symbols_in_watch_list_mock.call_args[0][0]:
        assert isinstance(call, WatchListSymbolModel)
