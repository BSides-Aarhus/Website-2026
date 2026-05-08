#!/usr/bin/env bash
# Mirror content/sessions/*.md and content/speakers/*.md to *.da.md
# (talks are held in English — same content shown on both /sessions/ and /da/sessions/)
# _index.md files are skipped: each language has its own real translation.
set -euo pipefail

cd "$(dirname "$0")/.."

for dir in content/sessions content/speakers; do
  for src in "$dir"/*.md; do
    base=$(basename "$src" .md)
    case "$base" in
      _index|*.da) continue ;;
    esac
    cp "$src" "$dir/${base}.da.md"
  done
done

echo "Synced session/speaker translations."
