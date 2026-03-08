/** Компонент Loader */

import React from 'react';

interface LoaderProps {
  text?: string;
  fullScreen?: boolean;
}

export const Loader: React.FC<LoaderProps> = ({
  text = 'Загрузка...',
  fullScreen = false,
}) => {
  const style: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '1rem',
    padding: '2rem',
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
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Загрузка...</span>
      </div>
      {text && <p className="text-muted mb-0">{text}</p>}
    </div>
  );
};
