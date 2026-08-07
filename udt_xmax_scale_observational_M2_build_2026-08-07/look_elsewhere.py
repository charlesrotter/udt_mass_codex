#!/usr/bin/env python3
"""Look-elsewhere module (M3 prereg SS4, frozen method; built at M3-PREP SS5.2).

Three significances, all calibrated on the SAME joint null ensemble
(deterministic seeds; diagonal-jackknife-covariance caveat travels with all):
  1. per-shell LOCAL p: the shell's max-dchi2 vs its own null-mock dist;
  2. GLOBAL trials-corrected p: P(max over kept shells of per-shell max-dchi2
     >= observed max) under the joint null mocks;
  3. JOINT UDT shape-fit significance: statistic = max over the frozen
     (profile, s, shape) grid of the SUM over shells of dchi2 with the bump
     center TIED to theta_b(z_i) = s / g(z_i; profile, shape) (nearest-bin
     center approximation, stated); calibrated on the same ensemble.

Machinery: the same GLS projection quadratic forms as v_bao's calibrator
(q = y' B y); per shell an A-matrix A[mock, center] = max over the frozen
width grid of (q_alt - q_null) >= 0. All grids frozen; no LCDM seeding; the
s-grid spans the FULL theta window (F-STEER).
"""
import numpy as np

import v_bao

JOINT_S_REF_QUANTILE = 0.5    # s-grid anchored at the median-z shell (frozen)


def _design_forms(sig, theta=None):
    """Per-shell projection matrices: B_null and B_alt[center][width]."""
    if theta is None:
        theta = v_bao.theta_bin_centers()
    x = np.log(theta)
    good = np.isfinite(sig) & (sig > 0)
    xg = x[good]
    Wd = 1.0 / sig[good] ** 2
    Xn = v_bao._null_design(x)[good]

    def _B(X):
        WX = X * Wd[:, None]
        return WX @ np.linalg.solve(X.T @ WX, WX.T)

    B_null = _B(Xn)
    B_alt = [[_B(np.column_stack(
        [Xn, np.exp(-0.5 * ((xg - xc) / sw) ** 2)]))
        for sw in v_bao.BUMP_WIDTH_GRID] for xc in x]
    return {"x": x, "good": good, "sig": np.asarray(sig, float),
            "B_null": B_null, "B_alt": B_alt}


def _a_matrix(Y, forms):
    """A[m, center] = max over widths of dchi2 for each mock row of Y
    (Y already restricted to the good bins)."""
    q_null = np.einsum("mi,ij,mj->m", Y, forms["B_null"], Y)
    nc = len(forms["B_alt"])
    A = np.empty((Y.shape[0], nc))
    for c in range(nc):
        best = np.full(Y.shape[0], -np.inf)
        for B in forms["B_alt"][c]:
            np.maximum(best, np.einsum("mi,ij,mj->m", Y, B, Y), out=best)
        A[:, c] = best - q_null
    return A


def _joint_grid(z_shells, theta):
    """Frozen (profile, s, shape) grid + per-combo nearest-bin center index
    per shell (-1 = out of window, contributes 0)."""
    x = np.log(theta)
    L = np.log1p(np.asarray(z_shells, float))
    z_ref = float(np.quantile(z_shells, JOINT_S_REF_QUANTILE))
    L_ref = np.log1p(z_ref)
    combos = []
    for profile in v_bao.PROFILES:
        shapes = [None] if profile == "P2" else list(v_bao.SHAPE_GRID)
        for shape in shapes:
            g_ref = v_bao.shape_g(profile, L_ref, shape)
            g_all = v_bao.shape_g(profile, L, shape)
            for th_ref in theta:                 # s so theta_b(z_ref)=th_ref
                s = np.radians(th_ref) * g_ref
                th_i = np.degrees(s / g_all)
                ki = np.array([int(np.argmin(np.abs(x - np.log(t))))
                               if theta[0] * 0.999 <= t <= theta[-1] * 1.001
                               else -1 for t in th_i])
                if (ki >= 0).sum() >= 2:         # need >=2 tied shells
                    combos.append({"profile": profile, "shape": shape,
                                   "s_rad": float(s), "k": ki})
    return combos


