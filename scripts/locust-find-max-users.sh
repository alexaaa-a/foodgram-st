set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

if [[ -f backend/locust.env ]]; then
  set -a
  source backend/locust.env
  set +a
fi

HOST="${LOCUST_HOST:-http://localhost:8000}"
SPAWN_RATE="${LOCUST_SPAWN_RATE:-5}"
RUN_TIME="${LOCUST_RUN_TIME:-90s}"
MAX_AVG_SEC="${LOCUST_MAX_AVG_RESPONSE_SEC:-7}"
USER_STEPS="${USER_STEPS:-5 10 20 30 50 80 100}"

REPORT_DIR="${ROOT_DIR}/loadtest-reports"
mkdir -p "$REPORT_DIR"

echo "Host: $HOST"
echo "Spawn rate: $SPAWN_RATE/s, duration: $RUN_TIME"
echo "Criteria: 0% failures, avg response < ${MAX_AVG_SEC}s"
echo "---"

LAST_OK_USERS=0

for USERS in $USER_STEPS; do
  PREFIX="${REPORT_DIR}/users_${USERS}"
  echo ">>> Testing with $USERS users..."

  locust -f backend/locustfile.py \
    --headless \
    --host="$HOST" \
    -u "$USERS" \
    -r "$SPAWN_RATE" \
    -t "$RUN_TIME" \
    --only-summary \
    --csv="$PREFIX" \
    AnonymousUser 2>&1 | tail -20

  STATS="${PREFIX}_stats.csv"
  if [[ ! -f "$STATS" ]]; then
    echo "    No stats file, skip."
    continue
  fi

  LINE=$(grep -E ',Aggregated,' "$STATS" || true)
  if [[ -z "$LINE" ]]; then
    echo "    No Aggregated row in $STATS"
    continue
  fi

  FAIL_COUNT=$(echo "$LINE" | cut -d, -f4)
  AVG_MS=$(echo "$LINE" | cut -d, -f6)
  REQ_COUNT=$(echo "$LINE" | cut -d, -f3)

  if [[ -z "$AVG_MS" || "$AVG_MS" == "N/A" ]]; then
    AVG_SEC=999
  else
    AVG_SEC=$(awk "BEGIN {printf \"%.2f\", $AVG_MS / 1000}")
  fi

  FAIL_COUNT=${FAIL_COUNT:-0}
  REQ_COUNT=${REQ_COUNT:-0}

  if [[ "$REQ_COUNT" -gt 0 ]]; then
    FAIL_PCT=$(awk "BEGIN {printf \"%.1f\", 100 * $FAIL_COUNT / $REQ_COUNT}")
  else
    FAIL_PCT=100
  fi

  echo "    Requests: $REQ_COUNT, failures: $FAIL_COUNT (${FAIL_PCT}%), avg: ${AVG_SEC}s"

  OK=1
  [[ "$FAIL_COUNT" -gt 0 ]] && OK=0
  awk "BEGIN {exit !($AVG_SEC < $MAX_AVG_SEC)}" || OK=0

  if [[ "$OK" -eq 1 ]]; then
    LAST_OK_USERS=$USERS
    echo "    OK — within limits."
  else
    echo "    FAIL — threshold exceeded."
    echo ""
    echo "Maximum stable users (last OK step): $LAST_OK_USERS"
    echo "Reports: $REPORT_DIR"
    exit 0
  fi
  echo ""
done

echo "All steps passed. Try higher USER_STEPS, e.g.:"
echo "  USER_STEPS='120 150 200' ./scripts/locust-find-max-users.sh"
echo "Maximum stable users in this run: $LAST_OK_USERS"
echo "Reports: $REPORT_DIR"
