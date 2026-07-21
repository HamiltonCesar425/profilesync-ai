export interface Profile {
  id: number;
  user_id: number;
  full_name: string;
  professional_title: string;
  summary: string;
  location: string | null;
  linkedin_url: string | null;
  github_url: string | null;
}

export interface ProfilePayload {
  full_name: string;
  professional_title: string;
  summary: string;
  location: string | null;
  linkedin_url: string | null;
  github_url: string | null;
}
