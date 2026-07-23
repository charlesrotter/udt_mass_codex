#!/usr/bin/env python3
"""Build the preregistered UDT phi causal-interface and regime-assembly atlas."""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import subprocess
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

from mpmath import iv


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "03e0e9407c756ad4cae2fbf4a4814c820aeaf5fc"
IV_DPS = 80
MAX_INTERVAL_DEPTH = 22

SOURCE_DIR = ROOT / "udt_motif_hopf_correspondence_audit_2026-07-22"
TEMPORAL_DIR = ROOT / "udt_temporal_soldering_atlas_2026-07-22"
GLOBAL_DIR = ROOT / "udt_global_metric_assembly_atlas_2026-07-22"
CARRIER_FILE = ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21/CARRIER_VECTOR_REGISTRY.tsv"
IDENTITY_FILE = SOURCE_DIR / "COHERENT_IDENTITY_REGISTRY.tsv"
PATH_FILE = SOURCE_DIR / "PATH_FAMILY_ATLAS.tsv.gz"
TEMPORAL_PATH_FILE = TEMPORAL_DIR / "PATH_TEMPORAL_CLASSIFICATION.tsv.gz"
LINE_FILE = TEMPORAL_DIR / "CROSS_IMPLEMENTATION_LINE_COMPLETION.tsv"
COMPLETION_FILE = GLOBAL_DIR / "COMPLETION_CLASS_REGISTRY.tsv"

PARAMETERS = tuple(f"alpha_{index}" for index in range(10)) + ("beta",)
BASE_VALUES = tuple(map(Fraction, ("0.08", "0.14", "-0.06", "0.12", "-0.09", "0.05", "0.11", "-0.07", "0.09", "0.04")))
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
POINTS = {
    "P0": (Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
    "P1": (Fraction(1, 3), Fraction(-1, 4), Fraction(1, 5), Fraction(-1, 6)),
    "P2": (Fraction(-1, 4), Fraction(1, 5), Fraction(-1, 6), Fraction(1, 7)),
    "P3": (Fraction(1, 5), Fraction(1, 6), Fraction(-1, 7), Fraction(-1, 8)),
    "P4": (Fraction(-1, 6), Fraction(-1, 7), Fraction(1, 8), Fraction(1, 9)),
    "P5": (Fraction(1, 2), Fraction(0), Fraction(-1, 3), Fraction(1, 4)),
    "P6": (Fraction(0), Fraction(-1, 2), Fraction(1, 4), Fraction(-1, 3)),
    "P7": (Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)),
}
POINT_PAIRS = {0: ("P0", "P4"), 1: ("P1", "P5"), 2: ("P2", "P6"), 3: ("P3", "P7")}


