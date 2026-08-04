import { httpClient } from "./httpClient";

import type {
  CareerAnalysis,
  DetectedCompetenciesResponse,
  RegisteredJobAnalysisRequest,
} from "../types/careerAnalysis";

export async function analyzeRegisteredJob(
  jobId: number,
  analysisData: RegisteredJobAnalysisRequest,
): Promise<CareerAnalysis> {
  const response = await httpClient.post<CareerAnalysis>(
    `/career-intelligence/jobs/${jobId}/analyze`,
    analysisData,
  );

  return response.data;
}

export async function getDetectedCompetencies(
  profileId: number,
): Promise<DetectedCompetenciesResponse> {
  const response = await httpClient.get<DetectedCompetenciesResponse>(
    `/career-intelligence/profiles/${profileId}/competencies`,
  );

  return response.data;
}
