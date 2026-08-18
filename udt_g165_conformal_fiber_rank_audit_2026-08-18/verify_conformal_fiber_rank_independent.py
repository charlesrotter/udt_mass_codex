#!/usr/bin/env python3
"""Implementation-distinct exact-rational verification for G165."""

from __future__ import annotations

import csv
import json
import random
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def rational_trials() -> int:
    rng = random.Random(165)
    trials = 1200
    for _ in range(trials):
        clock = Fraction(rng.randint(1, 12), rng.randint(1, 9))
        ruler = Fraction(rng.randint(1, 12), rng.randint(1, 9))
        beta = Fraction(rng.randint(-8, 8), rng.randint(1, 9))
        a = -(clock**2)
        b = -(clock**2) * beta
        c = ruler**2 - clock**2 * beta**2
        det = a * c - b * b
        assert det == -(clock * ruler) ** 2 < 0
        scale = Fraction(rng.randint(1, 12), rng.randint(1, 12))
        ap, bp, cp = scale * scale * a, scale * scale * b, scale * scale * c
        detp = ap * cp - bp * bp
        assert detp == scale**4 * det
        assert bp / ap == b / a
        assert (ap * ap) / (-detp) == (a * a) / (-det)
        clock_p, ruler_p = scale * clock, scale * ruler
        assert clock_p / ruler_p == clock / ruler
        assert (ruler_p - clock_p) / (ruler_p + clock_p) == (ruler - clock) / (ruler + clock)
    return trials


def independent_owner_census() -> dict[str, int]:
    g155 = read_tsv(ROOT / "udt_g155_scale_sector_closure_whiteboard_2026-08-18/EQUATION_ROLE_LEDGER.tsv")
    assert len(g155) == 41
    active_physical = [
        row for row in g155
        if row["role"] in {"PHYSICAL_HISTORY_CONSTRAINT", "PHYSICAL_HISTORY_EVOLUTION"}
        and row["active_status"].startswith("ACTIVE")
    ]
    assert not active_physical

    g156 = read_tsv(ROOT / "udt_g156_three_observer_scale_carry_audit_2026-08-18/CLAIM_LEDGER.tsv")
    by_id = {row["claim_id"]: row for row in g156}
    assert by_id["C10"]["status"] == "OPEN_PHYSICAL_OWNER"
    assert by_id["C11"]["status"] == "OPEN"

    phrase_guards = {
        "udt_g157_regime_dependent_channel_balance_regrading_2026-08-18/AUDIT_REPORT.md": "PHYSICAL_CROSS_QUERY_CARRY_AND_HISTORY_EVOLUTION_REMAIN_OPEN",
        "udt_g158_complete_coframe_semidirect_score_audit_2026-08-18/AUDIT_REPORT.md": "PHYSICAL_CARRY_HISTORY_SCORE_AND_GLOBAL_COMPLETION_OPEN",
        "udt_g159_complete_score_terminal_descent_2026-08-18/AUDIT_REPORT.md": "PHYSICAL_HISTORY_QUERY_LAMBDA_AND_GLOBAL_COMPLETION_OPEN",
        "udt_g160_three_observer_timelive_first_jet_carry_2026-08-18/AUDIT_REPORT.md": "PHYSICAL_CARRY_HISTORY_QUERY_LAMBDA_AND_COMPLETION_OPEN",
        "udt_g161_pair_carry_lorentz_quotient_screen_resolution_2026-08-18/AUDIT_REPORT.md": "physical history or observer query",
        "udt_g162_lambda_dependence_frontier_census_2026-08-18/AUDIT_REPORT.md": "HISTORY_VALUE_OR_EVOLUTION_OPEN",
        "udt_g163_xmax_dependency_reversal_audit_2026-08-18/AUDIT_REPORT.md": "does not prove that physical distance",
        "udt_g164_scaffold_subtraction_anchor_sufficiency_whiteboard_2026-08-18/AUDIT_REPORT.md": "PONDER_LEAD__NOT_A_PREREGISTERED_DERIVATION",
    }
    for relative, phrase in phrase_guards.items():
        assert phrase in (ROOT / relative).read_text(encoding="utf-8"), relative

    return {
        "g155_rows": len(g155),
        "g155_active_physical_restrictors": len(active_physical),
        "g156_open_owner_rows_checked": 2,
        "post_g156_report_guards": len(phrase_guards),
    }


def main() -> None:
    trials = rational_trials()
    census = independent_owner_census()
    production = json.loads((PKG / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert production["primary_landing"] == "NO_OWNED_NONIDENTITY_CONDITION"
    assert production["secondary_classifications"]["current_anchor_readout_map"] == "FUNCTIONAL_KERNEL"
    assert production["secondary_classifications"]["full_valued_rank_complete_network"] == "VALUED_NETWORK_RECONSTRUCTION_ONLY"
    assert production["candidate_counts"]["owned_metric_restrictors"] == 0

    result = {
        "status": "PASS",
        "exact_rational_trials": trials,
        "independent_census": census,
        "primary_landing": production["primary_landing"],
    }
    (PKG / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
