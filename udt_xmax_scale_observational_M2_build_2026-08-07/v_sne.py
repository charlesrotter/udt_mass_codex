"""V-SNe validator (M2 prereg SS3; D1 'FOR THE BUILDERS' forms implemented exactly).

M2_GUARD: at M2, fitting REAL magnitudes is FORBIDDEN (F-PEEK). Fit functions raise
unless the DataVector is tagged synthetic. M3 flips M2_GUARD deliberately (new prereg gate).

Frozen design (prereg SS3, F-SHOP):
  cut z > 0.023 on the mode's fit-redshift column; calibrator rows (IS_CALIBRATOR==1)
  excluded from all shape modes (A, C, D) and from mode B's fit vector (B anchors via the
  EXTERNAL M_B premise, not via calibrator rows). Duplicate SNe: rows kept as-is (the
  1701-row covariance convention; verified 1701 rows / 1543 unique CIDs at build).
Menu (prereg SS2): P1 A=(1-r/R_w)^n, P2 A=e^(-r/X), P3 A=(1+r/X)^(-alpha).
Sampling coordinates (D1 SS2 item 4, Category-A conditioning): (X_eff, 1/n) resp.
  (X_eff, 1/alpha); X_eff enters magnitudes only through the additive offset
  B = 5*log10(X_eff) + 25 + M_B, so shape modes profile the offset ANALYTICALLY and
  X_eff is structurally unidentified without an anchor (mode B translates B -> X_eff).
F-STEER: no default/start seeds n=1 or alpha=2.
"""
import os
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize

# ---------------------------------------------------------------- guard (F-PEEK)
M2_GUARD = True  # M3 flips this deliberately, under its own prereg. Do not flip at M2.
M3_PREREG_COMMIT = "523f4aca"   # udt_xmax_scale_observational_M3_runs prereg


def authorize_m3(prereg_commit):
    """The ONLY sanctioned M2_GUARD flip (M3 prereg SS5.4): the caller must
    cite the M3 prereg commit hash. Process-local; the import default stays
    guarded."""
    global M2_GUARD
    if prereg_commit != M3_PREREG_COMMIT:
        raise RuntimeError(
            f"authorize_m3: commit '{prereg_commit}' does not match the "
            f"frozen M3 prereg commit {M3_PREREG_COMMIT}")
    M2_GUARD = False
    return True

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(_REPO, "Data", "Pantheon+SH0ES.dat")
COV_PATH = os.path.join(_REPO, "Data", "Pantheon+SH0ES_STAT+SYS.cov")
_COV_CACHE = os.environ.get("VSNE_COV_CACHE", "")  # optional .npy cache path

FROZEN_Z_CUT = 0.023          # prereg SS3 (CHOSE-convention, peculiar-velocity floor)
LN10 = np.log(10.0)

# Column whitelist per mode (loader exposes ONLY these; prereg SS3 modes).
MODE_COLUMNS = {
    "A": ("CID", "zCMB", "m_b_corr", "IS_CALIBRATOR"),
    "B": ("CID", "zCMB", "m_b_corr", "IS_CALIBRATOR"),
    "C": ("CID", "zCMB", "mB", "mBERR", "x1", "x1ERR", "c", "cERR", "IS_CALIBRATOR"),
    "D": ("CID", "zCMB", "zHD", "zHEL", "m_b_corr", "IS_CALIBRATOR"),
}
# Frozen multi-start grids (deterministic; NO randomness; F-STEER: exclude 1/n=1, 1/alpha=0.5).
SHAPE_STARTS = (0.25, 0.75, 1.5, 3.0)
SHAPE_BOUNDS = (1e-4, 40.0)
TRIPP_STARTS = ((0.10, 2.5), (0.20, 3.5))   # (alpha, beta) Tripp nuisance starts
TRIPP_SIGMA_INIT = (0.15, 3.0)              # sigma-model init for the iteration (nuisance)

PROFILES = ("P1", "P2", "P3")
SHAPE_NAME = {"P1": "inv_n", "P2": None, "P3": "inv_alpha"}


def _assert_fit_allowed(dv):
    """Hard F-PEEK guard: refuse real magnitude vectors while M2_GUARD is set."""
    if M2_GUARD and not getattr(dv, "synthetic", False):
        raise RuntimeError(
            "M2_GUARD/F-PEEK: fitting a non-synthetic DataVector is forbidden at M2. "
            "Real-data fits are M3, separately preregistered and gated.")


