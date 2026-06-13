from repositories.profile_repository import ProfileRepository
from domain.profile import Profile

class ProfileService:
    def __init__(
            self,
            repository: ProfileRepository
    ) -> None:
        self._repository = repository

    def create_profile(
            self,
            full_name: str,
            professional_title: str,
            summary: str,
            location: str | None = None,
            linkedin_url: str | None = None,
            github_url: str | None = None,
        
    ) -> Profile:
            
        return self._repository.create(
            full_name=full_name,
            professional_title=professional_title,
            summary=summary,
            location=location,
            linkedin_url=linkedin_url,
            github_url=github_url,
            
        )
        
    def list_profiles(self) -> list[Profile]:
        return self._repository.list_all()
    
    def get_profile(
            self,
            profile_id: int
    ) -> Profile | None:
        
        return self._repository.get_by_id(profile_id)