import logging.config
from flask import Flask
from pytest import mark
from unittest.mock import patch
from werkzeug.test import Headers
from decouple import Config, RepositoryEnv

with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from etria_logger import Gladsheim
                from heimdall_client.bifrost import Heimdall, HeimdallStatusResponses
                from main import get_onboarding_step_us
                from src.services.onboarding_steps.service import OnboardingSteps

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

onboarding_steps_result_dummy = {
    "current_onboarding_step": "finished",
    "suitability_step": True,
    "user_identifier_data_step": True,
    "user_selfie_step": True,
    "user_complementary_step": True,
    "user_document_validator": True,
    "user_data_validation": True,
    "user_electronic_signature": True,
    "finished": True,
}


@mark.asyncio
@patch.object(OnboardingSteps, "onboarding_user_current_step_us")
@patch.object(Heimdall, "decode_payload")
async def test_get_onboarding_step_us_when_request_is_ok(
    decode_payload_mock, onboarding_steps_mock
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    onboarding_steps_mock.return_value = onboarding_steps_result_dummy

    app = Flask(__name__)
    with app.test_request_context(
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        get_onboarding_step_us_result = await get_onboarding_step_us(request)

        assert (
            get_onboarding_step_us_result.data
            == b'{"result": {"current_onboarding_step": "finished", "suitability_step": true, "user_identifier_data_step": true, "user_selfie_step": true, "user_complementary_step": true, "user_document_validator": true, "user_data_validation": true, "user_electronic_signature": true, "finished": true}, "message": "Success", "success": true, "code": 0}'
        )
        assert onboarding_steps_mock.called
        decode_payload_mock.assert_called_with(jwt="test")


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(OnboardingSteps, "onboarding_user_current_step_us")
@patch.object(Heimdall, "decode_payload")
async def test_get_onboarding_step_us_when_jwt_is_invalid(
    decode_payload_mock, onboarding_steps_mock, etria_mock
):
    decode_payload_mock.return_value = (
        decoded_jwt_invalid,
        HeimdallStatusResponses.INVALID_TOKEN,
    )
    onboarding_steps_mock.return_value = True

    app = Flask(__name__)
    with app.test_request_context(
        headers=Headers({"x-thebes-answer": "test_error"}),
    ).request as request:

        get_onboarding_step_us_result = await get_onboarding_step_us(request)

        assert (
            get_onboarding_step_us_result.data
            == b'{"result": null, "message": "JWT invalid or not supplied", "success": false, "code": 30}'
        )
        assert not onboarding_steps_mock.called
        decode_payload_mock.assert_called_with(jwt="test_error")
        etria_mock.assert_called()


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(OnboardingSteps, "onboarding_user_current_step_us")
@patch.object(Heimdall, "decode_payload")
async def test_get_onboarding_step_us_when_generic_exception_happens(
    decode_payload_mock, onboarding_steps_mock, etria_mock
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    onboarding_steps_mock.side_effect = Exception("erro")

    app = Flask(__name__)
    with app.test_request_context(
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        get_onboarding_step_us_result = await get_onboarding_step_us(request)

        assert (
            get_onboarding_step_us_result.data
            == b'{"result": null, "message": "Unexpected error occurred", "success": false, "code": 100}'
        )
        assert onboarding_steps_mock.called
        decode_payload_mock.assert_called_with(jwt="test")
        etria_mock.assert_called()
