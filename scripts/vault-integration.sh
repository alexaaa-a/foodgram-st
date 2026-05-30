set -euo pipefail

VAULT_ADDR="${VAULT_ADDR:-http://127.0.0.1:8200}"
VAULT_ROLE_ID="${VAULT_ROLE_ID:?VAULT_ROLE_ID is not set}"
VAULT_SECRET_ID="${VAULT_SECRET_ID:?VAULT_SECRET_ID is not set}"

log() { echo "[vault-integration] $*" >&2; }

log "Authenticating via AppRole at ${VAULT_ADDR} ..."

VAULT_TOKEN=$(curl -sf --request POST \
  --data "{\"role_id\":\"${VAULT_ROLE_ID}\",\"secret_id\":\"${VAULT_SECRET_ID}\"}" \
  "${VAULT_ADDR}/v1/auth/approle/login" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['auth']['client_token'])")

export VAULT_TOKEN
log "AppRole auth OK, token obtained."
log "Fetching Docker Hub credentials from Vault (foodgram/docker) ..."

DOCKER_VAULT_DATA=$(curl -sf \
  -H "X-Vault-Token: ${VAULT_TOKEN}" \
  "${VAULT_ADDR}/v1/foodgram/data/docker" \
  | python3 -c "import sys,json; d=json.load(sys.stdin)['data']['data']; print(d.get('username','')); print(d.get('password',''))")

DOCKER_USERNAME=$(echo "${DOCKER_VAULT_DATA}" | sed -n '1p')
DOCKER_PASSWORD=$(echo "${DOCKER_VAULT_DATA}" | sed -n '2p')

if [[ -z "${DOCKER_USERNAME}" || -z "${DOCKER_PASSWORD}" ]]; then
  log "WARNING: Docker credentials not found in Vault (foodgram/docker)."
  log "Falling back to env vars DOCKER_USERNAME / DOCKER_PASSWORD."
  DOCKER_USERNAME="${DOCKER_USERNAME:-${DOCKER_HUB_USERNAME:-}}"
  DOCKER_PASSWORD="${DOCKER_PASSWORD:-${DOCKER_HUB_PASSWORD:-}}"
fi

export DOCKER_USERNAME DOCKER_PASSWORD

if [[ -n "${DOCKER_USERNAME}" ]]; then
  log "Docker Hub login as ${DOCKER_USERNAME} ..."
  echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin
  log "Docker Hub login OK."
else
  log "WARNING: No Docker credentials — skipping docker login."
fi

log "Fetching application secrets from Vault ..."

get_vault_field() {
  local path="$1" field="$2"
  curl -sf \
    -H "X-Vault-Token: ${VAULT_TOKEN}" \
    "${VAULT_ADDR}/v1/foodgram/data/${path}" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['data']['${field}'])"
}

export POSTGRES_USER=$(get_vault_field db POSTGRES_USER)
export POSTGRES_PASSWORD=$(get_vault_field db POSTGRES_PASSWORD)
export POSTGRES_DB=$(get_vault_field db POSTGRES_DB)
export DJANGO_SECRET_KEY=$(get_vault_field backend secret_key)
export REDIS_PASSWORD=$(get_vault_field redis password)
export RABBITMQ_USERNAME=$(get_vault_field rabbitmq username)
export RABBITMQ_PASSWORD=$(get_vault_field rabbitmq password)

log "All secrets fetched successfully."
log "PostgreSQL: user=${POSTGRES_USER}, db=${POSTGRES_DB}"
log "Vault integration complete — environment is ready for werf converge."
