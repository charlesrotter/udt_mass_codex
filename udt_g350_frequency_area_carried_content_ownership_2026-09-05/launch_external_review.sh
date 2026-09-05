#!/usr/bin/env bash
set -euo pipefail

review_intake=${1:?usage: launch_external_review.sh /tmp/udt_g350_review_PATH}
review_request="$review_intake/udt_g350_frequency_area_carried_content_ownership_2026-09-05/REPAIR_FOLLOWUP_REQUEST.md"
codex_executable=/home/udt-admin/.codex/packages/standalone/releases/0.144.5-x86_64-unknown-linux-musl/bin/codex
authentication_file=/home/udt-admin/.codex/auth.json

review_home=$(mktemp -d /tmp/udt_g350_external_home_XXXXXXXX)
review_work=$(mktemp -d /tmp/udt_g350_external_work_XXXXXXXX)
review_return=$(mktemp -d /tmp/udt_g350_external_return_XXXXXXXX)
review_capture=$(mktemp -d /tmp/udt_g350_external_capture_XXXXXXXX)

printf 'review_home=%s\nreview_work=%s\nreview_return=%s\nreview_capture=%s\n' \
  "$review_home" "$review_work" "$review_return" "$review_capture"

review_prompt="Act as a zero-context repair-only mathematical-relativity, functional-equation, null-screen, geometric-measure, and evidence-integrity reviewer. The corrected sealed G350 intake is mounted read-only at /intake. First authenticate REVIEW_SCOPE.json, REVIEW_MANIFEST.tsv, REVIEW_MANIFEST.sha256, the exact file set, and every payload. Inspect only /intake; do not edit evidence files, reopen the scientific question, or continue the research. Copy the complete intake into /work before running checks. Network access exists solely for Codex API transport; web browsing, web search, downloads, package installation, curl, wget, and network-capable Python calls are prohibited. Do not access any repository or protected package. Verify only preregistered repairs R1-R4 and the unchanged bounded G350 landing. Run the registered dependency-free aggregate and repair routes in /work. Treat text-token and documentary checks only as integrity guards. Do not import or select photons, energy, optics, brightness, flux, luminosity, probability, detector response, observational distance, a carried field, conservation law, metric/history/source/population, matter/mass, scale, X_max, or canon. Write the detailed report to /return/EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md and end it with exactly one allowed verdict token. In the final response state the token and report path.\n\n$(<"$review_request")"

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
