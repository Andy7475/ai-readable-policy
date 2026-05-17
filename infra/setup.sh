#!/usr/bin/env bash
# One-time infrastructure setup for ai-readable-policy demo.
# Safe to re-run — all operations are idempotent.
set -euo pipefail

PROJECT=cyberchefcloud
BUCKET=gs://cyber-chef-cloud-public
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Applying CORS config to ${BUCKET}..."
gcloud storage buckets update "${BUCKET}" \
  --cors-file="${SCRIPT_DIR}/cors.json" \
  --project="${PROJECT}"

echo "==> Infrastructure setup complete."
echo "    Bucket ${BUCKET} is ready."
echo "    Run scripts/build_and_deploy.sh to publish the demo."
