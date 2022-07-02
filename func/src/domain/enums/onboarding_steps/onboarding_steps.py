from enum import Enum


class OnboardingStepsEnum(Enum):
    CURRENT = "current_step"
    TERMS = "terms"
    DOCUMENT_VALIDATOR = "user_document_validator"
    POLITICALLY_EXPOSED = "politically_exposed"
    EXCHANGE_MEMBER = "exchange_member"
    COMPANY_DIRECTOR = "company_director"
    TAX_CONFIRMATION = "external_fiscal_tax_confirmation"
    EMPLOY = "employ"
    TIME_EXPERIENCE = "time_experience"
    W8_CONFIRMATION = "w8_confirmation"
    FINISHED = "finished"
