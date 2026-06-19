#!/usr/bin/env bash
set -euo pipefail

# Helper to run the download + processing steps locally to simulate the workflow
# Usage: ./run-local.sh [source-file]

SOURCE_FILE=${1:-source-list.txt}

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
    /xmux/ { next }
    /extra/ { next }
    /type=tcp/ && /sec(urity|ure)=none/ { next }
    /sec(urity|ure)=none/ && !/type=xhttp/ { next }
    { print }
  ' "$file" >> WHITE_LIST_PROXY_COLLECTION.txt
done

echo "Results saved to WHITE_LIST_PROXY_COLLECTION.txt"
