#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${ROOT_DIR}/dist"

PYTHON="${ROOT_DIR}/.venv/bin/python"

cd "${ROOT_DIR}"

echo "==> Cleaning previous artifacts"

rm -rf "${DIST_DIR}"
mkdir -p "${DIST_DIR}"

rm -rf build
rm -rf src/*.egg-info
rm -rf adapters/fastapi/build
rm -rf adapters/fastapi/dist
rm -rf adapters/fastapi/*.egg-info
rm -rf adapters/sqlalchemy/build
rm -rf adapters/sqlalchemy/dist
rm -rf adapters/sqlalchemy/*.egg-info

echo "==> Building core package"

"${PYTHON}" -m build \
    --outdir "${DIST_DIR}" \
    .

echo "==> Building FastAPI adapter"

"${PYTHON}" -m build \
    --outdir "${DIST_DIR}" \
    adapters/fastapi

echo "==> Building SQLAlchemy adapter"

"${PYTHON}" -m build \
    --outdir "${DIST_DIR}" \
    adapters/sqlalchemy

echo "==> Checking artifacts"

"${PYTHON}" -m twine check \
    "${DIST_DIR}"/*

echo "==> Listing artifacts"

find "${DIST_DIR}" \
    -maxdepth 1 \
    -type f \
    -print \
    | sort

echo "==> Release validation complete"