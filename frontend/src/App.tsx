/** Главный компонент приложения */

import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Home } from './pages/Home';
import { Subscription } from './pages/Subscription';
import { Devices } from './pages/Devices';
import { Plans } from './pages/Plans';
import { Profile } from './pages/Profile';
import { useAuth } from './hooks/useAuth';
import { useAppStore } from './store';
import { Loader } from './components/common/Loader';
import { Error } from './components/common/Error';

const AppContent: React.FC = () => {
  const user = useAppStore((state) => state.user);
  const { initAuth, isAuthenticating } = useAuth();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const tg = window.Telegram?.WebApp;
    if (!tg) {
      setError('Telegram WebApp не доступен');
      return;
    }

    // Инициализируем Telegram WebApp
    tg.ready();
    tg.expand();

    // Настраиваем цвета под тему Telegram
    document.documentElement.style.setProperty(
      '--tg-theme-bg-color',
      tg.themeParams.bg_color || '#ffffff'
    );
    document.documentElement.style.setProperty(
      '--tg-theme-text-color',
      tg.themeParams.text_color || '#000000'
    );
    document.documentElement.style.setProperty(
      '--tg-theme-button-color',
      tg.themeParams.button_color || '#0d6efd'
    );
    document.documentElement.style.setProperty(
      '--tg-theme-button-text-color',
      tg.themeParams.button_text_color || '#ffffff'
    );

    // Получаем initData для аутентификации
    const initDataUnsafe = tg.initDataUnsafe;
    if (initDataUnsafe?.user) {
      // Создаём объект с данными для API
      const initData: Record<string, unknown> = {
        user: initDataUnsafe.user,
        auth_date: Math.floor(Date.now() / 1000),
        hash: tg.initData.split('hash=')[1]?.split('&')[0] || '',
      };

      if (initDataUnsafe.query_id) {
        initData.query_id = initDataUnsafe.query_id;
      }

      if (initDataUnsafe.start_param) {
        initData.start_param = initDataUnsafe.start_param;
      }

      // Инициализируем аутентификацию
      initAuth(initData).catch((err) => {
        console.error('Auth error:', err);
        setError('Ошибка аутентификации');
      });
    } else {
      setError('Не удалось получить данные пользователя');
    }
  }, []);

  if (error) {
    return <Error message={error} fullScreen />;
  }

  if (!user || isAuthenticating) {
    return <Loader fullScreen text="Загрузка..." />;
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/subscription" element={<Subscription />} />
        <Route path="/devices" element={<Devices />} />
        <Route path="/plans" element={<Plans />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </BrowserRouter>
  );
};

const App: React.FC = () => {
  return <AppContent />;
};

export default App;
