#!/usr/bin/env bash
set -euo pipefail

review_intake=/tmp/udt_g341_review_2q8fq7g3
review_request="$review_intake/g341/ADVERSARIAL_REVIEW_REQUEST.md"
codex_executable=/home/udt-admin/.codex/packages/standalone/releases/0.144.5-x86_64-unknown-linux-musl/bin/codex
authentication_file=/home/udt-admin/.codex/auth.json

review_home=$(mktemp -d /tmp/udt_g341_external_home_XXXXXXXX)
review_work=$(mktemp -d /tmp/udt_g341_external_work_XXXXXXXX)
review_return=$(mktemp -d /tmp/udt_g341_external_return_XXXXXXXX)
review_capture=$(mktemp -d /tmp/udt_g341_external_capture_XXXXXXXX)

printf 'review_home=%s\nreview_work=%s\nreview_return=%s\nreview_capture=%s\n' \
  "$review_home" "$review_work" "$review_return" "$review_capture"

review_prompt="Act as a fresh zero-context adversarial mathematical-relativity, causal-geometry, null-congruence, and observer-pair reviewer. The sealed G341 intake is mounted read-only at /intake. First authenticate REVIEW_SCOPE.json, REVIEW_MANIFEST.tsv, REVIEW_MANIFEST.sha256, the exact file set, and every payload. Inspect only /intake; do not edit evidence files or continue the research. Copy the complete intake into /work before running checks so its sealed sources/ layout remains available. Network access exists solely for Codex API transport; web browsing, web search, downloads, package installation, curl, wget, and network-capable Python calls are prohibited. Do not access any repository or protected package. Independently rederive and attack the bounded G341 result directly from the supplied exact Taub--Kasner metric: mixed null endpoint integrals and signs; positive endpoint determinant; global per-lift inverse including both principal charts; exact scope of the no-interior-conjugate-caustic claim; compact quotient winding and cut/tie typing; endpoint frequency and unique mixed zero-shift direction; direct Levi-Civita screen transport; distinction between trivial null-screen-quotient rotation and nonzero G269 full pair-plane mismatch; G298 pair-plane regularity; reversal; and all light-model, physical-route, population, scale, X_max, and completeness boundaries. Distinguish analytic proof from numerical regression, quotient branch multiplicity from per-lift nonuniqueness, and implementation independence from premise independence. Run the registered dependency-free aggregate replay in the writable /work copy. Write the detailed report to /return/EXTERNAL_REVIEW_RESPONSE.md and end it with exactly one allowed verdict token. In the final response state the token and report path.\n\n$(<"$review_request")"

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
