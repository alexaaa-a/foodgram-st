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
# Helmfile
brew install helmfile
# или вручную (arm64):
curl -L https://github.com/helmfile/helmfile/releases/download/v0.169.2/helmfile_0.169.2_darwin_arm64.tar.gz \
  | tar xz -C ~/bin helmfile

# helm-diff плагин (обязателен для helmfile)
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
helmfile sync -l name=prometheus
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

```bash
cd monitoring/
helmfile sync -l name=loki
helmfile sync -l name=promtail
```

Проверить, что promtail шлёт логи:
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
2. Выбери "Mail" → "Mac" (или любое другое устройство)
3. Скопируй 16-символьный пароль вида `xxxx xxxx xxxx xxxx`

### 2. Прописать SMTP в values

Открой `monitoring/values/prometheus-stack.yaml`, секция `grafana.grafana.ini.smtp`:
```yaml
grafana:
  grafana.ini:
    smtp:
      enabled: true
      host: smtp.gmail.com:587
      user: "your@gmail.com"          # ← вставить
      password: "xxxx xxxx xxxx xxxx" # ← App Password
      from_address: "your@gmail.com"  # ← вставить
```

Затем применить изменение:
```bash
cd monitoring/
helmfile apply -l name=prometheus
```

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
# Посмотреть все релизы helmfile
helmfile list

# Diff (что изменится)
helmfile diff

# Применить все релизы
helmfile sync

# Удалить все
helmfile destroy

# Логи конкретного компонента
kubectl logs -n monitoring -l app.kubernetes.io/name=prometheus --tail=50
kubectl logs -n monitoring -l app.kubernetes.io/name=loki --tail=50
```

## URL-ы

| Сервис | URL |
|--------|-----|
| Prometheus | http://prometheus.foodgram.local |
| Grafana | http://grafana.foodgram.local |
| Alertmanager | http://alertmanager.foodgram.local |
