from sqlalchemy.orm import Session

from domain.profile import Profile
from models.profile_model import ProfileModel


class ProfileRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        user_id: int,
        full_name: str,
        professional_title: str,
        summary: str,
        location: str | None = None,
        linkedin_url: str | None = None,
        github_url: str | None = None,
    ) -> Profile:
        profile_model = ProfileModel(
            user_id=user_id,
            full_name=full_name,
            professional_title=professional_title,
            summary=summary,
            location=location,
            linkedin_url=linkedin_url,
            github_url=github_url,
        )

        self.db.add(profile_model)
        self.db.commit()
        self.db.refresh(profile_model)

        return self._to_domain(profile_model)

    def list_by_user_id(self, user_id: int) -> list[Profile]:
        profiles = (
            self.db.query(ProfileModel).filter(ProfileModel.user_id == user_id).all()
        )

        return [self._to_domain(profile) for profile in profiles]

    def get_by_id_and_user_id(
        self,
        profile_id: int,
        user_id: int,
    ) -> Profile | None:
        profile = (
            self.db.query(ProfileModel)
            .filter(
                ProfileModel.id == profile_id,
                ProfileModel.user_id == user_id,
            )
            .first()
        )

        if profile is None:
            return None

        return self._to_domain(profile)

    def update(
        self,
        profile_id: int,
        user_id: int,
        full_name: str,
        professional_title: str,
        summary: str,
        location: str | None = None,
        linkedin_url: str | None = None,
        github_url: str | None = None,
    ) -> Profile | None:
        profile_model = (
            self.db.query(ProfileModel)
            .filter(
                ProfileModel.id == profile_id,
                ProfileModel.user_id == user_id,
            )
            .first()
        )

        if profile_model is None:
            return None

        profile_model.full_name = full_name
        profile_model.professional_title = professional_title
        profile_model.summary = summary
        profile_model.location = location
        profile_model.linkedin_url = linkedin_url
        profile_model.github_url = github_url

        self.db.commit()
        self.db.refresh(profile_model)

        return self._to_domain(profile_model)

    def delete(
        self,
        profile_id: int,
        user_id: int,
    ) -> bool:
        profile_model = (
            self.db.query(ProfileModel)
            .filter(
                ProfileModel.id == profile_id,
                ProfileModel.user_id == user_id,
            )
            .first()
        )

        if profile_model is None:
            return False

        self.db.delete(profile_model)
        self.db.commit()

        return True

    @staticmethod
    def _to_domain(profile_model: ProfileModel) -> Profile:
        return Profile(
            id=profile_model.id,
            user_id=profile_model.user_id,
            full_name=profile_model.full_name,
            professional_title=profile_model.professional_title,
            summary=profile_model.summary,
            location=profile_model.location,
            linkedin_url=profile_model.linkedin_url,
            github_url=profile_model.github_url,
        )