# ---------------------------------------------------------------- data loading
def read_pantheon_table(path=DATA_PATH):
    """Full whitespace table with header row (internal; columns exposed via ModeData)."""
    return np.genfromtxt(path, names=True, dtype=None, encoding="utf-8")


def load_cov(path=COV_PATH):
    """Cov file: first line N, then N*N whitespace/newline-separated values, row-major,
    order = the .dat row order (verified N=1701 at build). Symmetrized (text round-off
    asymmetry ~3e-8 observed)."""
    if _COV_CACHE and os.path.exists(_COV_CACHE):
        C = np.load(_COV_CACHE)
        return 0.5 * (C + C.T)
    with open(path) as f:
        n = int(f.readline())
        vals = np.fromfile(f, sep=" ")
    if vals.size != n * n:
        raise ValueError(f"cov count mismatch: header N={n}, got {vals.size} values")
    C = vals.reshape(n, n)
    if _COV_CACHE:
        np.save(_COV_CACHE, C)
    return 0.5 * (C + C.T)


class ModeData:
    """Whitelist-enforcing column view after the frozen cuts. col(name) refuses any
    column outside the mode's whitelist (even though the file holds 47 columns)."""

    def __init__(self, mode, cols, mask, cov=None, zcol="zCMB"):
        self.mode, self._cols, self.mask, self.cov, self.zcol = mode, cols, mask, cov, zcol

    def col(self, name):
        if name not in MODE_COLUMNS[self.mode]:
            raise ValueError(
                f"column '{name}' is not whitelisted for mode {self.mode} "
                f"(allowed: {MODE_COLUMNS[self.mode]})")
        return self._cols[name]

    @property
    def z(self):
        return self.col(self.zcol)

    @property
    def n(self):
        return int(self.mask.sum())


def load_mode_data(mode, zcol="zCMB", table=None, cov_full=None):
    """Load + cut per the frozen design. zcol only swappable in mode D (prereg SS3).
    Cov subset rows/cols by the same mask (modes A/B/D); mode C is diagonal-only."""
    if mode not in MODE_COLUMNS:
        raise ValueError(f"unknown mode {mode!r}")
    if zcol != "zCMB":
        if mode != "D":
            raise ValueError("redshift-column swap is mode D only (prereg SS3)")
        if zcol not in ("zHD", "zHEL"):
            raise ValueError("zcol must be zCMB, zHD or zHEL")
    tab = read_pantheon_table() if table is None else table
    z = np.asarray(tab[zcol], dtype=float)
    iscal = np.asarray(tab["IS_CALIBRATOR"], dtype=float)
    mask = (z > FROZEN_Z_CUT) & (iscal == 0)   # calibrators out of ALL fit vectors at M2 design
    cols = {}
    for name in MODE_COLUMNS[mode]:
        arr = np.asarray(tab[name])
        cols[name] = arr[mask] if arr.dtype.kind in "fiu" else arr[mask]
    cov = None
    if mode in ("A", "B", "D"):
        Cf = load_cov() if cov_full is None else cov_full
        idx = np.flatnonzero(mask)
        cov = Cf[np.ix_(idx, idx)]
    return ModeData(mode, cols, mask, cov=cov, zcol=zcol)


class DataVector:
    """What fitters consume. synthetic=False vectors are refused while M2_GUARD holds."""

    def __init__(self, mode, z, y=None, cov=None, tripp=None, synthetic=False, meta=None):
        self.mode, self.z, self.y, self.cov, self.tripp = mode, np.asarray(z, float), y, cov, tripp
        self.synthetic, self.meta = bool(synthetic), dict(meta or {})

    @classmethod
    def from_real(cls, md, y_name="m_b_corr"):
        """Real-data vector (M3 path). Exists so M3 needs no loader changes; at M2 any
        fit on this object raises via M2_GUARD."""
        if md.mode == "C":
            tripp = {k: np.asarray(md.col(k), float)
                     for k in ("mB", "mBERR", "x1", "x1ERR", "c", "cERR")}
            return cls("C", md.z, tripp=tripp, synthetic=False)
        return cls(md.mode, md.z, y=np.asarray(md.col(y_name), float),
                   cov=md.cov, synthetic=False, meta={"zcol": md.zcol})


