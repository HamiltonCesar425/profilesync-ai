import { httpClient } from "./httpClient";

import type {
  Technology,
  TechnologyCreate,
  TechnologyUpdate,
} from "../types/technology";

export async function createTechnology(
  profileId: number,
  technologyData: TechnologyCreate,
): Promise<Technology> {
  const response = await httpClient.post<Technology>(
    `/technologies/profiles/${profileId}`,
    technologyData,
  );

  return response.data;
}

export async function listProfileTechnologies(
  profileId: number,
): Promise<Technology[]> {
  const response = await httpClient.get<Technology[]>(
    `/technologies/profiles/${profileId}`,
  );

  return response.data;
}

export async function getTechnology(technologyId: number): Promise<Technology> {
  const response = await httpClient.get<Technology>(
    `/technologies/${technologyId}`,
  );

  return response.data;
}

export async function updateTechnology(
  technologyId: number,
  technologyData: TechnologyUpdate,
): Promise<Technology> {
  const response = await httpClient.put<Technology>(
    `/technologies/${technologyId}`,
    technologyData,
  );

  return response.data;
}

export async function deleteTechnology(technologyId: number): Promise<void> {
  await httpClient.delete(`/technologies/${technologyId}`);
}
