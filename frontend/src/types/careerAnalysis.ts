export interface RegisteredJobAnalysisRequest {
  profile_id: number;
}

export interface DetectedCompetenciesResponse {
  profile_id: number;
  competencies: string[];
}

export interface ImpactRecommendation {
  skill: string;
  priority: string;
  impact_score: number;
  reason: string;
}

export interface CareerActionItem {
  priority: number;
  title: string;
  description: string;
  impact_score: number;
  estimated_effort: string;
  category: string;
}

export interface CareerActionPlan {
  current_score: number;
  estimated_score_after_actions: number;
  actions: CareerActionItem[];
}

export interface CareerAnalysis {
  target_role: string;
  compatibility_score: number;
  strengths: string[];
  gaps: string[];
  recommendations: ImpactRecommendation[];
  action_plan: CareerActionPlan;
}
