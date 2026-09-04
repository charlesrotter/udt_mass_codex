#!/usr/bin/env bash
set -euo pipefail

review_intake=/tmp/udt_g343_review__9x3loqe
review_request="$review_intake/g343/ADVERSARIAL_REVIEW_REQUEST.md"
codex_executable=/home/udt-admin/.codex/packages/standalone/releases/0.144.5-x86_64-unknown-linux-musl/bin/codex
authentication_file=/home/udt-admin/.codex/auth.json

review_home=$(mktemp -d /tmp/udt_g343_external_home_XXXXXXXX)
review_work=$(mktemp -d /tmp/udt_g343_external_work_XXXXXXXX)
review_return=$(mktemp -d /tmp/udt_g343_external_return_XXXXXXXX)
review_capture=$(mktemp -d /tmp/udt_g343_external_capture_XXXXXXXX)

printf 'review_home=%s\nreview_work=%s\nreview_return=%s\nreview_capture=%s\n' \
  "$review_home" "$review_work" "$review_return" "$review_capture"

review_prompt="Act as a fresh zero-context adversarial mathematical-relativity, causal-geometry, null-congruence, Hamiltonian-screen, and observer-pair reviewer. The sealed G343 intake is mounted read-only at /intake. First authenticate REVIEW_SCOPE.json, REVIEW_MANIFEST.tsv, REVIEW_MANIFEST.sha256, the exact file set, and every payload. Inspect only /intake; do not edit evidence files or continue the research. Copy the complete intake into /work before running checks so its sealed sources layout remains available. Network access exists solely for Codex API transport; web browsing, web search, downloads, package installation, curl, wget, and network-capable Python calls are prohibited. Do not access any repository or protected package. Independently rederive and attack the bounded G343 result directly from the supplied exact metric: the dimensionally typed reference-event projective chart; fixed-affine ray and direct Levi-Civita/Riemann screen tide; both scalar solutions and reduction-of-order measures; every bilocal A/B/C/D block; exact groupoid composition, unit Wronskians, full symplectic structure, and common-affine endpoint inverse; reference-event covariance and the discarded hidden-Tstar execution; separately unit-frequency endpoint conjugation and the metric-frequency factor in the reverse B block; exact recovery of G342; both principal-direction phase-space limits; and compact per-lift path-label typing. Distinguish geometric screen phase-space transport from electromagnetic/light transfer, brightness, luminosity, observational distance, physical route/population, topology or occupancy selection, stability, matter/mass, scale, X_max, or canon. Inspect the complete failure chronology and confirm whether either repair changed the scientific alternatives or only corrected dimensional and comparison bookkeeping. Run the registered dependency-free aggregate replay in the writable /work copy and perform an independent scratch rederivation where useful. Write the detailed report to /return/EXTERNAL_REVIEW_RESPONSE.md and end it with exactly one allowed verdict token. In the final response state the token and report path.\n\n$(<"$review_request")"

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
  /opt/codex -a never exec --ephemeral --ignore-user-config --skip-git-repo-check -m gpt-5.4
  -c 'model_reasoning_effort="high"'
  -c 'web_search="disabled"'
  -s workspace-write --add-dir /work --color never
  -o /return/final_response.md
  "$review_prompt"
)
printf -v review_command '%q ' "${review_args[@]}"
exec script -q -e -f -c "$review_command" "$review_capture/external_review_transcript.txt"
