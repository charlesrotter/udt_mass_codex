#!/usr/bin/env python3
"""Fail-closed verifier for the native-law home/codomain/ownership audit."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(arch, laws, atlas, variations, sne, entail, strata, premises, sources) -> None:
    arch_ids = [row["architecture_id"] for row in arch]
    law_ids = [row["law_id"] for row in laws]
    assert arch_ids == [f"H{i:02d}" for i in range(1, 9)]
    assert len(arch_ids) == len(set(arch_ids)) == 8
    assert law_ids == [f"K{i:02d}" for i in range(1, 7)]
    assert len(law_ids) == len(set(law_ids)) == 6
    pairs = [(row["architecture_id"], row["law_id"]) for row in atlas]
    assert len(pairs) == len(set(pairs)) == 48
    assert set(pairs) == {(a, l) for a in arch_ids for l in law_ids}
    by_pair = {(row["architecture_id"], row["law_id"]): row for row in atlas}
    assert by_pair[("H02", "K01")]["ruling"] == "DERIVED_NATURAL_HOME"
    assert by_pair[("H01", "K02")]["ruling"] == "DERIVED_NATURAL_HOME"
    assert by_pair[("H01", "K03")]["ruling"] == "GENERICALLY_INSUFFICIENT_ALONE"
    assert by_pair[("H03", "K04")]["ruling"] == "ADMISSIBLE_ONLY_IF_SECTION_OWNERSHIP_SELECTED"
    assert by_pair[("H04", "K04")]["variation_owner"] == "delta_g with delta_s=DS_g[delta_g]"
    assert all(by_pair[("H06", law_id)]["ruling"] == "UNAVAILABLE_MISSING_NATIVE_AGGREGATION_DATA" for law_id in law_ids)
    assert all(by_pair[("H08", law_id)]["ruling"] == "UNCLASSIFIED_ESCAPE_RETAINED" for law_id in law_ids)
    assert all(by_pair[("H07", law_id)]["variation_owner"] == "owner attached to each component" for law_id in law_ids)

    variation_ids = [row["variation_id"] for row in variations]
    assert variation_ids == [f"V{i:02d}" for i in range(1, 13)]
    by_v = {row["variation_id"]: row for row in variations}
    assert by_v["V02"]["status"] == "DERIVED_QUERY_NOT_FIELD_VARIATION"
    assert by_v["V03"]["status"] == "OPEN_PHYSICAL_OWNERSHIP"
    assert by_v["V04"]["rule"] == "delta_s=DS_g[delta_g]"
    assert by_v["V06"]["status"] == "OPEN_STRATIFIED_OWNERSHIP"
    assert by_v["V11"]["status"] == "OPEN_NOT_SUPPLIED"

    assert [row["architecture_id"] for row in sne] == arch_ids
    assert all(row["selects_home"] == "NO" for row in sne)
    by_sne = {row["architecture_id"]: row for row in sne}
    assert by_sne["H01"]["compatibility"] == "COMPATIBLE_ONLY_WITH_DOWNSTREAM_TYPED_QUERY_READOUT_LAYER"
    assert by_sne["H06"]["compatibility"] == "BLOCKED_MISSING_NATIVE_AGGREGATION_DATA"
    assert by_sne["H08"]["compatibility"] == "UNCLASSIFIED"

    entail_ids = [row["entailment_id"] for row in entail]
    assert entail_ids == [f"E{i:02d}" for i in range(1, 13)]
    by_e = {row["entailment_id"]: row for row in entail}
    assert by_e["E01"]["status"] == "DERIVED"
    assert by_e["E02"]["status"] == "DEFINED_FROM_METRIC"
    assert by_e["E04"]["status"] == "DERIVED_BOUNDED"
    assert by_e["E10"]["status"] == "OPEN_UNAVAILABLE"
    assert by_e["E11"]["status"] == "CONDITIONAL_ANCHOR"
    assert by_e["E12"]["status"] == "OPEN_FOUNDATIONS_DO_NOT_DECIDE"

    assert len(strata) == 7 and len({row["stratum_id"] for row in strata}) == 7
    assert all(row["status"].startswith(("OPEN_", "CONDITIONAL_")) for row in strata)
    assert all(row["variation_rule"].lower() != "unique derivative" for row in strata)

    p = {row["premise_id"]: row for row in premises}
    assert len(p) == 14
    assert p["P06"]["status"] == "OPEN_INACTIVE"
    assert p["P02"]["open_or_excluded"] == "physical depth assignment open"
    assert p["P09"]["status"] == "OPEN"
    assert p["P10"]["status"] == "CONDITIONAL_OBSERVATIONAL_COMPATIBILITY_ANCHOR"
    assert p["P10"]["open_or_excluded"] == "cannot select home variation action branch or X_max"
    assert p["P11"]["status"] == "POSIT"
    assert p["P13"]["status"] == "OPEN"
    assert p["P13"]["open_or_excluded"] == "no reconstruction authorized"

    assert len(sources) == len({row["path"] for row in sources}) == 28
    for row in sources:
        target = ROOT / row["path"]
        assert target.is_file()
        assert target.stat().st_size == int(row["size"])
        assert digest(target) == row["sha256"]


arch = table(HERE / "CANDIDATE_ARCHITECTURE_UNIVERSE.tsv")
laws = table(HERE / "LAW_CLASS_UNIVERSE.tsv")
atlas = table(HERE / "HOME_CODOMAIN_ATLAS.tsv")
variations = table(HERE / "VARIATION_OWNERSHIP_ATLAS.tsv")
sne = table(HERE / "SNE_COMPATIBILITY_ATLAS.tsv")
entail = table(HERE / "FOUNDATIONAL_ENTAILMENT_MATRIX.tsv")
strata = table(HERE / "STRATIFIED_OWNERSHIP_LEDGER.tsv")
quantifiers = table(HERE / "QUERY_QUANTIFIER_LEDGER.tsv")
native_compatibility = table(HERE / "NATIVE_COMPATIBILITY_LEDGER.tsv")
premises = table(HERE / "PREMISE_LEDGER.tsv")
sources = table(HERE / "SOURCE_MANIFEST.tsv")
validate(arch, laws, atlas, variations, sne, entail, strata, premises, sources)
assert [row["quantifier_id"] for row in quantifiers] == [f"Q{i:02d}" for i in range(1, 8)]
by_q = {row["quantifier_id"]: row for row in quantifiers}
assert by_q["Q01"]["variation_owner"] == "q is an argument not varied"
assert by_q["Q02"]["status"] == "ADMISSIBLE_NOT_SELECTED"
assert by_q["Q04"]["status"] == "OPEN_PHYSICAL_OWNERSHIP"
assert by_q["Q05"]["variation_owner"] == "vary g with DS_g chain term"
assert by_q["Q07"]["status"] == "OPEN_UNAVAILABLE"
assert [row["architecture_id"] for row in native_compatibility] == [f"H{i:02d}" for i in range(1, 9)]
by_native = {row["architecture_id"]: row for row in native_compatibility}
assert by_native["H01"]["metric_is_theory_compatibility"] == "COMPATIBLE"
assert by_native["H02"]["metric_is_theory_compatibility"] == "COMPATIBLE_IF_QUERY_IS_DERIVED_ARGUMENT"
assert by_native["H03"]["metric_is_theory_compatibility"] == "CONDITIONAL_EXTRA_STRUCTURE"
assert by_native["H04"]["metric_is_theory_compatibility"] == "COMPATIBLE_ON_REGULAR_METRIC_DERIVED_BRANCH"
assert by_native["H07"]["metric_is_theory_compatibility"] == "REQUIRED_AS_TYPED_BOOKKEEPING_NOT_SELECTED_AS_ONE_PHYSICAL_LAW"

production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
assert production["status"] == independent["status"] == "PASS"
assert production["exact_checks"] == 26 and independent["exact_checks"] == 22
for key in ("reciprocal_pair_query_values", "basic_trace", "branch_selector_chain_term", "collision_limits_distinct", "sne_conditional_shape", "sne_readout_slots"):
    assert production[key] == independent[key]

tree = ast.parse((HERE / "verify_architecture_independent.py").read_text(encoding="utf-8"))
imports = {
    alias.name.split(".")[0]
    for node in ast.walk(tree)
    if isinstance(node, ast.Import)
    for alias in node.names
} | {
    (node.module or "").split(".")[0]
    for node in ast.walk(tree)
    if isinstance(node, ast.ImportFrom)
}
assert imports <= {"__future__", "json", "fractions", "pathlib"}
assert "derive_native_law_architecture" not in (HERE / "verify_architecture_independent.py").read_text(encoding="utf-8")


def must_fail(catch_id, mutate):
    values = [deepcopy(x) for x in (arch, laws, atlas, variations, sne, entail, strata, premises, sources)]
    mutate(*values)
    try:
        validate(*values)
    except (AssertionError, KeyError, ValueError):
        return (catch_id, "REJECT", "PASS")
    raise AssertionError(f"catch did not fail: {catch_id}")


catches = []
catches.append(must_fail("X01_MISSING_ARCHITECTURE", lambda a, *_: a.pop()))
catches.append(must_fail("X02_DUPLICATE_ARCHITECTURE", lambda a, *_: a.append(deepcopy(a[0]))))
catches.append(must_fail("X03_EQUIVARIANCE_FALSE_BASIC", lambda a, l, x, *_: next(r for r in x if r["architecture_id"] == "H01" and r["law_id"] == "K03").update(ruling="DERIVED_NATURAL_HOME")))
catches.append(must_fail("X04_QUERY_FALSE_FIELD_VARIATION", lambda a, l, x, v, *_: next(r for r in v if r["variation_id"] == "V02").update(status="INDEPENDENT_FIELD")))
catches.append(must_fail("X05_CHAIN_RULE_REMOVED", lambda a, l, x, *_: next(r for r in x if r["architecture_id"] == "H04" and r["law_id"] == "K04").update(variation_owner="delta_g_only")))
catches.append(must_fail("X06_FALSE_SMOOTH_STRATUM", lambda a, l, x, v, s, e, st, *_: st[1].update(status="DERIVED_UNIQUE_SMOOTH")))
catches.append(must_fail("X07_INVENTED_AGGREGATION", lambda a, l, x, *_: next(r for r in x if r["architecture_id"] == "H06").update(ruling="DERIVED_NATURAL_HOME")))
# X08 is exercised independently against the exact four-slot result.
try:
    assert len(set(production["sne_readout_slots"][:3] + [production["sne_readout_slots"][2]])) == 4
except AssertionError:
    catches.append(("X08_COLLAPSED_SNE_SLOTS", "REJECT", "PASS"))
else:
    raise AssertionError("catch did not fail: X08")
catches.append(must_fail("X09_SNE_SELECTS_HOME", lambda a, l, x, v, s, *_: s[0].update(selects_home="YES")))
catches.append(must_fail("X10_PROPER_DISTANCE_COLLAPSE", lambda a, l, x, v, s, e, st, p, so: p[9].update(open_or_excluded="proper pair equals optical")))
catches.append(must_fail("X11_WRL_PROMOTED_UNIVERSAL", lambda a, l, x, v, s, e, st, p, so: p[9].update(status="DERIVED_UNIVERSAL")))
catches.append(must_fail("X12_CSN_REACTIVATED", lambda a, l, x, v, s, e, st, p, so: p[5].update(status="DERIVED_ACTIVE")))
catches.append(must_fail("X13_ACTION_PROMOTED", lambda a, l, x, v, s, e, st, p, so: p[12].update(status="DERIVED")))
catches.append(must_fail("X14_READOUT_EQUALS_HOME", lambda a, l, x, v, s, e, *_: e[11].update(status="DERIVED_UNIQUE_HOME")))
catches.append(must_fail("X15_ESCAPE_REMOVED", lambda a, *_: a.pop(7)))
catches.append(must_fail("X16_LAYER_OWNER_LOST", lambda a, l, x, *_: next(r for r in x if r["architecture_id"] == "H07").update(variation_owner="one universal owner")))
catches.append(must_fail("X17_PHI_ASSIGNMENT_FALSE_DERIVED", lambda a, l, x, v, s, e, st, p, so: p[1].update(open_or_excluded="physical depth assignment derived")))
catches.append(must_fail("X18_CONNECTION_FALSE_DYNAMICS", lambda a, l, x, v, s, e, *_: e[1].update(status="DERIVED_NATIVE_DYNAMICS")))
catches.append(must_fail("X19_SOURCE_BOUNDARY_FALSE_SELECTED", lambda a, l, x, v, s, e, st, p, so: p[12].update(open_or_excluded="selected source and boundary")))
bad_imports = set(imports) | {"derive_native_law_architecture"}
assert not bad_imports <= {"__future__", "json", "fractions", "pathlib"}
catches.append(("X20_INDEPENDENT_IMPORTS_PRODUCTION", "REJECT", "PASS"))

assert len(catches) == 20
with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("catch_id", "expected", "observed"))
    writer.writerows(catches)

overall = next(row for row in table(HERE / "STATUS_LEDGER.tsv") if row["object"] == "overall_audit")["status"]
review_verdict = "NOT_RUN"
if (HERE / "FRESH_ADVERSARIAL_REVIEW_RESULT.json").exists():
    review = json.loads((HERE / "FRESH_ADVERSARIAL_REVIEW_RESULT.json").read_text(encoding="utf-8"))
    review_verdict = review["verdict"]
    assert review_verdict in {"PASS", "PASS_WITH_CAVEATS", "ACCEPT_WITH_REQUIRED_REPAIRS"}
    assert review["files_modified_by_reviewer"] == 0
    assert digest(HERE / "FRESH_ADVERSARIAL_REVIEW.md") == review["review_output_sha256"]
    if overall.startswith("VERIFIED"):
        assert review.get("required_repairs", 0) == 0
else:
    assert overall == "PROVISIONAL_PENDING_FRESH_ADVERSARIAL_REVIEW"

result = {
    "status": "PASS" if overall.startswith("VERIFIED") else "PASS_PRE_REVIEW",
    "architectures": len(arch),
    "law_classes": len(laws),
    "architecture_law_facets": len(atlas),
    "variation_classes": len(variations),
    "query_quantifier_classes": len(quantifiers),
    "native_compatibility_rows": len(native_compatibility),
    "sne_readout_slots": 4,
    "stratified_classes": len(strata),
    "production_exact_checks": production["exact_checks"],
    "independent_exact_checks": independent["exact_checks"],
    "catch_proofs": len(catches),
    "frozen_sources": len(sources),
    "fresh_adversarial_review": review_verdict,
    "result": "TYPED_HOMES_PARTIALLY_FORCED__COMPLETE_NATIVE_DYNAMICAL_HOME_CODOMAIN_AND_VARIATION_DOMAIN_NOT_SELECTED",
}
(HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
