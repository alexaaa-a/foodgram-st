set -e
set -a
source /Users/alexandrakalimullina/PycharmProjects/foodgram-st/.env
set +a

export VAULT_ADDR=http://vault.local
export VAULT_AUTH_METHOD=${VAULT_AUTH_METHOD}
export VAULT_ROLE_ID=${VAULT_ROLE_ID}
export VAULT_SECRET_ID=${VAULT_SECRET_ID}

echo "foo: ref+vault://secret/data/foodgram/db#POSTGRES_USER" | vals eval

kubectl create namespace foodgram --dry-run=client -o yaml | kubectl apply -f -
helm secrets --evaluate-templates -b vals upgrade --install postgres ./foodgram-helm/charts/db -n foodgram \
  -f foodgram-helm/charts/db/values.yaml \

helm secrets --evaluate-templates -b vals upgrade --install rabbitmq ./foodgram-helm/charts/rabbitmq -n foodgram -f foodgram-helm/charts/rabbitmq/values.yml

helm secrets --evaluate-templates -b vals upgrade --install backend ./foodgram-helm/charts/backend -n foodgram \
  -f foodgram-helm/charts/backend/values.yaml

helm secrets --evaluate-templates -b vals upgrade --install nginx ./foodgram-helm/charts/nginx -n foodgram \
  -f foodgram-helm/charts/nginx/values.yaml

helm secrets --evaluate-templates -b vals upgrade --install jobs ./foodgram-helm/charts/jobs -n foodgram \
  -f foodgram-helm/charts/jobs/values.yaml

helm secrets --evaluate-templates -b vals upgrade --install celery ./foodgram-helm/charts/celery -n foodgram \
  -f foodgram-helm/charts/celery/values.yaml

helm secrets --evaluate-templates -b vals upgrade --install flower ./foodgram-helm/charts/flower -n foodgram \
  -f foodgram-helm/charts/flower/values.yaml
