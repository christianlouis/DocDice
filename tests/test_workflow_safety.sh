#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build="$repo_root/.github/workflows/docker-image.yml"
deploy="$repo_root/.github/workflows/deploy.yaml"

grep -Fq 'name: Build and Publish Container' "$build"
grep -Fq "if: github.event_name == 'pull_request'" "$build"
grep -Fq 'push: false' "$build"
grep -Fq "if: github.event_name == 'push'" "$build"
grep -Fq 'push: true' "$build"
grep -Fq "github.ref == 'refs/heads/main' && 'latest'" "$build"
if grep -Fq 'Build and Push Docker Image' "$build"; then
  printf 'unsafe legacy container workflow pattern found\n' >&2
  exit 1
fi
grep -Fq 'workflow_dispatch:' "$deploy"
grep -Fq "if: github.ref == 'refs/heads/main'" "$deploy"
grep -Fq 'DEPLOY_WEBHOOK_URL: ${{ secrets.DEPLOY_WEBHOOK_URL }}' "$deploy"
grep -Fq 'DEPLOY_WEBHOOK_TOKEN: ${{ secrets.DEPLOY_WEBHOOK_TOKEN }}' "$deploy"
if grep -Fq 'docker2.kuechenserver.org' "$deploy"; then
  printf 'literal deployment endpoint found\n' >&2
  exit 1
fi
printf 'workflow trigger and secret-safety checks passed\n'
