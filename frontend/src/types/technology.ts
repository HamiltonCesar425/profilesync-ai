export interface Technology {
  id: number;
  profile_id: number;
  name: string;
  category: string;
  proficiency_level: string;
  years_experience: number | null;
}

export interface TechnologyCreate {
  name: string;
  category: string;
  proficiency_level: string;
  years_experience: number | null;
}

export type TechnologyUpdate = Partial<TechnologyCreate>;
