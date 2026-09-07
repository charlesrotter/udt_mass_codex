#!/bin/sh
# Authenticate the single pending-status edit; this is packaging, not science.
set -eu
tm2_brief=udt_tidal_measurement_feasibility_campaign_2026-09-07/DECISION_BRIEF.md
tm2_actual=$(sha256sum "$tm2_brief")
test "$tm2_actual" = "0c5f2ce7b90bdac677ef1ce2638074de6a98f1072b6460b46abd501589be2672  $tm2_brief"
tm2_recovered=$(sed 's/^TM1 and TM2: VERIFIED-WITH-CAVEATS; conditional candidates, not promoted\.$/DRAFT: TM1 reviewed with caveats; TM2 direct review pending. No promotion./' "$tm2_brief" | sha256sum)
test "$tm2_recovered" = 'dd3720d5d4b1d1dc3e9874b3db021df7234709b073c8fe3b02f49141024394ac  -'
tm2_body=$(sed '/^TM1 and TM2: VERIFIED-WITH-CAVEATS; conditional candidates, not promoted\.$/d' "$tm2_brief" | sha256sum)
test "$tm2_body" = 'a95ce848900af7d4a6e212386de2bedbc3cfacf28b51a54a0e7fc75f9be7da65  -'
printf '%s\n' "$tm2_actual" "$tm2_recovered" "$tm2_body"
