/** Custom hook для устройств */

import { useState, useCallback } from 'react';
import apiClient from '../api';
import { Device } from '../types';
import { useAppStore } from '../store';

export function useDevices() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const devices = useAppStore((state) => state.devices);
  const setDevices = useAppStore((state) => state.setDevices);

  const fetchDevices = useCallback(async (subscriptionId?: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const params = subscriptionId ? { subscription_id: subscriptionId } : {};
      const response = await apiClient.get<Device[]>('/devices', { params });
      setDevices(response.data);
      return response.data;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка загрузки устройств';
      setError(message);
      return [];
    } finally {
      setIsLoading(false);
    }
  }, [setDevices]);

  const addDevice = useCallback(async (name: string, subscriptionId?: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const params = subscriptionId ? { subscription_id: subscriptionId } : {};
      const response = await apiClient.post<Device>('/devices', { name }, { params });
      setDevices([...devices, response.data]);
      return response.data;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка добавления устройства';
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  }, [devices, setDevices]);

  const removeDevice = useCallback(async (deviceId: number, subscriptionId?: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const params = subscriptionId ? { subscription_id: subscriptionId } : {};
      await apiClient.delete(`/devices/${deviceId}`, { params });
      setDevices(devices.filter((d) => d.id !== deviceId));
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка удаления устройства';
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  }, [devices, setDevices]);

  const resetDevices = useCallback(async (subscriptionId?: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const params = subscriptionId ? { subscription_id: subscriptionId } : {};
      await apiClient.post('/devices/reset', null, { params });
      setDevices([]);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка сброса устройств';
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  }, [setDevices]);

  return {
    devices,
    isLoading,
    error,
    fetchDevices,
    addDevice,
    removeDevice,
    resetDevices,
  };
}
