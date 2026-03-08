# 🚀 Отправка исправлений в GitHub

## Проблема

Локальные изменения исправлены, но не отправлены в GitHub. GitHub Actions использует старую версию файлов, поэтому сборка падает с теми же ошибками.

---

## Решение

### Способ 1: Через скрипт (рекомендуется)

```bash
# Запустите скрипт
./scripts/push-to-github.sh

# Скрипт запросит GitHub Personal Access Token
# Введите токен и нажмите Enter
```

### Способ 2: Вручную через токен

```bash
# 1. Установите токен в переменную
export GITHUB_TOKEN=ghp_yourtoken

# 2. Отправьте изменения
git remote set-url origin https://$GITHUB_TOKEN@github.com/d3myasha/d3m-vpn-miniapp.git
git push origin main

# 3. Верните оригинальный URL (опционально)
git remote set-url origin https://github.com/d3myasha/d3m-vpn-miniapp.git
```

### Способ 3: Через SSH

```bash
# 1. Переключите remote на SSH
git remote set-url origin git@github.com:d3myasha/d3m-vpn-miniapp.git

# 2. Проверьте SSH ключ
ssh -T git@github.com

# 3. Отправьте изменения
git push origin main
```

---

## 🔑 Получение Personal Access Token

1. Перейдите на https://github.com/settings/tokens
2. Нажмите **Generate new token (classic)**
3. Дайте название (например, "d3m-vpn-miniapp push")
4. Выберите scope'ы:
   - ✅ `repo` (полный доступ к репозиторию)
   - ✅ `workflow` (для управления GitHub Actions)
5. Нажмите **Generate token**
6. **Скопируйте токен** (начинается с `ghp_`)

⚠️ **Важно:** Сохраните токен! После закрытия страницы его нельзя будет увидеть снова.

---

## ✅ Проверка

После успешного пуша:

1. Перейдите на https://github.com/d3myasha/d3m-vpn-miniapp/actions
2. Проверьте что запустился новый workflow "Build and Push Docker Images"
3. Дождитесь завершения сборки
4. Убедитесь что образы опубликованы в GHCR

---

## 📝 Что было исправлено

| Файл | Исправление |
|------|-------------|
| `frontend/src/components/common/Footer.tsx` | Удалён неиспользуемый импорт `TelegramWebApp` |
| `frontend/src/components/common/Header.tsx` | Удалён неиспользуемый импорт `TelegramWebApp` |
| `frontend/src/components/subscription/SubscriptionCard.tsx` | Удалён неиспользуемый импорт `formatPercent` |
| `frontend/src/pages/Profile.tsx` | Удалены неиспользуемые импорты и переменные |
| `frontend/vite.config.ts` | Добавлен declaration merging для `ImportMetaEnv` |

---

## 🔄 Если пуш не работает

### Ошибка: "Authentication failed"

- Проверьте что токен действителен
- Убедитесь что у токена есть scope `repo`
- Попробуйте пересоздать токен

### Ошибка: "remote: Permission denied"

- Убедитесь что вы владелец репозитория
- Проверьте что токен имеет доступ к репозиторию

### Ошибка: "could not read Username"

Используйте один из альтернативных способов выше.

---

## 📞 Помощь

Если ничего не помогает:

1. Проверьте https://github.com/settings/tokens
2. Убедитесь что токен активен
3. Попробуйте создать новый токен
4. Проверьте https://github.com/d3myasha/d3m-vpn-miniapp/actions
