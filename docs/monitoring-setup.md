# Homework 10 — Helmfile, Prometheus, Loki, Grafana

## Структура

```
monitoring/
├── helmfile.yaml               # все релизы
├── smtp-secret.sh              # создать секрет для SMTP
└── values/
    ├── prometheus-stack.yaml   # Prometheus + Grafana + Alertmanager
    ├── loki.yaml               # Loki (хранение логов)
    └── promtail.yaml           # Promtail (сбор логов)
```

---

## Шаг 0 — Установка инструментов

```bash
brew install helmfile
helm plugin install https://github.com/databus23/helm-diff
```

---

## Часть 1 — Prometheus + метрики Ingress

### Добавить /etc/hosts

```bash
echo "$(minikube ip)  prometheus.foodgram.local grafana.foodgram.local alertmanager.foodgram.local" \
  | sudo tee -a /etc/hosts
```

### Деплой

```bash
cd monitoring/
helmfile sync
```

Дождаться Ready (~3-5 мин):
```bash
kubectl get pods -n monitoring -w
```

### Открыть Prometheus

Браузер → http://prometheus.foodgram.local

### Запрос метрик nginx

В Prometheus UI → Expression:
```promql
nginx_ingress_controller_requests_total
```
или:
```promql
rate(nginx_ingress_controller_requests_total[5m])
```

---

## Часть 2 — Loki + Promtail

Уже включены в `helmfile sync`. Проверить promtail:
```bash
kubectl logs -n monitoring -l app.kubernetes.io/name=promtail --tail=20
```

Grafana → Explore → Data source: Loki → запрос:
```logql
{namespace="foodgram"}
```

---

## Часть 3 — Grafana + Алертинг

### 1. Получить SMTP-токен (Gmail App Password)

1. Открой https://myaccount.google.com/apppasswords
2. Выбери "Mail" → "Mac"
3. Скопируй 16-символьный пароль вида `xxxx xxxx xxxx xxxx`

### 2. Создать секрет с SMTP-кредами

```bash
export SMTP_USER="your@gmail.com"
export SMTP_PASSWORD="xxxx xxxx xxxx xxxx"
./monitoring/smtp-secret.sh
kubectl rollout restart deployment/prometheus-grafana -n monitoring
```

Пароль **не хранится в values** — только в Kubernetes Secret.

### 3. Зайти в Grafana

Браузер → http://grafana.foodgram.local  
Логин: `admin` / `admin123`

### 4. Настроить Contact Point

Grafana → Alerting → Contact points → + New contact point:
- Name: `email-alert`
- Type: Email
- Addresses: `your@gmail.com`
- Нажать **Test** → прийдёт тестовое письмо

### 5. Создать Alert Rule

Grafana → Alerting → Alert rules → + New alert rule:

**Пример: высокий 5xx от nginx**
- Name: `Nginx 5xx High Rate`
- Data source: `Prometheus`
- Metrics query:
  ```promql
  sum(rate(nginx_ingress_controller_requests_total{status=~"5.."}[5m])) > 0.1
  ```
- Condition: IS ABOVE → `0.1`
- Evaluation: Every `1m`, For `2m`
- Contact point: `email-alert`

---

## Полезные команды

```bash
helmfile list
helmfile diff
helmfile sync
helmfile destroy
kubectl logs -n monitoring -l app.kubernetes.io/name=prometheus --tail=50
```

## URL-ы

| Сервис | URL |
|--------|-----|
| Prometheus | http://prometheus.foodgram.local |
| Grafana | http://grafana.foodgram.local |
| Alertmanager | http://alertmanager.foodgram.local |
