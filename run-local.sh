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

# Run existing filtering pipeline
> WHITE_LIST_PROXY_COLLECTION.txt
for file in input/*.txt; do
  echo "Processing $file..."
  awk '
    /xtls-rprx-vision-udp443/ { next }
    /Russia|RU|%F0%9F%87%B7%F0%9F%87%BA%20|Россия/ { next }
    /xmux/ { next }
    /extra/ { next }
    /type=tcp/ && /sec(urity|ure)=none/ { next }
    /sec(urity|ure)=none/ && !/type=xhttp/ { next }
    { print }
  ' "$file" >> WHITE_LIST_PROXY_COLLECTION.txt
done

awk '!seen[$0]++' WHITE_LIST_PROXY_COLLECTION.txt > WHITE_LIST_PROXY_COLLECTION.tmp || true
mv WHITE_LIST_PROXY_COLLECTION.tmp WHITE_LIST_PROXY_COLLECTION.txt || true

awk 'BEGIN { IGNORECASE = 0 } /^(hysteria2|hy2):\/\// { print }' WHITE_LIST_PROXY_COLLECTION.txt > HYSTERIA2.txt

echo "Lines & filename:" $(wc -l WHITE_LIST_PROXY_COLLECTION.txt)

