const ACCESS_TOKEN_KEY = "profilesync_access_token";

export const AUTH_CHANGED_EVENT = "profilesync:auth-changed";

function notifyAuthChanged(): void {
  window.dispatchEvent(new Event(AUTH_CHANGED_EVENT));
}

export function getAccessToken(): string | null {
  return sessionStorage.getItem(ACCESS_TOKEN_KEY);
}

export function setAccessToken(token: string): void {
  sessionStorage.setItem(ACCESS_TOKEN_KEY, token);
  notifyAuthChanged();
}

export function removeAccessToken(): void {
  sessionStorage.removeItem(ACCESS_TOKEN_KEY);
  notifyAuthChanged();
}
