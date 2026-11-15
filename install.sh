#!/usr/bin/env bash
set -euo pipefail

# Zero-clone installer for Premium Taste.
# Flags may come before the target directory. The target defaults to ".".
#   curl -fsSL https://raw.githubusercontent.com/02-OS/premium-taste/master/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/02-OS/premium-taste/master/install.sh | bash -s -- --agent all --mcp /path/to/app
#   curl -fsSL https://raw.githubusercontent.com/02-OS/premium-taste/master/install.sh | bash -s -- /path/to/app --agent all --mcp

REPO_URL="${PREMIUM_TASTE_REPO:-https://github.com/02-OS/premium-taste.git}"
REF="${PREMIUM_TASTE_REF:-master}"
# GitHub serves a branch, a tag, and a commit at /archive/<ref>.tar.gz.
ARCHIVE_URL="${PREMIUM_TASTE_ARCHIVE:-https://github.com/02-OS/premium-taste/archive/${REF}.tar.gz}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required to install Premium Taste." >&2
  exit 1
fi

TARGET="."
EXTRA_ARGS=()
while [ "$#" -gt 0 ]; do
  case "$1" in
    --agent)
      if [ "$#" -lt 2 ]; then
        echo "Error: --agent requires a value." >&2
        exit 1
      fi
      EXTRA_ARGS+=("$1" "$2")
      shift 2
      ;;
    --uninstall|--no-agents-md|--mcp|--dry-run)
      EXTRA_ARGS+=("$1")
      shift
      ;;
    --)
      shift
      break
      ;;
    -*)
      EXTRA_ARGS+=("$1")
      shift
      ;;
    *)
      TARGET="$1"
      shift
      ;;
  esac
done
while [ "$#" -gt 0 ]; do
  if [[ "$1" == -* ]]; then
    EXTRA_ARGS+=("$1")
  else
    TARGET="$1"
  fi
  shift
done

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

if command -v git >/dev/null 2>&1; then
  if [[ "$REF" =~ ^[0-9a-fA-F]{7,40}$ ]]; then
    git clone --quiet "$REPO_URL" "$TMP_DIR/repo"
    git -C "$TMP_DIR/repo" checkout --quiet "$REF"
  else
    git clone --quiet --depth 1 --branch "$REF" "$REPO_URL" "$TMP_DIR/repo"
  fi
  SRC_DIR="$TMP_DIR/repo"
else
  curl -fsSL "$ARCHIVE_URL" -o "$TMP_DIR/repo.tar.gz"
  tar -xzf "$TMP_DIR/repo.tar.gz" -C "$TMP_DIR"
  SRC_DIR="$(find "$TMP_DIR" -maxdepth 1 -mindepth 1 -type d | head -n 1)"
fi

python3 "$SRC_DIR/scripts/install.py" "$TARGET" ${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"}
