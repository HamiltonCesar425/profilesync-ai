from models.resume_model import Resume
from repositories.profile_repository import ProfileRepository
from repositories.resume_repository import ResumeRepository
from schemas.resume_schema import ResumeCreate, ResumeUpdate


class ResumeService:
    def __init__(
        self,
        resume_repository: ResumeRepository,
        profile_repository: ProfileRepository,
    ) -> None:
        self.resume_repository = resume_repository
        self.profile_repository = profile_repository

    def create_resume(
        self,
        resume_data: ResumeCreate,
        user_id: int,
    ) -> Resume:
        profile = self.profile_repository.get_by_id_and_user_id(
            resume_data.profile_id,
            user_id,
        )

        if profile is None:
            raise ValueError("Profile not found")

        resume = Resume(
            **resume_data.model_dump(),
            user_id=user_id,
        )
        return self.resume_repository.create(resume)

    def list_resumes_by_profile(
        self,
        profile_id: int,
        user_id: int,
    ) -> list[Resume]:
        profile = self.profile_repository.get_by_id_and_user_id(
            profile_id,
            user_id,
        )

        if profile is None:
            raise ValueError("Profile not found")

        return self.resume_repository.list_by_profile_id(profile_id)

    def get_resume(
        self,
        resume_id: int,
        profile_id: int,
        user_id: int,
    ) -> Resume:
        profile = self.profile_repository.get_by_id_and_user_id(
            profile_id,
            user_id,
        )

        if profile is None:
            raise ValueError("Profile not found")

        resume = self.resume_repository.get_by_id_and_profile_id(
            resume_id,
            profile_id,
        )

        if resume is None:
            raise ValueError("Resume not found")

        return resume

    def update_resume(
        self,
        resume_id: int,
        profile_id: int,
        resume_data: ResumeUpdate,
        user_id: int,
    ) -> Resume:
        resume = self.get_resume(
            resume_id=resume_id,
            profile_id=profile_id,
            user_id=user_id,
        )

        update_data = resume_data.model_dump(exclude_unset=True)

        return self.resume_repository.update(
            resume=resume,
            data=update_data,
        )

    def delete_resume(
        self,
        resume_id: int,
        profile_id: int,
        user_id: int,
    ) -> None:
        resume = self.get_resume(
            resume_id=resume_id,
            profile_id=profile_id,
            user_id=user_id,
        )

        self.resume_repository.delete(resume)