def _joint_stat(A_list, combos):
    """max over combos of sum over shells of A[:, k_i] (0 if out-of-window).
    A_list: per shell (n_mock, n_center). Returns (n_mock,) and argmax info
    for the observed row when n_mock==1."""
    n_mock = A_list[0].shape[0]
    best = np.full(n_mock, -np.inf)
    best_combo = np.full(n_mock, -1)
    for ci, cb in enumerate(combos):
        tot = np.zeros(n_mock)
        for A, k in zip(A_list, cb["k"]):
            if k >= 0:
                tot += A[:, k]
        upd = tot > best
        best[upd] = tot[upd]
        best_combo[upd] = ci
    return best, best_combo


def analyze_shells(w_list, sig_list, z_shells, n_mocks=300, seed=2026,
                   theta=None):
    """The full SS4 look-elsewhere analysis on kept shells.

    w_list/sig_list: per-shell observed w(theta) and diagonal jackknife
    sigma; z_shells: shell-center redshifts. Deterministic given seed.
    Returns per-shell local p, global trials-corrected p, and the joint
    shape-fit significance (overall + per profile).
    """
    if theta is None:
        theta = v_bao.theta_bin_centers()
    ns = len(w_list)
    rng = np.random.default_rng(seed)
    forms, A_obs, A_mock, obs_max, mock_max = [], [], [], [], []
    for i in range(ns):
        f = _design_forms(sig_list[i], theta)
        good = f["good"]
        Yo = np.asarray(w_list[i], float)[None, good]
        Ym = rng.normal(0.0, np.asarray(sig_list[i], float)[good],
                        size=(n_mocks, int(good.sum())))
        Ao, Am = _a_matrix(Yo, f), _a_matrix(Ym, f)
        forms.append(f)
        A_obs.append(Ao)
        A_mock.append(Am)
        obs_max.append(float(Ao.max()))
        mock_max.append(Am.max(axis=1))
    obs_max = np.array(obs_max)
    mock_max = np.array(mock_max)                    # (ns, n_mocks)
    local_p = [float(np.mean(mock_max[i] >= obs_max[i])) for i in range(ns)]
    glob_obs = float(obs_max.max())
    glob_dist = mock_max.max(axis=0)
    global_p = float(np.mean(glob_dist >= glob_obs))
    combos = _joint_grid(z_shells, theta)
    j_obs, j_combo = _joint_stat(A_obs, combos)
    j_dist, _ = _joint_stat(A_mock, combos)
    joint = {"stat_obs": float(j_obs[0]),
             "p": float(np.mean(j_dist >= j_obs[0])),
             "best_combo": ({} if j_combo[0] < 0 else
                            {k: (v.tolist() if isinstance(v, np.ndarray)
                                 else v)
                             for k, v in combos[int(j_combo[0])].items()})}
    per_profile = {}
    for prof in v_bao.PROFILES:
        sel = [c for c in combos if c["profile"] == prof]
        if not sel:
            continue
        po, _ = _joint_stat(A_obs, sel)
        pd, _ = _joint_stat(A_mock, sel)
        per_profile[prof] = {"stat_obs": float(po[0]),
                             "p": float(np.mean(pd >= po[0]))}
    return {"n_shells": ns, "n_mocks": n_mocks, "seed": seed,
            "local_max_dchi2": obs_max.tolist(), "local_p": local_p,
            "global_max_dchi2": glob_obs, "global_p": global_p,
            "joint": joint, "joint_per_profile": per_profile,
            "n_combos": len(combos),
            "caveat": ("diagonal jackknife covariance (M2 condition); "
                       "nearest-bin center tie approximation (stated)")}
