const ACCESS_TOKEN_KEY = "profilesync_access_token";

export const AUTH_CHANGED_EVENT = "profilesync:auth-changed";

export type AccessTokenRemovalReason = "logout" | "session-invalidated";

interface AuthChangedDetail {
  reason: "authenticated" | AccessTokenRemovalReason;
}

function notifyAuthChanged(reason: AuthChangedDetail["reason"]): void {
  window.dispatchEvent(
    new CustomEvent<AuthChangedDetail>(AUTH_CHANGED_EVENT, {
      detail: { reason },
    }),
  );
}

export function getAccessToken(): string | null {
  return sessionStorage.getItem(ACCESS_TOKEN_KEY);
}

export function setAccessToken(token: string): void {
  sessionStorage.setItem(ACCESS_TOKEN_KEY, token);
  notifyAuthChanged("authenticated");
}

export function removeAccessToken(
  reason: AccessTokenRemovalReason = "logout",
): void {
  sessionStorage.removeItem(ACCESS_TOKEN_KEY);
  notifyAuthChanged(reason);
}
