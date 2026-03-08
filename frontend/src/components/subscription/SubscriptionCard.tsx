/** Компонент карточки подписки */

import React from 'react';
import { Subscription } from '../../types';
import { formatTraffic, formatDate, formatPercent } from '../../utils/format';

interface SubscriptionCardProps {
  subscription: Subscription;
  trafficUsage?: {
    used: number;
    limit: number;
    remaining: number;
    percentage: number;
  };
}

export const SubscriptionCard: React.FC<SubscriptionCardProps> = ({
  subscription,
  trafficUsage,
}) => {
  const getStatusBadge = (status: string) => {
    const statusMap: Record<string, { class: string; label: string }> = {
      active: { class: 'bg-success', label: 'Активна' },
      expired: { class: 'bg-secondary', label: 'Истекла' },
      cancelled: { class: 'bg-danger', label: 'Отменена' },
      trial: { class: 'bg-info', label: 'Триал' },
      pending: { class: 'bg-warning text-dark', label: 'Ожидает' },
    };
    const { class: className, label } = statusMap[status.toLowerCase()] || {
      class: 'bg-secondary',
      label: status,
    };
    return <span className={`badge ${className}`}>{label}</span>;
  };

  const trafficPercent = trafficUsage?.percentage || 0;

  return (
    <div className="card shadow-sm">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h5 className="card-title mb-0">Ваша подписка</h5>
          {getStatusBadge(subscription.status)}
        </div>

        {/* Срок действия */}
        <div className="mb-3">
          <small className="text-muted">Действует до</small>
          <div className="fw-bold">{formatDate(subscription.expire_at)}</div>
          <small className="text-muted">
            Осталось дней: {subscription.days_left}
          </small>
        </div>

        {/* Трафик */}
        {subscription.traffic_limit > 0 && trafficUsage && (
          <div className="mb-3">
            <div className="d-flex justify-content-between mb-1">
              <small className="text-muted">Трафик</small>
              <small className="text-muted">
                {formatTraffic(trafficUsage.used)} из{' '}
                {formatTraffic(trafficUsage.limit)}
              </small>
            </div>
            <div className="progress" style={{ height: '8px' }}>
              <div
                className={`progress-bar ${trafficPercent > 80 ? 'bg-danger' : trafficPercent > 50 ? 'bg-warning' : 'bg-success'}`}
                role="progressbar"
                style={{ width: `${Math.min(trafficPercent, 100)}%` }}
              />
            </div>
            <small className="text-muted">
              Осталось: {formatTraffic(trafficUsage.remaining)}
            </small>
          </div>
        )}

        {/* Устройства */}
        <div className="d-flex justify-content-between">
          <div>
            <small className="text-muted">Устройства</small>
            <div className="fw-bold">
              {subscription.device_limit}{' '}
              <span className="fw-normal text-muted">
                макс.
              </span>
            </div>
          </div>
          <div>
            <small className="text-muted">Тип трафика</small>
            <div className="fw-bold text-capitalize">
              {subscription.traffic_limit_strategy === 'unlimited'
                ? '∞ Безлимит'
                : subscription.traffic_limit_strategy}
            </div>
          </div>
        </div>

        {/* Ключ подписки */}
        {subscription.url && (
          <div className="mt-3">
            <a
              href={subscription.url}
              className="btn btn-outline-primary w-100"
              target="_blank"
              rel="noopener noreferrer"
            >
              🔗 Открыть ключ подписки
            </a>
          </div>
        )}
      </div>
    </div>
  );
};
