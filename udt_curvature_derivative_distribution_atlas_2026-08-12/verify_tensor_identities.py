#!/usr/bin/env python3
"""Verify production covariant-derivative tensor identities from saved fields."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import importlib.util
import sys


HERE = Path(__file__).resolve().parent


def load_derivation():
    spec=importlib.util.spec_from_file_location("derivative_identity_metric_owner",HERE/"derive_derivative_atlas.py")
    if spec is None or spec.loader is None: raise RuntimeError("cannot load metric owners")
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module);return module


def relative(defect: np.ndarray, reference: np.ndarray) -> float:
    return float(np.linalg.norm(defect) / max(1.0, np.linalg.norm(reference)))


def main() -> None:
    saved = np.load(HERE / "PRODUCTION_DERIVATIVE_TENSORS.npz")
    maxima = {
        "riemann_first_pair_antisymmetry": 0.0,
        "riemann_last_pair_antisymmetry": 0.0,
        "riemann_pair_exchange": 0.0,
        "riemann_differential_bianchi": 0.0,
        "weyl_first_pair_antisymmetry": 0.0,
        "weyl_last_pair_antisymmetry": 0.0,
        "weyl_pair_exchange": 0.0,
        "ricci_symmetry": 0.0,
        "gram_symmetry": 0.0,
        "riemann_to_ricci_contraction": 0.0,
        "weyl_trace_free_contraction": 0.0,
    }
    derivation=load_derivation();jets=derivation.enumerate_jets()
    assert len(jets)==len(saved["keys"]) and [jet.key for jet in jets]==list(saved["keys"])
    for jet,nr, nric, nc, kr, kric, kc in zip(
        jets,
        saved["nabla_riemann"], saved["nabla_ricci"], saved["nabla_weyl"],
        saved["k_riem"], saved["k_ric"], saved["k_weyl"],
    ):
        x=derivation.torch.tensor(jet.x,dtype=derivation.torch.float64)
        metric=jet.metric_fn(x).detach().numpy();inverse=np.linalg.inv(metric)
        maxima["riemann_first_pair_antisymmetry"] = max(maxima["riemann_first_pair_antisymmetry"], relative(nr + nr.swapaxes(1, 2), nr))
        maxima["riemann_last_pair_antisymmetry"] = max(maxima["riemann_last_pair_antisymmetry"], relative(nr + nr.swapaxes(3, 4), nr))
        maxima["riemann_pair_exchange"] = max(maxima["riemann_pair_exchange"], relative(nr - nr.transpose(0, 3, 4, 1, 2), nr))
        cyclic = nr + nr.transpose(2, 0, 1, 3, 4) + nr.transpose(1, 2, 0, 3, 4)
        maxima["riemann_differential_bianchi"] = max(maxima["riemann_differential_bianchi"], relative(cyclic, nr))
        maxima["weyl_first_pair_antisymmetry"] = max(maxima["weyl_first_pair_antisymmetry"], relative(nc + nc.swapaxes(1, 2), nc))
        maxima["weyl_last_pair_antisymmetry"] = max(maxima["weyl_last_pair_antisymmetry"], relative(nc + nc.swapaxes(3, 4), nc))
        maxima["weyl_pair_exchange"] = max(maxima["weyl_pair_exchange"], relative(nc - nc.transpose(0, 3, 4, 1, 2), nc))
        maxima["ricci_symmetry"] = max(maxima["ricci_symmetry"], relative(nric - nric.swapaxes(1, 2), nric))
        maxima["gram_symmetry"] = max(maxima["gram_symmetry"], *(relative(k - k.T, k) for k in (kr, kric, kc)))
        contracted_ricci=np.einsum("ce,aebcd->abd",inverse,nr)
        maxima["riemann_to_ricci_contraction"]=max(maxima["riemann_to_ricci_contraction"],relative(contracted_ricci-nric,nric))
        contracted_weyl=np.einsum("bd,abcde->ace",inverse,nc)
        maxima["weyl_trace_free_contraction"]=max(maxima["weyl_trace_free_contraction"],relative(contracted_weyl,nc))
    status = "PASS" if max(maxima.values()) <= 2e-8 else "FAIL"
    result = {"schema": "udt-curvature-derivative-identities-v1", "status": status, "rows": len(saved["keys"]), "maximum_defects": maxima}
    (HERE / "TENSOR_IDENTITY_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if status != "PASS":
        raise RuntimeError("tensor identity gate failed")


if __name__ == "__main__":
    main()
