import type {
  ProfessionalExperience,
  ProfessionalExperienceCreate,
  ProfessionalExperienceUpdate,
} from "../types/professionalExperience";
import { httpClient } from "./httpClient";

const pendingListRequests = new Map<
  number,
  Promise<ProfessionalExperience[]>
>();

export function listProfessionalExperiences(
  profileId: number,
): Promise<ProfessionalExperience[]> {
  const pendingRequest = pendingListRequests.get(profileId);

  if (pendingRequest) {
    return pendingRequest;
  }

  const request = httpClient
    .get<ProfessionalExperience[]>(`/profiles/${profileId}/experiences`)
    .then((response) => response.data)
    .finally(() => {
      pendingListRequests.delete(profileId);
    });

  pendingListRequests.set(profileId, request);

  return request;
}

export async function getProfessionalExperience(
  profileId: number,
  experienceId: number,
): Promise<ProfessionalExperience> {
  const response = await httpClient.get<ProfessionalExperience>(
    `/profiles/${profileId}/experiences/${experienceId}`,
  );

  return response.data;
}

export async function createProfessionalExperience(
  profileId: number,
  experience: ProfessionalExperienceCreate,
): Promise<ProfessionalExperience> {
  const response = await httpClient.post<ProfessionalExperience>(
    `/profiles/${profileId}/experiences`,
    experience,
  );

  return response.data;
}

export async function updateProfessionalExperience(
  profileId: number,
  experienceId: number,
  experience: ProfessionalExperienceUpdate,
): Promise<ProfessionalExperience> {
  const response = await httpClient.put<ProfessionalExperience>(
    `/profiles/${profileId}/experiences/${experienceId}`,
    experience,
  );

  return response.data;
}

export async function deleteProfessionalExperience(
  profileId: number,
  experienceId: number,
): Promise<void> {
  await httpClient.delete(`/profiles/${profileId}/experiences/${experienceId}`);
}
