import { httpClient } from "./httpClient";

export interface HealthResponse {
  status: string;
}

export async function checkHealth(): Promise<HealthResponse> {
  const response = await httpClient.get<HealthResponse>("/health");

  return response.data;
}
