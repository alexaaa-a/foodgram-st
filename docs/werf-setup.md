# Werf: установка и деплой

## Что реализовано

### Часть 1: Установка werf и рефакторинг чарта

| Элемент | Файл | Описание |
|---------|------|----------|
| werf.yaml | `/werf.yaml` | Описание образов backend и frontend |
| werf-giterminism.yaml | `/werf-giterminism.yaml` | Конфигурация giterminism + env-vars для Vault |
| .helm/ | `/.helm/` | Helm-чарт в werf-формате |
| Глобальные values | `/.helm/values.yaml` | Единый источник значений для всех субчартов |
| Helm submodules | `/.helm/charts/` | Все субчарты как зависимости |

### Часть 2: Vault-интеграция и деплой

| Элемент | Файл | Описание |
|---------|------|----------|
| vault-integration.sh | `/scripts/vault-integration.sh` | AppRole auth, docker-токен, секреты |
| werf-deploy.sh | `/scripts/werf-deploy.sh` | Полный деплой через werf converge |

---

## Команды для скринкаста

### 1. Показать структуру проекта
```bash
ls -la                   # видно werf.yaml, werf-giterminism.yaml, .helm/
cat werf.yaml            # описание образов backend и frontend
cat werf-giterminism.yaml
```

### 2. Показать werf версию и помощь
```bash
source "$(/Users/alexandrakalimullina/bin/trdl use werf 2 stable)"
werf version
werf --help
```

### 3. Показать .helm/ структуру
```bash
tree .helm/ -L 3         # или: find .helm -maxdepth 3 -type f
cat .helm/values.yaml    # глобальные values
```

### 4. Проверить render (генерация манифестов без деплоя)
```bash
source "$(/Users/alexandrakalimullina/bin/trdl use werf 2 stable)"

werf render --dev \
  --set "global.db.user=postgres" \
  --set "global.db.password=testpass" \
  --set "global.db.name=foodgram" \
  --set "global.django.secretKey=test-key" \
  --set "global.redis.password=redispass" \
  --set "redis.auth.password=redispass" \
  --set "global.rabbitmq.username=guest" \
  --set "global.rabbitmq.password=guest"
```

### 5. Показать Vault-интеграцию
```bash
cat scripts/vault-integration.sh   # рассказать про AppRole + docker-токен

# Проверить что docker-credentials есть в Vault:
kubectl exec -n vault vault-0 -- env \
  VAULT_ADDR=http://127.0.0.1:8200 \
  VAULT_TOKEN=<ROOT_TOKEN> \
  vault kv get foodgram/docker
```

### 6. Деплой через werf
```bash
# Настроить переменные
source .env
export VAULT_ADDR VAULT_ROLE_ID VAULT_SECRET_ID

# Запустить деплой
./scripts/werf-deploy.sh development

# Или напрямую через werf:
source "$(/Users/alexandrakalimullina/bin/trdl use werf 2 stable)"
source scripts/vault-integration.sh
werf converge --env development --namespace foodgram \
  --set "global.db.user=${POSTGRES_USER}" \
  --set "global.db.password=${POSTGRES_PASSWORD}" \
  --set "global.db.name=${POSTGRES_DB}" \
  --set "global.django.secretKey=${DJANGO_SECRET_KEY}"
```

### 7. Проверка после деплоя
```bash
kubectl get pods -n foodgram
kubectl get deployments -n foodgram
kubectl describe deployment django-deployment -n foodgram
# Убедиться что image содержит werf-тег с digest
```

---

## Добавить docker-credentials в Vault (один раз)

```bash
kubectl exec -n vault vault-0 -- env \
  VAULT_ADDR=http://127.0.0.1:8200 \
  VAULT_TOKEN=<ROOT_TOKEN> \
  vault kv put foodgram/docker \
  username=YOUR_DOCKERHUB_LOGIN \
  password=YOUR_DOCKERHUB_TOKEN
```
