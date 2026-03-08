/** Типы данных для frontend */

// Пользователь
export interface User {
  id: number;
  telegram_id: number;
  username: string | null;
  name: string;
  role: string;
  language: string;
  points: number;
  personal_discount: number;
  purchase_discount: number;
  is_blocked: boolean;
  is_rules_accepted: boolean;
  current_subscription_id: number | null;
  created_at: string;
  updated_at: string;
}

// Подписка
export interface Subscription {
  id: number;
  user_remna_id: string;
  user_telegram_id: number;
  status: string;
  is_trial: boolean;
  traffic_limit: number;
  device_limit: number;
  traffic_limit_strategy: string;
  tag: string | null;
  internal_squads: string[];
  external_squad: string | null;
  expire_at: string;
  url: string;
  plan_snapshot: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  days_left: number;
}

// Устройство
export interface Device {
  id: number;
  subscription_id: number;
  name: string;
  device_id: string;
  is_active: boolean;
  last_seen: string | null;
  created_at: string;
  updated_at: string;
}

// Тарифный план
export interface Plan {
  id: number;
  name: string;
  description: string | null;
  type: string;
  availability: string;
  traffic_limit: number;
  device_limit: number;
  traffic_limit_strategy: string;
  order_index: number;
  is_active: boolean;
  tag: string | null;
  durations: PlanDuration[];
  created_at: string;
  updated_at: string;
}

export interface PlanDuration {
  id: number;
  days: number;
  prices: PlanPrice[];
}

export interface PlanPrice {
  id: number;
  currency: string;
  price: number;
}

// Транзакция
export interface Transaction {
  id: number;
  payment_id: string;
  user_telegram_id: number;
  status: string;
  is_test: boolean;
  purchase_type: string;
  gateway_type: string;
  currency: string;
  amount: number;
  pricing: Record<string, unknown>;
  plan_snapshot: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

// Промокод
export interface Promocode {
  id: number;
  code: string;
  type: string;
  value: number;
  is_active: boolean;
  max_uses: number | null;
  uses_count: number;
  expires_at: string | null;
  created_at: string;
  updated_at: string;
}

// Рефералы
export interface ReferralStats {
  total_referrals: number;
  paid_referrals: number;
  total_bonus_days: number;
  total_bonus_traffic: number;
  referral_code: string;
  referral_link: string;
}

// API ответы
export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface SuccessResponse {
  success: boolean;
  message: string;
}

export interface ErrorResponse {
  success: boolean;
  error: string;
}

// Telegram WebApp
export interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code?: string;
  is_premium?: boolean;
}

export interface TelegramWebApp {
  initData: string;
  initDataUnsafe: {
    user?: TelegramUser;
    query_id?: string;
    start_param?: string;
  };
  ready: () => void;
  expand: () => void;
  close: () => void;
  showPopup: (data: unknown) => void;
  showConfirm: (message: string, callback: (ok: boolean) => void) => void;
  showAlert: (message: string) => void;
  MainButton: {
    text: string;
    color: string;
    text_color: string;
    isVisible: boolean;
    isActive: boolean;
    isProgressVisible: boolean;
    show: () => void;
    hide: () => void;
    enable: () => void;
    disable: () => void;
    showProgress: (leaveActive: boolean) => void;
    hideProgress: () => void;
    onClick: (callback: () => void) => void;
    offClick: (callback: () => void) => void;
  };
  BackButton: {
    isVisible: boolean;
    onClick: (callback: () => void) => void;
    offClick: (callback: () => void) => void;
    show: () => void;
    hide: () => void;
  };
  themeParams: Record<string, string>;
  colorScheme: string;
}

declare global {
  interface Window {
    Telegram: {
      WebApp: TelegramWebApp;
    };
  }
}
