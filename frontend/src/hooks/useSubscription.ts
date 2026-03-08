/** Custom hook для подписок */

import { useState, useCallback, useEffect } from 'react';
import apiClient from '../api';
import { Subscription } from '../types';
import { useAppStore } from '../store';

export function useSubscription() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const subscription = useAppStore((state) => state.subscription);
  const setSubscription = useAppStore((state) => state.setSubscription);

  const fetchSubscription = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.get<Subscription | null>('/subscriptions/active');
      const data = response.data;
      setSubscription(data);
      return data;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка загрузки подписки';
      setError(message);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [setSubscription]);

  const renewSubscription = useCallback(async (subscriptionId: number, days: number = 30) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.post<Subscription>(
        `/subscriptions/${subscriptionId}/renew?days=${days}`
      );
      setSubscription(response.data);
      return response.data;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка продления подписки';
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  }, [setSubscription]);

  const getTrafficUsage = useCallback(async (subscriptionId: number) => {
    try {
      const response = await apiClient.get(`/subscriptions/${subscriptionId}/traffic`);
      return response.data;
    } catch (err) {
      console.error('Traffic usage error:', err);
      return null;
    }
  }, []);

  useEffect(() => {
    if (!subscription) {
      fetchSubscription();
    }
  }, []);

  return {
    subscription,
    isLoading,
    error,
    fetchSubscription,
    renewSubscription,
    getTrafficUsage,
  };
}
