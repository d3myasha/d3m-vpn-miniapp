/** Утилиты для форматирования */

/** Форматирование размера трафика */
export function formatTraffic(bytes: number): string {
  if (bytes === 0) return '0 Б';

  const units = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ'];
  const k = 1024;
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + units[i];
}

/** Форматирование даты */
export function formatDate(dateString: string, locale: string = 'ru-RU'): string {
  const date = new Date(dateString);
  return date.toLocaleDateString(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

/** Форматирование даты и времени */
export function formatDateTime(dateString: string, locale: string = 'ru-RU'): string {
  const date = new Date(dateString);
  return date.toLocaleString(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

/** Форматирование цены */
export function formatPrice(amount: number, currency: string = 'RUB'): string {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(amount);
}

/** Форматирование процентов */
export function formatPercent(value: number): string {
  return `${Math.round(value)}%`;
}

/** Склонение слов */
export function declension(number: number, titles: [string, string, string]): string {
  const cases = [2, 0, 1, 1, 1, 2];
  const index = (number % 100 < 4 && number % 100 > 20) ? number % 10 : cases[number % 10];
  return titles[index];
}

/** Примеры склонений */
export const declensions = {
  day: (n: number) => declension(n, ['день', 'дня', 'дней']),
  device: (n: number) => declension(n, ['устройство', 'устройства', 'устройств']),
  subscription: (n: number) => declension(n, ['подписка', 'подписки', 'подписок']),
  ruble: (n: number) => declension(n, ['рубль', 'рубля', 'рублей']),
};
