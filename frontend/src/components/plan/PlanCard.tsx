/** Компонент карточки тарифного плана */

import React, { useEffect, useState } from 'react';
import { Plan, PlanDuration } from '../../types';
import { formatTraffic, formatPrice } from '../../utils/format';

interface PlanCardProps {
  plan: Plan;
  onSelect?: (plan: Plan, duration: PlanDuration) => void;
}

export const PlanCard: React.FC<PlanCardProps> = ({ plan, onSelect }) => {
  const [selectedDuration, setSelectedDuration] = useState<PlanDuration | null>(
    plan.durations?.[0] || null
  );
  const [theme, setTheme] = useState<Record<string, string>>({});

  useEffect(() => {
    const tg = window.Telegram?.WebApp;
    if (tg) {
      setTheme(tg.themeParams);
    }
  }, []);

  const handleDurationChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const duration = plan.durations?.find(
      (d) => d.id === Number(e.target.value)
    );
    setSelectedDuration(duration || null);
  };

  const getBestPrice = () => {
    if (!selectedDuration?.prices?.length) return null;
    return selectedDuration.prices[0];
  };

  const bestPrice = getBestPrice();

  return (
    <div className="card shadow-sm mb-3">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-start mb-2">
          <div>
            <h5 className="card-title mb-1">{plan.name}</h5>
            {plan.description && (
              <p className="text-muted small mb-0">{plan.description}</p>
            )}
          </div>
          {plan.tag && (
            <span
              className="badge"
              style={{
                backgroundColor: theme.button_color || '#0d6efd',
                color: theme.button_text_color || '#fff',
              }}
            >
              {plan.tag}
            </span>
          )}
        </div>

        {/* Характеристики */}
        <div className="row g-2 my-2">
          <div className="col-4 text-center">
            <div className="p-2 rounded" style={{ backgroundColor: '#f8f9fa' }}>
              <div className="fw-bold">
                {plan.traffic_limit === 0
                  ? '∞'
                  : formatTraffic(plan.traffic_limit)}
              </div>
              <small className="text-muted">Трафик</small>
            </div>
          </div>
          <div className="col-4 text-center">
            <div className="p-2 rounded" style={{ backgroundColor: '#f8f9fa' }}>
              <div className="fw-bold">{plan.device_limit}</div>
              <small className="text-muted">Устройства</small>
            </div>
          </div>
          <div className="col-4 text-center">
            <div className="p-2 rounded" style={{ backgroundColor: '#f8f9fa' }}>
              <div className="fw-bold text-capitalize">
                {plan.traffic_limit_strategy === 'unlimited' ? '∞' : plan.traffic_limit_strategy}
              </div>
              <small className="text-muted">Тип</small>
            </div>
          </div>
        </div>

        {/* Выбор длительности */}
        {plan.durations && plan.durations.length > 1 && (
          <div className="mb-3">
            <label className="form-label small text-muted">
              Длительность
            </label>
            <select
              className="form-select form-select-sm"
              value={selectedDuration?.id || ''}
              onChange={handleDurationChange}
            >
              {plan.durations.map((duration) => (
                <option key={duration.id} value={duration.id}>
                  {duration.days} дн.
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Цена и кнопка */}
        <div className="d-flex justify-content-between align-items-center">
          <div>
            {bestPrice && (
              <>
                <div className="fw-bold fs-5">
                  {formatPrice(bestPrice.price, bestPrice.currency)}
                </div>
                <small className="text-muted">
                  {selectedDuration?.days} дн.
                </small>
              </>
            )}
          </div>
          {onSelect && (
            <button
              className="btn btn-primary"
              style={{
                backgroundColor: theme.button_color || '#0d6efd',
                borderColor: theme.button_color || '#0d6efd',
              }}
              onClick={() =>
                selectedDuration && onSelect(plan, selectedDuration)
              }
            >
              Выбрать
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
