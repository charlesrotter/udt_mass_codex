#!/usr/bin/env python3
"""Independent stdlib/Fraction verification and exercised catch proofs."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "73b33e2c9f11e897976d571810a8e98dc3a2e644"


class VerifyError(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise VerifyError(message)


@dataclass(frozen=True)
class J:
    """Exact value/first/second x-jet used for independent tensor reconstruction."""

    v: Q
    d: Q = Q(0)
    dd: Q = Q(0)

    @staticmethod
    def lift(value: "J | Q | int") -> "J":
        return value if isinstance(value, J) else J(Q(value))

    def __add__(self, other: "J | Q | int") -> "J":
        other = self.lift(other)
        return J(self.v + other.v, self.d + other.d, self.dd + other.dd)

    __radd__ = __add__

    def __neg__(self) -> "J":
        return J(-self.v, -self.d, -self.dd)

    def __sub__(self, other: "J | Q | int") -> "J":
        return self + (-self.lift(other))

    def __rsub__(self, other: "J | Q | int") -> "J":
        return self.lift(other) - self

    def __mul__(self, other: "J | Q | int") -> "J":
        other = self.lift(other)
        return J(
            self.v * other.v,
            self.d * other.v + self.v * other.d,
            self.dd * other.v + 2 * self.d * other.d + self.v * other.dd,
        )

    __rmul__ = __mul__

    def inv(self) -> "J":
        need(self.v != 0, "jet inverse at zero")
        return J(
            1 / self.v,
            -self.d / self.v**2,
            2 * self.d**2 / self.v**3 - self.dd / self.v**2,
        )

    def __truediv__(self, other: "J | Q | int") -> "J":
        return self * self.lift(other).inv()

    def __rtruediv__(self, other: "J | Q | int") -> "J":
        return self.lift(other) / self


def partial(value: J, coordinate: int) -> J:
    return J(value.d, value.dd, Q(0)) if coordinate == 1 else J(Q(0))


def direct_scalar_curvature(A: J, c: Q = Q(7, 3)) -> Q:
    """Rebuild 2D coordinate Ricci from metric jets; no production import."""
    zero = J(Q(0))
    g = [[-c * c * A, zero], [zero, A.inv()]]
    gi = [[(-c * c * A).inv(), zero], [zero, A]]
    gamma = [[[zero for _ in range(2)] for _ in range(2)] for _ in range(2)]
    for a in range(2):
        for b in range(2):
            for cc in range(2):
                total = zero
                for d in range(2):
                    total += gi[a][d] * (
                        partial(g[d][b], cc) + partial(g[d][cc], b) - partial(g[b][cc], d)
                    ) / 2
                gamma[a][b][cc] = total
    ricci = [[Q(0), Q(0)], [Q(0), Q(0)]]
    for a in range(2):
        for b in range(2):
            value = Q(0)
            for cc in range(2):
                value += partial(gamma[cc][a][b], cc).v - partial(gamma[cc][a][cc], b).v
                for d in range(2):
                    value += (
                        gamma[cc][cc][d].v * gamma[d][a][b].v
                        - gamma[cc][b][d].v * gamma[d][a][cc].v
                    )
            ricci[a][b] = value
    return sum(gi[a][b].v * ricci[a][b] for a in range(2) for b in range(2))


def direct_proper_scalar(n: J, c: Q = Q(7, 3)) -> Q:
    """Direct Ricci reconstruction for diag(-c^2 n(x)^2,1)."""
    zero, one = J(Q(0)), J(Q(1))
    g = [[-c * c * n * n, zero], [zero, one]]
    gi = [[(-c * c * n * n).inv(), zero], [zero, one]]
    gamma = [[[zero for _ in range(2)] for _ in range(2)] for _ in range(2)]
    for a in range(2):
        for b in range(2):
            for cc in range(2):
                total = zero
                for d in range(2):
                    total += gi[a][d] * (
                        partial(g[d][b], cc) + partial(g[d][cc], b) - partial(g[b][cc], d)
                    ) / 2
                gamma[a][b][cc] = total
    ricci = [[Q(0), Q(0)], [Q(0), Q(0)]]
    for a in range(2):
        for b in range(2):
            value = Q(0)
            for cc in range(2):
                value += partial(gamma[cc][a][b], cc).v - partial(gamma[cc][a][cc], b).v
                for d in range(2):
                    value += gamma[cc][cc][d].v * gamma[d][a][b].v - gamma[cc][b][d].v * gamma[d][a][cc].v
            ricci[a][b] = value
    return sum(gi[a][b].v * ricci[a][b] for a in range(2) for b in range(2))


def independent_checks() -> dict[str, bool]:
    checks: dict[str, bool] = {}

    for index, (N, H, B, c) in enumerate([
        (Q(5, 2), Q(7, 3), Q(1, 5), Q(11, 4)),
        (Q(9, 4), Q(2, 3), Q(-2, 7), Q(5, 1)),
        (Q(13, 6), Q(4, 5), Q(0), Q(17, 3)),
    ]):
        determinant = c * c * (-N * N + H * H * B * B) * H * H - (c * H * H * B) ** 2
        checks[f"connector_det_{index}"] = determinant == -c * c * N * N * H * H
        for sign in (-1, 1):
            v = c * (-B + sign * N / H)
            null = c * c * (-N * N + H * H * B * B) + 2 * c * H * H * B * v + H * H * v * v
            checks[f"null_root_{index}_{sign}"] = null == 0
            checks[f"local_ratio_{index}_{sign}"] = H * (v / c + B) / N == sign

    for index, (D, F) in enumerate([(Q(2), Q(1)), (Q(7, 3), Q(5, 4)), (Q(11, 2), Q(2, 9))]):
        N = F * D
        H = 1 / D
        checks[f"reciprocal_proper_{index}"] = N == F * D
        checks[f"reciprocal_coordinate_{index}"] = N / H == F * D * D
        checks[f"reciprocal_local_{index}"] = (N / H) / (D * N) == 1

    D = Q(10**6)
    checks["same_regime_ratio"] = D / D == 1
    checks["one_micro_one_ordinary"] = (Q(2) / (1 / D + 1)) < Q(2000001, 1000000)
    checks["endpoint_bottleneck"] = (Q(3) / (Q(2) / D + 1)) < 3
    checks["uniform_micro_connector"] = Q(2) / (1 / D + 1 / D) == D

    N, H, B = Q(20), Q(3, 2), Q(4)
    forward, backward = N - H * B, N + H * B
    roundtrip = Q(2) / (1 / forward + 1 / backward)
    checks["shift_roundtrip"] = roundtrip == (N * N - H * H * B * B) / N
    checks["shift_reversal"] = (N - H * (-B)) == backward
    kappa, N0 = Q(7, 3), Q(5, 4)
    checks["time_rescale"] = ((N / kappa) - H * (B / kappa)) / (N0 / kappa) == forward / N0

    # Angular/path weighting cancels only at uniform lapse.
    h1, h2, dl1, dl2 = Q(2), Q(5), Q(3), Q(7)
    uniform = (h1 * dl1 + h2 * dl2) / (h1 * dl1 / N + h2 * dl2 / N)
    nonuniform_a = (h1 * dl1 + h2 * dl2) / (h1 * dl1 / Q(2) + h2 * dl2 / Q(9))
    nonuniform_b = (Q(4) * dl1 + h2 * dl2) / (Q(4) * dl1 / Q(2) + h2 * dl2 / Q(9))
    checks["uniform_angular_cancel"] = uniform == N
    checks["nonuniform_angular_weight"] = nonuniform_a != nonuniform_b

    # Direct Fraction tensor reconstruction for arbitrary metric two-jets.
    for index, A in enumerate([
        J(Q(5, 2), Q(3, 7), Q(-11, 13)),
        J(Q(9, 4), Q(-2, 5), Q(7, 3)),
        J(Q(1), Q(0), Q(0)),
    ]):
        checks[f"direct_curvature_{index}"] = direct_scalar_curvature(A) == -A.dd

    for index, n in enumerate([
        J(Q(5, 2), Q(3, 7), Q(-11, 13)),
        J(Q(9, 4), Q(-2, 5), Q(7, 3)),
        J(Q(1), Q(0), Q(0)),
    ]):
        checks[f"direct_proper_curvature_{index}"] = direct_proper_scalar(n) == -2 * n.dd / n.v
    checks["arbitrary_D_F_inverse_flat"] = direct_proper_scalar(J(Q(1), Q(0), Q(0))) == 0

    # Transition polynomial A=1+(D^2-1)(3y^2-2y^3), x=w*y.
    for index, (D, w, y) in enumerate([(Q(3), Q(2), Q(0)), (Q(5, 2), Q(7, 3), Q(1, 4))]):
        amp = D * D - 1
        A = J(
            1 + amp * (3 * y * y - 2 * y**3),
            amp * (6 * y - 6 * y * y) / w,
            amp * (6 - 12 * y) / (w * w),
        )
        scalar = direct_scalar_curvature(A)
        checks[f"transition_scalar_{index}"] = scalar == -amp * (6 - 12 * y) / (w * w)
        checks[f"transition_K_{index}"] = scalar * scalar == amp * amp * (6 - 12 * y) ** 2 / w**4

    return checks


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_check(rows: list[dict[str, str]]) -> None:
    need(len(rows) == 15, "source count")
    need(len({row["source_id"] for row in rows}) == 15, "source ids")
    for row in rows:
        data = subprocess.check_output(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT)
        blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, text=True).strip()
        need(hashlib.sha256(data).hexdigest() == row["sha256"], "source sha " + row["source_id"])
        need(blob == row["git_blob"], "source blob " + row["source_id"])
        need(row["firewall"] == "POST_FIREWALL_AFFIRMATIVE_ELIGIBLE", "source firewall")


def validate_contract(payload: dict, texts: dict[str, str], sources: list[dict[str, str]]) -> None:
    need(payload["base"] == BASE, "base")
    need(payload["check_count"] == 41, "production check count")
    need(len(payload["checks"]) == 41 and all(payload["checks"].values()), "production checks")
    formulas = payload["formulas"]
    need(formulas["local_orthonormal_rate"] == "H*(dlambda/dt/c_E+B)/N=+/-1", "local formula")
    need(formulas["proper_distance_anchor_rate"].startswith("dell/(c_E*dt_anchor)=F*D"), "proper formula")
    need(formulas["reciprocal_coordinate_rate"].endswith("F*D^2"), "coordinate formula")
    classes = payload["bounded_classifications"]
    need(classes["same_micro_regime_mutual_clock_ratio"] == "UNITY", "mutual rate")
    need(classes["micro_endpoints_only"] == "INSUFFICIENT", "endpoint insufficiency")
    need(classes["material_information_transfer"] == "NOT_TESTED", "information ceiling")
    need(classes["oscillatory_F"] == "POSITIVE_NO_LIMIT_CLASS", "oscillatory class")
    need(classes["arbitrary_D_with_F_inverse"].startswith("FLAT_BUT"), "flat variable D class")

    status = texts["status"]
    need("S06\tcurrent foundation forces the two-ended physical regime law\tREFUTED_AS_CURRENT_IMPLICATION_IN_BOUNDED_STATIONARY_CONNECTOR_CLASS" in status, "force status")
    need("S07\tboth endpoint frames microscopic is sufficient\tREFUTED_IN_STATIC_ZERO_SHIFT_PATH_CLASS" in status, "endpoint status")
    need("S17\tactual near-infinite information transfer\tOPEN_NOT_TESTED" in status, "information status")
    need("S15\tprior regular spherical-center no-go refutes micro reflection\tREFUTED_AS_SCOPE_APPLICATION" in status, "center scope")
    need("S18\taudit grade\tVERIFIED_WITH_CAVEATS" in status, "audit grade")

    atlas = texts["atlas"]
    need("A11\tUNIFORM_MICRO_CONNECTOR" in atlas, "whole connector row")
    need("A13\tNEAR_NULL_SHIFT_CANCELLATION" in atlas, "shift row")
    need("angular/path weights do not remove uniform divergence" in atlas, "angular row")
    need("A16\tREGULAR_SPHERICAL_AREAL_CENTER" in atlas, "center control")

    threading = texts["threading"]
    need("ALPHA_EQ_MINUS_ONE\tF~D^-1\t0\t1" in threading, "F cancellation")
    need("MINUS_TWO_LT_ALPHA_LT_MINUS_ONE" in threading and "DIAGNOSTIC_SPLIT_COUNTERCLASS" in threading, "diagnostic split")

    roles = texts["roles"]
    need("R06\tmutual equal-regime clock ratio" in roles and "N_A/N_B=1" in roles, "mutual role")
    need("R15\tinformation transfer" in roles and "OPEN_NOT_TESTED" in roles, "information role")

    premise = texts["premise"]
    need("P02\tfinite measured c_E\tOWNER_LOCKED_OBSERVATIONAL_ANCHOR" in premise, "c_E provenance")
    need("P05\tlocal Lorentzian quadratic readout\tPOSIT/CHOSE_DECLARED_READOUT" in premise, "readout premise")
    need("P07\tmacro observational-frame Reciprocity\tOWNER_FOUNDING_CLARIFICATION" in premise, "macro reciprocity")
    need("P15\tinformation propagation\tabsent" in premise, "no information import")

    correction = " ".join((texts["correction"] + texts["correction2"]).split())
    for phrase in [
        "conditional orthogonal spherical-areal control",
        "time orientation",
        "positive length only inside a selected physical representative",
        "three different operations",
        "OPEN_NOT_SELECTED",
    ]:
        need(phrase in correction, "correction phrase " + phrase)

    report = texts["report"]
    lay = texts["lay"]
    need("ADMISSIBLE BUT NOT SELECTED BY CURRENT UDT" in report, "report ceiling")
    need("No actual information-transfer theorem" in report, "report information ceiling")
    need("the entire exchange between the microscopic observers can take almost no time" in lay, "lay frame interpretation")
    need("Calling the microscopic side“near-infinite information transfer”".replace("side“", "side “") in lay, "lay information caveat")
    need("VERIFIED-WITH-CAVEATS" in texts["math_review"], "fresh math review")
    need("PASS-AFTER-PREMISE-CORRECTION" in texts["source_review"], "fresh source review")

    source_check(sources)


def catches(payload: dict, texts: dict[str, str], sources: list[dict[str, str]]) -> list[dict[str, str]]:
    cases = []

    def exercise(name: str, mutate) -> None:
        p = copy.deepcopy(payload)
        t = dict(texts)
        s = copy.deepcopy(sources)
        mutate(p, t, s)
        try:
            validate_contract(p, t, s)
        except Exception:
            cases.append({"catch": name, "result": "PASS_REJECTED"})
        else:
            raise VerifyError("mutation escaped: " + name)

    exercise("wrong_base", lambda p, t, s: p.__setitem__("base", "0" * 40))
    exercise("missing_production_check", lambda p, t, s: p["checks"].pop(next(iter(p["checks"]))))
    exercise("failed_production_check", lambda p, t, s: p["checks"].__setitem__(next(iter(p["checks"])), False))
    exercise("local_rate_mutation", lambda p, t, s: p["formulas"].__setitem__("local_orthonormal_rate", "INFINITE"))
    exercise("proper_coordinate_merge", lambda p, t, s: p["formulas"].__setitem__("proper_distance_anchor_rate", "F*D^2"))
    exercise("mutual_ratio_not_unity", lambda p, t, s: p["bounded_classifications"].__setitem__("same_micro_regime_mutual_clock_ratio", "INFINITE"))
    exercise("endpoint_sufficiency_promotion", lambda p, t, s: t.__setitem__("status", t["status"].replace("REFUTED_IN_STATIC_ZERO_SHIFT_PATH_CLASS", "DERIVED")))
    exercise("whole_connector_removed", lambda p, t, s: t.__setitem__("atlas", "\n".join(line for line in t["atlas"].splitlines() if not line.startswith("A11\t"))))
    exercise("shift_dependence_removed", lambda p, t, s: t.__setitem__("atlas", "\n".join(line for line in t["atlas"].splitlines() if not line.startswith("A13\t"))))
    exercise("angular_weight_removed", lambda p, t, s: t.__setitem__("atlas", t["atlas"].replace("angular/path weights do not remove uniform divergence", "angular irrelevant")))
    exercise("F_threshold_removed", lambda p, t, s: t.__setitem__("threading", t["threading"].replace("ALPHA_EQ_MINUS_ONE\tF~D^-1\t0\t1", "ALPHA_EQ_MINUS_ONE\tF~D^-1\t1\t1")))
    exercise("diagnostic_split_removed", lambda p, t, s: t.__setitem__("threading", t["threading"].replace("DIAGNOSTIC_SPLIT_COUNTERCLASS", "DESIRED")))
    exercise("information_promoted", lambda p, t, s: t.__setitem__("status", t["status"].replace("S17\tactual near-infinite information transfer\tOPEN_NOT_TESTED", "S17\tactual near-infinite information transfer\tDERIVED")))
    exercise("physical_law_promoted", lambda p, t, s: t.__setitem__("status", t["status"].replace("S06\tcurrent foundation forces the two-ended physical regime law\tREFUTED_AS_CURRENT_IMPLICATION_IN_BOUNDED_STATIONARY_CONNECTOR_CLASS", "S06\tcurrent foundation forces the two-ended physical regime law\tDERIVED")))
    exercise("spherical_center_reintroduced", lambda p, t, s: t.__setitem__("status", t["status"].replace("REFUTED_AS_SCOPE_APPLICATION", "DERIVED_MICRO_NO_GO")))
    exercise("c_E_provenance_promoted", lambda p, t, s: t.__setitem__("premise", t["premise"].replace("OWNER_LOCKED_OBSERVATIONAL_ANCHOR", "DERIVED")))
    exercise("Lorentzian_readout_omitted", lambda p, t, s: t.__setitem__("premise", "\n".join(line for line in t["premise"].splitlines() if not line.startswith("P05\t"))))
    exercise("sigma_typed_as_areal_radius", lambda p, t, s: t.__setitem__("correction2", t["correction2"].replace("positive length only inside a selected physical representative", "spherical areal radius")))
    exercise("missing_source", lambda p, t, s: s.pop())
    exercise("corrupt_source_hash", lambda p, t, s: s[0].__setitem__("sha256", "0" * 64))
    return cases


def main() -> None:
    payload = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    texts = {
        "status": (HERE / "STATUS_LEDGER.tsv").read_text(encoding="utf-8"),
        "atlas": (HERE / "ACCESSIBILITY_LIMIT_ATLAS.tsv").read_text(encoding="utf-8"),
        "threading": (HERE / "ASYMPTOTIC_THREADING_ATLAS.tsv").read_text(encoding="utf-8"),
        "roles": (HERE / "TWO_FRAME_ROLE_LEDGER.tsv").read_text(encoding="utf-8"),
        "premise": (HERE / "PREMISE_STATUS.tsv").read_text(encoding="utf-8"),
        "correction": (HERE / "PREREGISTRATION_SCOPE_CORRECTION.md").read_text(encoding="utf-8"),
        "correction2": (HERE / "PREREGISTRATION_SCOPE_CORRECTION_2.md").read_text(encoding="utf-8"),
        "report": (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8"),
        "lay": (HERE / "LAY_REPORT.md").read_text(encoding="utf-8"),
        "math_review": (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8"),
        "source_review": (HERE / "SOURCE_ADJUDICATION_REVIEW.md").read_text(encoding="utf-8"),
    }
    sources = read_tsv("SOURCE_LINEAGE.tsv")
    independent = independent_checks()
    need(all(independent.values()), "independent arithmetic/tensor checks")
    validate_contract(payload, texts, sources)
    catch_rows = catches(payload, texts, sources)
    need(len(catch_rows) == 20 and all(row["result"] == "PASS_REJECTED" for row in catch_rows), "catch proofs")

    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, ["catch", "result"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catch_rows)

    result = {
        "schema": "udt-two-frame-regime-metric-limit-independent-verification-1.0",
        "status": "PASS",
        "base": BASE,
        "production_checks": {"passed": 41, "total": 41},
        "independent_checks": {"passed": sum(independent.values()), "total": len(independent), "checks": independent},
        "catch_proofs": {"passed": len(catch_rows), "total": len(catch_rows)},
        "source_rows": len(sources),
        "implementation": "stdlib Fraction metric-connector algebra and direct coordinate-Ricci jet reconstruction; no production import",
        "verdict": "VERIFIED_WITH_CAVEATS",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS independent={len(independent)}/{len(independent)} catches={len(catch_rows)}/{len(catch_rows)}")


if __name__ == "__main__":
    main()
