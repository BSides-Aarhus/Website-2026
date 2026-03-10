#!/usr/bin/env bash
# fetch-tickets.sh — Fetches ticket data from Ticket Butler API
# Runs at build time in GitHub Actions. Writes data/tickets.json for Hugo.
#
# Required env vars:
#   TICKETBUTLER_API_TOKEN — API token from Ticket Butler dashboard
#
# Optional env vars:
#   TICKETBUTLER_EVENT_UUID — Skip event discovery, use this UUID directly

set -euo pipefail

API_BASE="https://bsidesaarhus.ticketbutler.io/api/v3"
TOKEN="${TICKETBUTLER_API_TOKEN:-}"
DATA_DIR="$(cd "$(dirname "$0")/../data" && pwd)"
OUTPUT="$DATA_DIR/tickets.json"

if [ -z "$TOKEN" ]; then
  echo "⚠️  TICKETBUTLER_API_TOKEN not set — skipping fetch, using existing data/tickets.json"
  exit 0
fi

AUTH_HEADER="Authorization: Token $TOKEN"

# Step 1: Get the event UUID (use first active event, or use explicit UUID)
EVENT_UUID="${TICKETBUTLER_EVENT_UUID:-}"

if [ -z "$EVENT_UUID" ]; then
  echo "🔍 Discovering events..."
  EVENTS=$(curl -sf -H "$AUTH_HEADER" "$API_BASE/events/" 2>/dev/null || echo "[]")

  EVENT_UUID=$(echo "$EVENTS" | jq -r '.[0].uuid // empty')

  if [ -z "$EVENT_UUID" ]; then
    echo "⚠️  No events found — skipping fetch"
    exit 0
  fi
  echo "✅ Found event: $(echo "$EVENTS" | jq -r '.[0].title // "Unknown"') ($EVENT_UUID)"
fi

# Step 2: Fetch ticket types
echo "🎫 Fetching ticket types..."
TICKET_TYPES=$(curl -sf -H "$AUTH_HEADER" "$API_BASE/events/$EVENT_UUID/ticket-types/" 2>/dev/null || echo "[]")

# Step 3: Build the data file
TOTAL_SOLD=$(echo "$TICKET_TYPES" | jq '[.[].amount_sold // 0] | add // 0')
TOTAL_AVAILABLE=$(echo "$TICKET_TYPES" | jq '[.[].amount_total // 0] | add // 0')
FETCHED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Build clean JSON for Hugo
jq -n \
  --arg event_uuid "$EVENT_UUID" \
  --arg fetched_at "$FETCHED_AT" \
  --argjson total_sold "$TOTAL_SOLD" \
  --argjson total_available "$TOTAL_AVAILABLE" \
  --argjson ticket_types "$TICKET_TYPES" \
  '{
    event_uuid: $event_uuid,
    total_sold: $total_sold,
    total_available: $total_available,
    fetched_at: $fetched_at,
    ticket_types: [
      $ticket_types[] | {
        uuid: .uuid,
        title: .title,
        price: .price,
        currency: (.currency // "DKK"),
        amount_total: (.amount_total // 0),
        amount_sold: (.amount_sold // 0),
        amount_remaining: ((.amount_total // 0) - (.amount_sold // 0)),
        is_sold_out: ((.amount_sold // 0) >= (.amount_total // 0)),
        active: (.active // true)
      }
    ]
  }' > "$OUTPUT"

echo "✅ Wrote $OUTPUT"
echo "   Total sold: $TOTAL_SOLD / $TOTAL_AVAILABLE"
jq -r '.ticket_types[] | "   - \(.title): \(.amount_sold)/\(.amount_total) (\(.price) \(.currency))"' "$OUTPUT"
