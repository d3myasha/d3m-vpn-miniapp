/** Компонент списка тарифных планов */

import React from 'react';
import { Plan, PlanDuration } from '../../types';
import { PlanCard } from './PlanCard';

interface PlanListProps {
  plans: Plan[];
  onSelect?: (plan: Plan, duration: PlanDuration) => void;
  isLoading?: boolean;
}

export const PlanList: React.FC<PlanListProps> = ({
  plans,
  onSelect,
  isLoading = false,
}) => {
  if (isLoading) {
    return (
      <div className="text-center py-4">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Загрузка...</span>
        </div>
      </div>
    );
  }

  if (plans.length === 0) {
    return (
      <div className="text-center py-4">
        <div style={{ fontSize: '3rem' }}>💎</div>
        <p className="text-muted">Нет доступных тарифов</p>
      </div>
    );
  }

  return (
    <div className="px-3">
      {plans.map((plan) => (
        <PlanCard key={plan.id} plan={plan} onSelect={onSelect} />
      ))}
    </div>
  );
};
