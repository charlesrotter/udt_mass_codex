# LC1 immutable freeze scope

FREEZE_MANIFEST.sha256 authenticates the reviewed contract, input record,
initial wording, source checks and complete LC1 review directory at this seal.
It excludes itself. Paths are repository-root relative. Verify with sha256sum
--check --quiet on this manifest. Source bytes are separately pinned in INPUTS
and authenticated by source_contract_check; correspondence does not prove truth.

The mutable campaign log/current tracking and future LC2 artifacts are excluded
from this stage freeze. Their changes do not invalidate LC1. The final campaign
manifest will cover its complete return snapshot. The containing git commit
precedes the new numerical benchmark, but published outcome exposure is known;
this is not evidence of a blind empirical discovery.
