/** API клиент */

import axios, { AxiosInstance, AxiosError } from 'axios';

const API_BASE_URL = '/api/v1';

// Создаём axios инстанс
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Добавляем интерцептор для авторизации
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Добавляем Telegram ID из WebApp
    if (window.Telegram?.WebApp?.initDataUnsafe?.user?.id) {
      config.headers['X-Telegram-ID'] = String(
        window.Telegram.WebApp.initDataUnsafe.user.id
      );
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Обработка ошибок
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Токен истёк - очищаем и перенаправляем
      localStorage.removeItem('access_token');
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

export default apiClient;
