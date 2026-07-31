import { httpClient } from "./httpClient";

import type {
  CareerAnalysis,
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
