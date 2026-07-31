export interface JobBase {
  title: string;
  company: string | null;
  description: string;
}

export type JobCreate = JobBase;

export interface JobUpdate {
  title?: string;
  company?: string | null;
  description?: string;
}

export interface Job extends JobBase {
  id: number;
  user_id: number;
  created_at: string;
  updated_at: string;
}
