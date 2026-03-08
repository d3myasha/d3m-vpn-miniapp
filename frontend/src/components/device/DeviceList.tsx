/** Компонент списка устройств */

import React from 'react';
import { Device } from '../../types';
import { DeviceItem } from './DeviceItem';

interface DeviceListProps {
  devices: Device[];
  onRemove?: (id: number) => void;
  isLoading?: boolean;
}

export const DeviceList: React.FC<DeviceListProps> = ({
  devices,
  onRemove,
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

  if (devices.length === 0) {
    return (
      <div className="text-center py-4">
        <div style={{ fontSize: '3rem' }}>📱</div>
        <p className="text-muted">Нет устройств</p>
        <small className="text-muted">
          Добавьте первое устройство для подключения к VPN
        </small>
      </div>
    );
  }

  return (
    <div className="list-group list-group-flush">
      {devices.map((device) => (
        <DeviceItem key={device.id} device={device} onRemove={onRemove} />
      ))}
    </div>
  );
};
