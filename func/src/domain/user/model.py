from src.domain.enums.file.term_file import UserTerms


class User:
    def __init__(self, user_document: dict):
        self.__terms = user_document.get("terms", {})
        self.__politically_exposed = (
            user_document.get("external_exchange_requirements", {})
            .get("us", {})
            .get("is_politically_exposed")
        )
        self.__exchange_member = (
            user_document.get("external_exchange_requirements", {})
            .get("us", {})
            .get("is_exchange_member")
        )
        self.__company_director = (
            user_document.get("external_exchange_requirements", {})
            .get("us", {})
            .get("is_company_director")
        )
        self.__external_fiscal_tax_confirmation = (
            user_document.get("external_exchange_requirements", {})
            .get("us", {})
            .get("external_fiscal_tax_confirmation")
        )
        self.__employ_status = (
            user_document.get("external_exchange_requirements", {})
            .get("us", {})
            .get("user_employ_status")
        )
        self.__time_experience = (
            user_document.get("external_exchange_requirements", {})
            .get("us", {})
            .get("time_experience")
        )
        self.__created_on_dw = (
            user_document.get("portfolios", {})
            .get("default", {})
            .get("us", {})
            .get("dw_id")
        )
        self.__w8_confirmation = (
            user_document.get("external_exchange_requirements", {})
            .get("us", {})
            .get("w8_confirmation")
        )

    def has_terms(self) -> bool:
        terms = self.__terms
        user_signed_terms = set(
            [term_name if metadata else None for term_name, metadata in terms.items()]
        )
        terms_that_needs_be_signed = {
            UserTerms.TERM_OPEN_ACCOUNT_DW.value,
            UserTerms.TERM_APPLICATION_DW.value,
            UserTerms.TERM_PRIVACY_POLICY_AND_DATA_SHARING_POLICY_DW.value,
            UserTerms.TERM_DISCLOSURES_AND_DISCLAIMERS.value,
            UserTerms.TERM_MONEY_CORP.value,
            UserTerms.TERM_GRINGO_WORLD.value,
            UserTerms.TERM_GRINGO_WORLD_GENERAL_ADVICES.value,
        }
        terms_not_signed = terms_that_needs_be_signed - user_signed_terms
        all_terms_are_signed = not bool(terms_not_signed)
        return all_terms_are_signed

    def has_politically_exposed_data(self) -> bool:
        has_politically_exposed_data = self.__politically_exposed is not None
        return has_politically_exposed_data

    def has_exchange_member_data(self) -> bool:
        has_exchange_member_data = self.__exchange_member is not None
        return has_exchange_member_data

    def has_company_director_data(self) -> bool:
        has_company_director_data = self.__company_director is not None
        return has_company_director_data

    def has_external_fiscal_tax_confirmation_data(self) -> bool:
        has_external_fiscal_tax_confirmation_data = (
            self.__external_fiscal_tax_confirmation is not None
        )
        return has_external_fiscal_tax_confirmation_data

    def has_employ_status_data(self) -> bool:
        has_employ_status_data = self.__employ_status is not None
        return has_employ_status_data

    def has_time_experience_data(self) -> bool:
        has_time_experience_data = self.__time_experience is not None
        user_created_in_dw = self.__created_on_dw is not None
        completed_time_experience_step = has_time_experience_data and user_created_in_dw
        return completed_time_experience_step

    def has_w8_confirmation_data(self) -> bool:
        has_w8_confirmation_data = self.__w8_confirmation is not None
        return has_w8_confirmation_data
