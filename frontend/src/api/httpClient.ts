import axios from "axios";

import { getAccessToken, removeAccessToken } from "../auth/tokenStorage";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

if (!apiBaseUrl) {
  throw new Error(
    "A variável de ambiente VITE_API_BASE_URL não está configurada.",
  );
}

export const httpClient = axios.create({
  baseURL: apiBaseUrl,
  timeout: 10_000,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

function getRequestAccessToken(error: unknown): string | null {
  if (!axios.isAxiosError(error)) {
    return null;
  }

  const authorization = error.config?.headers.get("Authorization");

  if (typeof authorization !== "string") {
    return null;
  }

  const match = /^Bearer\s+(\S+)$/i.exec(authorization.trim());
  return match?.[1] ?? null;
}

httpClient.interceptors.request.use((config) => {
  const accessToken = getAccessToken();

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  return config;
});

httpClient.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      const requestAccessToken = getRequestAccessToken(error);
      const currentAccessToken = getAccessToken();

      if (
        requestAccessToken &&
        currentAccessToken &&
        requestAccessToken === currentAccessToken
      ) {
        removeAccessToken("session-invalidated");
      }
    }

    return Promise.reject(error);
  },
);
