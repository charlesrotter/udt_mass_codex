#!/usr/bin/env python3
"""Relational observers + hyp/lin contrast + local margin. Nature lean."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent


def main():
    out = {}
    # A relational numeric
    X = 1.0
    x0, x = 0.3, 0.7
    d = (x - x0) / (1 - x * x0 / X**2)
    dphi = np.arctanh(x / X) - np.arctanh(x0 / X)
    out["relational_check"] = {
        "d": d,
        "tanh_dphi": float(np.tanh(dphi)),
        "match": bool(abs(d - np.tanh(dphi)) < 1e-12),
        "d_to_wall": float((X - x0) / (1 - X * x0 / X**2)),
        "one_plus_z": float(np.exp(dphi)),
        "sqrt_form": float(np.sqrt((X + d) / (X - d))),
    }
    print("relational", out["relational_check"])

    def hyp_dL(z):
        u = 1 + z
        return u**2 * (u**2 - 1) / (u**2 + 1)

    def lin_dL(z):
        u = 1 + z
        return u**2 * (1 - 1 / u**2)

    out["contrast"] = [
        {"z": z, "hyp": hyp_dL(z), "lin": lin_dL(z)} for z in [0.1, 0.5, 1.0, 2.0]
    ]
    out["local_margin"] = "C=2m/R=(2/5)αR² → 1 merges to filled wall"
    out["verdict"] = (
        "relational hyp room; hyp vs lin characters; local C→1 bridges rooms"
    )
    print(out["verdict"])
    (ROOT / "simple_metric_relational_rooms_continue_out.json").write_text(
        json.dumps(out, indent=2)
    )
    print("DONE")


if __name__ == "__main__":
    main()
