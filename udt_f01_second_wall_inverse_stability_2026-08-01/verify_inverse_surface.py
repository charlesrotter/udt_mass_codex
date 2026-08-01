#!/usr/bin/env python3
"""Fail-closed verifier for the F01 inverse wall-stability surface."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from copy import deepcopy
from pathlib import Path

import mpmath as mp


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
BASE = "46c763770f3f71376a0e57338c276ed3981ce36b"
OUTCOME = "TWO_PARAMETER_CONDITIONAL_STABILITY_THRESHOLD_SURFACE_DERIVED"
ROOTS = (
    "udt_f01_lambda_schur_check_2026-08-01/",
    "udt_p4_stability_slice_2026-07-30/",
    "udt_p4_boundary_action_gate_2026-07-30/",
    "udt_stability_derivation_closure_sweep_2026-08-01/",
    "udt_stability_action_boundary_bridge_audit_2026-08-01/",
)
FILES = {"CURRENT_SCIENTIFIC_PREMISES.md", "CURRENT_SCIENTIFIC_PREMISES.tsv", "PONDER_MATH_ELEGANCE_2026-07-31.md"}
ALPHAS = ("1/4", "1/2", "3/4", "1/1")


def table(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def selected_paths() -> list[str]:
    raw = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "-z", BASE], cwd=ROOT, check=True, capture_output=True
    ).stdout
    paths = [token.decode("utf-8") for token in raw.split(b"\0") if token]
    return sorted(path for path in paths if path in FILES or any(path.startswith(root) for root in ROOTS))


def contains(value: str, interval: list[str]) -> bool:
    return mp.mpf(interval[0]) <= value <= mp.mpf(interval[1])


def validate(data: dict[str, object]) -> None:
    result = data["result"]
    certificate = data["certificate"]
    assert isinstance(result, dict) and isinstance(certificate, dict)
    if result.get("primary_outcome") != OUTCOME or certificate.get("status") != OUTCOME:
        raise AssertionError("outcome mutation")
    if result.get("tau_eta_selected") is not False:
        raise AssertionError("tau/eta promoted")
    if result.get("complete_wall_hessian_covered") is not False:
        raise AssertionError("slice promoted to full Hessian")
    if result.get("owned_domains_covered") != 4:
        raise AssertionError("owned-domain census")
    coordinates = certificate.get("coordinate_definitions")
    if not isinstance(coordinates, dict):
        raise AssertionError("coordinate definitions")
    if coordinates.get("tau_of_beta") != "s^2*beta/(1+beta*J)":
        raise AssertionError("finite-beta elimination lost")
    if coordinates.get("R06_endpoint_beta") != "+infinity only":
        raise AssertionError("R06 endpoint falsely assigned finite beta")
    branches = certificate.get("branches")
    if not isinstance(branches, dict) or set(branches) != {"DIRICHLET", "FREE"}:
        raise AssertionError("branch census")
    for label, branch in branches.items():
        if not isinstance(branch, dict):
            raise AssertionError(label)
        samples = branch.get("samples")
        if not isinstance(samples, list) or [row.get("alpha") for row in samples] != list(ALPHAS):
            raise AssertionError(f"sample census: {label}")
        tc = [mp.mpf(x) for x in branch["t_critical_interval"]]
        if not (0 < tc[0] <= tc[1] < 1):
            raise AssertionError(f"critical interval: {label}")
        if branch.get("region_below_crossing") != "field index one; no eta can repair":
            raise AssertionError(f"below-crossing promotion: {label}")
        if "no finite eta" not in str(branch.get("at_crossing")):
            raise AssertionError(f"singular crossing lost: {label}")
        if branch.get("eta_at_crossing") != "+infinity":
            raise AssertionError(f"finite eta assigned at crossing: {label}")
        if branch.get("m_direct_formula_overlap") is not True:
            raise AssertionError(f"m direct/formula check lost: {label}")
        n_interval = [mp.mpf(x) for x in branch["fine"]["n_green"]]
        if n_interval[0] <= 0 <= n_interval[1]:
            raise AssertionError(f"zero-mode coupling not certified: {label}")
        for row in samples:
            eta = [mp.mpf(x) for x in row["eta_critical_interval"]]
            eta_mu = [mp.mpf(x) for x in row["representative_eta_mu_critical_interval"]]
            if eta[0] <= 0 or eta_mu != [eta[0] / 4, eta[1] / 4]:
                raise AssertionError(f"eta sign/factor: {label} {row['alpha']}")
            if row.get("joint_condition") != "eta>=eta_critical; equality is semidefinite":
                raise AssertionError(f"joint condition: {label}")
    if "no wall response" not in str(certificate.get("conclusion_ceiling")):
        raise AssertionError("conclusion ceiling promoted")


def validate_threshold_table(certificate: dict[str, object]) -> None:
    actual = table("THRESHOLD_SURFACE.tsv")
    expected = []
    for label in ("DIRICHLET", "FREE"):
        branch = certificate["branches"][label]  # type: ignore[index]
        expected.append({
            "p_domain": label,
            "point_type": "FIELD_CROSSING",
            "alpha": "-",
            "t_lo": branch["t_critical_interval"][0],
            "t_hi": branch["t_critical_interval"][1],
            "tau_lo": branch["tau_critical_interval"][0],
            "tau_hi": branch["tau_critical_interval"][1],
            "eta_nu_lo": "+INF",
            "eta_nu_hi": "+INF",
            "representative_eta_mu_lo": "+INF",
            "representative_eta_mu_hi": "+INF",
            "joint_reading": "NO_FINITE_ETA__ZERO_MODE_COUPLES_TO_NU",
        })
        for sample in branch["samples"]:
            expected.append({
                "p_domain": label,
                "point_type": "ABOVE_CROSSING_SAMPLE",
                "alpha": sample["alpha"],
                "t_lo": sample["t_interval"][0],
                "t_hi": sample["t_interval"][1],
                "tau_lo": "-",
                "tau_hi": "-",
                "eta_nu_lo": sample["eta_critical_interval"][0],
                "eta_nu_hi": sample["eta_critical_interval"][1],
                "representative_eta_mu_lo": sample["representative_eta_mu_critical_interval"][0],
                "representative_eta_mu_hi": sample["representative_eta_mu_critical_interval"][1],
                "joint_reading": "NONNEGATIVE_IFF_ETA_AT_OR_ABOVE_THRESHOLD",
            })
    if actual != expected:
        raise AssertionError("threshold table does not exactly reproduce certificate")


def midpoint_recompute(certificate: dict[str, object]) -> dict[str, object]:
    mp.mp.dps = 80
    s = mp.findroot(
        lambda sv: mp.quad(lambda x: mp.log((sv**2 / 2) * x**2 + (sv**2 - sv) * x + 1 + sv**2 / 2 - sv), [-1, 1]),
        (mp.mpf("1.68102"), mp.mpf("1.68103")),
    )
    values = {}
    for label in ("DIRICHLET", "FREE"):
        def fields(x):
            w = (s**2 / 2) * x**2 + (s**2 - s) * x + 1 + s**2 / 2 - s
            wp = s**2 * x + s**2 - s
            lw = mp.log(w)
            v1 = wp / w
            v1p = s**2 / w - wp**2 / w**2
            v2 = 1 - 1 / w
            v2p = wp / w**2
            if label == "DIRICHLET":
                wr = 1 - 2 * s + 2 * s**2
                bu = -(wr * (1 - mp.log(wr)) + 2 * s - 1) / (wr - 1)
            else:
                bu = -1 / (2 * s - 1)
            u = 1 - lw + v1 / s + bu * v2
            up = -wp / w + v1p / s + bu * v2p
            ellu = s**2 * u * (1 + lw * (1 - 1 / w)) + lw * wp * up
            diag = s**2 * lw**2 * (1 - 1 / w)
            return w, u, ellu + diag

        j = mp.quad(lambda x: 1 / fields(x)[0], [-1, 1])
        n = mp.quad(lambda x: -fields(x)[1] / fields(x)[0], [-1, 1])
        s0 = mp.quad(lambda x: fields(x)[2], [-1, 1])
        wr = 1 - 2 * s + 2 * s**2
        d = 2 / (s - 1) if label == "DIRICHLET" else 2 * (4 * s**2 - 3 * s + 1) / ((2 * s - 1) * wr)
        tcrit = j / (j + d)
        tauinf = s**2 / j
        branch = certificate["branches"][label]  # type: ignore[index]
        if not contains(j, branch["fine"]["J"]) or not contains(n, branch["fine"]["n_green"]) or not contains(s0, branch["fine"]["S0"]):
            raise AssertionError(f"midpoint primary integral exclusion: {label}")
        if not contains(tcrit, branch["t_critical_interval"]) or not contains(tauinf * tcrit, branch["tau_critical_interval"]):
            raise AssertionError(f"midpoint crossing exclusion: {label}")
        samples = {}
        for row in branch["samples"]:
            num, den = row["alpha"].split("/")
            alpha = mp.mpf(num) / mp.mpf(den)
            schur = s0 - s**2 * n**2 * (j + alpha * d) / (alpha * d * (j + d))
            eta = -schur
            if not contains(eta, row["eta_critical_interval"]):
                raise AssertionError(f"midpoint eta exclusion: {label} {row['alpha']}")
            samples[row["alpha"]] = mp.nstr(eta, 50)
        values[label] = {
            "s": mp.nstr(s, 50), "J": mp.nstr(j, 50), "n": mp.nstr(n, 50),
            "S0": mp.nstr(s0, 50), "tcrit": mp.nstr(tcrit, 50), "eta_samples": samples,
        }
    return values


def mutation_catches(base: dict[str, object]) -> list[list[str]]:
    rows = []

    def expect(name: str, mutation) -> None:
        trial = deepcopy(base)
        mutation(trial)
        caught = False
        try:
            validate(trial)
        except (AssertionError, KeyError, IndexError, TypeError):
            caught = True
        rows.append([name, "PASS" if caught else "FAIL"])

    expect("select_tau", lambda d: d["result"].update(tau_eta_selected=True))
    expect("promote_full_hessian", lambda d: d["result"].update(complete_wall_hessian_covered=True))
    expect("drop_branch", lambda d: d["certificate"]["branches"].pop("FREE"))
    expect("drop_sample", lambda d: d["certificate"]["branches"]["DIRICHLET"]["samples"].pop())
    expect("negative_eta_threshold", lambda d: d["certificate"]["branches"]["DIRICHLET"]["samples"][0].update(eta_critical_interval=["-2", "-1"]))
    expect("lose_factor_four", lambda d: d["certificate"]["branches"]["DIRICHLET"]["samples"][0].update(representative_eta_mu_critical_interval=["1", "2"]))
    expect("finite_eta_at_crossing", lambda d: d["certificate"]["branches"]["FREE"].update(at_crossing="eta=1 repairs"))
    expect("eta_repairs_below_crossing", lambda d: d["certificate"]["branches"]["FREE"].update(region_below_crossing="eta repairs"))
    expect("promote_outcome", lambda d: d["result"].update(primary_outcome="NATIVE_STABILITY_DERIVED"))
    expect("select_wall_in_ceiling", lambda d: d["certificate"].update(conclusion_ceiling="wall response selected"))
    expect("finite_beta_at_R06_endpoint", lambda d: d["certificate"]["coordinate_definitions"].update(R06_endpoint_beta="beta=1"))
    expect("finite_eta_at_formula_crossing", lambda d: d["certificate"]["branches"]["DIRICHLET"].update(eta_at_crossing="1"))
    expect("zero_zero_mode_coupling", lambda d: d["certificate"]["branches"]["FREE"]["fine"].update(n_green=["0", "0"]))
    expect("crossing_outside_slice", lambda d: d["certificate"]["branches"]["FREE"].update(t_critical_interval=["1.1", "1.2"]))
    return rows


def main() -> None:
    inventory = table("SOURCE_INVENTORY.tsv")
    if [row["path"] for row in inventory] != selected_paths():
        raise AssertionError("source path coverage")
    for row in inventory:
        blob = subprocess.run(["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip()
        payload = subprocess.run(["git", "cat-file", "blob", blob], cwd=ROOT, check=True, capture_output=True).stdout
        if blob != row["git_blob"] or str(len(payload)) != row["bytes"] or sha(payload) != row["sha256"]:
            raise AssertionError(f"source identity: {row['path']}")
    manifest = (PKG / "SOURCE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    if manifest != [f"{row['sha256']}  {row['path']}" for row in inventory]:
        raise AssertionError("source manifest")

    certificate = json.loads((PKG / "PRIMARY_CERTIFICATE.json").read_text(encoding="utf-8"))
    result = json.loads((PKG / "RESULT.json").read_text(encoding="utf-8"))
    data: dict[str, object] = {"certificate": certificate, "result": result}
    validate(data)
    validate_threshold_table(certificate)
    controls = table("EXACT_CONTROL_LEDGER.tsv")
    if len(controls) != 15 or any(row["status"] != "PASS" for row in controls):
        raise AssertionError("computed controls")
    midpoint = midpoint_recompute(certificate)
    catches = mutation_catches(data)
    if any(row[1] != "PASS" for row in catches):
        raise AssertionError("mutation catches")
    with (PKG / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["mutation", "caught"])
        writer.writerows(catches)
    verification = {
        "status": "PASS",
        "base_commit": BASE,
        "source_count": len(inventory),
        "computed_controls_passed": len(controls),
        "computed_controls_total": len(controls),
        "semantic_catches_passed": len(catches),
        "semantic_catches_total": len(catches),
        "midpoint_adaptive_recomputation": midpoint,
        "primary_outcome": OUTCOME,
        "tau_eta_selected": False,
        "complete_wall_hessian_covered": False,
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in verification.items() if key != "midpoint_adaptive_recomputation"}, sort_keys=True))


if __name__ == "__main__":
    main()