# ---------------------------------------------------------------- menu models (D1 exact forms)
def ln_g(profile, L, shape):
    """ln g where r(z) = X_eff * g(z; shape); L = log1p(z). D1 'FOR THE BUILDERS' forms:
    P1 r = Rw*(-expm1(-2*inv_n*L)), Rw = X_eff/inv_n  ->  g = (-expm1(-2 s L))/s
    P2 r = 2*X*L                                      ->  g = 2 L        (X_eff = X)
    P3 r = X*expm1(2*inv_alpha*L), X = X_eff/inv_alpha -> g = expm1(2 s L)/s
    Numerically safe for all z>0, s>0 (log of expm1 arguments, no cancellation)."""
    L = np.asarray(L, float)
    if profile == "P2":
        return np.log(2.0 * L)
    s = float(shape)
    if s <= 0:
        raise ValueError("shape parameter (1/n or 1/alpha) must be > 0")
    if profile == "P1":
        return np.log(-np.expm1(-2.0 * s * L)) - np.log(s)
    if profile == "P3":
        return np.log(np.expm1(2.0 * s * L)) - np.log(s)
    raise ValueError(f"unknown profile {profile!r}")


def mu_shape(profile, z, shape=None):
    """(5/ln10)*log d_L with X_eff factored out: model magnitude = mu_shape + B,
    B = 5*log10(X_eff) + 25 + M_B (offset; analytic-profiled in shape modes)."""
    L = np.log1p(z)
    return (5.0 / LN10) * (2.0 * L + ln_g(profile, L, shape))


def model_mag(profile, z, X_eff, shape=None, M_B=0.0):
    """Absolute-model magnitude, X_eff in Mpc: m = 5 log10 d_L[Mpc] + 25 + M_B."""
    return mu_shape(profile, z, shape) + 5.0 * np.log10(X_eff) + 25.0 + M_B


def r_of_z(profile, z, X_eff, shape=None):
    """Areal r(z) (Mpc), D1-safe forms; for tests/BAO cross-use."""
    return X_eff * np.exp(ln_g(profile, np.log1p(z), shape))


# ---------------------------------------------------------------- chi2 machinery
class CovChi2:
    """Gaussian chi2 with full covariance via Cholesky (cho_factor once; never an
    explicit inverse). Analytic profiling of the additive offset B."""

    def __init__(self, cov):
        self.cho = cho_factor(np.asarray(cov, float), lower=True)
        n = cov.shape[0]
        one = np.ones(n)
        self.w1 = cho_solve(self.cho, one)      # C^-1 1
        self.s11 = float(one @ self.w1)         # 1^T C^-1 1

    def chi2_profiled_offset(self, resid0):
        """min_B (resid0 - B 1)^T C^-1 (resid0 - B 1); returns (chi2, B*)."""
        wr = cho_solve(self.cho, resid0)
        s1r = float(self.w1 @ resid0)
        chi2 = float(resid0 @ wr) - s1r * s1r / self.s11
        return chi2, s1r / self.s11

    def chi2_fixed_offset(self, resid0, B):
        r = resid0 - B
        return float(r @ cho_solve(self.cho, r))


