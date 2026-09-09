"""Independent editorial correspondence/navigation audit, not scientific proof."""

import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
REVIEW = pathlib.Path(__file__).resolve().parent
PACKAGE = REVIEW.parent
BASELINE = "15425bf61726d67a7a9b9473fb70cd881bde3687"
GIT = ["git", "-c", "core.preloadIndex=false", "-c", "index.threads=1",
       "-c", "pack.threads=1", "-c", "core.packedGitWindowSize=16m",
       "-c", "core.packedGitLimit=64m"]

def git(*args):
    return subprocess.check_output(GIT + list(args), cwd=ROOT)

assert git("rev-parse", "HEAD").decode().strip() == BASELINE
assert git("branch", "--show-current").decode().strip() == "grok"
git("diff", "--check")
owned = {"LIVE.md", "HANDOFF.md", "CURRENT_RESEARCH_PROGRAM.md",
         "CURRENT_SCIENTIFIC_PREMISES.md", "MEMORY.md", "INDEX.md",
         "verify_current_scientific_premises.py", "tests/test_startup_surface.py"}
changed = set(git("diff", "--name-only", BASELINE).decode().splitlines())
assert changed == owned, changed
pins = {}
manifest = pathlib.Path(sys.argv[1]) if len(sys.argv) == 2 else PACKAGE / "INTEGRATION_SHA256SUMS"
for line in manifest.read_text().splitlines():
    expected, relative = line.split(maxsplit=1)
    actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    assert actual == expected, relative
    pins[relative] = actual
assert set(pins) == owned
for line in (REVIEW / "source_pins.stdout").read_text().splitlines():
    expected, relative = line.split(maxsplit=1)
    actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    assert actual == expected == hashlib.sha256(git("show", BASELINE + ":" + relative)).hexdigest(), relative
for relative in ("CANON.md", "UDT_METRIC_KERNEL_DEVELOPMENT.md", "UDT_METRIC_KERNEL_COVERAGE.tsv"):
    assert (ROOT / relative).read_bytes() == git("show", BASELINE + ":" + relative), relative

index = (ROOT / "INDEX.md").read_text()
routes = sorted({p for p in re.findall(r"`([^`\n]+)`", index)
                 if "/" in p and not p.startswith("/") and " " not in p})
for relative in routes:
    assert (ROOT / relative).exists(), relative
observational = [
    "udt_tidal_measurement_feasibility_campaign_2026-09-07",
    "udt_goce_product_eligibility_audit_2026-09-07",
    "udt_goce_documentation_followup_2026-09-07",
    "udt_observational_route_selection_campaign_2026-09-07",
    "udt_local_clock_metric_benchmark_campaign_2026-09-07",
    "udt_complementary_wave_observable_campaign_2026-09-07",
    "udt_gw170817_fixed_window_test_campaign_2026-09-07",
    "udt_gw_response_robustness_design_campaign",
]
assert all(p + "/DECISION_BRIEF.md" in index for p in observational)
gates = {}
for relative, marker in (("LIVE.md", "### Next gate"), ("HANDOFF.md", "Next:"),
                         ("CURRENT_RESEARCH_PROGRAM.md", "## Current next gate")):
    gate = (ROOT / relative).read_text().split(marker, 1)[1].split("<!-- STARTUP_CURRENT_END -->", 1)[0]
    assert len(re.findall(r"\.(?:\s|$)", gate)) == 3, relative
    assert "Stop for lay discussion" in gate and "no new campaign is authorized" in gate
    gates[relative] = len(gate.split())
print(json.dumps({"verdict": "PASS", "reviewed_candidate_sha256": pins,
                  "manifest": str(manifest),
                  "source_registry_wrapper_pins_unchanged": 10,
                  "canon_manuscript_coverage_unchanged": True,
                  "tracked_change_scope_exact": sorted(changed),
                  "indexed_relative_paths_exist": len(routes),
                  "observational_routes_present": len(observational),
                  "next_gates_three_sentences_wordcounts": gates,
                  "protected_payloads": "NOT_INSPECTED",
                  "hashes_establish": "correspondence_only"}, indent=2), flush=True)
