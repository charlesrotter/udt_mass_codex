#!/usr/bin/env python3
"""Build the preregistered slot-level equation-ownership census.

The classifications below are explicit source-audit judgments, not keyword
predictions.  The script enforces exact slot/report/hash coverage and emits the
judgments in a reviewable table.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


PKG = Path(__file__).resolve().parent
EXTRACTS = PKG / "PRIMARY_CLAIM_EXTRACTS.tsv"
OUT = PKG / "EQUATION_OWNERSHIP_CENSUS.tsv"
SUMMARY = PKG / "EQUATION_OWNERSHIP_RESULT.json"


# slot: (primary class, load-bearing role, history verdict)
JUDGMENTS = {
    "G165": ("C11", "ownership/rank no-owner audit", "no owned nonidentity condition found"),
    "G166": ("C01", "founded ordered-pair reciprocal readout", "derives response after depth; does not generate depth profile"),
    "G167": ("C03", "full static-spherical pair pullback and terminal readout", "evaluates supplied pair germ"),
    "G168": ("C09", "ordered pair-germ plane typing", "physical germ remains supplied"),
    "G169": ("C04", "reversal and matched-chain identities", "identities do not populate relations"),
    "G170": ("C09", "endpoint-relative calibration scope", "calibration carry remains supplied"),
    "G171": ("C03", "multi-pair scalar readout", "pair responses do not generate metric values"),
    "G172": ("C05", "smooth static-family pair evaluator", "arbitrary profile and angular tangent survive"),
    "G173": ("C09", "turning-chart calibration atlas", "metric admits multiple candidate calibrations"),
    "G174": ("C09", "calibrated-germ uniqueness", "unique only after calibrated germ is supplied"),
    "G175": ("C09", "relation-wide calibration carry", "one complete pair map remains supplied"),
    "G176": ("C02", "completed-pair Dual Reciprocity premise", "fixes ruler normalization on each supplied pullback; no ambient history cut"),
    "G177": ("C11", "scaffolding regression audit", "confirms bounded dependency; no history law"),
    "G178": ("C11", "fresh review of G176/G177", "certification only"),
    "G179": ("C03", "arbitrary-coframe pullback/readout", "evaluates every supplied regular metric and germ"),
    "G180": ("C03", "smooth completed-tape descent", "integrates supplied pair metric"),
    "G181": ("C07", "singular-endpoint/extension test", "filters endpoint behavior; does not choose history"),
    "G182": ("C07", "two-sided metric and germ carry test", "join conditions act on supplied branches"),
    "G183": ("C07", "degenerate and multibranch strata", "classifies domain; branch population remains open"),
    "G184": ("C06", "typed realization equivalence quotient", "identifies representations; does not select realization"),
    "G185": ("C10", "conditional SNe replay", "observational interface, not history generation"),
    "G186": ("C05", "nonradial local pair/screen evaluator", "metric-fixed output on supplied germ"),
    "G187": ("C05", "finite Jacobi propagation", "propagates supplied metric and null query"),
    "G188": ("C05", "complete-coframe null Jacobi functor", "evaluator for supplied history/query"),
    "G189": ("C10", "conditional radiative-transfer/flux interface", "imports transfer and supplied profile"),
    "G190": ("C05", "time-live frequency/screen evaluator", "evaluates supplied metric and monotone branch"),
    "G191": ("C08", "one chosen time-live mixing witness", "existence witness does not select functions"),
    "G192": ("C08", "chosen two-function coframe family", "classifies supplied family only"),
    "G193": ("C08", "chosen symmetric mixing family", "arbitrary functions remain free within ansatz"),
    "G194": ("C08", "chosen arbitrary symmetric screen-mixing arena", "factorization theorem does not select functions"),
    "G195": ("C08", "chosen real screen-mixing arena", "rotation/factorization theorem does not select history"),
    "G196": ("C08", "chosen longitudinal mixing family", "directional theorem does not generate history"),
    "G197": ("C11", "native-provenance audit", "explicitly finds supplied history/germ boundary"),
    "G198": ("C08", "opposite-germ chosen-coframe control", "metric-encoded response in supplied family"),
    "G199": ("C05", "primary-metric radial null evaluator", "reversal symmetry leaves phi profile free"),
    "G200": ("C05", "primary-metric nonradial null evaluator", "different sampling of same supplied profile"),
    "G201": ("C05", "phi-jet regime-amplitude evaluator", "relates instrument volumes without selecting phi"),
    "G202": ("C08", "quiet-overlap jet control", "quiet premise yields a local jet restriction but infinite profiles survive"),
    "G203": ("C11", "quiet-parameter ownership audit", "founding does not own order/location/steepness"),
    "G204": ("C08", "chosen center-regular profile family", "center regularity restricts but does not own family or parameters"),
    "G205": ("C07", "geodesic/causal completion classification", "derived property of chosen family; no UDT selection premise"),
    "G206": ("C08", "common-scale extension controls", "arbitrary omega history survives"),
    "G207": ("C08", "tracefree-screen extension controls", "arbitrary shear history survives"),
    "G208": ("C08", "radial-screen-mixing extension controls", "arbitrary mixer history survives"),
    "G209": ("C08", "time-space-shift extension controls", "arbitrary shift history survives"),
    "G210": ("C08", "spatial-volume extension controls", "arbitrary volume history survives"),
    "G211": ("C03", "diagonal scalar-basis decomposition", "basis identifies degrees of freedom but supplies no values"),
    "G212": ("C06", "valued-network metric reconstruction", "all-germ isotropy would cut history but is not UDT-owned"),
    "G213": ("C06", "rank-complete completed-network reconstruction", "network must already be valued and populated"),
    "G214": ("C06", "overlap/descent reconstruction", "glues supplied values; creates none"),
    "G215": ("C04", "shared-clock scalar cocycle", "cycle identity does not determine endpoint state"),
    "G216": ("C03", "proper-clock rate readout", "derived on supplied event-pair germ"),
    "G217": ("C03", "positive first-jet readout", "event incidence and smooth germ remain supplied"),
    "G218": ("C09", "query-indexed clock correspondence", "depth field/event anchor must be supplied or separately owned"),
    "G219": ("C09", "clock-arrow protocol discrimination", "multiple lawful correspondences survive"),
    "G220": ("C05", "covariant null clock-arrow evaluator", "null remains a query type, not universal owner"),
    "G221": ("C05", "complete-coframe null clock evaluator", "full dynamic orchestra is supplied through metric"),
    "G222": ("C05", "null-incidence pair-plane/ribbon evaluator", "null family and global ruler remain supplied"),
    "G223": ("C06", "null-ribbon overlap descent", "descent glues supplied ribbon values"),
    "G224": ("C04", "shared-event vertical carry identity", "no independent direct relation or screen map generated"),
    "G225": ("C05", "normal-screen carry/holonomy evaluator", "path-labelled holonomy does not select history"),
    "G226": ("C05", "conformal-symplectic null-chain transport", "compatibility of supplied edges, not value generation"),
    "G227": ("C06", "same-event curvature tomography", "reconstructs supplied curvature values"),
    "G228": ("C04", "differential Bianchi compatibility", "identity for metric curvature jets"),
    "G229": ("C06", "local Lorentz metric jet realization", "realizes supplied jets; generates no values"),
    "G230": ("C04", "Ricci-commutator/Bianchi overlap compatibility", "standard identity on every metric history"),
    "G231": ("C06", "Cartan regional realization bridge", "integrates compatible supplied data; no physical valuation"),
    "G232": ("C11", "Cartan-closure whiteboard map", "fixed member evaluative; family closure conditional"),
    "G233": ("C11", "finite-order autonomous-closure obstruction", "rules out one route; supplies no alternative law"),
    "G234": ("C11", "closure-architecture ownership map", "names local/global routes but finds no active owner"),
    "G235": ("C06", "matched rank-complete network reconstruction", "tested global network condition accepts invariant twins"),
    "G236": ("C10", "dual-SNe relative-state reconstruction", "observational lead; no profile law"),
    "G237": ("C10", "joint SNe state freeze", "chosen covariance and no prediction"),
    "G238": ("C09", "BAO query typing", "source/history/forward map incomplete; outcomes unopened"),
    "G239": ("C10", "reference-projected point-process evaluator", "conditional operator with supplied source/history"),
    "G240": ("C09", "all-regular-null-image query rule", "removes branch weights only after supplied history/source"),
    "G241": ("C10", "SNe-to-tidal anchor adequacy test", "no adequate smooth anchor found"),
    "G242": ("C10", "exact quiet observational control", "incompatible control; small response remains open"),
    "G243": ("C10", "reciprocal SNe spline freeze attempt", "failed covariance/route gate; no history frozen"),
    "G244": ("C05", "observer-sky area/shape query evaluator", "catalog identification and history remain supplied"),
    "G245": ("C05", "metric-owned local null-cone field", "local causal field does not populate sources/branches"),
    "G246": ("C05", "two-observer null-incidence evaluator", "local branches derived conditionally; global population open"),
    "G247": ("C06", "global route-labelled branch-atlas descent", "assembles branch quiver; does not aggregate/select branches"),
    "G248": ("C09", "regular-incidence measure typing", "character/source/physical branch measure remain open"),
    "G249": ("C11", "homothety/absolute-scale nonownership theorem", "dimensionless history leaves one scale orbit"),
    "G250": ("C10", "absolute-anchor type classification", "one attached datum calibrates scale; no history value selected"),
    "G251": ("C11", "same-object attachment ownership audit", "no registered native absolute datum owner"),
    "G252": ("C10", "proper-clock attachment contract", "downstream scale calibration, not kernel/history modification"),
    "G253": ("C11", "minimal dependency/provenance compression", "confirms mixed-status evaluator chain and open history"),
    "G254": ("C11", "time-live residual ownership audit", "owned ambient evolution-equation count is zero"),
}


def main() -> None:
    with EXTRACTS.open(newline="", encoding="utf-8") as handle:
        extracts = list(csv.DictReader(handle, delimiter="\t"))
    observed = [row["slot"] for row in extracts]
    expected = [f"G{number}" for number in range(165, 255)]
    if observed != expected:
        raise RuntimeError("primary-claim extract is not the exact ordered G165-G254 census")
    if set(JUDGMENTS) != set(expected):
        missing = sorted(set(expected) - set(JUDGMENTS))
        extra = sorted(set(JUDGMENTS) - set(expected))
        raise RuntimeError(f"judgment coverage mismatch: missing={missing}, extra={extra}")

    rows = []
    for source in extracts:
        slot = source["slot"]
        class_id, role, verdict = JUDGMENTS[slot]
        rows.append(
            {
                "slot": slot,
                "primary_class": class_id,
                "load_bearing_role": role,
                "history_verdict": verdict,
                "passes_owned_history_gate": "true" if class_id in {"C12", "C13"} else "false",
                "g254_counterhistory_gate": "NOT_REJECTED" if class_id not in {"C12", "C13"} else "REQUIRES_EXACT_TEST",
                "decisive_report": source["report"],
                "decisive_report_sha256": source["report_sha256"],
            }
        )

    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    counts = Counter(row["primary_class"] for row in rows)
    result = {
        "slot_count": len(rows),
        "source_count": 321,
        "first_slot": rows[0]["slot"],
        "last_slot": rows[-1]["slot"],
        "class_counts": dict(sorted(counts.items())),
        "owned_local_metric_condition_count": counts["C12"],
        "owned_global_relation_law_count": counts["C13"],
        "candidate_unresolved_count": counts["C14"],
        "landing": "NO_LOST_CLOSURE_IN_G165_G254" if counts["C12"] == counts["C13"] == counts["C14"] == 0 else "CANDIDATE_REQUIRES_SEPARATE_TEST",
    }
    SUMMARY.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
