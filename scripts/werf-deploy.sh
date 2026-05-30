set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

WERF_ENV="${1:-${WERF_ENV:-development}}"
KUBE_NAMESPACE="${KUBE_NAMESPACE:-foodgram}"
WERF_REPO="${WERF_REPO:-}"

log() { echo "[werf-deploy] $*"; }

if command -v trdl &>/dev/null; then
  log "Activating werf via trdl ..."
  source "$(/Users/alexandrakalimullina/bin/trdl use werf 2 stable)" 2>/dev/null || true
fi

if ! command -v werf &>/dev/null; then
  echo "ERROR: werf is not installed. Run: curl -sSL https://werf.io/install.sh | bash" >&2
  exit 1
fi

log "werf version: $(werf version)"

if [[ -f "${ROOT_DIR}/.env" ]]; then
  log "Loading .env ..."
  set -a; source "${ROOT_DIR}/.env"; set +a
fi

log "Running Vault integration ..."
source "${SCRIPT_DIR}/vault-integration.sh"

kubectl create namespace "${KUBE_NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic app-env \
  --namespace="${KUBE_NAMESPACE}" \
  --from-literal=VAULT_ADDR="${VAULT_ADDR:-http://vault.local}" \
  --from-literal=VAULT_ROLE_ID="${VAULT_ROLE_ID}" \
  --from-literal=VAULT_SECRET_ID="${VAULT_SECRET_ID}" \
  --from-literal=SECRET_KEY="${DJANGO_SECRET_KEY}" \
  --dry-run=client -o yaml | kubectl apply -f -

log "Starting werf converge (env=${WERF_ENV}) ..."

WERF_ARGS=(
  --env "${WERF_ENV}"
  --namespace "${KUBE_NAMESPACE}"
  --set "global.db.user=${POSTGRES_USER}"
  --set "global.db.password=${POSTGRES_PASSWORD}"
  --set "global.db.name=${POSTGRES_DB}"
  --set "global.django.secretKey=${DJANGO_SECRET_KEY}"
  --set "global.redis.password=${REDIS_PASSWORD}"
  --set "global.rabbitmq.username=${RABBITMQ_USERNAME}"
  --set "global.rabbitmq.password=${RABBITMQ_PASSWORD}"
  --set "backend.celery.broker.username=${RABBITMQ_USERNAME}"
  --set "backend.celery.broker.password=${RABBITMQ_PASSWORD}"
)

if [[ -n "${WERF_REPO}" ]]; then
  WERF_ARGS+=(--repo "${WERF_REPO}")
fi

werf converge "${WERF_ARGS[@]}"

log "Deployment complete!"
log "Namespace: ${KUBE_NAMESPACE}"
log "Environment: ${WERF_ENV}"

log "Pod status:"
kubectl get pods -n "${KUBE_NAMESPACE}"
