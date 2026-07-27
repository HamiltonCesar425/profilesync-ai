export interface Project {
  id: number;
  profile_id: number;
  name: string;
  description: string | null;
  role: string | null;
  repository_url: string | null;
  demo_url: string | null;
  start_date: string | null;
  end_date: string | null;
  is_current: boolean;
  created_at: string;
  update_at: string;
}

export interface ProjectCreate {
  profile_id: number;
  name: string;
  description?: string | null;
  role?: string | null;
  repository_url?: string | null;
  demo_url?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  is_current?: boolean;
}

export interface ProjectUpdate {
  name?: string;
  description?: string | null;
  role?: string | null;
  repository_url?: string | null;
  demo_url?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  is_current?: boolean;
}
