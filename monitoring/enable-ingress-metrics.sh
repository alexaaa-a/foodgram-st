#!/usr/bin/env bash
# enable-ingress-metrics.sh — включить Prometheus-метрики ingress-nginx (v1.12+)
set -euo pipefail

NAMESPACE="${INGRESS_NAMESPACE:-ingress-nginx}"
DEPLOYMENT="${INGRESS_DEPLOYMENT:-ingress-nginx-controller}"

if kubectl get deployment "${DEPLOYMENT}" -n "${NAMESPACE}" \
  -o jsonpath='{.spec.template.spec.containers[0].args}' \
  | grep -q 'enable-metrics=true'; then
  echo "✓ Metrics already enabled on ${DEPLOYMENT}"
  exit 0
fi

kubectl patch deployment "${DEPLOYMENT}" -n "${NAMESPACE}" --type='json' -p='[
  {"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--enable-metrics=true"}
]'

kubectl rollout status deployment/"${DEPLOYMENT}" -n "${NAMESPACE}" --timeout=120s
echo "✓ ingress-nginx metrics enabled"
