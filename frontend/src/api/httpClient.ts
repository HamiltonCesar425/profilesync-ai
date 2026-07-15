import axios from "axios";

import { authTokenStorage } from "../services/authTokenStorange";

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
    "Content-Type": "application/json",
  },
});

httpClient.interceptors.request.use((config) => {
  const accessToken = authTokenStorage.get();

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  return config;
});
