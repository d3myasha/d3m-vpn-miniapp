/** Компонент Footer с навигацией */

import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

export const Footer: React.FC = () => {
  const location = useLocation();
  const [theme, setTheme] = useState<Record<string, string>>({});

  useEffect(() => {
    const tg = window.Telegram?.WebApp;
    if (tg) {
      setTheme(tg.themeParams);
    }
  }, []);

  const navItems = [
    { path: '/', label: 'Главная', icon: '🏠' },
    { path: '/subscription', label: 'Подписка', icon: '📦' },
    { path: '/devices', label: 'Устройства', icon: '📱' },
    { path: '/plans', label: 'Тарифы', icon: '💎' },
    { path: '/profile', label: 'Профиль', icon: '👤' },
  ];

  return (
    <nav
      className="fixed-bottom py-2 px-3"
      style={{
        backgroundColor: theme.secondary_bg_color || '#fff',
        borderTop: '1px solid rgba(0,0,0,0.1)',
      }}
    >
      <div className="d-flex justify-content-around">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className="text-decoration-none text-center"
              style={{
                color: isActive
                  ? theme.button_color || '#0d6efd'
                  : theme.text_color || '#6c757d',
                fontSize: '0.75rem',
              }}
            >
              <div style={{ fontSize: '1.25rem' }}>{item.icon}</div>
              <div>{item.label}</div>
            </Link>
          );
        })}
      </div>
    </nav>
  );
};