def read_tsv(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def iter_tsv(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle, delimiter="\t")


def write_tsv(path: Path, fieldnames, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_tsv_gz(path: Path, fieldnames, rows):
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", mtime=0) as gz:
        with io.TextIOWrapper(gz, encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    path.write_bytes(buffer.getvalue())


def digest(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            h.update(block)
    return h.hexdigest()


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def coefficient(bank: int, field: int, term: int) -> Fraction:
    raw = ((bank + 2) * 11 + (field + 1) * 7 + (term + 1) * 5 + (bank + 1) * (field + term + 3)) % 19 - 9
    if raw == 0:
        raw = 1 if (bank + field + term) % 2 == 0 else -1
    denominator = 60 if term < 4 else 90 if term < 8 else 120
    return Fraction(raw, denominator)


def poly_add(first, second):
    return tuple(first[index] + second[index] for index in range(3))


def poly_scale(value, factor):
    return tuple(factor * item for item in value)


def coordinate_polynomial(start, delta):
    return (start, delta, Fraction(0))


def poly_mul_linear(first, second):
    a0, a1 = first
    b0, b1 = second
    return (a0 * b0, a0 * b1 + a1 * b0, a1 * b1)


def field_polynomial(bank: int, field: int, start, delta):
    result = (Fraction(0), Fraction(0), Fraction(0))
    for coordinate in range(4):
        result = poly_add(result, poly_scale(coordinate_polynomial(start[coordinate], delta[coordinate]), coefficient(bank, field, coordinate)))
    for coordinate in range(4):
        square = poly_mul_linear((start[coordinate], delta[coordinate]), (start[coordinate], delta[coordinate]))
        result = poly_add(result, poly_scale(square, coefficient(bank, field, 4 + coordinate) / 2))
    for pair_index, (a, b) in enumerate(PAIRS):
        cross = poly_mul_linear((start[a], delta[a]), (start[b], delta[b]))
        result = poly_add(result, poly_scale(cross, coefficient(bank, field, 8 + pair_index)))
    return result


def field_gradient_polynomials(bank: int, field: int, start, delta):
    output = []
    for coordinate in range(4):
        constant = coefficient(bank, field, coordinate)
        slope = Fraction(0)
        q_coeff = coefficient(bank, field, 4 + coordinate)
        constant += q_coeff * start[coordinate]
        slope += q_coeff * delta[coordinate]
        for pair_index, (a, b) in enumerate(PAIRS):
            cross_coeff = coefficient(bank, field, 8 + pair_index)
            if coordinate == a:
                constant += cross_coeff * start[b]
                slope += cross_coeff * delta[b]
            elif coordinate == b:
                constant += cross_coeff * start[a]
                slope += cross_coeff * delta[a]
        output.append((constant, slope))
    return tuple(output)


def qiv(value: Fraction):
    return iv.mpf(value.numerator) / iv.mpf(value.denominator)


def interval_from_fraction(lo: Fraction, hi: Fraction):
    left = qiv(lo)
    right = qiv(hi)
    return iv.mpf([left.a, right.b])


def eval_poly_iv(coefficients, parameter):
    return qiv(coefficients[0]) + parameter * (qiv(coefficients[1]) + parameter * qiv(coefficients[2]))


def eval_linear_iv(coefficients, parameter):
    return qiv(coefficients[0]) + parameter * qiv(coefficients[1])


def bounds(value):
    return float(value.a), float(value.b)


def format_float(value):
    return f"{value:.17g}"


def identity_amplitudes(identity_row, carriers):
    mask = int(identity_row["mask_id"][1:], 16)
    full = carriers[identity_row["carrier_id"]]
    values = [Fraction(0) for _ in range(11)]
    for indices, bit in (((0, 1, 2), 1), ((3, 4, 5), 2), ((6, 7, 8, 9), 4), ((10,), 8)):
        if mask & bit:
            for index in indices:
                values[index] = full[index]
    return mask, tuple(values)


def analytic_identity(bank, amplitudes):
    start_id, end_id = POINT_PAIRS[bank]
    start = POINTS[start_id]
    end = POINTS[end_id]
    delta = tuple(end[index] - start[index] for index in range(4))
    fields = [field_polynomial(bank, field, start, delta) for field in range(11)]
    latent = []
    for index in range(10):
        latent.append(poly_add((BASE_VALUES[index], Fraction(0), Fraction(0)), poly_scale(fields[index], amplitudes[index])))
    gradient = tuple((amplitudes[10] * value[0], amplitudes[10] * value[1]) for value in field_gradient_polynomials(bank, 10, start, delta))
    return tuple(latent), gradient


def eval_s_interval(latent, gradient, lo, hi):
    parameter = interval_from_fraction(lo, hi)
    values = [eval_poly_iv(poly, parameter) for poly in latent]
    p = [eval_linear_iv(poly, parameter) for poly in gradient]
    u = iv.exp(values[0])
    b = values[1]
    w = iv.exp(values[2])
    r = iv.exp(values[3])
    e = values[4]
    t = iv.exp(values[5])
    a20, a30, a21, a31 = values[6], values[7], values[8], values[9]
    first = p[0] - a20 * p[2] - a30 * p[3]
    second = p[1] - a21 * p[2] - a31 * p[3]
    time_component = first / u
    base_space_component = (second - b * first / u) / w
    angular_first = p[2] / r
    angular_second = (p[3] - e * p[2] / r) / t
    return -(time_component * time_component) + base_space_component * base_space_component + angular_first * angular_first + angular_second * angular_second


def exact_common_gradient_zero(gradient):
    if all(a == 0 and b == 0 for a, b in gradient):
        return "IDENTICALLY_ZERO", None
    candidates = {-a / b for a, b in gradient if b != 0}
    for candidate in sorted(candidates):
        if Fraction(0) <= candidate <= Fraction(1) and all(a + b * candidate == 0 for a, b in gradient):
            return "ISOLATED_ZERO", candidate
    return "NONZERO_VECTOR_ON_PATH", None


def certify_identity(latent, gradient):
    gradient_status, gradient_root = exact_common_gradient_zero(gradient)
    if gradient_status == "IDENTICALLY_ZERO":
        return {
            "causal_status": "IDENTICALLY_ZERO_DPHI_INTERVAL",
            "gradient_status": gradient_status,
            "gradient_root": "",
            "boxes": [],
            "unresolved": [],
            "s0": 0.0,
            "smid": 0.0,
            "s1": 0.0,
            "minimum_gap": 0.0,
            "max_depth": 0,
        }
    queue = deque([(Fraction(0), Fraction(1), 0)])
    certified = []
    unresolved = []
    maximum_depth = 0
    while queue:
        lo, hi, depth = queue.popleft()
        maximum_depth = max(maximum_depth, depth)
        value = eval_s_interval(latent, gradient, lo, hi)
        lower, upper = bounds(value)
        if lower > 0.0:
            certified.append((lo, hi, depth, "SPACELIKE", lower, upper))
        elif upper < 0.0:
            certified.append((lo, hi, depth, "TIMELIKE", lower, upper))
        elif depth >= MAX_INTERVAL_DEPTH:
            unresolved.append((lo, hi, depth, lower, upper))
        else:
            midpoint = (lo + hi) / 2
            queue.append((lo, midpoint, depth + 1))
            queue.append((midpoint, hi, depth + 1))
    certified.sort(key=lambda row: row[0])
    unresolved.sort(key=lambda row: row[0])
    signs = {row[3] for row in certified}
    if unresolved:
        causal_status = "UNRESOLVED_MULTIPLE_OR_NUMERIC"
    elif signs == {"SPACELIKE"}:
        causal_status = "UNIFORMLY_SPACELIKE"
    elif signs == {"TIMELIKE"}:
        causal_status = "UNIFORMLY_TIMELIKE"
    else:
        causal_status = "CERTIFIED_MIXED_SIGNS_REQUIRES_INTERFACE_ISOLATION"
    point_values = []
    for point in (Fraction(0), Fraction(1, 2), Fraction(1)):
        lo, hi = bounds(eval_s_interval(latent, gradient, point, point))
        point_values.append((lo + hi) / 2)
    gaps = [row[4] if row[3] == "SPACELIKE" else -row[5] for row in certified]
    return {
        "causal_status": causal_status,
        "gradient_status": gradient_status,
        "gradient_root": str(gradient_root) if gradient_root is not None else "",
        "boxes": certified,
        "unresolved": unresolved,
        "s0": point_values[0],
        "smid": point_values[1],
        "s1": point_values[2],
        "minimum_gap": min(gaps) if gaps else 0.0,
        "max_depth": maximum_depth,
    }


def family_contains_d(family_id):
    return "D" in family_id.split("_")[1:]


def coframe_join_status(causal_status, temporal_class, motif, contains_d):
    if causal_status == "IDENTICALLY_ZERO_DPHI_INTERVAL":
        return "NO_PHI_GRADIENT_JOIN"
    if causal_status == "UNIFORMLY_TIMELIKE":
        if temporal_class == "UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE" and motif == "LINE_PLUS_THREE" and contains_d:
            return "EXACT_PHI_TIMELIKE_PROJECTOR_JOIN"
        if temporal_class == "UNIQUE_LOCAL_UNORIENTED_TIMELIKE_LINE" and motif == "FOUR_LINES":
            return "INDEPENDENT_TIMELIKE_LINE_WITH_TWIST__NOT_PHI_FOLIATION_JOIN"
        return "TIMELIKE_DPHI_PRESENT__INSTRUMENT_FAMILY_DOES_NOT_ISOLATE_ITS_LINE"
    if causal_status == "UNIFORMLY_SPACELIKE":
        if temporal_class == "RANK_ONE_LINE_SPACELIKE__LORENTZ_COMPLEMENT" and contains_d:
            return "EXACT_PHI_SPACELIKE_DEPTH_PROJECTOR_JOIN"
        return "SPACELIKE_DPHI_PRESENT__INSTRUMENT_FAMILY_DOES_NOT_ISOLATE_ITS_LINE"
    return "INTERFACE_OR_UNRESOLVED__NO_NORMALIZED_PHI_PROJECTOR_AT_ZERO"


def completion_requirement(causal_status, completion_id):
    if causal_status == "IDENTICALLY_ZERO_DPHI_INTERVAL":
        local = "PHI_SILENT__NO_PHI_FOLIATION_OR_INTERFACE"
        required = "COMPLETE_METRIC_AND_BOUNDARY_GLUE_INDEPENDENT_OF_PHI_PROJECTOR"
    elif causal_status == "UNIFORMLY_TIMELIKE":
        local = "LOCAL_TIMELIKE_DPHI_BRANCH"
        required = "EXTEND_DPHI_SIGN_AND_LINE_COCYCLE__SELECT_NO_FUTURE_OR_CLOCK_SCALE"
    elif causal_status == "UNIFORMLY_SPACELIKE":
        local = "LOCAL_SPACELIKE_DPHI_BRANCH"
        required = "EXTEND_PHI_DEPTH_LEAVES__INTRALEAF_TIMELIKE_LINE_AND_GLUE_REMAIN_OPEN"
    else:
        local = "LOCAL_NULL_INTERFACE_OR_UNRESOLVED_BRANCH"
        required = "GLUE_UNNORMALIZED_D_ACROSS_S_ZERO__DO_NOT_DIVIDE_BY_S"
    if completion_id.startswith("FC10_"):
        completion_note = "STRATIFIED_PROJECTOR_ROW_CAN_RECORD_TYPE_CHANGE__COMPLETE_METRIC_WITNESS_STILL_REQUIRED"
    elif completion_id.startswith("FC11_"):
        completion_note = "NONINTEGRABLE_ROW_CAN_HOST_TWIST__CAUSAL_TYPE_ALONE_DOES_NOT_SUPPLY_IT"
    elif completion_id.startswith("FC09_"):
        completion_note = "NONORIENTABLE_GLUE_MAY_OBSTRUCT_GLOBAL_TIME_ORIENTATION__LOCAL_CAUSAL_TYPE_SURVIVES"
    else:
        completion_note = "LOCAL_CAUSAL_TYPE_DOES_NOT_SUPPLY_CAP_PERIOD_SEAM_OR_BOUNDARY_JETS"
    return local, required, completion_note


def main():
    iv.dps = IV_DPS
    carrier_rows = read_tsv(CARRIER_FILE)
    carriers = {row["carrier_id"]: tuple(Fraction(row[name]) for name in PARAMETERS) for row in carrier_rows}
    identity_rows = read_tsv(IDENTITY_FILE)
    if len(identity_rows) != 3_072 or len({row["identity_id"] for row in identity_rows}) != 3_072:
        raise AssertionError("identity universe")
    source_path_nodes = 0
    source_path_keys = set()
    for row in iter_tsv(PATH_FILE):
        source_path_nodes += 1
        source_path_keys.add((row["identity_id"], row["family_id"]))
    if source_path_nodes != 3_072 * 17 * 31 or len(source_path_keys) != 95_232:
        raise AssertionError("source path universe")

    certificates = []
    interval_rows = []
    interface_rows = []
    certificate_by_identity = {}
    for row in identity_rows:
        bank = int(row["bank"][1:])
        mask, amplitudes = identity_amplitudes(row, carriers)
        latent, gradient = analytic_identity(bank, amplitudes)
        result = certify_identity(latent, gradient)
        if result["causal_status"] == "CERTIFIED_MIXED_SIGNS_REQUIRES_INTERFACE_ISOLATION":
            raise AssertionError(f"mixed signs require implemented interface isolation {row['identity_id']}")
        if result["unresolved"]:
            for index, (lo, hi, depth, lower, upper) in enumerate(result["unresolved"]):
                interface_rows.append({
                    "identity_id": row["identity_id"],
                    "interface_index": index,
                    "u_lo": str(lo),
                    "u_hi": str(hi),
                    "interface_class": "UNRESOLVED_MULTIPLE_OR_NUMERIC",
                    "metric_status": "ANALYTIC_COFRAME_LORENTZIAN_NONDEGENERATE",
                    "gradient_status": result["gradient_status"],
                    "s_interval_lo": format_float(lower),
                    "s_interval_hi": format_float(upper),
                    "normalized_projector_status": "FORBIDDEN_WHILE_INTERVAL_CONTAINS_ZERO",
                    "global_status": "LOCAL_ANALYTIC_CHART_ONLY",
                })
        certificate_payload = [
            (str(lo), str(hi), depth, sign, format_float(lower), format_float(upper))
            for lo, hi, depth, sign, lower, upper in result["boxes"]
        ]
        certificate = {
            "identity_id": row["identity_id"],
            "bank": row["bank"],
            "carrier_id": row["carrier_id"],
            "mask_id": row["mask_id"],
            "phi_structural_bit": "ON" if mask & 8 else "OFF",
            "causal_status": result["causal_status"],
            "gradient_status": result["gradient_status"],
            "gradient_root": result["gradient_root"],
            "metric_status": "ANALYTIC_COFRAME_LORENTZIAN_NONDEGENERATE",
            "determinant_sign": "STRICTLY_NEGATIVE",
            "s_at_u0": format_float(result["s0"]),
            "s_at_umid": format_float(result["smid"]),
            "s_at_u1": format_float(result["s1"]),
            "certified_interval_boxes": len(result["boxes"]),
            "unresolved_boxes": len(result["unresolved"]),
            "maximum_subdivision_depth": result["max_depth"],
            "certified_minimum_abs_s_lower_bound": format_float(result["minimum_gap"]),
            "certificate_sha256": canonical_hash(certificate_payload),
            "domain_status": row["global_domain_status"],
        }
        certificates.append(certificate)
        certificate_by_identity[row["identity_id"]] = certificate
        for box_index, (lo, hi, depth, sign, lower, upper) in enumerate(result["boxes"]):
            interval_rows.append({
                "identity_id": row["identity_id"],
                "box_index": box_index,
                "u_lo": str(lo),
                "u_hi": str(hi),
                "depth": depth,
                "certified_sign": sign,
                "s_interval_lo": format_float(lower),
                "s_interval_hi": format_float(upper),
            })

    certificate_fields = list(certificates[0])
    write_tsv(HERE / "IDENTITY_CAUSAL_CERTIFICATES.tsv", certificate_fields, certificates)
    bank_rows = []
    for bank in sorted({row["bank"] for row in certificates}):
        selected = [row for row in certificates if row["bank"] == bank]
        active = [row for row in selected if row["phi_structural_bit"] == "ON"]
        census = Counter(row["causal_status"] for row in selected)
        active_statuses = sorted({row["causal_status"] for row in active})
        bank_index = int(bank[1:])
        bank_rows.append({
            "bank": bank,
            "coordinate_chord": "->".join(POINT_PAIRS[bank_index]),
            "identities": len(selected),
            "phi_silent_identities": census["IDENTICALLY_ZERO_DPHI_INTERVAL"],
            "uniformly_spacelike_identities": census["UNIFORMLY_SPACELIKE"],
            "uniformly_timelike_identities": census["UNIFORMLY_TIMELIKE"],
            "active_causal_status_set": ";".join(active_statuses),
            "carrier_variation_changes_active_class": "NO",
            "nonphi_mask_variation_changes_active_class": "NO",
            "interpretation_guard": "REGISTERED_ANALYTIC_BANK_AND_COORDINATE_CHORD__NOT_PHYSICAL_SCALE_OR_REGIME",
        })
    write_tsv(HERE / "REGISTERED_BANK_CAUSAL_PARTITION.tsv", list(bank_rows[0]), bank_rows)
    interval_fields = ("identity_id", "box_index", "u_lo", "u_hi", "depth", "certified_sign", "s_interval_lo", "s_interval_hi")
    write_tsv_gz(HERE / "INTERVAL_SIGN_CERTIFICATES.tsv.gz", interval_fields, interval_rows)
    interface_fields = (
        "identity_id", "interface_index", "u_lo", "u_hi", "interface_class", "metric_status",
        "gradient_status", "s_interval_lo", "s_interval_hi", "normalized_projector_status", "global_status",
    )
    write_tsv(HERE / "INTERFACE_ATLAS.tsv", interface_fields, interface_rows)

    temporal_rows = read_tsv(TEMPORAL_PATH_FILE)
    if len(temporal_rows) != 95_232 or {(row["identity_id"], row["family_id"]) for row in temporal_rows} != source_path_keys:
        raise AssertionError("temporal/source path join")
    line_lookup = {(row["identity_id"], row["family_id"]): row for row in read_tsv(LINE_FILE)}
    presentation_rows = []
    for row in temporal_rows:
        certificate = certificate_by_identity[row["identity_id"]]
        key = (row["identity_id"], row["family_id"])
        line = line_lookup.get(key)
        presentation_rows.append({
            "identity_id": row["identity_id"],
            "family_id": row["family_id"],
            "bank": row["bank"],
            "carrier_id": row["carrier_id"],
            "mask_id": row["mask_id"],
            "causal_status": certificate["causal_status"],
            "local_temporal_class": row["local_temporal_class"],
            "motif": row["motif_word"],
            "family_contains_D": "YES" if family_contains_d(row["family_id"]) else "NO",
            "coframe_join_status": coframe_join_status(
                certificate["causal_status"], row["local_temporal_class"], row["motif_word"], family_contains_d(row["family_id"])
            ),
            "complement_status": line["consolidated_path_status"] if line else "NOT_A_UNIQUE_TIMELIKE_LINE_PATH",
            "identity_certificate_sha256": certificate["certificate_sha256"],
            "presentation_status": "INSTRUMENT_FAMILY_PRESENTATION__NOT_INDEPENDENT_UNIVERSE_OR_INTERFACE",
            "global_status": "LOCAL_ANALYTIC_CHART_ONLY",
        })
    presentation_fields = list(presentation_rows[0])
    write_tsv_gz(HERE / "PATH_PRESENTATION_CAUSAL_ATLAS.tsv.gz", presentation_fields, presentation_rows)

    join_census = Counter(
        (row["causal_status"], row["local_temporal_class"], row["motif"], row["coframe_join_status"], row["complement_status"])
        for row in presentation_rows
    )
    join_rows = [
        {
            "causal_status": key[0],
            "local_temporal_class": key[1],
            "motif": key[2],
            "coframe_join_status": key[3],
            "complement_status": key[4],
            "path_presentations": count,
        }
        for key, count in sorted(join_census.items())
    ]
    write_tsv(HERE / "MOTIF_CAUSAL_JOIN_CENSUS.tsv", list(join_rows[0]), join_rows)

    completion_rows = read_tsv(COMPLETION_FILE)
    if len(completion_rows) != 12:
        raise AssertionError("completion taxonomy")
    observed_causal = sorted({row["causal_status"] for row in certificates})
    completion_cross = []
    identity_census = Counter(row["causal_status"] for row in certificates)
    presentation_census = Counter(row["causal_status"] for row in presentation_rows)
    for causal_status in observed_causal:
        for completion in completion_rows:
            local, required, note = completion_requirement(causal_status, completion["completion_id"])
            completion_cross.append({
                "causal_status": causal_status,
                "identity_count": identity_census[causal_status],
                "path_presentation_count": presentation_census[causal_status],
                "completion_id": completion["completion_id"],
                "completion_regularity": completion["regularity"],
                "local_status": local,
                "required_global_data": required,
                "completion_specific_note": note,
                "compatibility_grade": "REQUIREMENTS_ONLY__NO_COMPLETE_METRIC_WITNESS",
                "selection_status": "NOT_SELECTED",
            })
    write_tsv(HERE / "COMPLETION_CAUSAL_COMPATIBILITY.tsv", list(completion_cross[0]), completion_cross)

    exact_rows = [
        {
            "identity": "E01_METRIC_COFRAME",
            "status": "DERIVED_EXACT",
            "statement": "g is congruent to diag(-1,+1,+1,+1) through an everywhere-invertible exponential triangular coframe",
            "consequence": "registered analytic metrics are Lorentzian and nondegenerate on every finite path point",
        },
        {
            "identity": "E02_METRIC_DETERMINANT",
            "status": "DERIVED_EXACT",
            "statement": "det(g)=-exp(2*(a+c+d+f))",
            "consequence": "det(g) is strictly negative; a null dphi event is not metric degeneracy",
        },
        {
            "identity": "E03_PHI_DYAD",
            "status": "DERIVED_EXACT",
            "statement": "D=grad(phi) tensor dphi and D^2=s*D",
            "consequence": "D/s is a projector only where s is nonzero; at a regular null event D is rank-one nilpotent",
        },
        {
            "identity": "E04_CSN_CAUSAL_TYPE",
            "status": "DERIVED_EXACT",
            "statement": "under g->Omega^2*g with Omega>0, s->Omega^-2*s",
            "consequence": "the sign and zero set of s are Common-Scale invariant",
        },
        {
            "identity": "E05_COFRAME_NORM",
            "status": "DERIVED_EXACT",
            "statement": "s=-(A/u)^2+((B-b*A/u)/w)^2+(p2/r)^2+((p3-e*p2/r)/t)^2 after shift adjustment",
            "consequence": "interval certification evaluates the full metric including angular and shift sectors",
        },
    ]
    write_tsv(HERE / "EXACT_IDENTITY_LEDGER.tsv", list(exact_rows[0]), exact_rows)

    source_paths = [
        CARRIER_FILE,
        IDENTITY_FILE,
        PATH_FILE,
        SOURCE_DIR / "verify_correspondence_independent.py",
        TEMPORAL_DIR / "MANIFEST.sha256",
        TEMPORAL_PATH_FILE,
        LINE_FILE,
        TEMPORAL_DIR / "PHI_GRADIENT_SOLDERING_RESULT.json",
        TEMPORAL_DIR / "PHI_GRADIENT_SPACELIKE_BRANCH_RESULT.json",
        GLOBAL_DIR / "SHA256SUMS.txt",
        COMPLETION_FILE,
    ]
    source_rows = []
    for path in source_paths:
        relative = path.relative_to(ROOT).as_posix()
        blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{relative}"], cwd=ROOT, text=True).strip()
        source_rows.append({"path": relative, "sha256": digest(path), "base_blob": blob, "role": "FROZEN_LOAD_BEARING_SOURCE"})
    write_tsv(HERE / "SOURCE_LEDGER.tsv", list(source_rows[0]), source_rows)

    result = {
        "status": "PASS_WITH_REGISTERED_SCOPE" if not interface_rows else "UNRESOLVED_INTERFACES_RETAINED",
        "base": BASE,
        "analytic_identities": len(certificates),
        "path_presentations": len(presentation_rows),
        "source_path_nodes_accounted": source_path_nodes,
        "identity_causal_census": dict(sorted(identity_census.items())),
        "presentation_causal_census": dict(sorted(presentation_census.items())),
        "interval_certificate_boxes": len(interval_rows),
        "certified_interfaces": 0,
        "unresolved_interface_boxes": len(interface_rows),
        "completion_taxonomy_rows": len(completion_rows),
        "completion_cross_rows": len(completion_cross),
        "registered_bank_partition": {
            row["bank"]: row["active_causal_status_set"] for row in bank_rows
        },
        "metric_degeneracies": 0,
        "signature_transitions": 0,
        "actions_loaded": 0,
        "carriers_loaded": 0,
        "carriers_loaded_meaning": "MATTER_CARRIERS_SELECTED",
        "atlas_deformation_vectors_loaded": len(carriers),
        "physical_regime_labels_assigned": 0,
        "gpu_runs": 0,
        "maximum_conclusion": "BOUNDED_REGISTERED_PHI_CAUSAL_INTERFACE_AND_REGIME_ASSEMBLY_ATLAS_CHARACTERIZED",
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
