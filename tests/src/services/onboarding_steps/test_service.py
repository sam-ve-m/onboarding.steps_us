from unittest.mock import patch

from pytest import mark

from src.domain.user.model import User
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository
from src.services.onboarding_steps.service import OnboardingSteps

payload_dummy = {"user": {"unique_id": "test"}}


user_document_dummy = {
    "terms": {
        "term_application": "term",
        "term_open_account": "term",
        "term_retail_liquid_provider": "term",
        "term_refusal": "term",
        "term_non_compliance": "term",
        "term_open_account_dw": "term",
        "term_and_privacy_policy_data_sharing_policy_dw": "term",
        "term_application_dw": "term",
        "term_disclosures_and_disclaimers": "term",
        "term_gringo_world": "term",
        "term_gringo_world_general_advices": "term",
        "term_money_corp": "term",
    },
    "portfolios": {"default": {"us": {"dw_id": "conta"}}},
    "external_exchange_requirements": {
        "us": {
            "is_politically_exposed": False,
            "is_exchange_member": False,
            "is_company_director": False,
            "external_fiscal_tax_confirmation": True,
            "user_employ_status": "EMPLOYED",
            "user_employ_type": "UTILITIES",
            "time_experience": "YRS_1_2",
            "w8_confirmation": True,
        }
    },
}

find_user_return_dummy_with_all_data = User(user_document_dummy)
find_user_return_dummy_with_no_data = User({})

build_return_dummy_all_true = {
    "terms": True,
    "user_document_validator": True,
    "politically_exposed": True,
    "exchange_member": True,
    "company_director": True,
    "external_fiscal_tax_confirmation": True,
    "employ": True,
    "time_experience": True,
    "w8_confirmation": True,
    "current_step": "finished",
}
build_return_dummy_all_false = {
    "terms": False,
    "user_document_validator": False,
    "politically_exposed": False,
    "exchange_member": False,
    "company_director": False,
    "external_fiscal_tax_confirmation": False,
    "employ": False,
    "time_experience": False,
    "w8_confirmation": False,
    "current_step": "terms",
}


@mark.asyncio
@patch.object(FileRepository, "user_file_exists", return_value=True)
@patch.object(
    UserRepository, "find_user", return_value=find_user_return_dummy_with_all_data
)
async def test_onboarding_user_current_step_br(find_user_mock, file_exists_mock):
    result = await OnboardingSteps.onboarding_user_current_step_us(payload_dummy)
    expected_result = build_return_dummy_all_true
    assert result == expected_result


@mark.asyncio
@patch.object(FileRepository, "user_file_exists", return_value=True)
@patch.object(
    UserRepository, "find_user", return_value=find_user_return_dummy_with_no_data
)
async def test_onboarding_user_current_step_br_when_user_is_none(
    find_user_mock, file_exists_mock
):
    result = await OnboardingSteps.onboarding_user_current_step_us(payload_dummy)
    expected_result = build_return_dummy_all_false
    assert result == expected_result
