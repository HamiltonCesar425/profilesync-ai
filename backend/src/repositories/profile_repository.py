from domain.profile import Profile

class ProfileRepository:
    def __init__(sef) -> None:
        self._profiles: list[Profile] = []
        self._next_id =1

    def create(
            self,
            full_name: str,
            professional_title: str,
            summary: str,
            location: str | None = None,
            linkedin_url: str | None = None,
            github_url: str | None = None,
    
    ) -> Profile:
        
        profile = Profile(
            id=self._next_id,
            full_name=full_name,
            professional_title=professional_title,
            summary=summary,
            location=location,
            linkedin_url=linkedin_url,
            github_url=github_url,
        )
        self._profiles.append(profile)
        self._next_id += 1
        return profile
    
    def list_all(self) -> list[Profile]:
        return self._profiles.copy()
    
    def get_by_id(self, profile_id: int) -> Profile | None:
        for profile in self._profiles:
            if profile.id == profile_id:
                return profile
        return None