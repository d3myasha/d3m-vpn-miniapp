/** Страница устройств */

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Header } from '../components/common/Header';
import { Footer } from '../components/common/Footer';
import { DeviceList } from '../components/device/DeviceList';
import { useDevices } from '../hooks/useDevices';
import { useSubscription } from '../hooks/useSubscription';
import { Loader } from '../components/common/Loader';

export const Devices: React.FC = () => {
  const navigate = useNavigate();
  const { subscription } = useSubscription();
  const { devices, isLoading, fetchDevices, addDevice, removeDevice } =
    useDevices();
  const [showAddModal, setShowAddModal] = useState(false);
  const [newDeviceName, setNewDeviceName] = useState('');

  useEffect(() => {
    if (subscription?.id) {
      fetchDevices(subscription.id);
    }
  }, [subscription]);

  const handleAddDevice = async () => {
    if (!newDeviceName.trim() || !subscription) return;

    try {
      await addDevice(newDeviceName.trim(), subscription.id);
      setNewDeviceName('');
      setShowAddModal(false);
      window.Telegram?.WebApp?.showAlert('Устройство добавлено');
    } catch (err) {
      window.Telegram?.WebApp?.showAlert(
        err instanceof Error ? err.message : 'Ошибка добавления устройства'
      );
    }
  };

  const handleRemoveDevice = async (deviceId: number) => {
    try {
      await removeDevice(deviceId, subscription?.id);
      window.Telegram?.WebApp?.showAlert('Устройство удалено');
    } catch (err) {
      window.Telegram?.WebApp?.showAlert(
        err instanceof Error ? err.message : 'Ошибка удаления устройства'
      );
    }
  };

  const handleResetDevices = async () => {
    window.Telegram?.WebApp?.showConfirm(
      'Сбросить все устройства? Это действие нельзя отменить.',
      async (ok: boolean) => {
        if (ok) {
          try {
            // TODO: реализовать сброс через API
            window.Telegram?.WebApp?.showAlert('Функция сброса в разработке');
          } catch (err) {
            window.Telegram?.WebApp?.showAlert('Ошибка сброса устройств');
          }
        }
      }
    );
  };

  if (isLoading && devices.length === 0) {
    return <Loader fullScreen />;
  }

  return (
    <div className="pb-5 mb-5">
      <Header title="Устройства" showBack onBack={() => navigate(-1)} />

      <div className="px-3">
        {/* Информация о лимитах */}
        {subscription && (
          <div className="card shadow-sm mb-3">
            <div className="card-body">
              <div className="d-flex justify-content-between">
                <div>
                  <small className="text-muted">Устройства</small>
                  <div className="fw-bold">
                    {devices.filter((d) => d.is_active).length} /{' '}
                    {subscription.device_limit}
                  </div>
                </div>
                <div>
                  <small className="text-muted">Лимит</small>
                  <div className="fw-bold">{subscription.device_limit}</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Список устройств */}
        <DeviceList devices={devices} onRemove={handleRemoveDevice} />

        {/* Кнопки действий */}
        {subscription && devices.length < subscription.device_limit && (
          <div className="mt-3">
            <button
              className="btn btn-primary w-100"
              onClick={() => setShowAddModal(true)}
            >
              ➕ Добавить устройство
            </button>
          </div>
        )}

        {devices.length > 0 && (
          <div className="mt-2">
            <button
              className="btn btn-outline-danger w-100"
              onClick={handleResetDevices}
            >
              🔄 Сбросить все устройства
            </button>
          </div>
        )}
      </div>

      {/* Модальное окно добавления устройства */}
      {showAddModal && (
        <div
          className="modal fade show d-block"
          style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}
          onClick={() => setShowAddModal(false)}
        >
          <div
            className="modal-dialog modal-dialog-centered"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Новое устройство</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setShowAddModal(false)}
                />
              </div>
              <div className="modal-body">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Название устройства"
                  value={newDeviceName}
                  onChange={(e) => setNewDeviceName(e.target.value)}
                  autoFocus
                />
                <small className="text-muted">
                  Например: iPhone, MacBook, Android
                </small>
              </div>
              <div className="modal-footer">
                <button
                  className="btn btn-secondary"
                  onClick={() => setShowAddModal(false)}
                >
                  Отмена
                </button>
                <button
                  className="btn btn-primary"
                  onClick={handleAddDevice}
                  disabled={!newDeviceName.trim()}
                >
                  Добавить
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  );
};
