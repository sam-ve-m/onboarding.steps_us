from unittest.mock import patch

from etria_logger import Gladsheim
from flask import Flask
from heimdall_client.bifrost import Heimdall
from heimdall_client.bifrost import HeimdallStatusResponses
from pytest import mark
from werkzeug.test import Headers

from main import save_symbols
from src.services.onboarding_steps import OnboardingSteps

decoded_jwt_ok = {
    "is_payload_decoded": True,
    "decoded_jwt": {"user": {"unique_id": "test"}},
    "message": "Jwt decoded",
}
decoded_jwt_invalid = {
    "is_payload_decoded": False,
    "decoded_jwt": {"user": {"unique_id": "test_error"}},
    "message": "Jwt decoded",
}

request_json_ok = {"symbols": [{"symbol": "PETR4", "region": "BR"}]}
requests_with_json_invalid = [
    {"smbols": [{"symbol": "PETR4", "region": "BR"}]},
    {"smbols": [{"symbo": "PETR4", "region": "BR"}]},
    {"smbols": [{"symbol": "PETR4", "reion": "BR"}]},
    {"smbols": [{"symbol": "P", "region": "BR"}]},
    {"smbols": [{"symbol": "PETR4", "region": "PR"}]},
    {},
]


@mark.asyncio
@patch.object(OnboardingSteps, "onboarding_user_current_step_us")
@patch.object(Heimdall, "decode_payload")
async def test_save_symbols_when_request_is_ok(
    decode_payload_mock, register_symbols_mock
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    register_symbols_mock.return_value = True

    app = Flask(__name__)
    with app.test_request_context(
        json=request_json_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        save_symbols_result = await save_symbols(request)

        assert (
            save_symbols_result.data
            == b'{"result": null, "message": "Symbols successfully saved", "success": true, "code": 0}'
        )
        assert register_symbols_mock.called
        decode_payload_mock.assert_called_with(jwt="test")


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(OnboardingSteps, "onboarding_user_current_step_us")
@patch.object(Heimdall, "decode_payload")
async def test_save_symbols_when_jwt_is_invalid(
    decode_payload_mock, register_symbols_mock, etria_mock
):
    decode_payload_mock.return_value = (
        decoded_jwt_invalid,
        HeimdallStatusResponses.INVALID_TOKEN,
    )
    register_symbols_mock.return_value = True

    app = Flask(__name__)
    with app.test_request_context(
        json=request_json_ok,
        headers=Headers({"x-thebes-answer": "test_error"}),
    ).request as request:

        save_symbols_result = await save_symbols(request)

        assert (
            save_symbols_result.data
            == b'{"result": null, "message": "JWT invalid or not supplied", "success": false, "code": 30}'
        )
        assert not register_symbols_mock.called
        decode_payload_mock.assert_called_with(jwt="test_error")
        etria_mock.assert_called()


@mark.asyncio
@mark.parametrize("request_json", requests_with_json_invalid)
@patch.object(Gladsheim, "error")
@patch.object(OnboardingSteps, "onboarding_user_current_step_us")
@patch.object(Heimdall, "decode_payload")
async def test_save_symbols_when_json_is_invalid(
    decode_payload_mock, register_symbols_mock, etria_mock, request_json
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    register_symbols_mock.return_value = True

    app = Flask(__name__)
    with app.test_request_context(
        json=request_json,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        save_symbols_result = await save_symbols(request)

        assert (
            save_symbols_result.data
            == b'{"result": null, "message": "Invalid parameters", "success": false, "code": 10}'
        )
        assert not register_symbols_mock.called
        decode_payload_mock.assert_called_with(jwt="test")
        etria_mock.assert_called()


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(OnboardingSteps, "onboarding_user_current_step_us")
@patch.object(Heimdall, "decode_payload")
async def test_save_symbols_when_generic_exception_happens(
    decode_payload_mock, register_symbols_mock, etria_mock
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    register_symbols_mock.side_effect = Exception("erro")

    app = Flask(__name__)
    with app.test_request_context(
        json=request_json_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        save_symbols_result = await save_symbols(request)

        assert (
            save_symbols_result.data
            == b'{"result": null, "message": "Unexpected error occurred", "success": false, "code": 100}'
        )
        assert register_symbols_mock.called
        decode_payload_mock.assert_called_with(jwt="test")
        etria_mock.assert_called()
