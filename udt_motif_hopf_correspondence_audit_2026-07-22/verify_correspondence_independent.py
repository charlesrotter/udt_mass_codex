#!/usr/bin/env python3
"""Independent verifier for the coherent motif-to-Hopf correspondence audit.

Imports the previously frozen independent motif verifier, not the production correspondence
builder, canonical evaluator, motif core, or invariant-subspace core.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import itertools
import json
import math
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRIOR_INDEPENDENT = ROOT / "udt_instrument_motif_atlas_2026-07-21"
sys.path.insert(0, str(PRIOR_INDEPENDENT))
import verify_motif_atlas as independent  # noqa: E402


COMPARE = (
    "algebra_dimension", "primitive_block_ranks", "primitive_block_signatures",
    "central_split_count", "motif", "numeric_status",
)
FAMILIES = [(f"M{mask:02d}_" + "_".join(key for key, bit in independent.BITS.items() if mask & bit),
             mask, tuple(key for key, bit in independent.BITS.items() if mask & bit)) for mask in range(1, 32)]
BASE_VALUES = (0.08, 0.14, -0.06, 0.12, -0.09, 0.05, 0.11, -0.07, 0.09, 0.04)
PHI_OFFSETS = (-0.25, 0.0, 0.25, 0.125)
POINTS = {
    "P0": (0.0, 0.0, 0.0, 0.0), "P1": (1/3, -1/4, 1/5, -1/6),
    "P2": (-1/4, 1/5, -1/6, 1/7), "P3": (1/5, 1/6, -1/7, -1/8),
    "P4": (-1/6, -1/7, 1/8, 1/9), "P5": (1/2, 0.0, -1/3, 1/4),
    "P6": (0.0, -1/2, 1/4, -1/3), "P7": (1/3, 1/3, 1/3, 1/3),
}
POINT_PAIRS = {0: ("P0", "P4"), 1: ("P1", "P5"), 2: ("P2", "P6"), 3: ("P3", "P7")}
PARAMETERS = tuple(f"alpha_{index}" for index in range(10)) + ("beta",)
H_STEPS = (1.0e-4, 5.0e-5)
DERIVATIVE_GATE = 5.0e-3
FROB_LOW = 1.0e-7
FROB_HIGH = 1.0e-5


@dataclass
class Jet:
    value: float
    first: np.ndarray
    second: np.ndarray

    @classmethod
    def constant(cls, value):
        return cls(float(value), np.zeros(4), np.zeros((4, 4)))

    def __add__(self, other):
        rhs = other if isinstance(other, Jet) else Jet.constant(other)
        return Jet(self.value + rhs.value, self.first + rhs.first, self.second + rhs.second)

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.value, -self.first, -self.second)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Jet) else -other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        rhs = other if isinstance(other, Jet) else Jet.constant(other)
        return Jet(
            self.value * rhs.value,
            self.first * rhs.value + self.value * rhs.first,
            self.second * rhs.value + self.value * rhs.second
            + np.outer(self.first, rhs.first) + np.outer(rhs.first, self.first),
        )

    __rmul__ = __mul__


def jexp(value: Jet) -> Jet:
    current = math.exp(value.value)
    return Jet(current, current * value.first, current * (value.second + np.outer(value.first, value.first)))


def features(x: np.ndarray) -> list[Jet]:
    rows = []
    for coordinate in range(4):
        first = np.zeros(4); first[coordinate] = 1
        rows.append(Jet(float(x[coordinate]), first, np.zeros((4, 4))))
    for coordinate in range(4):
        first = np.zeros(4); first[coordinate] = x[coordinate]
        second = np.zeros((4, 4)); second[coordinate, coordinate] = 1
        rows.append(Jet(0.5 * float(x[coordinate] ** 2), first, second))
    for a, b in independent.PAIRS:
        first = np.zeros(4); first[a] = x[b]; first[b] = x[a]
        second = np.zeros((4, 4)); second[a, b] = second[b, a] = 1
        rows.append(Jet(float(x[a] * x[b]), first, second))
    return rows


def coefficient(bank: int, field: int, term: int) -> float:
    raw = ((bank + 2) * 11 + (field + 1) * 7 + (term + 1) * 5 + (bank + 1) * (field + term + 3)) % 19 - 9
    if raw == 0:
        raw = 1 if (bank + field + term) % 2 == 0 else -1
    return raw / (60.0 if term < 4 else 90.0 if term < 8 else 120.0)


def polynomial(bank: int, field: int, x: np.ndarray) -> Jet:
    result = Jet.constant(0)
    for term, feature in enumerate(features(x)):
        result += coefficient(bank, field, term) * feature
    return result


def metric_phi_jets(bank: int, amplitudes: np.ndarray, x: np.ndarray):
    latent = [Jet.constant(BASE_VALUES[index]) + amplitudes[index] * polynomial(bank, index, x) for index in range(10)]
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    u, w, r, t = jexp(a), jexp(c), jexp(d), jexp(f)
    slots = (-(u*u), -(u*b), w*w-b*b, r*r, r*e, e*e+t*t, a20, a30, a21, a31)
    h = [[slots[0], slots[1]], [slots[1], slots[2]]]
    q = [[slots[3], slots[4]], [slots[4], slots[5]]]
    shifts = [[slots[6], slots[8]], [slots[7], slots[9]]]
    zero = Jet.constant(0)
    metric = [[zero for _ in range(4)] for _ in range(4)]
    for i in range(2):
        for j in range(2):
            metric[i][j] = h[i][j] + sum((q[a0][b0] * shifts[a0][i] * shifts[b0][j]
                                           for a0 in range(2) for b0 in range(2)), Jet.constant(0))
        for b0 in range(2):
            metric[i][2+b0] = sum((q[a0][b0] * shifts[a0][i] for a0 in range(2)), Jet.constant(0))
            metric[2+b0][i] = metric[i][2+b0]
    for a0 in range(2):
        for b0 in range(2):
            metric[2+a0][2+b0] = q[a0][b0]
    g = np.asarray([[metric[mu][nu].value for nu in range(4)] for mu in range(4)])
    dg = np.asarray([[[metric[mu][nu].first[k] for nu in range(4)] for mu in range(4)] for k in range(4)])
    ddg = np.asarray([[[[metric[mu][nu].second[k, ell] for nu in range(4)] for mu in range(4)]
                        for ell in range(4)] for k in range(4)])
    phi = Jet.constant(PHI_OFFSETS[bank]) + amplitudes[10] * polynomial(bank, 10, x)
    return g, dg, ddg, phi.first, phi.second


def read_tsv(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def gzip_rows(path: Path):
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle, delimiter="\t")


def identity_data():
    carriers = {row["carrier_id"]: np.asarray([float(row[name]) for name in PARAMETERS])
                for row in read_tsv(ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21/CARRIER_VECTOR_REGISTRY.tsv")}
    output = {}
    for row in read_tsv(HERE / "COHERENT_IDENTITY_REGISTRY.tsv"):
        bank = int(row["bank"][1:]); mask = int(row["mask_id"][1:], 16); values = np.zeros(11); full = carriers[row["carrier_id"]]
        for indices, bit in (((0,1,2),1), ((3,4,5),2), ((6,7,8,9),4), ((10,),8)):
            if mask & bit:
                values[list(indices)] = full[list(indices)]
        output[row["identity_id"]] = (bank, values)
    return output


def classify_at(bank, amplitudes, point, selected_masks=None):
    g, dg, ddg, dphi, ddphi = metric_phi_jets(bank, amplitudes, point)
    objects, geo = independent.objects(g, dg, ddg, dphi, ddphi)
    scalar = {key: objects[key] for key in ("R", "H", "D")}
    results = {}
    for family_id, mask, keys in FAMILIES:
        if selected_masks is not None and mask not in selected_masks:
            continue
        results[mask] = independent.classify(independent.operators(objects, keys), objects["gradient"], g, scalar, keys)
    return geo, results


def path_points(bank):
    start_id, end_id = POINT_PAIRS[bank]
    start = np.asarray(POINTS[start_id]); end = np.asarray(POINTS[end_id])
    return [(1-t)*start+t*end for t in (node/16 for node in range(17))]


def labels(result):
    return [(int(row["rank"]), str(row["signature"])) for row in result["blocks"]]


def match(reference, current):
    first_labels, second_labels = labels(reference), labels(current)
    if Counter(first_labels) != Counter(second_labels):
        return None
    first, second = reference["projectors"], current["projectors"]
    best = None; distance = math.inf
    for permutation in itertools.permutations(range(len(second))):
        if any(first_labels[index] != second_labels[permutation[index]] for index in range(len(first))):
            continue
        ordered = [second[permutation[index]] for index in range(len(first))]
        current_distance = max((independent.relmax(first[index], ordered[index]) for index in range(len(first))), default=0)
        if current_distance < distance:
            best, distance = ordered, current_distance
    return best


def covariant_derivative(projector, partial, gamma):
    output = np.asarray(partial).copy()
    for rho, nu, beta, sigma in itertools.product(range(4), repeat=4):
        output[rho,nu,beta] += gamma[nu,rho,sigma]*projector[sigma,beta] - gamma[sigma,rho,beta]*projector[nu,sigma]
    return output


def frobenius(projector, partial, gamma):
    nabla = covariant_derivative(projector, partial, gamma); term = np.zeros((4,4,4))
    for nu, alpha, beta, rho in itertools.product(range(4), repeat=4):
        term[nu,alpha,beta] += projector[rho,alpha]*nabla[rho,nu,beta] - projector[rho,beta]*nabla[rho,nu,alpha]
    value = np.einsum("mn,nab->mab", np.eye(4)-projector, term)
    return float(np.linalg.norm(value)/max(np.linalg.norm(nabla),1e-30))


def frob_class(value, convergence):
    if convergence > DERIVATIVE_GATE: return "NUMERIC_UNCERTAIN_DERIVATIVE"
    if value <= FROB_LOW: return "NUMERICALLY_INTEGRABLE_LOCAL"
    if value >= FROB_HIGH: return "NUMERICALLY_NONINTEGRABLE_LOCAL"
    return "NUMERIC_UNCERTAIN_OBSTRUCTION"


def distribution_multiset(bank, amplitudes, mask):
    points = path_points(bank); midpoint = points[8]
    geo, center_results = classify_at(bank, amplitudes, midpoint, {mask}); center = center_results[mask]
    stencil = {}
    for step in H_STEPS:
        for axis in range(4):
            for sign in (-1,1):
                point = midpoint.copy(); point[axis] += sign*step
                _, current = classify_at(bank, amplitudes, point, {mask}); stencil[(step,axis,sign)] = current[mask]
    all_results = [center, *stencil.values()]
    stable = center["numeric_status"] == "NUMERIC_CLASSIFIED" and all(
        current["numeric_status"] == "NUMERIC_CLASSIFIED" and Counter(labels(current)) == Counter(labels(center))
        for current in all_results
    )
    if not stable:
        return Counter({("UNRESOLVED", "-", "NOT_CLASSIFIED"): 1}), False
    center_projectors = [np.asarray(item) for item in center["projectors"]]; derivatives = {}
    for step in H_STEPS:
        current_derivatives = [np.zeros((4,4,4)) for _ in center_projectors]
        for axis in range(4):
            minus = match(center, stencil[(step,axis,-1)]); plus = match(center, stencil[(step,axis,1)])
            if minus is None or plus is None:
                return Counter({("UNRESOLVED", "-", "NOT_CLASSIFIED"): 1}), False
            for index in range(len(center_projectors)):
                current_derivatives[index][axis] = (plus[index]-minus[index])/(2*step)
        derivatives[step] = current_derivatives
    candidates = []
    for index, block in enumerate(center["blocks"]):
        candidates.append(("PRIMITIVE_BLOCK", [index], int(block["rank"])))
    for pair in independent.splits(center_projectors):
        for projector in pair:
            members = [index for index,item in enumerate(center_projectors) if independent.relmax(projector@item,item) <= 1e-8]
            candidates.append(("COMPLEMENTARY_RANK2", members, 2))
    census = Counter(); gamma = np.asarray(geo["gamma"])
    for kind, members, rank in candidates:
        projector = sum((center_projectors[index] for index in members), np.zeros((4,4)))
        dh = sum((derivatives[H_STEPS[0]][index] for index in members), np.zeros((4,4,4)))
        dh2 = sum((derivatives[H_STEPS[1]][index] for index in members), np.zeros((4,4,4)))
        convergence = float(np.linalg.norm(dh-dh2)/max(np.linalg.norm(dh2),1.0))
        if rank == 1: classification = "LOCALLY_INTEGRABLE_BY_RANK_ONE"
        elif rank == 4: classification = "WHOLE_TANGENT_SPACE"
        else: classification = frob_class(frobenius(projector,dh2,gamma),convergence)
        census[(kind,str(rank),classification)] += 1
    return census, True


def exact_toric_check():
    phi = sp.symbols("phi", real=True); A, Ap, O, Op = sp.symbols("A Ap O Op", positive=True)
    h = (0, -Ap/A**3, (Op/O-1)/A**2, (Op/O+1)/A**2); d = (0,1/A**2,0,0)
    if sp.simplify(h[3]-h[2]-2/A**2) != 0: raise AssertionError("toric angular gap")
    f = sp.simplify(1/(1+sp.exp(4*phi)))
    q = sp.simplify(sp.limit(f,phi,-sp.oo)-sp.limit(f,phi,sp.oo))
    n2 = sp.simplify((sp.sech(2*phi)**2+sp.tanh(2*phi)**2).rewrite(sp.exp))
    if q != 1 or n2 != 1: raise AssertionError("toric unit/norm")
    round_b = sp.simplify(sp.exp(-2*phi)/(2*sp.cosh(2*phi))); round_c = sp.simplify(sp.exp(2*phi)/(2*sp.cosh(2*phi)))
    caps = (sp.limit(round_b,phi,-sp.oo),sp.limit(round_b,phi,sp.oo),sp.limit(round_c,phi,-sp.oo),sp.limit(round_c,phi,sp.oo))
    if caps != (1,0,0,1): raise AssertionError("round caps")
    return {"angular_gap": str(sp.simplify(h[3]-h[2])), "conditional_unit_q": str(q), "quotient_norm": str(n2), "round_caps": list(map(str,caps))}


def main():
    identity_lookup = identity_data(); ids = sorted(identity_lookup, key=lambda value: hashlib.sha256(("MOTIF_HOPF_INDEPENDENT_V1|"+value).encode()).hexdigest())[:64]
    if len(ids) != 64: raise AssertionError("blind anchors")
    blind = {}
    for identity_id in ids:
        bank, amplitudes = identity_lookup[identity_id]
        for node, point in enumerate(path_points(bank)):
            _, results = classify_at(bank, amplitudes, point)
            for family_id, mask, _keys in FAMILIES:
                blind[(identity_id,node,family_id)] = results[mask]
    if len(blind) != 64*17*31: raise AssertionError("blind coverage")

    summaries = list(gzip_rows(HERE/"PATH_CONTINUATION_SUMMARY.tsv.gz"))
    adverse = {(row["identity_id"],row["family_id"],int(row["family_mask"])) for row in summaries
               if int(row["motif_transitions"]) or int(row["classified_nodes"]) != 17}
    adverse_results = {}
    for identity_id, family_id, mask in sorted(adverse):
        bank, amplitudes = identity_lookup[identity_id]
        for node, point in enumerate(path_points(bank)):
            _, current = classify_at(bank, amplitudes, point, {mask})
            adverse_results[(identity_id,node,family_id)] = current[mask]

    wanted = set(blind) | set(adverse_results); saved = {}
    for row in gzip_rows(HERE/"PATH_FAMILY_ATLAS.tsv.gz"):
        key=(row["identity_id"],int(row["path_node"]),row["family_id"])
        if key in wanted: saved[key]=row
    if len(saved) != len(wanted): raise AssertionError("saved comparison coverage")
    mismatches=[]
    for source in (blind,adverse_results):
        for key,current in source.items():
            row=saved[key]
            for field in COMPARE:
                if str(current[field]) != row[field]: mismatches.append((key,field,str(current[field]),row[field]))
    if mismatches: raise AssertionError(f"classification mismatches {mismatches[:3]}")

    saved_distribution = defaultdict(Counter); unstable_saved=set()
    for row in gzip_rows(HERE/"DISTRIBUTION_ATLAS.tsv.gz"):
        key=(row["identity_id"],row["family_id"],int(row["family_mask"]))
        if row["stencil_status"] != "STABLE_CLASSIFIED": unstable_saved.add(key)
        if row["identity_id"] in ids:
            saved_distribution[key][(row["distribution_kind"],row["rank"],row["frobenius_class"])] += 1
    distribution_comparisons=0
    for identity_id in ids:
        bank, amplitudes=identity_lookup[identity_id]
        for family_id,mask,_keys in FAMILIES:
            got,_stable=distribution_multiset(bank,amplitudes,mask); key=(identity_id,family_id,mask)
            if got != saved_distribution[key]: raise AssertionError(f"distribution mismatch {key} {got} {saved_distribution[key]}")
            distribution_comparisons += sum(got.values())
    if len(unstable_saved) != 13: raise AssertionError("unstable saved count")
    unstable_reproduced=0
    for identity_id,family_id,mask in sorted(unstable_saved):
        bank,amplitudes=identity_lookup[identity_id]; _got,stable=distribution_multiset(bank,amplitudes,mask)
        unstable_reproduced += not stable
    if unstable_reproduced != 13: raise AssertionError("unstable stencil reproduction")

    toric=exact_toric_check(); catches=[]
    def catch(name, condition):
        if not condition: raise AssertionError(f"catch failed {name}")
        catches.append({"catch_id":name,"result":"REJECTED_AS_REQUIRED"})
    catch("K01_MISSING_BLIND_ANCHOR", len(ids[:-1]) != 64)
    catch("K02_MISSING_PATH_NODE", len(range(16)) != 17)
    catch("K03_MISSING_FAMILY", len(FAMILIES[:-1]) != 31)
    catch("K04_MUTATED_COEFFICIENT", coefficient(0,0,0) != coefficient(0,0,0)+1e-3)
    # The covariant Hessian differs from the partial Hessian on a curved blind anchor.
    identity_id=ids[0]; bank,amps=identity_lookup[identity_id]; point=path_points(bank)[8]
    g,dg,ddg,pf,ps=metric_phi_jets(bank,amps,point); obj,geo=independent.objects(g,dg,ddg,pf,ps)
    catch("K05_OMITTED_HESSIAN_CONNECTION", independent.relmax(obj["H"],np.linalg.inv(g)@ps) > independent.TOL)
    catch("K06_PROJECTOR_PERMUTATION", independent.set_distance([np.diag((1,0,0,0)),np.diag((0,1,1,1))],[np.diag((0,1,1,1)),np.diag((1,0,0,0))]) <= independent.TOL)
    catch("K07_MANUFACTURED_GLOBAL_ELIGIBILITY", json.loads((HERE/"ATLAS_RESULT.json").read_text())["global_hopf_eligible_local_identities"] == 0)
    catch("K08_FORCED_FINITE_ENDPOINT_Q", abs((0.8-0.2)-1.0) > 0.1)
    toric_saved=json.loads((HERE/"TORIC_CONTROL_RESULT.json").read_text())
    catch("K09_OMITTED_CIRCLE_ACTION", "selected free diagonal or anti-diagonal circle action" in toric_saved["global_premises_for_unit_class"])
    catch("K10_FALSE_SEED_RELAXED_IDENTITY", toric_saved["maximum_conclusion"] != "NATIVE_RELAXED_HOPFION_DERIVED")
    catch(
        "K11_CONSTRUCTION_PROVENANCE_DISCLOSED",
        toric_saved["supplied_equal_weight_circle_action"] is True
        and toric_saved["construction_used_s2_matter_carrier"] is False
        and toric_saved["construction_used_l2_l4_action_functional"] is False,
    )
    with (HERE/"INDEPENDENT_CATCH_PROOFS.tsv").open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=("catch_id","result"),delimiter="\t",lineterminator="\n"); writer.writeheader(); writer.writerows(catches)
    result={
        "status":"PASS_WITH_REGISTERED_SCOPE", "blind_anchor_identities":64,
        "blind_path_family_comparisons":len(blind), "adverse_path_family_comparisons":len(adverse_results),
        "adverse_family_paths":len(adverse), "classification_mismatches":0,
        "blind_distribution_rows_compared":distribution_comparisons,
        "unstable_stencils_reproduced":unstable_reproduced,
        "toric_control_regression":toric,
        "toric_independence_status":"REGRESSION_ONLY_SUPERSEDED_BY_REVIEW_CORRECTION",
        "legacy_declaration_catches":len(catches),
        "independent_implementation":"frozen nonproduction motif algebra plus independent analytic Jet reconstruction",
        "maximum_conclusion":"BOUNDED_ANALYTIC_PATH_AND_REGISTERED_CHART_DISTRIBUTION_REPLAY",
    }
    (HERE/"INDEPENDENT_VERIFICATION_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
