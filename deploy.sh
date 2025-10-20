set -e

export VAULT_ADDR=http://vault.local
export VAULT_AUTH_METHOD=${VAULT_AUTH_METHOD}
export VAULT_ROLE_ID=${VAULT_ROLE_ID}
export VAULT_SECRET_ID=${VAULT_SECRET_ID}
export POSTGRES_PASSWORD=$(kubectl get secret db-secrets -n foodgram -o jsonpath="{.data.postgres-password}" | base64 -d)

echo "foo: ref+vault://secret/data/foodgram/db#POSTGRES_USER" | vals eval

POSTGRES_USER=$(vals eval -f tmp-secrets.yaml -s -o yaml | grep POSTGRES_USER | awk '{print $2}')
POSTGRES_DB=$(vals eval -f tmp-secrets.yaml -s -o yaml | grep POSTGRES_DB | awk '{print $2}')
POSTGRES_PASSWORD=$(vals eval -f tmp-secrets.yaml -s -o yaml | grep POSTGRES_PASSWORD | awk '{print $2}')

echo "POSTGRES_USER=$POSTGRES_USER"
echo "POSTGRES_DB=$POSTGRES_DB"
echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD"

helm upgrade --install foodgram-helm ./foodgram-helm \
  -n foodgram \
  -f foodgram-helm/values.yaml \
  --set postgresql.auth.username=$POSTGRES_USER \
  --set postgresql.auth.database=$POSTGRES_DB \
  --set postgresql.auth.postgresPassword=$POSTGRES_PASSWORD

