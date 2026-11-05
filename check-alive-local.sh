#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$ROOT_DIR/.bin"
SING_BOX_VERSION="1.14.4"
XRAY_VERSION="26.10.31"
LEGACY_XRAY_VERSION="1.8.24"

SING_BOX_BIN=""
XRAY_BIN=""
LEGACY_XRAY_BIN=""
TEMP_DIRS=()

for tool in curl python3; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Required tool is missing: $tool" >&2
    exit 1
  fi
done

cleanup() {
  local temp_dir
  for temp_dir in "${TEMP_DIRS[@]}"; do
    rm -rf -- "$temp_dir"
  done
}
trap cleanup EXIT

check_local_binary() {
  local command_name="$1"
  local expected_version="$2"
  local result_variable="$3"
  local installed_path

  if installed_path="$(command -v "$command_name")" \
    && "$installed_path" version 2>&1 | grep -Fq "$expected_version"; then
    printf -v "$result_variable" '%s' "$installed_path"
    echo "Using installed $command_name ($expected_version): $installed_path"
    return 0
  fi

  return 1
}

check_cached_binary() {
  local binary_path="$1"
  local expected_version="$2"

  [[ -x "$binary_path" ]] \
    && "$binary_path" version 2>&1 | grep -Fq "$expected_version"
}

require_linux_amd64_for_download() {
  if [[ "$(uname -s)" != "Linux" || "$(uname -m)" != "x86_64" ]]; then
    echo "Automatic binary downloads currently support Linux x86_64 only." >&2
    echo "Install the required pinned binaries and add them to PATH, then retry." >&2
    exit 1
  fi

  for tool in curl find install mktemp sha256sum tar unzip; do
    if ! command -v "$tool" >/dev/null 2>&1; then
      echo "Required tool for downloading binaries is missing: $tool" >&2
      exit 1
    fi
  done
}

install_sing_box() {
  local temp_dir
  temp_dir="$(mktemp -d "$BIN_DIR/.sing-box-install.XXXXXX")"
  TEMP_DIRS+=("$temp_dir")
  local archive="$temp_dir/sing-box-${SING_BOX_VERSION}-linux-amd64.tar.gz"

  echo "Downloading sing-box $SING_BOX_VERSION into $BIN_DIR"
  curl -fsSL \
    "https://github.com/SagerNet/sing-box/releases/download/v${SING_BOX_VERSION}/sing-box-${SING_BOX_VERSION}-linux-amd64.tar.gz" \
    -o "$archive"
  echo "699a1b510aa4396b2176d32d1181920399ebf1e267835da6f3b598d0f7c24968  $archive" \
    | sha256sum --check

  mkdir "$temp_dir/unpacked"
  tar -xzf "$archive" -C "$temp_dir/unpacked"
  local binary
  binary="$(find "$temp_dir/unpacked" -type f -name sing-box -print -quit)"
  if [[ -z "$binary" ]]; then
    echo "sing-box executable was not found in the downloaded archive" >&2
    return 1
  fi
  install -m 0755 "$binary" "$BIN_DIR/sing-box"
  SING_BOX_BIN="$BIN_DIR/sing-box"
}

install_xray() {
  local temp_dir
  temp_dir="$(mktemp -d "$BIN_DIR/.xray-install.XXXXXX")"
  TEMP_DIRS+=("$temp_dir")
  local archive="$temp_dir/Xray-${XRAY_VERSION}-linux-64.zip"

  echo "Downloading Xray $XRAY_VERSION into $BIN_DIR"
  curl -fsSL \
    "https://github.com/XTLS/Xray-core/releases/download/v${XRAY_VERSION}/Xray-linux-64.zip" \
    -o "$archive"
  echo "e4bd9119f50ae7c41658b1abd0679ae06f98bd864a2907ff33f2f2cf7081b214  $archive" \
    | sha256sum --check
  unzip -q "$archive" xray -d "$temp_dir"
  install -m 0755 "$temp_dir/xray" "$BIN_DIR/xray"
  XRAY_BIN="$BIN_DIR/xray"
}

install_legacy_xray() {
  local temp_dir
  temp_dir="$(mktemp -d "$BIN_DIR/.legacy-xray-install.XXXXXX")"
  TEMP_DIRS+=("$temp_dir")
  local archive="$temp_dir/Xray-${LEGACY_XRAY_VERSION}-linux-64.zip"

  echo "Downloading legacy Xray $LEGACY_XRAY_VERSION into $BIN_DIR"
  curl -fsSL \
    "https://github.com/XTLS/Xray-core/releases/download/v${LEGACY_XRAY_VERSION}/Xray-linux-64.zip" \
    -o "$archive"
  echo "47a860787e823474a358d6bca536547df6dd08b69c6de482ea92a9e7e8f8969c  $archive" \
    | sha256sum --check
  unzip -q "$archive" xray -d "$temp_dir"
  install -m 0755 "$temp_dir/xray" "$BIN_DIR/xray-legacy"
  LEGACY_XRAY_BIN="$BIN_DIR/xray-legacy"
}

resolve_binary() {
  local command_name="$1"
  local target_path="$2"
  local expected_version="$3"
  local result_variable="$4"

  if check_local_binary "$command_name" "$expected_version" "$result_variable"; then
    return
  fi

  if check_cached_binary "$target_path" "$expected_version"; then
    printf -v "$result_variable" '%s' "$target_path"
    echo "Using cached $command_name ($expected_version): $target_path"
    return
  fi

  require_linux_amd64_for_download
  mkdir -p "$BIN_DIR"
  case "$command_name" in
    sing-box) install_sing_box ;;
    xray) install_xray ;;
    xray-legacy) install_legacy_xray ;;
    *) echo "Unknown binary: $command_name" >&2; return 1 ;;
  esac
  echo "Installed $command_name ($expected_version)"
}

resolve_binary sing-box "$BIN_DIR/sing-box" "$SING_BOX_VERSION" SING_BOX_BIN
resolve_binary xray "$BIN_DIR/xray" "$XRAY_VERSION" XRAY_BIN
resolve_binary xray-legacy "$BIN_DIR/xray-legacy" "$LEGACY_XRAY_VERSION" LEGACY_XRAY_BIN

cd "$ROOT_DIR"
echo "Running proxy health tests..."
python3 -B -m unittest discover -s tests -p 'test_check_alive.py'

echo "Rebuilding ALIVE.txt from WHITE_LIST_PROXY_COLLECTION.txt..."
python3 -B scripts/check_alive.py \
  "$SING_BOX_BIN" \
  "$XRAY_BIN" \
  "$LEGACY_XRAY_BIN" \
  WHITE_LIST_PROXY_COLLECTION.txt \
  ALIVE.txt

echo "Done. ALIVE.txt was updated locally; no commit or push was performed."
