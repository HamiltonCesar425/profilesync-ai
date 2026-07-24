export interface ProfessionalExperience {
  id: number;
  profile_id: number;
  company_name: string;
  position: string;
  employment_type: string | null;
  work_model: string | null;
  location: string | null;
  description: string | null;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProfessionalExperienceCreate {
  company_name: string;
  position: string;
  employment_type: string | null;
  work_model: string | null;
  location: string | null;
  description: string | null;
  start_date: string | null;
  end_date: string | null;
  is_current: boolean;
}

export interface ProfessionalExperienceUpdate {
  company_name?: string;
  position?: string;
  employment_type?: string | null;
  work_model?: string | null;
  location?: string | null;
  description?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  is_current?: boolean;
}