# ---------------------------------------------------------------- interval scanner
def profile_interval(chi2_of_p, p_best, chi2_min, lo_bound, hi_bound, step0=None,
                     max_steps=40, dchi2=1.0):
    """Delta-chi2 = dchi2 profile-likelihood interval: deterministic outward bracketing
    then BISECTION refinement of the crossing (a linear interpolation over a large first
    step collapses the interval for a locally-quadratic chi2 — caught by the synthetic
    gate's coverage check at build; bisection is shape-agnostic and deterministic).
    Open ends (bound reached below dchi2) are flagged, per D1 SS2 (one-sided posteriors
    toward the P2 limit expected)."""
    if step0 is None:
        step0 = max(0.02, 0.05 * abs(p_best))
    out = {}
    for tag, sgn, bound in (("lo", -1.0, lo_bound), ("hi", +1.0, hi_bound)):
        p_in, d_in, step, p_out = p_best, 0.0, step0, None
        for _ in range(max_steps):          # bracket: walk outward until d >= dchi2
            p = min(max(p_best + sgn * step, lo_bound), hi_bound)
            d = chi2_of_p(p) - chi2_min
            if d >= dchi2:
                p_out, d_out = p, d
                break
            p_in, d_in = p, d
            if p == bound:
                break
            step *= 1.6
        if p_out is None:
            out[tag], out[tag + "_open"] = bound, True
        else:
            for _ in range(18):             # bisection to the Delta-chi2 crossing
                pm = 0.5 * (p_in + p_out)
                dm = chi2_of_p(pm) - chi2_min
                if dm >= dchi2:
                    p_out, d_out = pm, dm
                else:
                    p_in, d_in = pm, dm
                if abs(p_out - p_in) < 1e-4 * max(step0, abs(p_out - p_best)) or \
                        abs(dm - dchi2) < 0.005:
                    break
            frac = ((dchi2 - d_in) / (d_out - d_in)) if d_out > d_in else 0.5
            out[tag], out[tag + "_open"] = float(p_in + frac * (p_out - p_in)), False
    out["best"] = float(p_best)
    return out


# ---------------------------------------------------------------- shape modes (A, D; B via A)
def _fit_shape_cov(dv, profile, cc=None):
    """Core of modes A/D: y vs mu_shape + B, full cov, B analytic. Returns result dict."""
    _assert_fit_allowed(dv)
    cc = cc or CovChi2(dv.cov)
    z, y = dv.z, dv.y

    def chi2_at_shape(s):
        c2, _ = cc.chi2_profiled_offset(y - mu_shape(profile, z, s))
        return c2

    if profile == "P2":
        s_best, chi2_best = None, chi2_at_shape(None)
    else:
        cands = []
        for s0 in SHAPE_STARTS:   # frozen deterministic multi-start (F-STEER-clean grid)
            r = minimize(lambda p: chi2_at_shape(p[0]), x0=[s0], method="Nelder-Mead",
                         bounds=[SHAPE_BOUNDS], options={"xatol": 1e-6, "fatol": 1e-9})
            cands.append((float(r.fun), float(r.x[0])))
        chi2_best, s_best = min(cands)
    _, B_best = cc.chi2_profiled_offset(y - mu_shape(profile, z, s_best))
    npar = 1 + (0 if profile == "P2" else 1)
    res = {"mode": dv.mode, "profile": profile, "chi2": chi2_best, "n_data": len(y),
           "ndof": len(y) - npar, "offset_B": float(B_best),
           "shape_name": SHAPE_NAME[profile], "shape": s_best,
           "note_scale": ("X_eff is degenerate with the free offset B in anchor-free "
                          "modes (D1 SS2 item 1); identified only via mode B's anchor.")}
    # interval on the shape parameter (offset profiled analytically inside chi2_at_shape)
    if profile != "P2":
        res["shape_interval"] = profile_interval(chi2_at_shape, s_best, chi2_best,
                                                 *SHAPE_BOUNDS)
        iv = res["shape_interval"]
        inv = {"P1": "n", "P3": "alpha"}[profile]
        res["frozen_param_" + inv] = {          # monotone map s -> 1/s; ends swap
            "best": 1.0 / s_best, "lo": 1.0 / iv["hi"], "hi": 1.0 / iv["lo"],
            "lo_open": iv["hi_open"], "hi_open": iv["lo_open"]}
    # interval on the offset B (re-minimize shape at fixed B)
    def chi2_at_B(B):
        if profile == "P2":
            return cc.chi2_fixed_offset(y - mu_shape(profile, z, None), B)
        best = np.inf
        for s0 in (s_best,) + SHAPE_STARTS[:2]:
            r = minimize(lambda p: cc.chi2_fixed_offset(y - mu_shape(profile, z, p[0]), B),
                         x0=[s0], method="Nelder-Mead", bounds=[SHAPE_BOUNDS],
                         options={"xatol": 1e-5, "fatol": 1e-8})
            best = min(best, float(r.fun))
        return best
    res["offset_interval"] = profile_interval(chi2_at_B, float(B_best), chi2_best,
                                              float(B_best) - 5.0, float(B_best) + 5.0,
                                              step0=0.01)
    return res


