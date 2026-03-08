/** Компонент использования трафика */

import React from 'react';
import { formatTraffic, formatPercent } from '../../utils/format';

interface TrafficUsageProps {
  used: number;
  limit: number;
  remaining: number;
  percentage: number;
}

export const TrafficUsage: React.FC<TrafficUsageProps> = ({
  used,
  limit,
  remaining,
  percentage,
}) => {
  const isUnlimited = limit === 0;

  if (isUnlimited) {
    return (
      <div className="card bg-success text-white">
        <div className="card-body text-center">
          <h3 className="mb-0">∞</h3>
          <p className="mb-0">Безлимитный трафик</p>
        </div>
      </div>
    );
  }

  const getProgressClass = () => {
    if (percentage > 80) return 'bg-danger';
    if (percentage > 50) return 'bg-warning';
    return 'bg-success';
  };

  return (
    <div className="card shadow-sm">
      <div className="card-body">
        <h6 className="card-title mb-3">Использование трафика</h6>

        <div className="text-center mb-3">
          <div className="display-4 fw-bold">{formatPercent(percentage)}</div>
          <small className="text-muted">использовано</small>
        </div>

        <div className="progress mb-3" style={{ height: '12px' }}>
          <div
            className={`progress-bar ${getProgressClass()}`}
            role="progressbar"
            style={{ width: `${Math.min(percentage, 100)}%` }}
          />
        </div>

        <div className="row text-center">
          <div className="col-4">
            <small className="text-muted">Использовано</small>
            <div className="fw-bold">{formatTraffic(used)}</div>
          </div>
          <div className="col-4 border-start border-end">
            <small className="text-muted">Лимит</small>
            <div className="fw-bold">{formatTraffic(limit)}</div>
          </div>
          <div className="col-4">
            <small className="text-muted">Осталось</small>
            <div className="fw-bold">{formatTraffic(remaining)}</div>
          </div>
        </div>
      </div>
    </div>
  );
};
