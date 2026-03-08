/** Компонент Error */

import React from 'react';

interface ErrorProps {
  message?: string;
  onRetry?: () => void;
  fullScreen?: boolean;
}

export const Error: React.FC<ErrorProps> = ({
  message = 'Произошла ошибка',
  onRetry,
  fullScreen = false,
}) => {
  const style: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '1rem',
    padding: '2rem',
    textAlign: 'center',
  };

  if (fullScreen) {
    style.position = 'fixed';
    style.top = 0;
    style.left = 0;
    style.right = 0;
    style.bottom = 0;
    style.backgroundColor = 'rgba(0,0,0,0.5)';
    style.zIndex = 9999;
  }

  return (
    <div style={style}>
      <div style={{ fontSize: '3rem' }}>❌</div>
      <p className="text-muted">{message}</p>
      {onRetry && (
        <button className="btn btn-primary" onClick={onRetry}>
          Повторить
        </button>
      )}
    </div>
  );
};
