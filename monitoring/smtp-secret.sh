set -euo pipefail

: "${SMTP_USER:?Set SMTP_USER (e.g. your@gmail.com)}"
: "${SMTP_PASSWORD:?Set SMTP_PASSWORD (Google App Password)}"

NAMESPACE="${KUBE_NAMESPACE:-monitoring}"

kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic grafana-smtp-secret \
  --namespace="${NAMESPACE}" \
  --from-literal=GF_SMTP_USER="${SMTP_USER}" \
  --from-literal=GF_SMTP_PASSWORD="${SMTP_PASSWORD}" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "✓ Secret grafana-smtp-secret created in namespace ${NAMESPACE}"
echo "  Update monitoring/values/prometheus-stack.yaml:"
echo "    grafana.grafana\\.ini.smtp.user: ${SMTP_USER}"
echo "    grafana.grafana\\.ini.smtp.from_address: ${SMTP_USER}"
