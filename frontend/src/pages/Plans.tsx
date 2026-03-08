/** Страница тарифных планов */

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Header } from '../components/common/Header';
import { Footer } from '../components/common/Footer';
import { PlanList } from '../components/plan/PlanList';
import { Plan, PlanDuration } from '../types';
import { Loader } from '../components/common/Loader';

export const Plans: React.FC = () => {
  const navigate = useNavigate();
  const [plans, setPlans] = useState<Plan[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPlans = async () => {
      try {
        const response = await axios.get<Plan[]>('/api/v1/plans');
        setPlans(response.data);
      } catch (err) {
        setError('Ошибка загрузки тарифов');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPlans();
  }, []);

  const handleSelectPlan = (plan: Plan, duration: PlanDuration) => {
    const price = duration.prices[0];

    window.Telegram?.WebApp?.showConfirm(
      `Оформить подписку "${plan.name}" на ${duration.days} дней за ${price.price} ${price.currency}?`,
      (ok: boolean) => {
        if (ok) {
          // TODO: реализовать оформление подписки через API
          window.Telegram?.WebApp?.showAlert('Функция покупки в разработке');
        }
      }
    );
  };

  if (isLoading) {
    return <Loader fullScreen />;
  }

  if (error) {
    return (
      <div className="text-center py-5">
        <div style={{ fontSize: '3rem' }}>❌</div>
        <p className="text-muted">{error}</p>
        <button
          className="btn btn-primary"
          onClick={() => window.location.reload()}
        >
          Обновить
        </button>
      </div>
    );
  }

  return (
    <div className="pb-5 mb-5">
      <Header title="Тарифы" showBack onBack={() => navigate(-1)} />

      <div className="px-3">
        <div className="mb-3">
          <p className="text-muted mb-0">
            Выберите подходящий тарифный план для подключения к VPN
          </p>
        </div>

        <PlanList plans={plans} onSelect={handleSelectPlan} />
      </div>

      <Footer />
    </div>
  );
};
