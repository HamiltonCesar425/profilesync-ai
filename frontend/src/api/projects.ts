import type { Project, ProjectCreate, ProjectUpdate } from "../types/project";
import { httpClient } from "./httpClient";

const pendingProjectRequests = new Map<string, Promise<Project[]>>();

export async function getProjectsByProfile(
  profileId: number,
): Promise<Project[]> {
  const requestKey = `projects-profile-${profileId}`;
  const pendingRequest = pendingProjectRequests.get(requestKey);

  if (pendingRequest) {
    return pendingRequest;
  }

  const request = httpClient
    .get<Project[]>(`/projects/profile/${profileId}`)
    .then((response) => response.data)
    .finally(() => {
      pendingProjectRequests.delete(requestKey);
    });

  pendingProjectRequests.set(requestKey, request);

  return request;
}

export async function getProject(
  profileId: number,
  projectId: number,
): Promise<Project> {
  const response = await httpClient.get<Project>(
    `/projects/${projectId}/profile/${profileId}`,
  );

  return response.data;
}

export async function createProject(
  projectData: ProjectCreate,
): Promise<Project> {
  const response = await httpClient.post<Project>("/projects", projectData);

  return response.data;
}

export async function updateProject(
  profileId: number,
  projectId: number,
  projectData: ProjectUpdate,
): Promise<Project> {
  const response = await httpClient.put<Project>(
    `/projects/${projectId}/profile/${profileId}`,
    projectData,
  );

  return response.data;
}

export async function deleteProject(
  profileId: number,
  projectId: number,
): Promise<void> {
  await httpClient.delete(`/projects/${projectId}/profile/${profileId}`);
}
