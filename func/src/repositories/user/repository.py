from typing import Optional

from decouple import config
from etria_logger import Gladsheim

from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class OnboardingStepsRepository:
    infra = MongoDBInfrastructure
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[cls.database]
            collection = database[cls.collection]
            return collection
        except Exception as ex:
            message = (
                f"UserRepository::_get_collection::Error when trying to get collection"
            )
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def find_user(cls, query: dict) -> Optional[dict]:
        try:
            collection = await cls.__get_collection()
            data = await collection.find_one(query)
            return data

        except Exception as ex:
            Gladsheim.error(error=ex)
            raise ex

    @classmethod
    async def is_user_using_suitability_or_refuse_term(cls, unique_id: str) -> str:
        collection = await cls.__get_collection()
        user = await collection.find_user({"unique_id": unique_id})
        suitability = user.get("suitability")
        term_refusal = user["terms"].get("term_refusal")

        has_suitability = suitability is not None
        has_term_refusal = term_refusal is not None

        suitability_and_refusal_term = (True, True)
        only_suitability = (True, False)
        only_refusal_term = (False, True)
        nothing = (False, False)

        user_trade_match = {
            suitability_and_refusal_term: cls.suitability_and_refusal_term_callback,
            only_suitability: lambda _suitability, _term_refusal: "suitability",
            only_refusal_term: lambda _suitability, _term_refusal: "term_refusal",
            nothing: lambda _suitability, _term_refusal: None,
        }

        user_trade_profile_callback = user_trade_match.get(
            (has_suitability, has_term_refusal)
        )
        user_trade_profile = user_trade_profile_callback(suitability, term_refusal)

        return user_trade_profile

    @staticmethod
    def suitability_and_refusal_term_callback(_suitability, _term_refusal):
        last_trade_profile_signed = (
            _suitability["submission_date"] > _term_refusal["date"]
        )
        return "suitability" if last_trade_profile_signed else "term_refusal"
