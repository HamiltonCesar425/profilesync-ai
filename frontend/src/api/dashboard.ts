import { httpClient } from "./httpClient";

export interface ProfileResponse {
  id: number;
  user_id: number;
  full_name: string;
  professional_title: string;
  summary: string;
  location: string | null;
  linkedin_url: string | null;
  github_url: string | null;
}

export interface TechnologyResponse {
  id: number;
  profile_id: number;
  name: string;
  category: string;
  proficiency_level: string;
  years_experience: number | null;
}

export interface ProfessionalDiagnosis {
  score: number;
  strengths: string[];
  improvements: string[];
  recommendations: string[];
}

export interface CareerActionItem {
  priority: number;
  title: string;
  description: string;
  impact_score: number;
  estimated_effort: string;
  category: string;
}

export interface CareerActionPlanResponse {
  current_score: number;
  estimated_score_after_actions: number;
  actions: CareerActionItem[];
}

export interface ImpactRecommendation {
  title: string;
  description: string;
  impact_score: number;
}

export interface CareerGoalRequest {
  target_role: string;
  description: string | null;
  skills: string[];
  seniority: string | null;
}

export interface CareerAnalysisResponse {
  target_role: string;
  compatibility_score: number;
  strengths: string[];
  gaps: string[];
  recommendations: ImpactRecommendation[];
  action_plan: CareerActionPlanResponse;
}

interface ResourceResponse {
  id: number;
}

export interface DashboardData {
  profile: ProfileResponse | null;

  profileSummary: {
    completionPercentage: number;
    experiencesCount: number;
    projectsCount: number;
    technologiesCount: number;
  };

  profileDiagnosis: ProfessionalDiagnosis | null;
  careerAnalysis: CareerAnalysisResponse | null;

  profileScore: number;
  recommendations: string[];
  actions: string[];
}

const EMPTY_DASHBOARD_DATA: DashboardData = {
  profile: null,

  profileSummary: {
    completionPercentage: 0,
    experiencesCount: 0,
    projectsCount: 0,
    technologiesCount: 0,
  },

  profileDiagnosis: null,
  careerAnalysis: null,

  profileScore: 0,
  recommendations: [],
  actions: [],
};

function calculateCompletionPercentage(
  profile: ProfileResponse,
  technologiesCount: number,
  projectsCount: number,
  experiencesCount: number,
): number {
  const completionCriteria = [
    profile.full_name.trim().length > 0,
    profile.professional_title.trim().length > 0,
    profile.summary.trim().length > 0,
    Boolean(profile.location?.trim()),
    Boolean(profile.linkedin_url?.trim()),
    Boolean(profile.github_url?.trim()),
    technologiesCount > 0,
    projectsCount > 0,
    experiencesCount > 0,
  ];

  const completedCriteria = completionCriteria.filter(Boolean).length;

  return Math.round((completedCriteria / completionCriteria.length) * 100);
}

async function getProfiles(): Promise<ProfileResponse[]> {
  const response = await httpClient.get<ProfileResponse[]>("/profiles");

  return response.data;
}

async function getProfileTechnologies(
  profileId: number,
): Promise<TechnologyResponse[]> {
  const response = await httpClient.get<TechnologyResponse[]>(
    `/technologies/profiles/${profileId}`,
  );

  return response.data;
}

async function getProfileProjects(
  profileId: number,
): Promise<ResourceResponse[]> {
  const response = await httpClient.get<ResourceResponse[]>(
    `/projects/profile/${profileId}`,
  );

  return response.data;
}

async function getProfileExperiences(
  profileId: number,
): Promise<ResourceResponse[]> {
  const response = await httpClient.get<ResourceResponse[]>(
    `/profiles/${profileId}/experiences`,
  );

  return response.data;
}

async function getProfileDiagnosis(
  profile: ProfileResponse,
): Promise<ProfessionalDiagnosis> {
  const response = await httpClient.post<ProfessionalDiagnosis>(
    "/profile-intelligence/analyze",
    null,
    {
      params: {
        profile_id: profile.id,
        target_role: profile.professional_title,
      },
    },
  );

  return response.data;
}

async function getCareerAnalysis(
  profile: ProfileResponse,
  technologies: TechnologyResponse[],
): Promise<CareerAnalysisResponse> {
  const request: CareerGoalRequest = {
    target_role: profile.professional_title,
    description: profile.summary || null,
    skills: technologies.map((technology) => technology.name),
    seniority: null,
  };

  const response = await httpClient.post<CareerAnalysisResponse>(
    "/career-intelligence/analyze",
    request,
  );

  return response.data;
}

async function loadDashboardData(): Promise<DashboardData> {
  const profiles = await getProfiles();
  const profile = profiles[0] ?? null;

  if (profile === null) {
    return EMPTY_DASHBOARD_DATA;
  }

  const [technologies, projects, experiences] = await Promise.all([
    getProfileTechnologies(profile.id),
    getProfileProjects(profile.id),
    getProfileExperiences(profile.id),
  ]);

  const [profileDiagnosis, careerAnalysis] = await Promise.all([
    getProfileDiagnosis(profile),
    getCareerAnalysis(profile, technologies),
  ]);

  return {
    profile,

    profileSummary: {
      completionPercentage: calculateCompletionPercentage(
        profile,
        technologies.length,
        projects.length,
        experiences.length,
      ),
      experiencesCount: experiences.length,
      projectsCount: projects.length,
      technologiesCount: technologies.length,
    },

    profileDiagnosis,
    careerAnalysis,

    profileScore: profileDiagnosis.score,
    recommendations: profileDiagnosis.recommendations,
    actions: careerAnalysis.action_plan.actions.map((action) => action.title),
  };
}

let dashboardDataRequest: Promise<DashboardData> | null = null;

export function getDashboardData(): Promise<DashboardData> {
  if (dashboardDataRequest === null) {
    dashboardDataRequest = loadDashboardData().finally(() => {
      dashboardDataRequest = null;
    });
  }

  return dashboardDataRequest;
}
