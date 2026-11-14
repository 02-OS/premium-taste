#!/usr/bin/env bash
set -euo pipefail

# Zero-clone installer for Premium Taste.
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/02-OS/premium-taste/master/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/02-OS/premium-taste/master/install.sh | bash -s -- /path/to/app --agent all --mcp

REPO_URL="${PREMIUM_TASTE_REPO:-https://github.com/02-OS/premium-taste.git}"
REF="${PREMIUM_TASTE_REF:-master}"
ARCHIVE_URL="${PREMIUM_TASTE_ARCHIVE:-https://github.com/02-OS/premium-taste/archive/refs/heads/${REF}.tar.gz}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required to install Premium Taste." >&2
  exit 1
fi

TARGET="."
EXTRA_ARGS=()
if [ "$#" -gt 0 ] && [[ "${1:-}" != -* ]]; then
  TARGET="$1"
  shift
fi
if [ "$#" -gt 0 ]; then
  EXTRA_ARGS=("$@")
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

if command -v git >/dev/null 2>&1; then
  git clone --quiet --depth 1 --branch "$REF" "$REPO_URL" "$TMP_DIR/repo"
  SRC_DIR="$TMP_DIR/repo"
else
  curl -fsSL "$ARCHIVE_URL" -o "$TMP_DIR/repo.tar.gz"
  tar -xzf "$TMP_DIR/repo.tar.gz" -C "$TMP_DIR"
  SRC_DIR="$(find "$TMP_DIR" -maxdepth 1 -mindepth 1 -type d | head -n 1)"
fi

python3 "$SRC_DIR/scripts/install.py" "$TARGET" "${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"}"
