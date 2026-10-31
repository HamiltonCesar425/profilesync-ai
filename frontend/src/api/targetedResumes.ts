import type {
  TargetedResumePreviewRequest,
  TargetedResumePreviewResponse,
} from "../types/targetedResume";
import { httpClient } from "./httpClient";

export async function generateTargetedResumePreview(
  request: TargetedResumePreviewRequest,
): Promise<TargetedResumePreviewResponse> {
  const response = await httpClient.post<TargetedResumePreviewResponse>(
    "/targeted-resumes/preview",
    request,
  );

  return response.data;
}
