from sqlalchemy.orm import Session

from domain.profile import Profile
from models.profile_model import ProfileModel


class ProfileRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        full_name: str,
        professional_title: str,
        summary: str,
        location: str | None = None,
        linkedin_url: str | None = None,
        github_url: str | None = None,
    ) -> Profile:
        profile_model = ProfileModel(
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

    def list_all(self) -> list[Profile]:
        profiles = self.db.query(ProfileModel).all()

        return [self._to_domain(profile) for profile in profiles]

    def get_by_id(self, profile_id: int) -> Profile | None:
        profile = (
            self.db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
        )

        if profile is None:
            return None

        return self._to_domain(profile)

    @staticmethod
    def _to_domain(profile_model: ProfileModel) -> Profile:
        return Profile(
            id=profile_model.id,
            full_name=profile_model.full_name,
            professional_title=profile_model.professional_title,
            summary=profile_model.summary,
            location=profile_model.location,
            linkedin_url=profile_model.linkedin_url,
            github_url=profile_model.github_url,
        )
