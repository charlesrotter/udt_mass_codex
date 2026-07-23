#!/usr/bin/env python3
"""Independent fail-closed verifier for the global persistence selector audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "2f0853e070529925d38f5e8e9be99ce0c27684c8"
EXPECTED_SELECTOR_IDS = {f"S{i:02d}" for i in range(1, 13)}
EXPECTED_PROFILE_IDS = {"C01_LINEAR", "C02_CUBIC_CRITICAL", "C03_TRIVIAL"}
EXPECTED_RULING = (
    "FOUNDING_RECIPROCITY_IS_VALUE_LEVEL_AND_DOES_NOT_FORCE_GLOBAL_"
    "DERIVATIVE_BASED_3PLUS3_PERSISTENCE__PERSISTENCE_REQUIRES_A_"
    "FUTURE_NATIVE_EQUATION_OR_AN_ADDITIONAL_PREMISE"
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def independent_algebra() -> dict[str, object]:
    x, p, q = sp.symbols("x p q", real=True)

    def rep(z: sp.Expr) -> sp.Matrix:
        return sp.Matrix([[sp.exp(-z), 0], [0, sp.exp(z)]])

    cubic = x**3
    cubic_rep = rep(cubic)
    cubic_current = sp.simplify(cubic_rep.inv() * sp.diff(cubic_rep, x))
    return {
        "det": sp.simplify(rep(p).det()) == 1,
        "compose": sp.simplify(rep(p) * rep(q) - rep(p + q)) == sp.zeros(2),
        "reverse": sp.simplify(rep(p).inv() - rep(-p)) == sp.zeros(2),
        "cubic_is_odd": sp.simplify(cubic.subs(x, -x) + cubic) == 0,
        "cubic_is_nonconstant": sp.diff(cubic, x) != 0,
        "cubic_value_at_seal": str(cubic.subs(x, 0)),
        "cubic_derivative_at_seal": str(sp.diff(cubic, x).subs(x, 0)),
        "cubic_rep_at_seal": str(cubic_rep.subs(x, 0).tolist()),
        "cubic_current_at_seal": str(cubic_current.subs(x, 0).tolist()),
        "cubic_norm": str(sp.expand(sp.diff(cubic, x) ** 2)),
    }


def validate(
    result: dict[str, object],
    selectors: list[dict[str, str]],
    profiles: list[dict[str, str]],
    graph: list[dict[str, str]],
    status: list[dict[str, str]],
    scope: list[dict[str, str]],
    lineage: list[dict[str, str]],
) -> None:
    if result["schema"] != "udt-global-reciprocal-persistence-selector-1.0":
        raise AssertionError("schema")
    if result["base_commit"] != BASE or result["sympy_version"] != "1.14.0":
        raise AssertionError("environment identity")
    if result["selector_ruling"] != EXPECTED_RULING:
        raise AssertionError("maximum ruling")
    if not result["maximum_conclusion_respected"]:
        raise AssertionError("scope")

    ids = [row["selector_id"] for row in selectors]
    if len(ids) != 12 or len(set(ids)) != 12 or set(ids) != EXPECTED_SELECTOR_IDS:
        raise AssertionError("selector coverage")
    if any(row["ruling"] == "FORCES_GLOBAL_PERSISTENCE" for row in selectors):
        raise AssertionError("invented selector")
    by_selector = {row["selector_id"]: row for row in selectors}
    required = {
        "S01": "VALUE_LEVEL_ONLY",
        "S02": "VALUE_LEVEL_ONLY",
        "S03": "VALUE_LEVEL_ONLY",
        "S04": "OBSERVED_NONTRIVIALITY_ONLY",
        "S06": "COMPATIBLE_BUT_NONSELECTING",
        "S07": "EXPLICITLY_LEAVES_DERIVATIVE_FREE",
        "S09": "ON_SHELL_ADMISSIBILITY_NO_OPERATION",
        "S10": "CONDITIONAL_FUTURE_ROUTE",
        "S11": "CONDITIONAL_FUTURE_ROUTE",
        "S12": "CONDITIONAL_FUTURE_ROUTE",
    }
    if any(by_selector[key]["ruling"] != value for key, value in required.items()):
        raise AssertionError("selector classification")
    if "PHI_ZERO_AT_SEAL_WITH_FREE_NORMAL_DERIVATIVE" != by_selector["S07"][
        "reason"
    ]:
        raise AssertionError("seal derivative")
    if "NO_TYPED_OPERATION" not in by_selector["S09"]["reason"]:
        raise AssertionError("bootstrap operation")
    if "PHYSICAL_OWNER" not in by_selector["S11"]["reason"]:
        raise AssertionError("physical ownership")

    profile_ids = [row["profile_id"] for row in profiles]
    if (
        len(profile_ids) != 3
        or len(set(profile_ids)) != 3
        or set(profile_ids) != EXPECTED_PROFILE_IDS
    ):
        raise AssertionError("profile coverage")
    by_profile = {row["profile_id"]: row for row in profiles}
    cubic = by_profile["C02_CUBIC_CRITICAL"]
    cubic_expected = {
        "phi": "x**3",
        "odd_at_seal": "True",
        "phi_at_seal": "0",
        "dphi_dx": "3*x**2",
        "dphi_at_seal": "0",
        "gradient_norm_control": "9*x**4",
        "D_at_seal": "[[1, 0], [0, 1]]",
        "J_at_seal": "[[0, 0], [0, 0]]",
        "det_D": "1",
        "value_character_defined_at_seal": "True",
        "derivative_projector_defined_at_seal": "False",
        "nontriviality": "NONTRIVIAL",
        "implication_role": "DECISIVE_FOUNDATION_LEVEL_COUNTERCONFIGURATION",
        "scope_guard": "KINEMATIC_CONFIGURATION_NOT_COMPLETE_ON_SHELL_UNIVERSE",
    }
    if any(cubic[key] != value for key, value in cubic_expected.items()):
        raise AssertionError("cubic counterconfiguration")
    if by_profile["C01_LINEAR"]["derivative_projector_defined_at_seal"] != "True":
        raise AssertionError("positive control")
    if by_profile["C03_TRIVIAL"]["nontriviality"] != "TRIVIAL_ALLOWED":
        raise AssertionError("trivial representation")

    edge_ids = [row["edge_id"] for row in graph]
    if len(edge_ids) != 8 or len(set(edge_ids)) != 8:
        raise AssertionError("implication graph coverage")
    by_edge = {row["edge_id"]: row for row in graph}
    if (
        by_edge["I04"]["missing_join"] != "NONZERO_NONNULL_DPHI"
        or by_edge["I06"]["status"] != "OPEN"
        or by_edge["I07"]["status"] != "NOT_DERIVED"
        or by_edge["I08"]["status"] != "OPEN_NO_OPERATION"
    ):
        raise AssertionError("missing joins")

    by_status = {row["object"]: row for row in status}
    if len(status) != 7 or len(by_status) != 7:
        raise AssertionError("status coverage")
    if by_status["global_3plus3_persistence"]["status"] != "OPEN_NOT_DERIVED":
        raise AssertionError("global persistence promotion")
    if (
        by_status["physical_reciprocal_sector_ownership"]["status"]
        != "OPEN_NOT_DERIVED"
    ):
        raise AssertionError("ownership promotion")
    if by_status["additional_persistence_premise"]["status"] != "NOT_ADOPTED":
        raise AssertionError("premise insertion")
    if len(scope) != 4 or any(
        row["item"] == "physical_universe" and row["coverage"] != "NOT_SOLVED"
        for row in scope
    ):
        raise AssertionError("scope ledger")

    if len(lineage) != 16 or len({row["path"] for row in lineage}) != 16:
        raise AssertionError("source lineage coverage")
    for row in lineage:
        path = ROOT / row["path"]
        if (
            not path.is_file()
            or sha256(path) != row["sha256"]
            or path.stat().st_size != int(row["size"])
        ):
            raise AssertionError("source identity")

    expected_counts = {
        "selectors": 12,
        "forcing_selectors": 0,
        "counterconfigurations": 3,
        "nontrivial_counterconfigurations_with_critical_seal": 1,
        "implication_edges": 8,
        "sources": 16,
    }
    if result["counts"] != expected_counts:
        raise AssertionError("result counts")
    decisive = result["decisive_counterconfiguration"]
    if decisive != {
        "profile": "phi=x^3",
        "satisfies_value_level_reciprocal_character": True,
        "satisfies_static_odd_seal": True,
        "nontrivial": True,
        "dphi_zero_at_seal": True,
        "D_defined_at_seal": True,
        "on_shell_complete_universe_claimed": False,
        "logical_role": "DEFEATS_DIRECT_IMPLICATION_FROM_REGISTERED_FOUNDATION",
    }:
        raise AssertionError("decisive result")

    algebra = independent_algebra()
    if algebra != {
        "det": True,
        "compose": True,
        "reverse": True,
        "cubic_is_odd": True,
        "cubic_is_nonconstant": True,
        "cubic_value_at_seal": "0",
        "cubic_derivative_at_seal": "0",
        "cubic_rep_at_seal": "[[1, 0], [0, 1]]",
        "cubic_current_at_seal": "[[0, 0], [0, 0]]",
        "cubic_norm": "9*x**4",
    }:
        raise AssertionError(f"independent algebra: {algebra}")
    if result["algebra"]["group"] != {
        "composition": True,
        "determinant_one": True,
        "reversal": True,
    }:
        raise AssertionError("recorded group algebra")
    if result["algebra"]["csn"] != {
        "norm_transform": "s/omega**2",
        "positive_scale_cannot_select_nonzero": True,
        "positive_scale_preserves_zero": True,
    }:
        raise AssertionError("CSN algebra")


def main() -> None:
    result = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    selectors = read_tsv(HERE / "SELECTOR_LEDGER.tsv")
    profiles = read_tsv(HERE / "COUNTERCONFIGURATION_LEDGER.tsv")
    graph = read_tsv(HERE / "IMPLICATION_GRAPH.tsv")
    status = read_tsv(HERE / "STATUS_LEDGER.tsv")
    scope = read_tsv(HERE / "COMPLETENESS_SCOPE.tsv")
    lineage = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    validate(result, selectors, profiles, graph, status, scope, lineage)

    catches: list[dict[str, str]] = []

    def catch(catch_id: str, mutation: str, mutator) -> None:
        values = [
            copy.deepcopy(result),
            copy.deepcopy(selectors),
            copy.deepcopy(profiles),
            copy.deepcopy(graph),
            copy.deepcopy(status),
            copy.deepcopy(scope),
            copy.deepcopy(lineage),
        ]
        mutator(*values)
        try:
            validate(*values)
        except AssertionError:
            catches.append(
                {"catch_id": catch_id, "mutation": mutation, "status": "CAUGHT"}
            )
            return
        raise AssertionError(f"uncaught mutation {catch_id}: {mutation}")

    catch("C01", "remove_selector", lambda r, s, p, g, t, c, l: s.pop())
    catch(
        "C02",
        "duplicate_selector",
        lambda r, s, p, g, t, c, l: s.append(copy.deepcopy(s[0])),
    )
    catch(
        "C03",
        "promote_reciprocal_c_to_global_selector",
        lambda r, s, p, g, t, c, l: s[0].update(
            ruling="FORCES_GLOBAL_PERSISTENCE"
        ),
    )
    catch(
        "C04",
        "promote_composition_to_jet_law",
        lambda r, s, p, g, t, c, l: s[2].update(
            ruling="FORCES_GLOBAL_PERSISTENCE"
        ),
    )
    catch(
        "C05",
        "equate_observed_nontriviality_with_nowhere_critical",
        lambda r, s, p, g, t, c, l: s[3].update(
            ruling="FORCES_GLOBAL_PERSISTENCE"
        ),
    )
    catch(
        "C06",
        "make_CSN_a_selector",
        lambda r, s, p, g, t, c, l: s[5].update(
            ruling="FORCES_GLOBAL_PERSISTENCE"
        ),
    )
    catch(
        "C07",
        "fix_seal_derivative_nonzero",
        lambda r, s, p, g, t, c, l: s[6].update(
            reason="PHI_ZERO_AT_SEAL_FORCES_NONNULL_NORMAL_DERIVATIVE"
        ),
    )
    catch(
        "C08",
        "invent_bootstrap_operation",
        lambda r, s, p, g, t, c, l: s[8].update(
            reason="TYPED_OPERATION_EXCLUDES_CRITICAL_POINTS"
        ),
    )
    catch(
        "C09",
        "promote_gradient_slot",
        lambda r, s, p, g, t, c, l: s[9].update(
            ruling="FORCES_GLOBAL_PERSISTENCE"
        ),
    )
    catch(
        "C10",
        "promote_physical_owner",
        lambda r, s, p, g, t, c, l: s[10].update(
            ruling="FORCES_GLOBAL_PERSISTENCE"
        ),
    )
    catch("C11", "remove_cubic_profile", lambda r, s, p, g, t, c, l: p.pop(1))
    catch(
        "C12",
        "make_cubic_derivative_nonzero",
        lambda r, s, p, g, t, c, l: p[1].update(dphi_at_seal="1"),
    )
    catch(
        "C13",
        "make_cubic_D_undefined",
        lambda r, s, p, g, t, c, l: p[1].update(
            value_character_defined_at_seal="False"
        ),
    )
    catch(
        "C14",
        "claim_cubic_complete_universe",
        lambda r, s, p, g, t, c, l: p[1].update(
            scope_guard="COMPLETE_ON_SHELL_UNIVERSE"
        ),
    )
    catch(
        "C15",
        "erase_nonzero_dphi_missing_join",
        lambda r, s, p, g, t, c, l: g[3].update(missing_join="NONE"),
    )
    catch(
        "C16",
        "close_physical_ownership",
        lambda r, s, p, g, t, c, l: g[5].update(status="DERIVED"),
    )
    catch(
        "C17",
        "derive_global_persistence",
        lambda r, s, p, g, t, c, l: next(
            row for row in t if row["object"] == "global_3plus3_persistence"
        ).update(status="DERIVED"),
    )
    catch(
        "C18",
        "adopt_extra_persistence_premise",
        lambda r, s, p, g, t, c, l: next(
            row for row in t if row["object"] == "additional_persistence_premise"
        ).update(status="ADOPTED"),
    )
    catch(
        "C19",
        "claim_physical_universe_solved",
        lambda r, s, p, g, t, c, l: next(
            row for row in c if row["item"] == "physical_universe"
        ).update(coverage="SOLVED"),
    )
    catch("C20", "drop_source", lambda r, s, p, g, t, c, l: l.pop())
    catch(
        "C21",
        "change_maximum_ruling",
        lambda r, s, p, g, t, c, l: r.update(
            selector_ruling="GLOBAL_PERSISTENCE_DERIVED"
        ),
    )
    catch(
        "C22",
        "claim_on_shell_counteruniverse",
        lambda r, s, p, g, t, c, l: r["decisive_counterconfiguration"].update(
            on_shell_complete_universe_claimed=True
        ),
    )
    catch(
        "C23",
        "CSN_removes_zero_stratum",
        lambda r, s, p, g, t, c, l: r["algebra"]["csn"].update(
            positive_scale_preserves_zero=False
        ),
    )

    if len(catches) != 23 or any(row["status"] != "CAUGHT" for row in catches):
        raise AssertionError("catch proof count")
    with (HERE / "CATCH_PROOFS.tsv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["catch_id", "mutation", "status"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(catches)

    verification = {
        "schema": "udt-global-reciprocal-persistence-independent-verification-1.0",
        "status": "PASS",
        "sympy_version": sp.__version__,
        "independent_algebra": independent_algebra(),
        "selector_counts": dict(Counter(row["ruling"] for row in selectors)),
        "catch_proofs": len(catches),
        "catch_proofs_passed": len(catches),
        "source_hashes_replayed": len(lineage),
        "ruling": EXPECTED_RULING,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(verification, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
