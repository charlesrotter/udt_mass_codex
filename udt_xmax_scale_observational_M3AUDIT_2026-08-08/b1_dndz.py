#!/usr/bin/env python3
"""B1: dN/dz edge structure at the 9 target shells (contract 2d9933d1).
Catalog-level only (loader-legal, no pair counting, no guard flip needed —
same access class as the M3 dry-run census). Weighted fine-binned dN/dz per
tracer and cap; slope/curvature of ln n(z) at each target shell boundary;
within-shell tilt of the weighted mean z (feeds the drift-direction note).
Saves arrays to audit_data/b1_dndz.npz + summary json. FORENSICS ONLY."""
import json
import numpy as np
import audit_lib as al
import v_bao

FINE = {"LRG": 0.005, "QSO": 0.010}          # fine bin = shell_dz/10 or /15


def tracer_hist(tracer):
    zlo, zhi = v_bao.TRACER_ZRANGE[tracer]
    d = FINE[tracer]
    edges = np.arange(zlo, zhi + d / 2, d)
    per_cap = {}
    for cap in al.CAPS:
        c = v_bao.load_catalog(al.dat_path(tracer, cap), zrange=(zlo, zhi),
                               use_sys=True)
        per_cap[cap] = {"h": np.histogram(c.z, bins=edges, weights=c.w)[0],
                        "z": c.z, "w": c.w}
    return edges, per_cap


def logslope(edges, h, z0, half=0.01):
    """d ln n/dz at boundary z0 from mean n in (z0-half, z0) vs (z0, z0+half)."""
    c = 0.5 * (edges[:-1] + edges[1:])
    lo = h[(c > z0 - half) & (c < z0)]
    hi = h[(c > z0) & (c < z0 + half)]
    if lo.size == 0 or hi.size == 0 or lo.mean() <= 0 or hi.mean() <= 0:
        return np.nan
    return float(np.log(hi.mean() / lo.mean()) / half)


def main():
    out = {"contract": [al.M3_PREREG_COMMIT, al.AUDIT_PREREG_COMMIT],
           "targets": []}
    arrays = {}
    hists = {}
    for tracer in ("LRG", "QSO"):
        edges, per_cap = tracer_hist(tracer)
        h_tot = sum(per_cap[c]["h"] for c in al.CAPS)
        arrays[f"{tracer}_edges"] = edges
        arrays[f"{tracer}_h_tot"] = h_tot
        for cap in al.CAPS:
            arrays[f"{tracer}_h_{cap}"] = per_cap[cap]["h"]
        hists[tracer] = (edges, per_cap, h_tot)
        # tracer-wide typical |slope| for context (median over interior)
        c = 0.5 * (edges[:-1] + edges[1:])
        ln = np.where(h_tot > 0, np.log(np.maximum(h_tot, 1e-300)), np.nan)
        sl = np.gradient(ln, c)
        arrays[f"{tracer}_lnslope"] = sl
        out[f"{tracer}_median_abs_slope"] = float(np.nanmedian(np.abs(sl)))
    for tracer, zlo, zhi, role in al.TARGETS:
        edges, per_cap, h_tot = hists[tracer]
        c = 0.5 * (edges[:-1] + edges[1:])
        m = (c > zlo) & (c < zhi)
        rec = {"tracer": tracer, "z": [zlo, zhi], "role": role}
        for name, h in [("comb", h_tot)] + [(cap, per_cap[cap]["h"])
                                            for cap in al.CAPS]:
            rec[name] = {
                "slope_lo": logslope(edges, h, zlo),
                "slope_hi": logslope(edges, h, zhi),
                "in_shell_slope": float(np.polyfit(
                    c[m], np.log(np.maximum(h[m], 1e-300)), 1)[0]),
                "in_shell_curv": float(np.polyfit(
                    c[m], np.log(np.maximum(h[m], 1e-300)), 2)[0]),
                "edge_ratio_hi_over_lo": float(h[m][-1] / max(h[m][0], 1e-300)),
            }
        zz = np.concatenate([per_cap[cap]["z"] for cap in al.CAPS])
        ww = np.concatenate([per_cap[cap]["w"] for cap in al.CAPS])
        sm = (zz >= zlo) & (zz < zhi)
        zbar = float(np.sum(zz[sm] * ww[sm]) / np.sum(ww[sm]))
        rec["zbar_weighted"] = zbar
        rec["tilt_frac"] = float((zbar - 0.5 * (zlo + zhi)) / (0.5 * (zhi - zlo)))
        out["targets"].append(rec)
    np.savez(al.AUDIT_DATA + "/b1_dndz.npz", **arrays)
    with open(al.AUDIT_DATA + "/b1_summary.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1)[:4000])


if __name__ == "__main__":
    main()
