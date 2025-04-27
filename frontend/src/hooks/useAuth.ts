import { useState, useEffect, useCallback } from 'react';
import authService from '../services/authService';
import { User } from '../types/auth';

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchUser = useCallback(async () => {
    try {
      setLoading(true);
      const userData = await authService.getCurrentUser();
      setUser(userData);
      setError(null);
    } catch (err) {
      setError('Failed to fetch user data');
      setUser(null);
    } finally {
      setLoading(false);
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
    } catch (err) {
      setError('Logout failed');
    } finally {
      setLoading(false);
    }
  };

  const isAuthenticated = useCallback(async (): Promise<boolean> => {
    if (user) return true;
    try {
      const isAuth = await authService.isAuthenticated();
      if (isAuth && !user) {
        await fetchUser();
      }
      return isAuth;
    } catch (err) {
      return false;
    }
  }, [user, fetchUser]);

  return {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated,
    fetchUser
  };
};

export default useAuth; 