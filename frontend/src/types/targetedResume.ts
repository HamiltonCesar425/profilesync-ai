export type ResumeSection =
  | "SUMMARY"
  | "EXPERIENCE"
  | "PROJECTS"
  | "TECHNOLOGIES";

export type FactName =
  | "full_name"
  | "professional_title"
  | "summary"
  | "location"
  | "linkedin_url"
  | "github_url"
  | "company_name"
  | "position"
  | "employment_type"
  | "work_model"
  | "description"
  | "start_date"
  | "end_date"
  | "is_current"
  | "project_name"
  | "role"
  | "repository_url"
  | "demo_url"
  | "technology_name"
  | "category"
  | "proficiency_level"
  | "years_experience";

export type FactualSourceType =
  | "profile"
  | "professional_experience"
  | "project"
  | "technology";

export interface TargetedResumePreviewRequest {
  profile_id: number;
  job_id: number;
}

export interface SourceReference {
  source_type: FactualSourceType;
  source_id: number;
}

export interface FactualValue {
  name: FactName;
  value: string | number | boolean;
}

export interface FactualBlock {
  section: ResumeSection;
  facts: FactualValue[];
  provenance: SourceReference[];
}

export interface TargetedResumeComposition {
  profile_id: number;
  job_id: number;
  ruleset_version: string;
  blocks: FactualBlock[];
  source_manifest: SourceReference[];
}

export interface TargetedResumePreviewResponse {
  preview_id: string;
  state: "preview";
  composition: TargetedResumeComposition;
}
