from src.domain.enums.onboarding_steps.onboarding_steps import OnboardingStepsEnum
from src.domain.user.model import User


class OnboardingStepBuilder:
    def __init__(self, user: User):
        self.__user = user
        self.__step = 0
        self.__onboarding_steps = {
            0: OnboardingStepsEnum.TERMS,
            1: OnboardingStepsEnum.DOCUMENT_VALIDATOR,
            2: OnboardingStepsEnum.POLITICALLY_EXPOSED,
            3: OnboardingStepsEnum.EXCHANGE_MEMBER,
            4: OnboardingStepsEnum.COMPANY_DIRECTOR,
            5: OnboardingStepsEnum.TAX_CONFIRMATION,
            6: OnboardingStepsEnum.EMPLOY,
            7: OnboardingStepsEnum.TIME_EXPERIENCE,
            8: OnboardingStepsEnum.W8_CONFIRMATION,
            9: OnboardingStepsEnum.FINISHED,
        }

    def get_current_step(self):
        step = self.__onboarding_steps.get(self.__step)
        return step

    def is_current_step(self, step: OnboardingStepsEnum) -> bool:
        current_step = self.get_current_step()
        is_current_step = step == current_step
        return is_current_step

    def terms_step(self):
        terms = self.__user.has_terms()
        is_current_step = self.is_current_step(OnboardingStepsEnum.TERMS)
        terms_step = terms and is_current_step
        if terms_step:
            self.__step += 1
        return terms_step

    def user_document_validator_step(self, document_exists: bool):
        document = document_exists
        is_current_step = self.is_current_step(OnboardingStepsEnum.DOCUMENT_VALIDATOR)
        document_step = document and is_current_step
        if document_step:
            self.__step += 1
        return document_step

    def politically_exposed_step(self):
        politically_exposed = self.__user.has_politically_exposed_data()
        is_current_step = self.is_current_step(OnboardingStepsEnum.POLITICALLY_EXPOSED)
        politically_exposed_step = politically_exposed and is_current_step
        if politically_exposed_step:
            self.__step += 1
        return politically_exposed_step

    def exchange_member_step(self):
        exchange_member = self.__user.has_exchange_member_data()
        is_current_step = self.is_current_step(OnboardingStepsEnum.EXCHANGE_MEMBER)
        exchange_member_step = exchange_member and is_current_step
        if exchange_member_step:
            self.__step += 1
        return exchange_member_step

    def company_director_step(self):
        company_director = self.__user.has_company_director_data()
        is_current_step = self.is_current_step(OnboardingStepsEnum.COMPANY_DIRECTOR)
        company_director_step = company_director and is_current_step
        if company_director_step:
            self.__step += 1
        return company_director_step

    def external_fiscal_tax_confirmation_step(self):
        external_fiscal_tax_confirmation = (
            self.__user.has_external_fiscal_tax_confirmation_data()
        )
        is_current_step = self.is_current_step(OnboardingStepsEnum.TAX_CONFIRMATION)
        external_fiscal_tax_confirmation_step = (
            external_fiscal_tax_confirmation and is_current_step
        )
        if external_fiscal_tax_confirmation_step:
            self.__step += 1
        return external_fiscal_tax_confirmation_step

    def employ_step(self):
        employ_step = self.__user.has_employ_status_data()
        is_current_step = self.is_current_step(OnboardingStepsEnum.EMPLOY)
        employ_step_step = employ_step and is_current_step
        if employ_step_step:
            self.__step += 1
        return employ_step_step

    def time_experience_step(self):
        time_experience = self.__user.has_time_experience_data()
        is_current_step = self.is_current_step(OnboardingStepsEnum.TIME_EXPERIENCE)
        time_experience_step = time_experience and is_current_step
        if time_experience_step:
            self.__step += 1
        return time_experience_step

    def w8_confirmation_step(self):
        w8_confirmation = self.__user.has_w8_confirmation_data()
        is_current_step = self.is_current_step(OnboardingStepsEnum.W8_CONFIRMATION)
        w8_confirmation_step = w8_confirmation and is_current_step
        if w8_confirmation_step:
            self.__step += 1
        return w8_confirmation_step

    async def build(self, document_exists: bool) -> dict:
        onboarding_steps = {
            OnboardingStepsEnum.TERMS.value: self.terms_step(),
            OnboardingStepsEnum.DOCUMENT_VALIDATOR.value: self.user_document_validator_step(
                document_exists
            ),
            OnboardingStepsEnum.POLITICALLY_EXPOSED.value: self.politically_exposed_step(),
            OnboardingStepsEnum.EXCHANGE_MEMBER.value: self.exchange_member_step(),
            OnboardingStepsEnum.COMPANY_DIRECTOR.value: self.company_director_step(),
            OnboardingStepsEnum.TAX_CONFIRMATION.value: self.external_fiscal_tax_confirmation_step(),
            OnboardingStepsEnum.EMPLOY.value: self.employ_step(),
            OnboardingStepsEnum.TIME_EXPERIENCE.value: self.time_experience_step(),
            OnboardingStepsEnum.W8_CONFIRMATION.value: self.w8_confirmation_step(),
            OnboardingStepsEnum.CURRENT.value: self.get_current_step().value,
        }
        return onboarding_steps
