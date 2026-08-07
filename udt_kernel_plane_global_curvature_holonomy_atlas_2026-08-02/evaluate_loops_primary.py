#!/usr/bin/env python3
"""Primary preregistered high-precision finite-loop atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import mpmath as mp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PANELS = (256, 512, 1024, 2048)
OWNERS = ("C04", "C08", "C09", "C10")
CONTROLS = (("C16", "C08", 4), ("C17", "C08", 5))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_tsv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_sources():
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == len({row["path"] for row in rows}) == 114
    for row in rows:
        content = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT,
            capture_output=True, check=True,
        ).stdout
        assert len(content) == int(row["bytes"])
        assert digest(content) == row["sha256"]
    assert digest((HERE / "SOURCE_MANIFEST.tsv").read_bytes()) == (HERE / "SOURCE_MANIFEST.sha256").read_text().strip()


def stereo_path(loop_id, radius, t):
    c, s = mp.cos(t), mp.sin(t)
    if loop_id == "R01":
        x, y, z = radius * c, radius * s, mp.mpf("0")
        dx, dy, dz = -radius * s, radius * c, mp.mpf("0")
    elif loop_id == "R02":
        x, y, z = radius * c, radius * s, mp.mpf("2")
        dx, dy, dz = -radius * s, radius * c, mp.mpf("0")
    elif loop_id == "R03":
        x, y, z = 1 + radius * c, radius * s, mp.mpf("0")
        dx, dy, dz = -radius * s, radius * c, mp.mpf("0")
    elif loop_id == "R04":
        x, y, z = -1 + radius * c, radius * s, mp.mpf("0")
        dx, dy, dz = -radius * s, radius * c, mp.mpf("0")
    elif loop_id == "R05":
        x, y, z = radius * s, 1 + radius * c, mp.mpf("0")
        dx, dy, dz = radius * c, -radius * s, mp.mpf("0")
    elif loop_id == "R06":
        x, y, z = radius * s, -1 + radius * c, mp.mpf("0")
        dx, dy, dz = radius * c, -radius * s, mp.mpf("0")
    else:
        raise ValueError(loop_id)
    radius_squared = x*x + y*y + z*z
    denominator = 1 + radius_squared
    d_radius_squared = 2 * (x*dx + y*dy + z*dz)
    q = (
        (1 - radius_squared) / denominator,
        2*x / denominator,
        2*y / denominator,
        2*z / denominator,
    )
    dq = (
        -2*d_radius_squared / denominator**2,
        2*(dx*denominator - x*d_radius_squared) / denominator**2,
        2*(dy*denominator - y*d_radius_squared) / denominator**2,
        2*(dz*denominator - z*d_radius_squared) / denominator**2,
    )
    return q, dq


def pole_path(loop_id, delta, t):
    epsilon = mp.mpf(1) / 10
    cap = mp.sqrt(1 - epsilon**2)
    c, s = mp.cos(t), mp.sin(t)
    prefix, number = loop_id[:2], int(loop_id[2:])
    pole_sign = 1 if prefix == "PN" else -1
    if number == 1:
        v, dv = (cap, epsilon*c, epsilon*s), (0, -epsilon*s, epsilon*c)
    elif number == 2:
        v, dv = (-cap, epsilon*c, epsilon*s), (0, -epsilon*s, epsilon*c)
    elif number == 3:
        v, dv = (epsilon*c, cap, epsilon*s), (-epsilon*s, 0, epsilon*c)
    elif number == 4:
        v, dv = (epsilon*c, -cap, epsilon*s), (-epsilon*s, 0, epsilon*c)
    elif number == 5:
        v, dv = (epsilon*c, epsilon*s, cap), (-epsilon*s, epsilon*c, 0)
    else:
        raise ValueError(loop_id)
    q = (delta*v[0], delta*v[1], delta*v[2], pole_sign*mp.sqrt(1-delta**2))
    dq = (delta*dv[0], delta*dv[1], delta*dv[2], mp.mpf("0"))
    return q, dq


def connection_integrand(candidate_id, a, q, dq):
    q0, q1, q2, q3 = q
    f12 = q0*q1*q1 + 3*q0*q2*q2 + 2*q1*q2*q3
    f13 = q0*q0*q1 + 3*q0*q2*q3 - 2*q1*q2*q2
    f23 = 3*q0*q0*q2 - q0*q1*q3 + 2*q1*q1*q2
    u = 3 + q0*q0 + 2*q1*q1 + 4*q2*q2 + 8*q3*q3
    v = 1 + (q0*q0 + 3*q1*q1 + 7*q2*q2 + 9*q3*q3) / 10
    if candidate_id == "C04":
        area, r, b = v, mp.mpf(1), mp.mpf(0)
    else:
        lam = {"C08": 0, "C09": -1, "C10": 1}[candidate_id]
        area = u**lam * v
        r = 1 + (2*q0*q0 + 5*q1*q1 + 11*q2*q2 + 13*q3*q3) / 10
        b = (q0*q1 + 2*q0*q2 + 3*q0*q3 + 5*q1*q2 + 7*q1*q3 + 11*q2*q3) / 10
    S = u*f12*f12 + area*((b*f13-r*f23)**2 + f13*f13/(r*r))
    P = u*S
    sigma1 = q0*dq[1] - q1*dq[0] + q3*dq[2] - q2*dq[3]
    sigma2 = q0*dq[2] - q2*dq[0] - q3*dq[1] + q1*dq[3]
    return -a * (f13*sigma1 + f23*sigma2) / mp.sqrt(P)


def trapezoid(candidate_id, a, path_function, path_value, panels, reverse=False):
    step = 2*mp.pi/panels
    sign = -1 if reverse else 1
    values = []
    for index in range(panels):
        t = sign * index * step
        q, dq = path_function(path_value, t)
        dq = tuple(sign * value for value in dq)
        values.append(connection_integrand(candidate_id, a, q, dq))
    return step * mp.fsum(values)


def main():
    mp.mp.dps = 100
    verify_sources()
    loop_rows = read_tsv(HERE / "LOOP_FAMILY_UNIVERSE.tsv")
    assert len(loop_rows) == 16
    geometric_loops = []
    for row in loop_rows:
        loop_id = row["loop_id"]
        if loop_id.startswith("R"):
            for value in (mp.mpf(1)/100, mp.mpf(1)/20, mp.mpf(1)/10):
                geometric_loops.append((loop_id, "rho", value, lambda v, t, lid=loop_id: stereo_path(lid, v, t)))
        else:
            for value in (mp.mpf(1)/20, mp.mpf(1)/10):
                geometric_loops.append((loop_id, "delta", value, lambda v, t, lid=loop_id: pole_path(lid, v, t)))
    assert len(geometric_loops) == 38

    configurations = [(owner, owner, 1, "PRIMARY_OWNER") for owner in OWNERS]
    configurations.extend((control, parent, a, "TWIST_SCALING_CONTROL") for control, parent, a in CONTROLS)
    rows = []
    for output_id, profile_id, a, role in configurations:
        for loop_id, parameter_name, value, path_function in geometric_loops:
            estimates = [trapezoid(profile_id, a, path_function, value, panels) for panels in PANELS]
            difference = abs(estimates[-1] - estimates[-2])
            threshold = max(mp.mpf("1e-70"), mp.mpf("1e-65")*abs(estimates[-1]))
            reverse = trapezoid(profile_id, a, path_function, value, PANELS[-1], reverse=True)
            reversal_error = abs(reverse + estimates[-1])
            rows.append({
                "candidate_id": output_id,
                "profile_id": profile_id,
                "role": role,
                "a": str(a),
                "loop_id": loop_id,
                "parameter_name": parameter_name,
                "parameter_value": mp.nstr(value, 30),
                "H_256": mp.nstr(estimates[0], 105),
                "H_512": mp.nstr(estimates[1], 105),
                "H_1024": mp.nstr(estimates[2], 105),
                "H_2048": mp.nstr(estimates[3], 105),
                "convergence_difference": mp.nstr(difference, 105),
                "convergence_threshold": mp.nstr(threshold, 105),
                "orientation_reverse_H_2048": mp.nstr(reverse, 105),
                "orientation_reversal_error": mp.nstr(reversal_error, 105),
                "status": "PASS_PRIMARY" if difference <= threshold and reversal_error <= threshold else "UNRESOLVED_NUMERICAL",
            })
        print(f"complete {output_id} loops={len(geometric_loops)}", flush=True)

    assert len(rows) == 228
    target = HERE / "FINITE_LOOP_PRIMARY.tsv"
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    result = {
        "schema": "udt-finite-loop-primary-1.0",
        "status": "PASS" if all(row["status"] == "PASS_PRIMARY" for row in rows) else "UNRESOLVED_NUMERICAL",
        "mpmath_version": mp.__version__,
        "dps": mp.mp.dps,
        "panels": list(PANELS),
        "geometric_loops": len(geometric_loops),
        "primary_owner_integrals": 152,
        "twist_control_integrals": 76,
        "total_integrals": len(rows),
        "exact_twist_scaling_identity": "omega(a)=a*omega(1); Omega(a)=a*Omega(1)",
        "output_sha256": digest(target.read_bytes()),
    }
    (HERE / "FINITE_LOOP_PRIMARY_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
