#!/usr/bin/env bash
# Build policy HTML + search index, then deploy to GCS.
# Usage: ./scripts/build_and_deploy.sh
set -euo pipefail

PROJECT=cyberchefcloud
BUCKET=gs://cyber-chef-cloud-public
PREFIX=ai-readable-policy
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DIST="${REPO_ROOT}/dist"

echo "==> Building..."
cd "${REPO_ROOT}"
uv run --with markdown --with jinja2 --with pyyaml --with python-slugify --with beautifulsoup4 \
  python src/build.py

echo ""
echo "==> Deploying to ${BUCKET}/${PREFIX}/..."
gcloud storage cp --recursive "${DIST}/" "${BUCKET}/${PREFIX}/" \
  --project="${PROJECT}"

echo ""
echo "==> Setting cache headers..."

# Search index: never cache (must reflect latest build)
gcloud storage objects update "${BUCKET}/${PREFIX}/search-index.json" \
  --cache-control="no-cache, no-store" \
  --project="${PROJECT}"

# Main UI: short cache
gcloud storage objects update "${BUCKET}/${PREFIX}/index.html" \
  --cache-control="max-age=300" \
  --project="${PROJECT}"

# JS + CSS: longer cache (versioned by content)
for asset in app.js style.css; do
  gcloud storage objects update "${BUCKET}/${PREFIX}/${asset}" \
    --cache-control="max-age=3600" \
    --project="${PROJECT}"
done

PUBLIC_URL="https://storage.googleapis.com/cyber-chef-cloud-public/${PREFIX}/index.html"
echo ""
echo "==> Deployed successfully."
echo "    Live at: ${PUBLIC_URL}"
