/** Главная страница */

import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Header } from '../components/common/Header';
import { useAppStore } from '../store';
import { useSubscription } from '../hooks/useSubscription';
import { SubscriptionCard } from '../components/subscription/SubscriptionCard';
import { TrafficUsage } from '../components/subscription/TrafficUsage';

export const Home: React.FC = () => {
  const user = useAppStore((state) => state.user);
  const { subscription, getTrafficUsage } = useSubscription();
  const [trafficUsage, setTrafficUsage] = useState<{
    used: number;
    limit: number;
    remaining: number;
    percentage: number;
  } | null>(null);

  useEffect(() => {
    if (subscription?.id) {
      getTrafficUsage(subscription.id).then(setTrafficUsage);
    }
  }, [subscription]);

  const quickActions = [
    { to: '/subscription', label: 'Подписка', icon: '📦', color: '#0d6efd' },
    { to: '/devices', label: 'Устройства', icon: '📱', color: '#198754' },
    { to: '/plans', label: 'Тарифы', icon: '💎', color: '#6f42c1' },
    { to: '/profile', label: 'Профиль', icon: '👤', color: '#fd7e14' },
  ];

  return (
    <div className="pb-5">
      <Header title="D3M VPN" />

      <div className="px-3">
        {/* Приветствие */}
        <div className="mb-4">
          <h4 className="mb-1">
            Привет, {user?.name.split(' ')[0] || 'Пользователь'}! 👋
          </h4>
          <p className="text-muted mb-0">Добро пожаловать в D3M VPN</p>
        </div>

        {/* Карточка подписки */}
        {subscription ? (
          <>
            <SubscriptionCard
              subscription={subscription}
              trafficUsage={trafficUsage || undefined}
            />

            {trafficUsage && subscription.traffic_limit > 0 && (
              <div className="mt-3">
                <TrafficUsage {...trafficUsage} />
              </div>
            )}
          </>
        ) : (
          <div className="card shadow-sm mb-3">
            <div className="card-body text-center py-4">
              <div style={{ fontSize: '3rem' }} className="mb-2">
                📦
              </div>
              <h5 className="mb-2">У вас нет активной подписки</h5>
              <p className="text-muted mb-3">
                Выберите тарифный план для подключения к VPN
              </p>
              <Link to="/plans" className="btn btn-primary">
                Выбрать тариф
              </Link>
            </div>
          </div>
        )}

        {/* Быстрые действия */}
        <div className="row g-2 mt-4">
          {quickActions.map((action) => (
            <div key={action.to} className="col-6">
              <Link
                to={action.to}
                className="text-decoration-none"
              >
                <div
                  className="card shadow-sm h-100"
                  style={{ border: 'none' }}
                >
                  <div className="card-body text-center py-3">
                    <div
                      style={{
                        fontSize: '2rem',
                        color: action.color,
                      }}
                    >
                      {action.icon}
                    </div>
                    <div className="fw-bold mt-1">{action.label}</div>
                  </div>
                </div>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
