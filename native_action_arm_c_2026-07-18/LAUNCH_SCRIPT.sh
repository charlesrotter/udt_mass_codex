#!/usr/bin/env bash
set -euo pipefail

prompt=$(</tmp/udt_armc_prompt.txt)

args=(
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
  --ro-bind /home/udt-admin/.codex/packages/standalone/releases/0.144.5-x86_64-unknown-linux-musl/bin/codex /opt/codex
  --ro-bind /home/udt-admin/.local/lib/python3.10/site-packages /opt/python-site
  --bind /tmp/udt_armc_home_retry.Z1LEGL /home/udt-admin
  --dir /controller
  --ro-bind /home/udt-admin/udt_mass_codex/UDT_NATIVE_ACTION_DERIVATION_DISPATCH.md /controller/UDT_NATIVE_ACTION_DERIVATION_DISPATCH.md
  --dir /cold
  --ro-bind /home/udt-admin/udt_mass_codex/UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md /cold/UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md
  --ro-bind /home/udt-admin/udt_mass_codex/UDT_NATIVE_ACTION_COLD_PACKET.md /cold/UDT_NATIVE_ACTION_COLD_PACKET.md
  --dir /stage1
  --ro-bind /home/udt-admin/udt_mass_codex/native_action_stage1_2026-07-18/arm_A /stage1/arm_A
  --ro-bind /home/udt-admin/udt_mass_codex/native_action_stage1_2026-07-18/arm_B /stage1/arm_B
  --dir /stage2
  --ro-bind /home/udt-admin/udt_mass_codex/native_action_stage2_2026-07-18/arm_A /stage2/arm_A
  --ro-bind /home/udt-admin/udt_mass_codex/native_action_stage2_2026-07-18/arm_B /stage2/arm_B
  --dir /packet
  --dir /packet/w_alg_verifier_scripts
  --dir /packet/archive
  --ro-bind /home/udt-admin/udt_mass_codex/CANON.md /packet/CANON.md
  --ro-bind /home/udt-admin/udt_mass_codex/udt_field_equations_derivation_results.md /packet/udt_field_equations_derivation_results.md
  --ro-bind /home/udt-admin/udt_mass_codex/native_geometric_action_results.md /packet/native_geometric_action_results.md
  --ro-bind /home/udt-admin/udt_mass_codex/simple_metric_S9_native_action_honesty_results.md /packet/simple_metric_S9_native_action_honesty_results.md
  --ro-bind /home/udt-admin/udt_mass_codex/matter_carrier_provenance_audit_results.md /packet/matter_carrier_provenance_audit_results.md
  --ro-bind /home/udt-admin/udt_mass_codex/noNull_energy.py /packet/noNull_energy.py
  --ro-bind /home/udt-admin/udt_mass_codex/w_alg_verifier_scripts/UDT_H3_STATIC_MASS_BACKREACTION_DISPATCH.md /packet/w_alg_verifier_scripts/UDT_H3_STATIC_MASS_BACKREACTION_DISPATCH.md
  --ro-bind /home/udt-admin/udt_mass_codex/pre_native_era_census.md /packet/pre_native_era_census.md
  --ro-bind /home/udt-admin/udt_mass_codex/macro_spine_provenance_2026-07-06.md /packet/macro_spine_provenance_2026-07-06.md
  --ro-bind /home/udt-admin/udt_mass_codex/archive/native_action_chat_2026-07-14_15 /packet/archive/native_action_chat_2026-07-14_15
  --dir /manifests
  --ro-bind /home/udt-admin/udt_mass_codex/UDT_NATIVE_ACTION_STAGE2_A1_A6_SHA256SUMS_2026-07-18.txt /manifests/UDT_NATIVE_ACTION_STAGE2_A1_A6_SHA256SUMS_2026-07-18.txt
  --ro-bind /home/udt-admin/udt_mass_codex/UDT_NATIVE_ACTION_ARM_C_INPUT_SHA256SUMS_2026-07-18.txt /manifests/UDT_NATIVE_ACTION_ARM_C_INPUT_SHA256SUMS_2026-07-18.txt
  --bind /tmp/udt_armc_return_retry.9G8Rsi /return
  --setenv HOME /home/udt-admin
  --setenv CODEX_HOME /home/udt-admin/.codex
  --setenv PYTHONPATH /opt/python-site
  --setenv PYTHONDONTWRITEBYTECODE 1
  --chdir /return
  /opt/codex exec --ephemeral --ignore-user-config -m gpt-5.6-sol
  -c 'model_reasoning_effort="high"' -c 'web_search="disabled"'
  --dangerously-bypass-approvals-and-sandbox --color never -o /return/final_response.md
  "$prompt"
)

printf -v command '%q ' "${args[@]}"
exec script -q -e -f -c "$command" /tmp/udt_armc_capture_retry.x3m5U1/OUTER_TRANSCRIPT.txt
