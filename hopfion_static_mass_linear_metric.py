"""hopfion_static_mass_linear_metric.py -- Phase A (baseline+axisymmetry) + Section-2 identity
verification + Phase C (frozen-source linear lapse mass) for the H3 static mass-backreaction
dispatch. Full linear metric (Phase D) and continuation (Phase E) are separate.

Usage: PYTHONPATH=$(pwd) python3 hopfion_static_mass_linear_metric.py \
          --input hopfion_arc_scripts_2026-07-05/prod_an256.npz [--phase baseline|lapse]
DATA-BLIND. No fitted couplings; xi=k4=1 gauge from the banked field.
"""
import argparse, json, numpy as np, torch
import hopfion_static_mass_common as C
torch.set_default_dtype(torch.float64)

GIT_SHA = "88aed6ccc05556162fba3ea19f71a869081c6da4"
H3_SHA256 = "5878f1dbaf870bd143be754490d805470afa028c462b986fa7f83dbd6b757b81"


def run(path):
    d = C.load_h3(path); n = d["n"]; h = d["h"]; L = d["L"]; xi = d["xi"]; k4 = d["k4"]
    mf = C.matter_fields(n, h, xi, k4)
    E2, E4 = C.energies(mf, h); Qs = float(d["stored"]["Q"])

    # ---- identities (Section 2) ----
    rhoS = mf["rho"] + mf["S"]; k4Y = 0.5 * k4 * mf["Y"]
    err_id = float((rhoS - k4Y).abs().max() / (k4Y.abs().max() + 1e-30))
    err_2r4 = float((k4Y - 2 * mf["rho4"]).abs().max())
    Sform = -0.5 * xi * mf["X"] + 0.25 * k4 * mf["Y"]
    err_S = float((mf["S"] - Sform).abs().max() / (mf["S"].abs().max() + 1e-30))
    r4min = float(mf["rho4"].min())
    # random smooth unit field
    torch.manual_seed(1); g = torch.randn(3, d["N"], d["N"], d["N"], device=d["dev"])
    for _ in range(4):
        g = sum(torch.roll(g, s, a) for a in (1, 2, 3) for s in (1, -1)) / 6
    g = g / g.norm(dim=0, keepdim=True); mfr = C.matter_fields(g, h, xi, k4)
    err_rand = float(((mfr["rho"] + mfr["S"]) - 2 * mfr["rho4"]).abs().max()
                     / (2 * mfr["rho4"].abs().max() + 1e-30))

    # ---- Phase A axisymmetry ----
    ax = dict(rho=C.axisymmetry_residual(mf["rho"], L),
              rho4=C.axisymmetry_residual(mf["rho4"], L),
              S=C.axisymmetry_residual(mf["S"], L))

    # ---- Phase C mass flux + lapse ----
    Rs, MN, _ = C.cumulative_mass_flux(mf["rho4"], L)
    plateau = float(MN[-1]); spread = float(np.ptp(MN[-8:]) / (abs(np.mean(MN[-8:])) + 1e-30))
    u = C.poisson_solve_open(mf["rho4"], L); uc = float(u[d["N"] // 2, d["N"] // 2, d["N"] // 2])

    out = dict(
        provenance=dict(git_sha=GIT_SHA, branch="grok", h3_path=path, h3_sha256=H3_SHA256,
                        device=str(d["dev"]), dtype="float64"),
        baseline=dict(grid=dict(N=d["N"], L=L, h=h), Q_H=Qs, E2=E2, E4=E4, E2_over_E4=E2 / E4,
                      axisymmetry_residuals=ax),
        identities=dict(rhoS_eq_k4Y_relerr=err_id, k4Y_eq_2rho4_abserr=err_2r4,
                        S_formula_relerr=err_S, random_rhoS_2rho4_relerr=err_rand,
                        min_rho4=r4min, positivity_holds=bool(r4min >= -1e-12)),
        linear_lapse=dict(mass_flux_limit=plateau, predicted_2E4=2 * E4,
                          mass_over_carrier_energy=plateau / (E2 + E4), far_R_spread=spread,
                          lapse_center_sign="negative(depressed)" if uc < 0 else "positive",
                          surface_fluxes=[[float(Rs[k]), float(MN[k])] for k in range(0, len(Rs), 8)],
                          gate="PASS" if (spread < 1e-6 and abs(plateau - 2 * E4) < 1e-3) else "FAIL"),
        hessian=dict(gate="NOT_RUN (Phase B)"),
        linear_metric=dict(gate="NOT_RUN (Phase D)"),
        continuation=dict(gate="NOT_RUN (Phase E)"),
        verdict="PHASE_A_C_PASS_CONDITIONAL (EH-frame; B/D/E pending)")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="hopfion_arc_scripts_2026-07-05/prod_an256.npz")
    ap.add_argument("--phase", default="lapse")
    a = ap.parse_args()
    out = run(a.input)
    json.dump(out, open("hopfion_static_mass_out.json", "w"), indent=1)
    print(json.dumps(out, indent=1))
