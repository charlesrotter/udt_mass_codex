#!/usr/bin/env python3
"""Preregistered non-certifying numerical reconnaissance for curvature zeros."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy import __version__ as scipy_version
from scipy.optimize import least_squares


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OWNERS = ("C04", "C08", "C09", "C10")
SEED = 20260802
STARTS = 1024


def digest(data):
    return hashlib.sha256(data).hexdigest()


def records(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_sources():
    rows = records(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == len({row["path"] for row in rows}) == 114
    for row in rows:
        content = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT,
            capture_output=True, check=True,
        ).stdout
        assert len(content) == int(row["bytes"]) and digest(content) == row["sha256"]
    assert digest((HERE / "SOURCE_MANIFEST.tsv").read_bytes()) == (HERE / "SOURCE_MANIFEST.sha256").read_text().strip()


def fields(q):
    q0, q1, q2, q3 = q
    f12 = q0*q1**2+3*q0*q2**2+2*q1*q2*q3
    f13 = q0**2*q1+3*q0*q2*q3-2*q1*q2**2
    f23 = 3*q0**2*q2-q0*q1*q3+2*q1**2*q2
    d13 = 2*q0**2*q2+3*q0*q1*q3+2*q2**3+3*q2*q3**2
    d23 = 2*q0**2*q1+q0*q2*q3+2*q1**3-q1*q3**2
    x1 = np.array((-q1, q0, q3, -q2), dtype=np.result_type(q))
    x2 = np.array((-q2, -q3, q0, q1), dtype=np.result_type(q))
    # d12 is evaluated as X1(f23)-X2(f13) by complex step below.
    return f12, f13, f23, d13, d23, x1, x2


def profile_p(candidate, q):
    q0, q1, q2, q3 = q
    f12, f13, f23, _d13, _d23, _x1, _x2 = fields(q)
    u = 3+q0**2+2*q1**2+4*q2**2+8*q3**2
    v = 1+(q0**2+3*q1**2+7*q2**2+9*q3**2)/10
    if candidate == "C04":
        area, r, b = v, 1, 0
    else:
        area = u**{"C08": 0, "C09": -1, "C10": 1}[candidate]*v
        r = 1+(2*q0**2+5*q1**2+11*q2**2+13*q3**2)/10
        b = (q0*q1+2*q0*q2+3*q0*q3+5*q1*q2+7*q1*q3+11*q2*q3)/10
    S = u*f12**2+area*((b*f13-r*f23)**2+f13**2/r**2)
    return u*S


def directional_complex(function, q, vector):
    step = 1e-20
    return np.imag(function(q.astype(complex)+1j*step*vector))/step


def curvature(candidate, q):
    f12, f13, f23, d13, d23, x1, x2 = fields(q)
    x3 = np.array((-q[3], q[2], -q[1], q[0]), dtype=float)
    p = float(np.real(profile_p(candidate, q)))
    if not np.isfinite(p) or p <= 0:
        return np.full(3, 1e6)
    lp = []
    for vector in (x1, x2, x3):
        derivative = directional_complex(lambda value: profile_p(candidate, value), q, vector)
        lp.append(float(derivative/p))

    def f13_function(value): return fields(value)[1]
    def f23_function(value): return fields(value)[2]
    d12 = directional_complex(f23_function, q, x1)-directional_complex(f13_function, q, x2)
    root = np.sqrt(p)
    return -np.array((
        d12-0.5*(lp[0]*f23-lp[1]*f13),
        d13+0.5*lp[2]*f13,
        d23+0.5*lp[2]*f23,
    ), dtype=float)/root


def defect(q):
    f12, f13, f23, *_ = fields(q)
    return float(np.real(f12*f12+f13*f13+f23*f23))


def residual(candidate, q):
    return np.concatenate((curvature(candidate, q), [np.dot(q, q)-1]))


def same_antipodal(first, second):
    return min(np.linalg.norm(first-second), np.linalg.norm(first+second)) < 1e-7


def main():
    verify_sources()
    rng = np.random.default_rng(SEED)
    all_rows = []
    summary = {}
    for candidate in OWNERS:
        starts = rng.normal(size=(STARTS, 4))
        starts /= np.linalg.norm(starts, axis=1)[:, None]
        clusters = []
        accepted = 0
        for start in starts:
            fit = least_squares(
                lambda value: residual(candidate, value), start,
                max_nfev=3000, ftol=1e-13, xtol=1e-13, gtol=1e-13,
            )
            maximum = float(np.max(np.abs(residual(candidate, fit.x))))
            defect_value = defect(fit.x)
            if maximum <= 1e-10 and defect_value > 1e-12:
                accepted += 1
                unit = fit.x/np.linalg.norm(fit.x)
                existing = next((entry for entry in clusters if same_antipodal(unit, entry["q"])), None)
                if existing is None:
                    clusters.append({"q": unit, "hits": 1, "residual": maximum, "defect": defect_value})
                else:
                    existing["hits"] += 1
                    if maximum < existing["residual"]:
                        existing.update(q=unit, residual=maximum, defect=defect_value)
        for index, cluster in enumerate(clusters, 1):
            all_rows.append({
                "candidate_id": candidate,
                "cluster_id": f"{candidate}_Z{index:03d}",
                "hits": cluster["hits"],
                "q0": format(cluster["q"][0], ".17g"),
                "q1": format(cluster["q"][1], ".17g"),
                "q2": format(cluster["q"][2], ".17g"),
                "q3": format(cluster["q"][3], ".17g"),
                "max_residual": format(cluster["residual"], ".17g"),
                "defect_measure": format(cluster["defect"], ".17g"),
                "status": "DIAGNOSTIC_CANDIDATE_NOT_CERTIFIED",
            })
        summary[candidate] = {"starts": STARTS, "accepted_runs": accepted, "antipodal_clusters": len(clusters)}
        print(candidate, json.dumps(summary[candidate], sort_keys=True), flush=True)

    target = HERE / "ZERO_RECONNAISSANCE_CLUSTERS.tsv"
    fields_out = ["candidate_id", "cluster_id", "hits", "q0", "q1", "q2", "q3", "max_residual", "defect_measure", "status"]
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields_out, lineterminator="\n")
        writer.writeheader(); writer.writerows(all_rows)
    result = {
        "schema": "udt-curvature-zero-reconnaissance-1.0",
        "status": "DIAGNOSTIC_ONLY_NO_COMPLETENESS_CLAIM",
        "numpy_version": np.__version__,
        "scipy_version": scipy_version,
        "seed": SEED,
        "starts_per_candidate": STARTS,
        "summary": summary,
        "output_sha256": digest(target.read_bytes()),
    }
    (HERE / "ZERO_RECONNAISSANCE_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
