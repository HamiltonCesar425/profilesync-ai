import { httpClient } from "./httpClient";

import type { Job, JobCreate } from "../types/job";

export async function createJob(jobData: JobCreate): Promise<Job> {
  const response = await httpClient.post<Job>("/jobs", jobData);

  return response.data;
}

export async function listJobs(): Promise<Job[]> {
  const response = await httpClient.get<Job[]>("/jobs");

  return response.data;
}