def fit_mode_A(dv, profile, cc=None):
    """Mode A (primary shape): m_b_corr + full STAT+SYS cov + free offset (prereg SS3).
    Carried caveat: m_b_corr's BBC layer is LCDM-adjacent (M1 catch) - travels in output.
    cc: optional pre-factored CovChi2 (Category-A conditioning: reuse across mocks)."""
    res = _fit_shape_cov(dv, profile, cc=cc)
    res["premise"] = ("mode A: shape-only, anchor-free; m_b_corr BBC-bias-corrected "
                      "(LCDM-adjacent layer; caveat carried, quantified by |C-A| at M3)")
    return res


def fit_mode_D(dv, profile, cc=None):
    """Mode D: identical statistic to mode A with the fit-redshift column swapped
    (zCMB primary / zHD / zHEL); the swap happens in load_mode_data(zcol=...)."""
    res = _fit_shape_cov(dv, profile, cc=cc)
    res["premise"] = f"mode D: redshift column = {dv.meta.get('zcol', 'zCMB')} (swap test)"
    return res


def fit_mode_B(dv, profile, M_B_ext, M_B_err=0.0,
               M_B_premise="EXTERNAL anchor M_B (premise travels: F-ANCHOR/CP4)", cc=None):
    """Mode B (anchored): mode A's chi2 surface with the offset translated to an ABSOLUTE
    scale via the EXTERNAL M_B input: B = 5 log10(X_eff) + 25 + M_B  =>
    X_eff = 10**((B - 25 - M_B)/5) [Mpc]. The anchor adds no shape information; it converts
    the offset and its interval (monotone map). M_B_err (if given) is added in quadrature
    to the offset interval half-widths before translation (anchor premise, tagged)."""
    res = _fit_shape_cov(dv, profile, cc=cc)
    res["mode"] = "B"
    res["premise"] = (f"mode B: {M_B_premise}; M_B = {M_B_ext} +/- {M_B_err} "
                      "(every absolute number below is conditional on this anchor chain)")
    B = res["offset_B"]
    iv = res["offset_interval"]
    lo_hw = np.hypot(B - iv["lo"], M_B_err)
    hi_hw = np.hypot(iv["hi"] - B, M_B_err)
    to_X = lambda b: 10.0 ** ((b - 25.0 - M_B_ext) / 5.0)
    res["X_eff_Mpc"] = {"best": to_X(B), "lo": to_X(B - lo_hw), "hi": to_X(B + hi_hw),
                        "lo_open": iv["lo_open"], "hi_open": iv["hi_open"]}
    if profile == "P1":   # frozen-param translation R_w = n * X_eff (D1 SS2 item 3: pair, not marginal)
        n = 1.0 / res["shape"]
        res["R_w_Mpc_at_best_n"] = {"value": n * res["X_eff_Mpc"]["best"],
            "note": ("R_w = n*X_eff at BEST-FIT n only; honest reporting quotes the "
                     "(X_eff, n) pair with covariance (F-SCOPE), not marginal R_w")}
    if profile == "P3":
        a = 1.0 / res["shape"]
        res["X_Mpc_at_best_alpha"] = {"value": a * res["X_eff_Mpc"]["best"],
            "note": "X = alpha*X_eff at best-fit alpha only; quote the pair (F-SCOPE)"}
    return res


# ---------------------------------------------------------------- mode C (own Tripp)
def _tripp_sigma2(tr, alpha, beta):
    """Diagonal variance for the Tripp vector (STATED choice, prereg SS3 mode C):
    sigma_i^2 = mBERR^2 + alpha^2 x1ERR^2 + beta^2 cERR^2 (the provided per-SN
    uncertainty columns; the official m_b_corr covariance does NOT apply here)."""
    return tr["mBERR"] ** 2 + alpha ** 2 * tr["x1ERR"] ** 2 + beta ** 2 * tr["cERR"] ** 2


