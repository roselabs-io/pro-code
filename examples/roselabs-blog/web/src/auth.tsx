import { createContext, useContext, useMemo, useState, type ReactNode } from "react";

import { getToken, login as apiLogin, setToken } from "./api";

interface AuthContextValue {
  isAuthed: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setTok] = useState<string | null>(() => getToken());

  const value = useMemo<AuthContextValue>(
    () => ({
      isAuthed: Boolean(token),
      login: async (email, password) => {
        const next = await apiLogin(email, password);
        setToken(next);
        setTok(next);
      },
      logout: () => {
        setToken(null);
        setTok(null);
      },
    }),
    [token],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}
