/** Store для управления состоянием */

import { create } from 'zustand';
import { User, Subscription, Device, Plan } from '../types';

interface AppState {
  // Пользователь
  user: User | null;
  setUser: (user: User | null) => void;

  // Подписка
  subscription: Subscription | null;
  setSubscription: (subscription: Subscription | null) => void;

  // Устройства
  devices: Device[];
  setDevices: (devices: Device[]) => void;

  // Планы
  plans: Plan[];
  setPlans: (plans: Plan[]) => void;

  // Загрузка
  isLoading: boolean;
  setLoading: (loading: boolean) => void;

  // Ошибка
  error: string | null;
  setError: (error: string | null) => void;

  // Очистка состояния
  clearState: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Пользователь
  user: null,
  setUser: (user) => set({ user }),

  // Подписка
  subscription: null,
  setSubscription: (subscription) => set({ subscription }),

  // Устройства
  devices: [],
  setDevices: (devices) => set({ devices }),

  // Планы
  plans: [],
  setPlans: (plans) => set({ plans }),

  // Загрузка
  isLoading: false,
  setLoading: (loading) => set({ isLoading: loading }),

  // Ошибка
  error: null,
  setError: (error) => set({ error: error }),

  // Очистка состояния
  clearState: () =>
    set({
      user: null,
      subscription: null,
      devices: [],
      plans: [],
      isLoading: false,
      error: null,
    }),
}));
