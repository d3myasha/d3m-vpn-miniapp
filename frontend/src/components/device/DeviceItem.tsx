/** Компонент элемента устройства */

import React, { useEffect, useState } from 'react';
import { Device } from '../../types';
import { formatDateTime } from '../../utils/format';

interface DeviceItemProps {
  device: Device;
  onRemove?: (id: number) => void;
}

export const DeviceItem: React.FC<DeviceItemProps> = ({ device, onRemove }) => {
  const [theme, setTheme] = useState<Record<string, string>>({});

  useEffect(() => {
    const tg = window.Telegram?.WebApp;
    if (tg) {
      setTheme(tg.themeParams);
    }
  }, []);

  const handleRemove = () => {
    if (onRemove) {
      window.Telegram?.WebApp?.showConfirm(
        `Удалить устройство "${device.name}"?`,
        (ok: boolean) => {
          if (ok) {
            onRemove(device.id);
          }
        }
      );
    }
  };

  return (
    <div
      className="list-group-item d-flex justify-content-between align-items-center"
      style={{
        backgroundColor: 'transparent',
        borderBottom: '1px solid rgba(0,0,0,0.1)',
      }}
    >
      <div className="d-flex align-items-center gap-3">
        <div
          className="rounded-circle d-flex align-items-center justify-content-center"
          style={{
            width: '40px',
            height: '40px',
            backgroundColor: theme.button_color || '#0d6efd',
            color: theme.button_text_color || '#fff',
          }}
        >
          📱
        </div>
        <div>
          <div className="fw-bold">{device.name}</div>
          <small className="text-muted">
            {device.last_seen
              ? `Был в сети: ${formatDateTime(device.last_seen)}`
              : 'Не активен'}
          </small>
        </div>
      </div>
      <div className="d-flex align-items-center gap-2">
        {device.is_active ? (
          <span className="badge bg-success">Активно</span>
        ) : (
          <span className="badge bg-secondary">Неактивно</span>
        )}
        {onRemove && (
          <button
            className="btn btn-sm btn-outline-danger"
            onClick={handleRemove}
          >
            ✕
          </button>
        )}
      </div>
    </div>
  );
};
