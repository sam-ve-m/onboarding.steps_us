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

    @staticmethod
    def _is_single_terms_signed(user_signed_terms: set) -> bool:
        single_terms_that_needs_be_signed = {
            UserTerms.TERM_ALL_AGREEMENT_GRINGO_DL.value,
            UserTerms.TERM_GRINGO_WORLD.value,
            UserTerms.TERM_GRINGO_WORLD_GENERAL_ADVICES.value,
        }
        single_terms_not_signed = single_terms_that_needs_be_signed - user_signed_terms

        all_single_terms_are_signed = not bool(single_terms_not_signed)

        return all_single_terms_are_signed

    @staticmethod
    def _is_i18n_terms_signed(user_signed_terms: set) -> bool:

        term_and_privacy_policy_data_sharing_policy_dl = {
            UserTerms.TERM_AND_PRIVACY_POLICY_DATA_SHARING_POLICY_DL_US.value,
            UserTerms.TERM_AND_PRIVACY_POLICY_DATA_SHARING_POLICY_DL_PT.value,
        }

        term_not_signed_and_privacy_policy_data_sharing_policy_dl = (
            term_and_privacy_policy_data_sharing_policy_dl - user_signed_terms
        )

        term_open_account_dl = {
            UserTerms.TERM_OPEN_ACCOUNT_DL_PT.value,
            UserTerms.TERM_OPEN_ACCOUNT_DL_US.value,
        }

        term_not_signed_open_account_dl = term_open_account_dl - user_signed_terms

        term_business_continuity_plan_dl = {
            UserTerms.TERM_BUSINESS_CONTINUITY_PLAN_DL_PT.value,
            UserTerms.TERM_BUSINESS_CONTINUITY_PLAN_DL_US.value,
        }

        term_not_signed_business_continuity_plan_dl = (
            term_business_continuity_plan_dl - user_signed_terms
        )

        term_customer_relationship_summary_dl = {
            UserTerms.TERM_CUSTOMER_RELATIONSHIP_SUMMARY_DL_PT.value,
            UserTerms.TERM_CUSTOMER_RELATIONSHIP_SUMMARY_DL_US.value,
        }

        term_not_signed_customer_relationship_summary_dl = (
            term_customer_relationship_summary_dl - user_signed_terms
        )

        minimal_one_of_each_i18n_terms_are_signed = all(
            [
                len(term_not_signed_and_privacy_policy_data_sharing_policy_dl) <= 1,
                len(term_not_signed_open_account_dl) <= 1,
                len(term_not_signed_business_continuity_plan_dl) <= 1,
                len(term_not_signed_customer_relationship_summary_dl) <= 1,
            ]
        )

        return minimal_one_of_each_i18n_terms_are_signed

    def has_terms(self) -> bool:
        terms = self.__terms
        user_signed_terms = set(
            [term_name if metadata else None for term_name, metadata in terms.items()]
        )
        all_single_terms_are_signed = self._is_single_terms_signed(
            user_signed_terms=user_signed_terms
        )
        minimal_one_of_each_i18n_terms_are_signed = self._is_i18n_terms_signed(
            user_signed_terms=user_signed_terms
        )
        all_terms_are_signed = (
            all_single_terms_are_signed and minimal_one_of_each_i18n_terms_are_signed
        )
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
