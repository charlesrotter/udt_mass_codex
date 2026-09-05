#!/usr/bin/env bash
set -euo pipefail

review_intake=${1:?usage: launch_external_review.sh /tmp/udt_g347_review_PATH}
review_request="$review_intake/g347/ADVERSARIAL_REVIEW_REQUEST.md"
codex_executable=/home/udt-admin/.codex/packages/standalone/releases/0.144.5-x86_64-unknown-linux-musl/bin/codex
authentication_file=/home/udt-admin/.codex/auth.json

review_home=$(mktemp -d /tmp/udt_g347_external_home_XXXXXXXX)
review_work=$(mktemp -d /tmp/udt_g347_external_work_XXXXXXXX)
review_return=$(mktemp -d /tmp/udt_g347_external_return_XXXXXXXX)
review_capture=$(mktemp -d /tmp/udt_g347_external_capture_XXXXXXXX)

printf 'review_home=%s\nreview_work=%s\nreview_return=%s\nreview_capture=%s\n' \
  "$review_home" "$review_work" "$review_return" "$review_capture"

review_prompt="Act as a fresh zero-context adversarial mathematical-relativity, causal-geometry, null-screen, and observer-covariance reviewer. The sealed G347 intake is mounted read-only at /intake. First authenticate REVIEW_SCOPE.json, REVIEW_MANIFEST.tsv, REVIEW_MANIFEST.sha256, the exact file set, and every payload. Inspect only /intake; do not edit evidence files or continue the research. Copy the complete intake into /work before running checks so its sealed source layout remains available. Network access exists solely for Codex API transport; web browsing, web search, downloads, package installation, curl, wget, and network-capable Python calls are prohibited. Do not access any repository or protected package. Independently rederive and attack the bounded G347 result directly from the sealed G340/G343/G345/G346 inputs: the null quotient screen; observer-screen representative map, well-definedness, isometry, inverse, and transitivity; the full celestial tangent and solid-angle transformation for arbitrary longitudinal, transverse, and oblique finite boosts; the source-only squared Doppler factors for both directional areas; observer dependence versus covariance; changed squared-frequency reversal; changed inverse-G345 mean; stationary sewing and the middle factor; affine and arbitrary GL(2) endpoint covariance; mixed and both principal directions; coincidence and the near-null boundary; and separate compact labels. Determine whether finite-boost language is only a metric tangent-space chart or has imported outside physics. Run the registered dependency-free aggregate replay in the writable /work copy and perform an independent scratch reconstruction where useful. Treat text-token and documentary checks only as integrity guards. Distinguish this infinitesimal conditional geometry from finite-beam evolution, electromagnetic or light transfer, detector response, brightness, flux, luminosity, probability, selected observational distance, preferred observer, physical route or observer population, generic spacetime theorem, stability, matter/mass, physical scale, X_max, or canon. Write the detailed report to /return/EXTERNAL_REVIEW_RESPONSE.md and end it with exactly one allowed verdict token. In the final response state the token and report path.\n\n$(<"$review_request")"

review_args=(
  bwrap --die-with-parent --unshare-all --share-net
  --ro-bind /usr /usr
  --ro-bind /bin /bin
  --ro-bind /lib /lib
  --ro-bind /lib64 /lib64
  --ro-bind /etc /etc
  --ro-bind /run/systemd/resolve /run/systemd/resolve
  --proc /proc
  --dev /dev
  --tmpfs /tmp
  --dir /opt
  --ro-bind "$codex_executable" /opt/codex
  --bind "$review_home" /home/udt-admin
  --ro-bind "$authentication_file" /home/udt-admin/.codex/auth.json
  --ro-bind "$review_intake" /intake
  --bind "$review_work" /work
  --bind "$review_return" /return
  --setenv HOME /home/udt-admin
  --setenv CODEX_HOME /home/udt-admin/.codex
  --chdir /return
  /opt/codex -a never exec --ephemeral --ignore-user-config --skip-git-repo-check -m gpt-5.6-sol
  -c 'model_reasoning_effort="high"'
  -c 'web_search="disabled"'
  -s workspace-write --add-dir /work --color never
  -o /return/final_response.md
  "$review_prompt"
)
printf -v review_command '%q ' "${review_args[@]}"
exec script -q -e -f -c "$review_command" "$review_capture/external_review_transcript.txt"
