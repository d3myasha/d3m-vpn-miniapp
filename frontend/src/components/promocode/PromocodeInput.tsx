/** Компонент ввода промокода */

import React, { useState } from 'react';

interface PromocodeInputProps {
  onActivate?: (code: string) => Promise<void>;
  isLoading?: boolean;
}

export const PromocodeInput: React.FC<PromocodeInputProps> = ({
  onActivate,
  isLoading = false,
}) => {
  const [code, setCode] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!code.trim()) {
      setError('Введите промокод');
      return;
    }

    try {
      await onActivate?.(code.trim().toUpperCase());
      setSuccess('Промокод успешно активирован!');
      setCode('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка активации промокода');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="input-group">
        <input
          type="text"
          className="form-control"
          placeholder="Введите промокод"
          value={code}
          onChange={(e) => setCode(e.target.value.toUpperCase())}
          disabled={isLoading}
          style={{ textTransform: 'uppercase' }}
        />
        <button
          className="btn btn-primary"
          type="submit"
          disabled={isLoading || !code.trim()}
        >
          {isLoading ? (
            <>
              <span
                className="spinner-border spinner-border-sm me-2"
                role="status"
              />
              Проверка...
            </>
          ) : (
            'Активировать'
          )}
        </button>
      </div>

      {error && (
        <div className="alert alert-danger mt-2 mb-0" role="alert">
          {error}
        </div>
      )}

      {success && (
        <div className="alert alert-success mt-2 mb-0" role="alert">
          {success}
        </div>
      )}
    </form>
  );
};