def fit_mode_C(dv, profile, n_sigma_iter=6):
    """Mode C: own standardization m_std = mB + alpha*x1 - beta*c, alpha/beta free,
    NO BBC correction, diagonal errors (see _tripp_sigma2). Because sigma depends on
    (alpha, beta), plain chi2 minimization inflates them; standard cure: iterate with
    sigma FROZEN at the previous (alpha, beta) until fixed point (deterministic)."""
    _assert_fit_allowed(dv)
    tr, z = dv.tripp, dv.z
    has_shape = profile != "P2"

    def chi2_and_M0(theta, w):
        # theta = (shape?, alpha, beta); M0 profiled analytically (weighted mean)
        if has_shape:
            s, al, be = theta
        else:
            s, (al, be) = None, theta
        resid0 = tr["mB"] + al * tr["x1"] - be * tr["c"] - mu_shape(profile, z, s)
        M0 = float(np.sum(w * resid0) / np.sum(w))
        return float(np.sum(w * (resid0 - M0) ** 2)), M0

    al_s, be_s = TRIPP_SIGMA_INIT
    best = None
    for it in range(n_sigma_iter):
        w = 1.0 / _tripp_sigma2(tr, al_s, be_s)   # sigma FROZEN this iteration
        starts = ([tuple(best["theta"])] if best else
                  [((s0,) if has_shape else ()) + ab
                   for ab in TRIPP_STARTS for s0 in (SHAPE_STARTS[:2] if has_shape else (0,))])
        if not has_shape and best is None:
            starts = [ab for ab in TRIPP_STARTS]
        bounds = ([SHAPE_BOUNDS] if has_shape else []) + [(-2.0, 2.0), (-10.0, 20.0)]
        cands = []
        for x0 in starts:
            r = minimize(lambda th: chi2_and_M0(th, w)[0], x0=list(x0),
                         method="Nelder-Mead", bounds=bounds,
                         options={"xatol": 1e-6, "fatol": 1e-9, "maxiter": 4000})
            cands.append((float(r.fun), tuple(float(v) for v in r.x)))
        chi2_b, theta_b = min(cands)
        al_n, be_n = theta_b[-2], theta_b[-1]
        conv = abs(al_n - al_s) < 1e-4 and abs(be_n - be_s) < 1e-3
        al_s, be_s = al_n, be_n
        best = {"chi2": chi2_b, "theta": theta_b, "w": w, "iters": it + 1}
        if conv:
            break
    theta = best["theta"]
    w = 1.0 / _tripp_sigma2(tr, al_s, be_s)       # final frozen sigma for intervals
    chi2_min, M0 = chi2_and_M0(theta, w)
    npar = (2 if has_shape else 1) + 2
    res = {"mode": "C", "profile": profile, "chi2": chi2_min, "n_data": len(z),
           "ndof": len(z) - npar, "alpha": al_s, "beta": be_s, "M0": M0,
           "shape_name": SHAPE_NAME[profile], "shape": theta[0] if has_shape else None,
           "sigma_iters": best["iters"],
           "premise": ("mode C: own Tripp standardization, diagonal errors "
                       "sigma^2 = mBERR^2 + alpha^2 x1ERR^2 + beta^2 cERR^2; no BBC; "
                       "sigma-frozen fixed-point iteration (deterministic)")}

    def chi2_prof(idx, val):
        # re-minimize the other Tripp/shape params at fixed component idx (sigma frozen)
        free_idx = [i for i in range(len(theta)) if i != idx]
        def f(sub):
            th = list(theta)
            th[idx] = val
            for k, i in enumerate(free_idx):
                th[i] = sub[k]
            return chi2_and_M0(th, w)[0]
        bounds_all = ([SHAPE_BOUNDS] if has_shape else []) + [(-2.0, 2.0), (-10.0, 20.0)]
        r = minimize(f, x0=[theta[i] for i in free_idx], method="Nelder-Mead",
                     bounds=[bounds_all[i] for i in free_idx],
                     options={"xatol": 1e-5, "fatol": 1e-8, "maxiter": 3000})
        return float(r.fun)

    if has_shape:
        res["shape_interval"] = profile_interval(lambda v: chi2_prof(0, v), theta[0],
                                                 chi2_min, *SHAPE_BOUNDS)
    ia, ib = (1, 2) if has_shape else (0, 1)
    res["alpha_interval"] = profile_interval(lambda v: chi2_prof(ia, v), al_s, chi2_min,
                                             -2.0, 2.0, step0=0.005)
    res["beta_interval"] = profile_interval(lambda v: chi2_prof(ib, v), be_s, chi2_min,
                                            -10.0, 20.0, step0=0.05)
    return res
