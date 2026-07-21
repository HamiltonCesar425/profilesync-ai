import type { Profile, ProfilePayload } from "../types/profile";
import { httpClient } from "./httpClient";

async function fetchProfiles(): Promise<Profile[]> {
  const response = await httpClient.get<Profile[]>("/profiles");

  return response.data;
}

let profilesRequest: Promise<Profile[]> | null = null;

export function listProfiles(): Promise<Profile[]> {
  if (profilesRequest === null) {
    profilesRequest = fetchProfiles().finally(() => {
      profilesRequest = null;
    });
  }

  return profilesRequest;
}

export async function getProfile(profileId: number): Promise<Profile> {
  const response = await httpClient.get<Profile>(`/profiles/${profileId}`);

  return response.data;
}

export async function createProfile(payload: ProfilePayload): Promise<Profile> {
  const response = await httpClient.post<Profile>("/profiles", payload);

  return response.data;
}

export async function updateProfile(
  profileId: number,
  payload: ProfilePayload,
): Promise<Profile> {
  const response = await httpClient.put<Profile>(
    `/profiles/${profileId}`,
    payload,
  );

  return response.data;
}

export async function deleteProfile(profileId: number): Promise<void> {
  await httpClient.delete(`/profiles/${profileId}`);
}
