/** Страница профиля */

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Header } from '../components/common/Header';
import { Footer } from '../components/common/Footer';
import { User } from '../types';
import { useAppStore } from '../store';
import { Loader } from '../components/common/Loader';
import { formatDateTime } from '../utils/format';

export const Profile: React.FC = () => {
  const navigate = useNavigate();
  const user = useAppStore((state) => state.user);
  const setUser = useAppStore((state) => state.setUser);
  const [isLoading, setIsLoading] = useState(false);
  const [referralStats, setReferralStats] = useState<{
    total_referrals: number;
    referral_code: string;
    referral_link: string;
  } | null>(null);

  useEffect(() => {
    const fetchReferralStats = async () => {
      try {
        const response = await axios.get('/api/v1/users/me/referrals');
        setReferralStats(response.data);
      } catch (err) {
        console.error('Referral stats error:', err);
      }
    };

    fetchReferralStats();
  }, []);

  const handleCopyReferralLink = () => {
    if (referralStats?.referral_link) {
      navigator.clipboard.writeText(referralStats.referral_link);
      window.Telegram?.WebApp?.showAlert('Ссылка скопирована в буфер обмена');
    }
  };

  const handleLogout = () => {
    window.Telegram?.WebApp?.showConfirm(
      'Выйти из приложения?',
      async (ok: boolean) => {
        if (ok) {
          try {
            await axios.post('/api/v1/auth/logout');
          } finally {
            localStorage.removeItem('access_token');
            setUser(null);
            window.location.reload();
          }
        }
      }
    );
  };

  if (!user) {
    return <Loader fullScreen />;
  }

  return (
    <div className="pb-5 mb-5">
      <Header title="Профиль" showBack onBack={() => navigate(-1)} />

      <div className="px-3">
        {/* Основная информация */}
        <div className="card shadow-sm mb-3">
          <div className="card-body">
            <div className="d-flex align-items-center gap-3 mb-3">
              <div
                className="rounded-circle d-flex align-items-center justify-content-center"
                style={{
                  width: '60px',
                  height: '60px',
                  backgroundColor: '#0d6efd',
                  color: '#fff',
                  fontSize: '1.5rem',
                }}
              >
                {user.name.charAt(0).toUpperCase()}
              </div>
              <div>
                <h5 className="mb-0">{user.name}</h5>
                {user.username && (
                  <small className="text-muted">@{user.username}</small>
                )}
              </div>
            </div>

            <div className="row g-2">
              <div className="col-6">
                <div
                  className="p-2 rounded text-center"
                  style={{ backgroundColor: '#f8f9fa' }}
                >
                  <div className="fw-bold">{user.points}</div>
                  <small className="text-muted">Баллы</small>
                </div>
              </div>
              <div className="col-6">
                <div
                  className="p-2 rounded text-center"
                  style={{ backgroundColor: '#f8f9fa' }}
                >
                  <div className="fw-bold">{user.personal_discount}%</div>
                  <small className="text-muted">Скидка</small>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Детали */}
        <div className="card shadow-sm mb-3">
          <div className="card-body">
            <h6 className="card-title mb-3">Информация</h6>

            <div className="mb-2">
              <small className="text-muted">ID пользователя</small>
              <div className="fw-bold">{user.telegram_id}</div>
            </div>

            <div className="mb-2">
              <small className="text-muted">Роль</small>
              <div className="fw-bold text-capitalize">{user.role}</div>
            </div>

            <div className="mb-2">
              <small className="text-muted">Язык</small>
              <div className="fw-bold text-uppercase">{user.language}</div>
            </div>

            <div className="mb-2">
              <small className="text-muted">Зарегистрирован</small>
              <div className="fw-bold">{formatDateTime(user.created_at)}</div>
            </div>
          </div>
        </div>

        {/* Реферальная программа */}
        {referralStats && (
          <div className="card shadow-sm mb-3">
            <div className="card-body">
              <h6 className="card-title mb-3">👥 Реферальная программа</h6>

              <div className="mb-3">
                <small className="text-muted">Приглашено</small>
                <div className="fw-bold">{referralStats.total_referrals}</div>
              </div>

              <div>
                <small className="text-muted">Ваша ссылка</small>
                <div className="input-group mt-1">
                  <input
                    type="text"
                    className="form-control form-control-sm"
                    value={referralStats.referral_link}
                    readOnly
                  />
                  <button
                    className="btn btn-outline-primary btn-sm"
                    onClick={handleCopyReferralLink}
                  >
                    Копировать
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Настройки */}
        <div className="card shadow-sm mb-3">
          <div className="card-body">
            <h6 className="card-title mb-3">Настройки</h6>

            <button
              className="btn btn-outline-primary w-100 mb-2"
              onClick={() => {
                window.Telegram?.WebApp?.showAlert('Функция в разработке');
              }}
            >
              🔔 Уведомления
            </button>

            <button
              className="btn btn-outline-primary w-100 mb-2"
              onClick={() => {
                window.Telegram?.WebApp?.showAlert('Функция в разработке');
              }}
            >
              🌐 Язык
            </button>

            <a
              href={`https://t.me/${import.meta.env.VITE_BOT_SUPPORT_USERNAME || 'support'}`}
              className="btn btn-outline-success w-100 mb-2"
              target="_blank"
              rel="noopener noreferrer"
            >
              💬 Поддержка
            </a>
          </div>
        </div>

        {/* Выход */}
        <button
          className="btn btn-outline-danger w-100 mb-3"
          onClick={handleLogout}
        >
          🚪 Выйти
        </button>
      </div>

      <Footer />
    </div>
  );
};
