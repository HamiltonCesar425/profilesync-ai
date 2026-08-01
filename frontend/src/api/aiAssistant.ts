import { httpClient } from "./httpClient";

interface ImproveProfessionalDescriptionRequest {
  text: string;
}

interface ImproveProfessionalDescriptionResponse {
  improved_description: string;
}

export async function improveProfessionalDescription(
  description: string,
): Promise<string> {
  const normalizedDescription = description.trim();

  if (!normalizedDescription) {
    throw new Error("A descrição profissional não pode estar vazia.");
  }

  const payload: ImproveProfessionalDescriptionRequest = {
    text: normalizedDescription,
  };

  const response =
    await httpClient.post<ImproveProfessionalDescriptionResponse>(
      "/ai-assistant/improve-professional-description",
      payload,
    );

  return response.data.improved_description;
}
