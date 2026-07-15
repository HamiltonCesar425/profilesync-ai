const ACCESS_TOKEN_KEY = "profilesync_access_token";

export const authTokenStorage = {
  get(): string | null {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  },

  set(token: string): void {
    localStorage.setItem(ACCESS_TOKEN_KEY, token);
  },

  remove(): void {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
  },
};
