/** Страница подписки */

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Header } from '../components/common/Header';
import { Footer } from '../components/common/Footer';
import { SubscriptionCard } from '../components/subscription/SubscriptionCard';
import { TrafficUsage } from '../components/subscription/TrafficUsage';
import { useSubscription } from '../hooks/useSubscription';
import { Loader } from '../components/common/Loader';
import { Error } from '../components/common/Error';

export const Subscription: React.FC = () => {
  const navigate = useNavigate();
  const { subscription, isLoading, error, fetchSubscription, getTrafficUsage } =
    useSubscription();
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

  const handleRenew = async () => {
    if (!subscription) return;

    window.Telegram?.WebApp?.showConfirm(
      'Продлить подписку на 30 дней?',
      async (ok: boolean) => {
        if (ok) {
          try {
            // TODO: реализовать продление через API
            window.Telegram?.WebApp?.showAlert('Функция продления в разработке');
          } catch (err) {
            window.Telegram?.WebApp?.showAlert('Ошибка продления подписки');
          }
        }
      }
    );
  };

  if (isLoading && !subscription) {
    return <Loader fullScreen />;
  }

  if (error && !subscription) {
    return <Error message={error || 'Ошибка загрузки'} onRetry={fetchSubscription} fullScreen />;
  }

  return (
    <div className="pb-5 mb-5">
      <Header title="Подписка" showBack onBack={() => navigate(-1)} />

      <div className="px-3">
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

            <div className="mt-3">
              <button
                className="btn btn-primary w-100 mb-2"
                onClick={handleRenew}
              >
                🔄 Продлить подписку
              </button>
              <a
                href={subscription.url}
                className="btn btn-outline-primary w-100"
                target="_blank"
                rel="noopener noreferrer"
              >
                🔗 Ключ подписки
              </a>
            </div>
          </>
        ) : (
          <div className="card shadow-sm">
            <div className="card-body text-center py-5">
              <div style={{ fontSize: '4rem' }} className="mb-3">
                📦
              </div>
              <h5 className="mb-2">Нет активной подписки</h5>
              <p className="text-muted mb-3">
                Оформите подписку для доступа к VPN
              </p>
              <button
                className="btn btn-primary"
                onClick={() => navigate('/plans')}
              >
                Выбрать тариф
              </button>
            </div>
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
};
