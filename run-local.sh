#!/usr/bin/env bash
set -euo pipefail

# Helper to run the download + processing steps locally to simulate the workflow
# Usage: ./run-local.sh [source-file]

SOURCE_FILE=${1:-source-list.txt}

rm -rf input/*
mkdir -p input

if [ ! -f "$SOURCE_FILE" ]; then
  echo "Source file $SOURCE_FILE not found" >&2
  exit 1
fi

# Read non-comment lines
mapfile -t lines < <(grep -E '^[[:space:]]*[^#[:space:]]' "$SOURCE_FILE" || true)

idx=0
for url in "${lines[@]}"; do
  url=$(echo "$url" | tr -d '\r' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
  if [ -z "$url" ]; then
    continue
  fi
  idx=$((idx+1))
  out="input/${idx}.txt"

  echo "Downloading $url -> $out"
  if curl -fsSL "$url" -o "$out"; then
    echo "Saved $out"
  else
    echo "Warning: failed to download $url"
    rm -f "$out" || true
  fi
done

# Filter this run's inputs and preserve duplicates in its snapshot.
archive_dir="WHITE_LIST_PROXY_COLLECTION"
mkdir -p "$archive_dir"
current=$(mktemp)
combined=$(mktemp)
trap 'rm -f "$current" "$combined"' EXIT

shopt -s nullglob
for file in input/*.txt; do
  echo "Processing $file..."
  awk '
    /^(ss|socks):\/\// { next }
    /xtls-rprx-vision-udp443/ { next }
    /Russia|RU|%F0%9F%87%B7%F0%9F%87%BA%20|Россия/ { next }
    /xmux/ { next }
    /extra/ { next }
    /type=tcp/ && /sec(urity|ure)=none/ { next }
    /sec(urity|ure)=none/ && !/type=xhttp/ { next }
    { print }
  ' "$file" >> "$current"
done

now_epoch=$(date -u +%s)
now_utc=$(date -u +%Y%m%dT%H%M%SZ)
run_id=${GITHUB_RUN_ID:-local-$$}
run_attempt=${GITHUB_RUN_ATTEMPT:-1}
snapshot="$archive_dir/${now_utc}-${now_epoch}-${run_id}-${run_attempt}.txt"
cp "$current" "$snapshot"

cutoff_epoch=$((now_epoch - 72 * 60 * 60))
for snapshot_file in "$archive_dir"/*.txt; do
  snapshot_name=${snapshot_file##*/}
  snapshot_epoch=${snapshot_name#*-}
  snapshot_epoch=${snapshot_epoch%%-*}
  if [[ "$snapshot_epoch" =~ ^[0-9]+$ ]] && (( snapshot_epoch <= cutoff_epoch )); then
    rm -f "$snapshot_file"
  fi
done

# Combine oldest-to-newest snapshots and keep each entry's first occurrence.
for snapshot_file in "$archive_dir"/*.txt; do
  cat "$snapshot_file" >> "$combined"
done
awk '!seen[$0]++' "$combined" > WHITE_LIST_PROXY_COLLECTION.txt

tmp=$(mktemp)
new=$(mktemp)
awk 'BEGIN { IGNORECASE = 0 } /^(hysteria2|hy2):\/\// { print }' WHITE_LIST_PROXY_COLLECTION.txt > "$new"
if [ -s "$new" ]; then
  now=$(date '+%Y-%m-%d %H:%M:%S')
  count=$(wc -l < "$new" | tr -d '[:space:]')
  printf '# %s (%s keys added)\n' "$now" "$count" > "$tmp"
  cat "$new" >> "$tmp"
  printf '\n' >> "$tmp"
fi
if [ -f HYSTERIA2.txt ]; then
  cat HYSTERIA2.txt >> "$tmp"
fi
awk '!seen[$0]++' "$tmp" > HYSTERIA2.txt || true
rm -f "$tmp" "$new"

tmp=$(mktemp)
new=$(mktemp)
awk '/^trojan:\/\// { print }' WHITE_LIST_PROXY_COLLECTION.txt > "$new"
if [ -s "$new" ]; then
  now=$(date '+%Y-%m-%d %H:%M:%S')
  count=$(wc -l < "$new" | tr -d '[:space:]')
  printf '# %s (%s keys added)\n' "$now" "$count" > "$tmp"
  cat "$new" >> "$tmp"
  printf '\n' >> "$tmp"
fi
if [ -f TROJAN.txt ]; then
  cat TROJAN.txt >> "$tmp"
fi
awk '!seen[$0]++' "$tmp" > TROJAN.txt || true
rm -f "$tmp" "$new"

tmp=$(mktemp)
new=$(mktemp)
awk '/^vless:\/\/.*[?&]type=xhttp(&|#|$)/ && !seen[$0]++ { print }' WHITE_LIST_PROXY_COLLECTION.txt > "$new"
if [ -s "$new" ]; then
  now=$(date '+%Y-%m-%d %H:%M:%S')
  count=$(wc -l < "$new" | tr -d '[:space:]')
  printf '# %s (%s current keys)\n' "$now" "$count" > "$tmp"
  cat "$new" >> "$tmp"
  printf '\n' >> "$tmp"
fi
mv "$tmp" XHTTP.txt
echo "Extracted xhttp lines:" "$(wc -l < "$new")"
rm -f "$new"

echo "Lines & filename:" $(wc -l WHITE_LIST_PROXY_COLLECTION.txt)

