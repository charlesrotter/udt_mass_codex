#!/usr/bin/env bash
set -euo pipefail
review_repo=$1
review_dir=$2
review_pin=70034a6faa9264bf054eb473d5eb7a0889f3d2de
review_candidate=06d523db
cd "$review_repo"
printf 'SOURCE_SNAPSHOT %s\n' "$review_pin"
printf 'CURRENT_HEAD '
git rev-parse HEAD
printf 'CANDIDATE_COMMIT '
git rev-parse "${review_candidate}^{commit}"
while IFS=$'\t' read -r reviewed_path recorded_sha read_selection source_role; do
    if [[ "$reviewed_path" == path ]]; then continue; fi
    current_sha=$(sha256sum -- "$reviewed_path")
    current_sha=${current_sha%% *}
    [[ "$current_sha" == "$recorded_sha" ]]
    snapshot=$review_pin
    if [[ "$reviewed_path" == udt_shared_readout_metric_constraint_campaign_2026-09-06/WORK_ORDER.md ]]; then
        snapshot=$review_candidate
    fi
    snapshot_sha=$(git show "$snapshot:$reviewed_path" | sha256sum)
    snapshot_sha=${snapshot_sha%% *}
    [[ "$snapshot_sha" == "$recorded_sha" ]]
    printf 'REVIEW_SOURCE_MATCH %s %s %s\n' "$snapshot" "$recorded_sha" "$reviewed_path"
done < "$review_dir/SOURCE_READS.tsv"
review_manifest=udt_shared_readout_metric_constraint_campaign_2026-09-06/step_01/SOURCE_SHA256SUMS
sha256sum -c "$review_manifest"
while read -r expected_sha reviewed_path; do
    snapshot_sha=$(git show "$review_pin:$reviewed_path" | sha256sum)
    snapshot_sha=${snapshot_sha%% *}
    [[ "$snapshot_sha" == "$expected_sha" ]]
    printf 'CANDIDATE_SOURCE_SNAPSHOT_MATCH %s\n' "$reviewed_path"
done < "$review_manifest"
sha256sum -c udt_shared_readout_metric_constraint_campaign_2026-09-06/step_01/CANDIDATE_SHA256SUMS
git diff --exit-code "$review_candidate" -- udt_shared_readout_metric_constraint_campaign_2026-09-06/step_01/CANDIDATE_ARGUMENT.md udt_shared_readout_metric_constraint_campaign_2026-09-06/step_01/QUESTION.md udt_shared_readout_metric_constraint_campaign_2026-09-06/step_01/SOURCE_SHA256SUMS udt_shared_readout_metric_constraint_campaign_2026-09-06/step_01/CANDIDATE_SHA256SUMS
cd "$review_dir"
sha256sum -c STAGE_A_SHA256SUMS
printf 'ALL_SOURCE_AND_FREEZE_CORRESPONDENCE_CHECKS_PASS\n'
