/** Custom hook для аутентификации */

import { useState, useCallback } from 'react';
import apiClient from '../api';
import { TokenResponse, User } from '../types';
import { useAppStore } from '../store';

export function useAuth() {
  const [isAuthenticating, setIsAuthenticating] = useState(false);
  const setUser = useAppStore((state) => state.setUser);

  const initAuth = useCallback(async (initData: Record<string, unknown>) => {
    setIsAuthenticating(true);
    try {
      const response = await apiClient.post<TokenResponse>('/auth/init', initData);
      localStorage.setItem('access_token', response.data.access_token);

      // Получаем данные пользователя
      const userResponse = await apiClient.get<User>('/auth/me');
      setUser(userResponse.data);

      return response.data;
    } catch (error) {
      console.error('Auth error:', error);
      throw error;
    } finally {
      setIsAuthenticating(false);
    }
  }, [setUser]);

  const logout = useCallback(async () => {
    try {
      await apiClient.post('/auth/logout');
    } finally {
      localStorage.removeItem('access_token');
      setUser(null);
    }
  }, [setUser]);

  return {
    initAuth,
    logout,
    isAuthenticating,
  };
}
