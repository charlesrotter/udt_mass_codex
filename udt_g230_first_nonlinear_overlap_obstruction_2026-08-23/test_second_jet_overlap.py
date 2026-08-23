import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_exact_landing_and_ranks():
    result = load("exact_results.json")
    assert result["landing"] == "FIRST_NONLINEAR_OVERLAP_OBSTRUCTION__FULL_LOCAL_4JET_REALIZATION"
    assert result["ranks"] == result["expected_ranks"]
    assert result["dimensions"]["compatible_affine_translation"] == 126
    assert all(result["checks"].values())


def test_complete_quadratic_polarization():
    result = load("exact_results.json")
    polarization = result["quadratic_polarization"]
    assert polarization["cases"] == 210
    assert polarization["covers_diagonal_monomials"] == 20
    assert polarization["covers_cross_monomials"] == 190
    assert polarization["max_differentiated_bianchi_nonzero"] == 0
    assert polarization["max_commutator_nonzero"] == 0


def test_nonzero_obstruction_witness():
    witness = load("exact_results.json")["nonzero_commutator_witness"]
    assert witness["nonzero_coefficients"] == [1]
    assert witness["rhs_nonzero_count"] == 2
    assert witness["rhs_first_nonzero_value"] == "-1"


def test_independent_full21_replay():
    result = load("independent_results.json")
    assert result["landing"] == "INDEPENDENT_FULL_21_SLOT_TWO_PRIME_AND_FRACTION_REPLAY_PASS"
    assert all(result["checks"].values())
    assert all(ranks == result["expected_ranks"] for ranks in result["ranks_by_prime"].values())


def test_hostile_mutations():
    result = load("hostile_results.json")
    assert result["landing"] == "HOSTILE_MUTATIONS_9_OF_9_CAUGHT"
    assert all(result["catches"].values())


def test_ceiling_guard():
    audit = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    next_gate = (ROOT / "NEXT_GATE.md").read_text(encoding="utf-8")
    normalized_next = " ".join(next_gate.split())
    assert "No finite-region field" in audit
    assert "physical/global history is derived" in audit
    assert "Do not continue by mechanically adding one derivative order" in next_gate
    assert "Neither route generates values or selects a physical history" in normalized_next
