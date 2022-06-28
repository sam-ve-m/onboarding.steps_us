from unittest.mock import patch

from pytest import mark, raises

from src.domain.exceptions.model import BadRequestError
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository
from src.services.onboarding_steps.service import OnboardingSteps

payload_dummy = {"user": {"unique_id": "test"}}
find_user_return_dummy = {"current_user": payload_dummy}


class OnboardingStepBuilderUSStub:
    def __init__(self):
        self.__onboarding_steps: dict = {
            "current_onboarding_step": "terms_step",
            "terms_step": False,
            "user_document_validator_step": False,
            "is_politically_exposed_step": False,
            "is_exchange_member_step": False,
            "is_company_director_step": False,
            "external_fiscal_tax_confirmation_step": False,
            "employ_step": False,
            "time_experience_step": False,
            "w8_confirmation_step": False,
            "finished": False,
        }
        self.__steps: list = [
            "terms_step",
            "user_document_validator_step",
            "is_politically_exposed_step",
            "is_exchange_member_step",
            "is_company_director_step",
            "external_fiscal_tax_confirmation_step",
            "employ_step",
            "time_experience_step",
            "w8_confirmation_step",
        ]
        self.bureau_status = None

    def terms_step(self, current_user: dict):
        self.__onboarding_steps["terms_step"] = True
        self.__onboarding_steps[
            "current_onboarding_step"
        ] = "user_document_validator_step"
        return self

    def user_document_validator_step(self, document_exists: bool):
        self.__onboarding_steps["user_document_validator_step"] = True
        self.__onboarding_steps[
            "current_onboarding_step"
        ] = "is_politically_exposed_step"
        return self

    def is_politically_exposed_step(self, current_user: dict):
        self.__onboarding_steps["is_politically_exposed_step"] = True
        self.__onboarding_steps[
            "current_onboarding_step"
        ] = "is_exchange_member_step"
        return self

    def is_exchange_member_step(self, current_user: dict):
        self.__onboarding_steps["is_exchange_member_step"] = True
        self.__onboarding_steps[
            "current_onboarding_step"
        ] = "is_company_director_step"
        return self

    def is_company_director_step(self, current_user: dict):
        self.__onboarding_steps["is_company_director_step"] = True
        self.__onboarding_steps[
            "current_onboarding_step"
        ] = "external_fiscal_tax_confirmation_step"
        return self

    def external_fiscal_tax_confirmation_step(self, current_user: dict):
        self.__onboarding_steps["external_fiscal_tax_confirmation_step"] = True
        self.__onboarding_steps["current_onboarding_step"] = "employ_step"
        return self

    def employ_step(self, current_user: dict):
        self.__onboarding_steps["employ_step"] = True
        self.__onboarding_steps["current_onboarding_step"] = "time_experience_step"
        return self

    def time_experience_step(self, current_user: dict):
        self.__onboarding_steps["time_experience_step"] = True
        self.__onboarding_steps["current_onboarding_step"] = "w8_confirmation_step"
        return self

    def w8_confirmation_step(self, current_user: dict):
        self.__onboarding_steps["w8_confirmation_step"] = True
        self.__onboarding_steps["current_onboarding_step"] = "finished"
        return self

    def is_finished(self):
        self.__onboarding_steps["current_onboarding_step"] = "finished"
        self.__onboarding_steps["finished"] = True

    async def build(self) -> dict:
        self.is_finished()
        onboarding_steps = self.__onboarding_steps
        return onboarding_steps


@mark.asyncio
@patch.object(FileRepository, "user_file_exists", return_value=True)
@patch.object(UserRepository, "find_user", return_value=find_user_return_dummy)
async def test_onboarding_user_current_step_us(
    find_user_mock, file_exists_mock, monkeypatch
):
    monkeypatch.setattr(
        target=OnboardingSteps, name="steps_builder", value=OnboardingStepBuilderUSStub
    )
    result = await OnboardingSteps.onboarding_user_current_step_us(payload_dummy)
    expected_result = {
            "current_onboarding_step": "finished",
            "terms_step": True,
            "user_document_validator_step": True,
            "is_politically_exposed_step": True,
            "is_exchange_member_step": True,
            "is_company_director_step": True,
            "external_fiscal_tax_confirmation_step": True,
            "employ_step": True,
            "time_experience_step": True,
            "w8_confirmation_step": True,
            "finished": True,
        }
    assert result == expected_result


@mark.asyncio
@patch.object(FileRepository, "user_file_exists", return_value=True)
@patch.object(UserRepository, "find_user", return_value=None)
async def test_onboarding_user_current_step_us_when_user_is_none(
    find_user_mock, file_exists_mock, monkeypatch
):
    monkeypatch.setattr(
        target=OnboardingSteps, name="steps_builder", value=OnboardingStepBuilderUSStub
    )
    with raises(BadRequestError):
        result = await OnboardingSteps.onboarding_user_current_step_us(payload_dummy)
