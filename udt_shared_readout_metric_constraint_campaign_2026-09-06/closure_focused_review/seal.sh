#!/usr/bin/env bash
set -euo pipefail
cd /tmp/tri_closure_final_delta.XLU1Mh
[[ ! -e REVIEW_SHA256SUMS ]]
review_files=(*)
sha256sum -- "${review_files[@]}" > REVIEW_SHA256SUMS
sha256sum --check REVIEW_SHA256SUMS
printf 'Payload count: %s\n' "${#review_files[@]}"
sha256sum REVIEW_SHA256SUMS FOCUSED_FIDELITY_REVIEW.md
