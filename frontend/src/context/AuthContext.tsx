import React, { createContext, useState, useEffect, useCallback, ReactNode, useRef } from 'react';
import authService from '../services/authService';
import { User } from '../types/auth';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
  isAuthenticated: () => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const fetchInProgress = useRef(false);
  const authChecked = useRef(false);

  const fetchUser = useCallback(async () => {
    if (!authService.isAuthenticated() || fetchInProgress.current || authChecked.current) {
      setLoading(false);
      return;
    }

    try {
      fetchInProgress.current = true;
      setLoading(true);
      const userData = await authService.getCurrentUser();
      setUser(userData);
      setError(null);
    } catch (err) {
      setError('Failed to fetch user data');
      setUser(null);
    } finally {
      setLoading(false);
      fetchInProgress.current = false;
      authChecked.current = true;
    }
  }, []);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      setLoading(true);
      const userData = await authService.login({ username, password });
      setUser(userData);
      setError(null);
      authChecked.current = true;
      return true;
    } catch (err) {
      setError('Invalid credentials');
      return false;
    } finally {
      setLoading(false);
    }
  };

  const logout = async (): Promise<void> => {
    try {
      setLoading(true);
      await authService.logout();
      setUser(null);
      authChecked.current = true;
    } catch (err) {
      setError('Logout failed');
    } finally {
      setLoading(false);
    }
  };

  const isAuthenticated = (): boolean => {
    return authService.isAuthenticated();
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        login,
        logout,
        isAuthenticated,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
