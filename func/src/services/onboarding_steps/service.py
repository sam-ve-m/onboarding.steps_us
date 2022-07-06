import asyncio

from decouple import config

from src.domain.enums.file.user_file import UserDocument
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository
from src.services.onboarding_steps_builder.service import OnboardingStepBuilder


class OnboardingSteps:
    bucket_name = config("AWS_BUCKET_USERS_FILES")
    user_repository = UserRepository
    file_repository = FileRepository
    steps_builder = OnboardingStepBuilder

    @classmethod
    async def onboarding_user_current_step_us(
        cls,
        payload: dict,
    ) -> dict:

        user_unique_id = payload["user"]["unique_id"]

        user_document_front_exists = cls.file_repository.user_file_exists(
            file_type=UserDocument.DOCUMENT_FRONT,
            unique_id=user_unique_id,
            bucket_name=OnboardingSteps.bucket_name,
        )
        user_document_back_exists = cls.file_repository.user_file_exists(
            file_type=UserDocument.DOCUMENT_BACK,
            unique_id=user_unique_id,
            bucket_name=OnboardingSteps.bucket_name,
        )
        user_document_exists = all(
            await asyncio.gather(user_document_front_exists, user_document_back_exists)
        )

        user = await cls.user_repository.find_user({"unique_id": user_unique_id})
        onboarding_step_builder = cls.steps_builder(user)

        onboarding_steps = await onboarding_step_builder.build(
            document_exists=user_document_exists
        )

        return onboarding_steps
