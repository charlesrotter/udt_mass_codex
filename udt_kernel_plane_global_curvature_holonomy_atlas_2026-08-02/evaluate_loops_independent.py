#!/usr/bin/env python3
"""Independent tanh-sinh replay of one preregistered finite-loop configuration."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import mpmath as mp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONFIGURATIONS = {
    "C04": ("C04", 1), "C08": ("C08", 1), "C09": ("C09", 1), "C10": ("C10", 1),
    "C16": ("C08", 4), "C17": ("C08", 5),
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def table(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_gate():
    rows = table(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == len({r["path"] for r in rows}) == 114
    for row in rows:
        blob = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT,
            check=True, capture_output=True,
        ).stdout
        assert len(blob) == int(row["bytes"]) and sha256(blob) == row["sha256"]
    assert sha256((HERE / "SOURCE_MANIFEST.tsv").read_bytes()) == (HERE / "SOURCE_MANIFEST.sha256").read_text().strip()


def registered_path(loop_id, parameter):
    """Return q(t) only; tangent is independently complex-step differentiated."""
    if loop_id.startswith("R"):
        def path(t):
            cosine, sine = mp.cos(t), mp.sin(t)
            if loop_id == "R01": x, y, z = parameter*cosine, parameter*sine, 0
            elif loop_id == "R02": x, y, z = parameter*cosine, parameter*sine, 2
            elif loop_id == "R03": x, y, z = 1+parameter*cosine, parameter*sine, 0
            elif loop_id == "R04": x, y, z = -1+parameter*cosine, parameter*sine, 0
            elif loop_id == "R05": x, y, z = parameter*sine, 1+parameter*cosine, 0
            elif loop_id == "R06": x, y, z = parameter*sine, -1+parameter*cosine, 0
            else: raise ValueError(loop_id)
            squared = x*x+y*y+z*z
            divisor = 1+squared
            return ((1-squared)/divisor, 2*x/divisor, 2*y/divisor, 2*z/divisor)
        return path

    epsilon = mp.mpf("0.1")
    fixed = mp.sqrt(1-epsilon*epsilon)
    north = loop_id.startswith("PN")
    number = int(loop_id[2:])
    def path(t):
        cosine, sine = mp.cos(t), mp.sin(t)
        if number == 1: v = (fixed, epsilon*cosine, epsilon*sine)
        elif number == 2: v = (-fixed, epsilon*cosine, epsilon*sine)
        elif number == 3: v = (epsilon*cosine, fixed, epsilon*sine)
        elif number == 4: v = (epsilon*cosine, -fixed, epsilon*sine)
        elif number == 5: v = (epsilon*cosine, epsilon*sine, fixed)
        else: raise ValueError(loop_id)
        pole = mp.sqrt(1-parameter*parameter)
        return (parameter*v[0], parameter*v[1], parameter*v[2], pole if north else -pole)
    return path


def quaternion_product(left, right):
    a, b, c, d = left
    e, f, g, h = right
    return (
        a*e-b*f-c*g-d*h,
        a*f+b*e+c*h-d*g,
        a*g-b*h+c*e+d*f,
        a*h+b*g-c*f+d*e,
    )


def integrand(profile_id, twist, path, t):
    step = mp.mpf("1e-40")
    q = path(t)
    shifted = path(t + 1j*step)
    dq = tuple(mp.im(value)/step for value in shifted)
    qbar = (q[0], -q[1], -q[2], -q[3])
    maurer_cartan = quaternion_product(qbar, dq)

    q0, q1, q2, q3 = q
    f12 = q0*q1**2 + 3*q0*q2**2 + 2*q1*q2*q3
    f13 = q0**2*q1 + 3*q0*q2*q3 - 2*q1*q2**2
    f23 = 3*q0**2*q2 - q0*q1*q3 + 2*q1**2*q2
    depth = 3+q0**2+2*q1**2+4*q2**2+8*q3**2
    angular_base = 1+(q0**2+3*q1**2+7*q2**2+9*q3**2)/10
    if profile_id == "C04":
        angular, radial, shear = angular_base, mp.mpf(1), mp.mpf(0)
    else:
        exponent = {"C08": 0, "C09": -1, "C10": 1}[profile_id]
        angular = depth**exponent*angular_base
        radial = 1+(2*q0**2+5*q1**2+11*q2**2+13*q3**2)/10
        shear = (q0*q1+2*q0*q2+3*q0*q3+5*q1*q2+7*q1*q3+11*q2*q3)/10
    norm_squared = depth*f12**2 + angular*((shear*f13-radial*f23)**2+f13**2/radial**2)
    return -twist*(f13*maurer_cartan[1]+f23*maurer_cartan[2])/mp.sqrt(depth*norm_squared)


def integrate(profile_id, twist, path):
    cuts = [0, mp.pi/2, mp.pi, 3*mp.pi/2, 2*mp.pi]
    return mp.quadts(lambda t: integrand(profile_id, twist, path, t), cuts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True, choices=tuple(CONFIGURATIONS))
    args = parser.parse_args()
    mp.mp.dps = 120
    source_gate()
    profile_id, twist = CONFIGURATIONS[args.candidate]
    loop_definitions = table(HERE / "LOOP_FAMILY_UNIVERSE.tsv")
    loops = []
    for definition in loop_definitions:
        loop_id = definition["loop_id"]
        values = (mp.mpf("0.01"), mp.mpf("0.05"), mp.mpf("0.1")) if loop_id.startswith("R") else (mp.mpf("0.05"), mp.mpf("0.1"))
        parameter_name = "rho" if loop_id.startswith("R") else "delta"
        loops.extend((loop_id, parameter_name, value) for value in values)
    assert len(loops) == 38

    primary = table(HERE / "FINITE_LOOP_PRIMARY.tsv")
    primary_index = {(r["candidate_id"], r["loop_id"], r["parameter_value"]): r for r in primary}
    rows = []
    for loop_id, parameter_name, value in loops:
        path = registered_path(loop_id, value)
        result = integrate(profile_id, twist, path)
        reversed_result = integrate(profile_id, twist, lambda t, base=path: base(-t))
        key = (args.candidate, loop_id, mp.nstr(value, 30))
        primary_value = mp.mpf(primary_index[key]["H_2048"])
        difference = abs(result-primary_value)
        threshold = max(mp.mpf("1e-70"), mp.mpf("1e-65")*abs(primary_value))
        reversal_error = abs(reversed_result+result)
        rows.append({
            "candidate_id": args.candidate,
            "profile_id": profile_id,
            "a": str(twist),
            "loop_id": loop_id,
            "parameter_name": parameter_name,
            "parameter_value": mp.nstr(value, 30),
            "H_independent": mp.nstr(result, 125),
            "H_reverse_independent": mp.nstr(reversed_result, 125),
            "primary_difference": mp.nstr(difference, 125),
            "orientation_reversal_error": mp.nstr(reversal_error, 125),
            "agreement_threshold": mp.nstr(threshold, 125),
            "status": "PASS_INDEPENDENT" if difference <= threshold and reversal_error <= threshold else "UNRESOLVED_INDEPENDENT",
        })
        print(f"{args.candidate} {loop_id} {mp.nstr(value,5)} {rows[-1]['status']}", flush=True)

    target = HERE / f"FINITE_LOOP_INDEPENDENT_{args.candidate}.tsv"
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    result = {
        "schema": "udt-finite-loop-independent-1.0",
        "candidate_id": args.candidate,
        "status": "PASS" if all(r["status"] == "PASS_INDEPENDENT" for r in rows) else "UNRESOLVED_INDEPENDENT",
        "dps": mp.mp.dps,
        "quadrature": "mpmath_tanh_sinh",
        "tangent": "independent_complex_step_h=1e-40",
        "coframe": "vector_part(conjugate(q)*dq)",
        "loop_count": len(rows),
        "output_sha256": sha256(target.read_bytes()),
    }
    (HERE / f"FINITE_LOOP_INDEPENDENT_{args.candidate}_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
