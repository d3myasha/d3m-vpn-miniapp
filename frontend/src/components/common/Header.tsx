/** Компонент Header */

import React, { useEffect, useState } from 'react';
import { useAppStore } from '../../store';
import { TelegramWebApp } from '../../types';

interface HeaderProps {
  title?: string;
  showBack?: boolean;
  onBack?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  title = 'D3M VPN',
  showBack = false,
  onBack,
}) => {
  const user = useAppStore((state) => state.user);
  const [theme, setTheme] = useState<Record<string, string>>({});

  useEffect(() => {
    const tg = window.Telegram?.WebApp;
    if (tg) {
      setTheme(tg.themeParams);
      tg.ready();
    }
  }, []);

  return (
    <header
      className="py-3 px-3 mb-3"
      style={{
        backgroundColor: theme.secondary_bg_color || '#f8f9fa',
        borderBottom: '1px solid rgba(0,0,0,0.1)',
      }}
    >
      <div className="d-flex align-items-center justify-content-between">
        <div className="d-flex align-items-center gap-2">
          {showBack && (
            <button
              className="btn btn-link p-0 text-decoration-none"
              onClick={onBack}
              style={{ color: theme.text_color || '#000' }}
            >
              ←
            </button>
          )}
          <h5 className="m-0 fw-bold" style={{ color: theme.text_color || '#000' }}>
            {title}
          </h5>
        </div>
        {user && (
          <div className="d-flex align-items-center gap-2">
            <span
              className="badge"
              style={{
                backgroundColor: theme.button_color || '#0d6efd',
                color: theme.button_text_color || '#fff',
              }}
            >
              {user.points} ⭐
            </span>
          </div>
        )}
      </div>
    </header>
  );
};
