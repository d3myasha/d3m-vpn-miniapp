/** Компонент выбора метода оплаты */

import React, { useEffect, useState } from 'react';

export interface PaymentMethodType {
  id: string;
  name: string;
  icon: string;
  description: string;
}

interface PaymentMethodProps {
  methods?: PaymentMethodType[];
  selectedMethod?: string;
  onSelect?: (methodId: string) => void;
}

const defaultMethods: PaymentMethodType[] = [
  { id: 'telegram_stars', name: 'Telegram Stars', icon: '⭐', description: 'Оплата через Telegram' },
  { id: 'yookassa', name: 'ЮKassa', icon: '💳', description: 'Банковская карта' },
  { id: 'cryptomus', name: 'Cryptomus', icon: '₿', description: 'Криптовалюта' },
  { id: 'robokassa', name: 'RoboKassa', icon: '💰', description: 'Электронные кошельки' },
];

export const PaymentMethod: React.FC<PaymentMethodProps> = ({
  methods = defaultMethods,
  selectedMethod,
  onSelect,
}) => {
  const [theme, setTheme] = useState<Record<string, string>>({});

  useEffect(() => {
    const tg = window.Telegram?.WebApp;
    if (tg) {
      setTheme(tg.themeParams);
    }
  }, []);

  return (
    <div className="list-group">
      {methods.map((method) => {
        const isSelected = selectedMethod === method.id;
        return (
          <button
            key={method.id}
            className={`list-group-item list-group-item-action d-flex align-items-center gap-3 ${
              isSelected ? 'active' : ''
            }`}
            style={{
              backgroundColor: isSelected
                ? theme.button_color || '#0d6efd'
                : 'transparent',
              borderColor: 'rgba(0,0,0,0.1)',
            }}
            onClick={() => onSelect?.(method.id)}
          >
            <div
              className="rounded-circle d-flex align-items-center justify-content-center"
              style={{
                width: '48px',
                height: '48px',
                backgroundColor: isSelected
                  ? 'rgba(255,255,255,0.2)'
                  : '#f8f9fa',
                fontSize: '1.5rem',
              }}
            >
              {method.icon}
            </div>
            <div className="text-start flex-grow-1">
              <div className="fw-bold">{method.name}</div>
              <small
                className="text-muted"
                style={{
                  color: isSelected
                    ? theme.button_text_color || '#fff'
                    : undefined,
                }}
              >
                {method.description}
              </small>
            </div>
            {isSelected && <div className="text-white">✓</div>}
          </button>
        );
      })}
    </div>
  );
};
