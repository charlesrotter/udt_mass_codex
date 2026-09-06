"""Capture actual frozen-candidate child streams and exits; writes no files."""
import datetime
import json
import subprocess
import time

root = "/home/udt-admin/udt_mass_codex"
package = "udt_g352_conserved_current_representation_candidate_2026-09-06"
cases = [
    (None, None),
    ("omit_area", "expanding_density_value"),
    ("coordinate_divergence", "expanding_current_conserved"),
    ("divergence_zero", "nonconserved_control_detected"),
    ("all_products", "phase_dependence_not_product"),
    ("omit_frequency", "cut_1_clock_rate"),
    ("omit_label_jacobian", "label_density_jacobian"),
]
records = []
for mutation, guard in cases:
    command = ["python3", f"{package}/check_exact.py"]
    if mutation is not None:
        command.extend(["--mutation", mutation])
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    clock = time.monotonic()
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=60)
    expected = (result.returncode == 0 and json.loads(result.stdout)["passed"] == 43
                if mutation is None else
                result.returncode == 1 and f"AssertionError: {guard}\n" in result.stderr)
    records.append({"command": command, "start_utc": start,
                    "elapsed_seconds": time.monotonic()-clock,
                    "returncode": result.returncode, "stdout": result.stdout,
                    "stderr": result.stderr, "expected_guard": guard,
                    "expected_outcome_observed": expected})
command = ["python3", f"{package}/recompute_saved_witness.py"]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
clock = time.monotonic()
result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=60)
expected = result.returncode == 0 and json.loads(result.stdout)["matches_saved"] is True
records.append({"command": command, "start_utc": start,
                "elapsed_seconds": time.monotonic()-clock, "returncode": result.returncode,
                "stdout": result.stdout, "stderr": result.stderr,
                "expected_outcome_observed": expected})
report = {"reviewer": "separate-context source-first then exposed direct review",
          "candidate_revision": "a4525d2176b0f6dbacf71830bab44f8c34e24627",
          "runs": records, "all_expected_outcomes": all(x["expected_outcome_observed"] for x in records)}
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["all_expected_outcomes"] else 1)
