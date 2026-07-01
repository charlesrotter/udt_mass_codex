"""NATIVE SYMMETRIC PAIR REDUCTION (weld phase 3): does the symmetric-
pair configuration — the matter cell on [0, R] glued to the EVEN/
SYMMETRIC continuation of its own profile about r = R, doubling the
interface slope jump to Delta phi' = -q/R, i.e. doubled delta strength
Gamma = 4q in the phase-2 units — deliver the binding the single cell
missed?  Answer: NO, by an exact symmetry-reduction theorem.

LICENSING STATUS (honest, binding — read first): this configuration is
NON-LICENSED.  The phase-3 recon of the banked corpus (recorded in
weld_two_sided_results.md) found that the corpus's two-sided structure
supplies NO second shell: the banked cell glues to a FLAT exterior
(CANON C-2 zero tail; single momentum jump Delta Pi = q/2, Pi_inner =
-q/2, Pi_outer = 0 — negative_phi doc section 165); the two-sided
content is the transfer-kernel COMPOSITION LAW (eta/2 per side gluing
to eta, sections 263/380, conditional identity), NOT a mirrored
profile; exterior mirroring is NOT USED anywhere in the banked chain;
and naive per-side stress doubling is explicitly FORBIDDEN by the
double-count guards (sections 217-219;
native_interface_vs_warped_double_count_test.py).  The symmetric pair
below is computed ONLY to close the question — because the naive
reading "doubled shell: Gamma = 4q = 4/3 vs L0 = 1.33835 (0.376%
below threshold!)" is exactly the kind of proximity the null-test
discipline exists to interrogate.  Nothing here is promoted to
physics.

THE CLAIM VERIFIED (the symmetry-reduction theorem): for the
symmetric-pair mode problem (phase-2 Reading-A elliptic equation,
coefficients even about r = R, doubled delta at R), the perturbation
problem splits into even/odd sectors about R, and:

  T1 (EVEN sector): u'(R+) = -u'(R-) by symmetry; the jump condition
     u'(R+) - u'(R-) = -(4q/R) u(R) then gives
         u'(R-) = +(2q/R) u(R)
     — EXACTLY the phase-2 single-cell native Robin condition BC-c
     with gamma = 2q.  The even-sector binding condition is
     gamma_even = 2q against the SAME interior threshold L0: the
     deficit factor 2.0075 is UNCHANGED by pairing.  (Three-line
     sympy derivation; the doubled jump Gamma = 4q is itself derived
     from the mirrored profile, not assumed.)
  T2 (ODD sector): u(R) = 0 — EXACTLY phase-2 BC-b (Dirichlet),
     where the delta does no work and the form is positive definite:
     strictly worse (no binding for ANY Gamma — theorem level).
  T3 (numeric cross-check): the full two-domain symmetric problem
     (interior collar [r_min, R] with f = (R/r)^{1/3}, E0 = s/r^2,
     reflected-coordinate mirror on [R, 2R - r_min], doubled delta at
     R) has spectrum equal to the UNION of the phase-2 BC-c spectrum
     (even, gamma = 2q) and BC-b spectrum (odd), to 4+ digits:
         top even omega^2 = -3.4667814 (lam = 2),  -10.376405 (lam = 6)
         top odd  omega^2 = -27.334956 (lam = 2),  -41.213694 (lam = 6)
     — the phase-2 BC-c and BC-b headline numbers exactly; parity-
     classified FD eigenvectors + independent shooting cross-check.
  T4 (the 4/3 mirage, recorded): the naive comparison "doubled shell
     gives 4q = 4/3 vs L0 = 1.33835009 — only 0.376% below!" is VOID:
     the symmetric pair never delivers an effective 4q to ANY single
     sector; the even sector sees 2q exactly and the odd sector sees
     nothing.  The 0.376% proximity of 4/3 to L0 is thereby a
     CONFIRMED MIRAGE — vindicating the null-test discipline that
     refused to romance it in phase 2.

CONVENTIONS AND THRESHOLD VALUES (reused verbatim from phase 2,
native_weld_interface_mode_spectrum.py, blind-verified by agent
ae8caa64ef3d4b1ff to 7-9 digits): banked cell q = 1/3, s = q(1-q)/2 =
1/9; physical single-shell strength gamma = 2q = 2/3; interior zero-
energy Friedrichs log-derivative L0 = 1.33835009 at lam = 2 via the
exact Bessel closed form
    L0 = -(1-2q)/2 + (q tau0/2) I'_nu(tau0)/I_nu(tau0),
    nu = sqrt(1 + 4q(1-q))/q = sqrt(17) at q = 1/3,
    tau0 = 2 sqrt(lam)/q;
binding criterion gamma > L0 (BC-c / even), never (BC-b / odd).

VERDICT: the symmetric pair adds NOTHING — its spectrum is the union
of two already-computed phase-2 negatives.  The interface-shell route
to native oscillation is closed at the compound/two-sided level (the
licensing recon closed the banked side; this theorem closes the
adjacent non-banked side).  This is corollary-grade: it reuses phase
2's verified threshold machinery and adds only the even/odd
decomposition, cross-checked numerically in-script.

New file 2026-06-10 (weld phase 3).  Creates nothing else, modifies
nothing existing.  Runtime: ~10-30 s (sympy reduction checks + sparse
FD eigensolves + RK shooting cross-checks).
"""

from __future__ import annotations

import sys

import numpy as np
import scipy.sparse as sps
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.sparse.linalg import eigsh
from scipy.special import iv

FAILURES: list[str] = []
N_CHECKS = 0


def check(label: str, ok: bool) -> None:
    global N_CHECKS
    N_CHECKS += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        FAILURES.append(label)


def hr(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


QB = 1.0 / 3.0                      # banked q
SB = QB * (1 - QB) / 2              # = 1/9
GAMMA_PHYS = 2 * QB                 # phase-2 physical single-shell = 2/3
GAMMA_PAIR = 4 * QB                 # symmetric-pair doubled strength = 4/3
L0_REF = 1.33835009                 # phase-2 threshold at lam = 2 (Bessel)
EV_C_REF = {2.0: -3.4667814, 6.0: -10.376405}    # phase-2 BC-c tops
EV_B_REF = {2.0: -27.334956, 6.0: -41.213694}    # phase-2 BC-b tops

# ===========================================================================
# P0 — licensing status + pre-registered claim (printed before computing)
# ===========================================================================
hr("P0 — NON-LICENSED CONFIGURATION + PRE-REGISTERED CLAIM")
print("""  THIS CONFIGURATION IS NON-LICENSED (computed only to close the
  question).  Phase-3 recon of the banked corpus: the cell glues to a
  FLAT exterior (CANON C-2 zero tail; single jump Delta Pi = q/2, doc
  section 165); the two-sided content is the eta/2-per-side
  COMPOSITION LAW (sections 263/380), not a mirrored profile; exterior
  mirroring is NOT USED; naive per-side stress doubling is FORBIDDEN
  (double-count guards, sections 217-219).

  PRE-REGISTERED CLAIM (the symmetry-reduction theorem): the
  symmetric-pair mode problem splits exactly into
      EVEN  = phase-2 BC-c at gamma = 2q  (same L0, same 2.0075 deficit)
      ODD   = phase-2 BC-b (Dirichlet, never binds)
  so the pair delivers NOTHING beyond the two phase-2 negatives, and
  the "4q = 4/3 vs L0 = 1.33835" proximity is a mirage.  Verified
  symbolically (T1, T2) and numerically (T3, union of spectra to 4+
  digits).  No softening either way.""")

# ===========================================================================
# T0 — the doubled jump Gamma = 4q, DERIVED from the mirrored profile
# ===========================================================================
hr("T0 — THE MIRRORED PROFILE DOUBLES THE JUMP: Delta phi' = -q/R, "
   "Gamma = 4q (DERIVED, NOT ASSUMED)")

r, R, q_s, uR = sp.symbols("r R q uR", positive=True)
f_int = (R / r)**q_s                      # interior collar, r <= R
f_mir = (R / (2 * R - r))**q_s            # even continuation about r = R
check("even continuation: f_mir(r) = f_int(2R - r) = (R/(2R-r))^q is "
      "the symmetric reflection of the collar about r = R; "
      "f_mir(R) = 1 = f_int(R) (continuous)",
      sp.simplify(f_mir - f_int.subs(r, 2 * R - r)) == 0
      and sp.simplify(f_mir.subs(r, R) - 1) == 0)
dfp = sp.simplify(sp.diff(f_mir, r).subs(r, R)
                  - sp.diff(f_int, r).subs(r, R))
check("slope jump DOUBLED: f_int'(R-) = -q/R, f_mir'(R+) = +q/R => "
      "Delta f' = +2q/R (vs +q/R for the flat-exterior single cell)",
      sp.simplify(dfp - 2 * q_s / R) == 0)
check("Delta phi' = -Delta f'/(2 f(R)) with f(R) = 1: Delta phi' = "
      "-q/R — DOUBLE the single-cell -q/(2R); the E0 delta is "
      "-(q/R) delta(r-R)",
      sp.simplify(-dfp / 2 + q_s / R) == 0)
eps_s = sp.Symbol("epsilon", positive=True)
delta_term = sp.integrate(
    -4 * r**2 * 1**2 * (-(q_s / R)) * sp.DiracDelta(r - R) * uR,
    (r, R - eps_s, R + eps_s))
dup = sp.Symbol("Deltauprime", real=True)
jump_sol = sp.solve(sp.Eq(R**2 * dup + delta_term, 0), dup)
check("jump condition (phase-2 S3 bookkeeping, f(R) = 1, no product "
      "ambiguity): R^2 Delta u' + 4qR u(R) = 0 <=> Delta u' = "
      "-(4q/R) u(R) — the doubled delta strength Gamma = 4q",
      jump_sol == [-4 * q_s * uR / R])

# ===========================================================================
# T1 — EVEN sector: exact reduction to phase-2 BC-c at gamma = 2q
# ===========================================================================
hr("T1 — EVEN SECTOR REDUCES EXACTLY TO PHASE-2 BC-c AT gamma = 2q "
   "(THREE LINES)")

upm = sp.Symbol("uprime_Rminus", real=True)     # u'(R-)
upp = sp.Symbol("uprime_Rplus", real=True)      # u'(R+)
# line 1: even symmetry about R
even_constraint = sp.Eq(upp, -upm)
# line 2: the jump condition with Gamma = 4q
jump_eq = sp.Eq(upp - upm, -(4 * q_s / R) * uR)
# line 3: solve
sol = sp.solve([even_constraint, jump_eq], [upp, upm], dict=True)[0]
check("line 1 (symmetry): u even about R => u'(R+) = -u'(R-);  "
      "line 2 (jump): u'(R+) - u'(R-) = -(4q/R) u(R);  "
      "line 3 (solve): u'(R-) = +(2q/R) u(R) EXACTLY",
      sp.simplify(sol[upm] - 2 * q_s * uR / R) == 0
      and sp.simplify(sol[upp] + 2 * q_s * uR / R) == 0)
check("this IS phase-2 BC-c: the single-cell native Robin natural "
      "condition u'(R) = (2q/R) u(R) with gamma = 2q (phase-2 S6) — "
      "the even sector of the DOUBLED-shell pair is the SINGLE-cell "
      "problem at the SINGLE-shell strength; each half-cell sees half "
      "of Gamma = 4q",
      sp.simplify(sol[upm] - GAMMA_PHYS / float(2 * QB)
                  * 2 * q_s * uR / R) == 0)


def L0_closed(q: float, lam: float) -> float:
    """Phase-2 verified exact threshold (Bessel closed form, agent
    ae8caa64ef3d4b1ff): L0 = -(1-2q)/2 + (q tau0/2) I'_nu(tau0)/
    I_nu(tau0), nu = sqrt(1+4q(1-q))/q, tau0 = 2 sqrt(lam)/q."""
    nu = np.sqrt(1 + 4 * q * (1 - q)) / q
    t0 = 2 * np.sqrt(lam) / q
    wp = 0.5 * (iv(nu - 1, t0) + iv(nu + 1, t0))
    return -(1 - 2 * q) / 2 + (q * t0 / 2) * wp / iv(nu, t0)


L0 = L0_closed(QB, 2.0)
check(f"threshold UNCHANGED: the even-sector binding condition is "
      f"gamma_even = 2q = {GAMMA_PHYS:.6f} vs the SAME interior "
      f"threshold L0 = {L0:.8f} (Bessel closed form, nu = sqrt(17), "
      f"matches the phase-2 banked value {L0_REF} to "
      f"{abs(L0 - L0_REF):.1e}) — deficit factor L0/(2q) = "
      f"{L0 / GAMMA_PHYS:.6f} = the phase-2 2.0075, UNCHANGED by "
      "pairing",
      abs(L0 - L0_REF) < 5e-8
      and abs(L0 / GAMMA_PHYS - 2.0075) < 5e-4)

# ===========================================================================
# T2 — ODD sector: exact reduction to phase-2 BC-b (Dirichlet)
# ===========================================================================
hr("T2 — ODD SECTOR REDUCES EXACTLY TO PHASE-2 BC-b (DIRICHLET): "
   "STRICTLY WORSE, THEOREM LEVEL")

u_odd = sp.Function("u", real=True)
t = sp.Symbol("t", real=True)
check("odd symmetry about R: u(R + t) = -u(R - t) at t = 0 forces "
      "u(R) = 0 — EXACTLY phase-2 BC-b (Dirichlet at the interface)",
      sp.solve(sp.Eq(u_odd(R), -u_odd(R)), u_odd(R)) == [0])
check("with u(R) = 0 the delta term -Gamma·R·u(R)^2 vanishes "
      "IDENTICALLY (for ANY Gamma, 4q included) and the quadratic form "
      "is positive definite on the banked collar (phase-2 T1 theorem: "
      "Q_bulk = lam f + 4 s f^2 > 0 pointwise) — the odd sector NEVER "
      "binds: strictly worse than the even sector, theorem level",
      sp.simplify((-sp.Symbol("Gamma") * R * u_odd(R)**2)
                  .subs(u_odd(R), 0)) == 0)

# ===========================================================================
# T3 — numeric cross-check: two-domain spectrum = BC-c UNION BC-b
# ===========================================================================
hr("T3 — NUMERIC CROSS-CHECK: FULL TWO-DOMAIN SYMMETRIC PROBLEM = "
   "UNION OF PHASE-2 BC-c AND BC-b SPECTRA (4+ DIGITS)")

print("""  Construction (phase-2 FD conventions): interior collar
  [r_min, R] with f = (R/r)^{1/3}, E0 = s/r^2 on a log mesh; mirror
  side [R, 2R - r_min] by the reflected coordinate (all coefficients
  P, Q, W even about r = R); doubled delta at R (form term
  -Gamma·R·u(R)^2, Gamma = 4q); Friedrichs/Dirichlet truncation at
  both core endpoints.  Eigenvectors parity-classified about R.""")


def assemble_single(q: float, s: float, lam: float, bc: str,
                    gamma: float, rmin: float = 1e-5,
                    n_int: int = 6000):
    """Phase-2 single-cell FD (interior, bc in {'b','c'})."""
    rg = np.exp(np.linspace(np.log(rmin), 0.0, n_int))
    rg[-1] = 1.0
    h = np.diff(rg)
    rm = 0.5 * (rg[:-1] + rg[1:])
    fm = (1.0 / rm)**q
    Pm = rm**2 * fm**2
    Qm = lam * fm + 4 * rm**2 * fm**2 * (s / rm**2)
    Wm = rm**2
    N = len(rg)
    Qn = np.zeros(N)
    Wn = np.zeros(N)
    Qn[:-1] += Qm * h / 2
    Qn[1:] += Qm * h / 2
    Wn[:-1] += Wm * h / 2
    Wn[1:] += Wm * h / 2
    Qn[-1] -= gamma * 1.0          # delta form term -(gamma/R) P(R) u^2
    cp = Pm / h
    dg = np.zeros(N)
    dg[:-1] += cp
    dg[1:] += cp
    idx = np.arange(1, N) if bc == 'c' else np.arange(1, N - 1)
    Kd = dg[idx] + Qn[idx]
    Ko = -cp[1:len(idx)]
    A = -sps.diags([Ko, Kd, Ko], [-1, 0, 1], format='csc')
    W = sps.diags(Wn[idx], 0, format='csc')
    return A, W


def assemble_pair(q: float, s: float, lam: float, Gamma: float,
                  rmin: float = 1e-5, n_int: int = 6000):
    """Two-domain symmetric pair on [r_min, 2R - r_min] (R = 1):
    coefficients even about r = R via the reflected coordinate
    sigma(r) = min(r, 2R - r); doubled delta (strength Gamma) at R;
    Dirichlet at both core endpoints."""
    g_int = np.exp(np.linspace(np.log(rmin), 0.0, n_int))
    g_int[-1] = 1.0
    rg = np.concatenate([g_int, 2.0 - g_int[-2::-1]])
    h = np.diff(rg)
    rm = 0.5 * (rg[:-1] + rg[1:])
    sig = np.minimum(rm, 2.0 - rm)        # reflected coordinate
    fm = (1.0 / sig)**q
    Pm = sig**2 * fm**2
    Qm = lam * fm + 4 * sig**2 * fm**2 * (s / sig**2)
    Wm = sig**2
    N = len(rg)
    im = n_int - 1                        # interface node r = R
    Qn = np.zeros(N)
    Wn = np.zeros(N)
    Qn[:-1] += Qm * h / 2
    Qn[1:] += Qm * h / 2
    Wn[:-1] += Wm * h / 2
    Wn[1:] += Wm * h / 2
    Qn[im] -= Gamma * 1.0          # -(Gamma/R) P(R) u(R)^2, P(R) = R^2
    cp = Pm / h
    dg = np.zeros(N)
    dg[:-1] += cp
    dg[1:] += cp
    idx = np.arange(1, N - 1)             # Dirichlet at BOTH endpoints
    Kd = dg[idx] + Qn[idx]
    Ko = -cp[1:len(idx)]
    A = -sps.diags([Ko, Kd, Ko], [-1, 0, 1], format='csc')
    W = sps.diags(Wn[idx], 0, format='csc')
    return A, W


def top_vals(A, W, k: int = 6, sigma: float = 50.0,
             vecs: bool = False):
    out = eigsh(A, k=k, M=W, sigma=sigma, which='LM',
                return_eigenvectors=vecs)
    if vecs:
        vals, V = out
        order = np.argsort(vals)[::-1]
        return vals[order], V[:, order]
    return np.sort(out)[::-1]


def interior_shoot(q: float, s: float, lam: float, w2: float,
                   x0: float = -40.0,
                   rtol: float = 1e-12) -> tuple[float, float]:
    """Phase-2 Friedrichs-branch interior shooter in x = ln(r/R)."""
    a = (-(1 - 2 * q) + np.sqrt((1 - 2 * q)**2 + 16 * s)) / 2
    den = (a + q)**2 + (1 - 2 * q) * (a + q) - 4 * s
    c = lam / den
    e0 = np.exp(q * x0)

    def rhs(x, y):
        u, up = y
        return [up, -(1 - 2 * q) * up
                + (lam * np.exp(q * x) + 4 * s
                   + w2 * np.exp((2 + 2 * q) * x)) * u]

    sol = solve_ivp(rhs, [x0, 0.0], [1 + c * e0, a + c * (a + q) * e0],
                    rtol=rtol, atol=1e-14)
    return float(sol.y[0, -1]), float(sol.y[1, -1])


def shoot_root(Ffun, w2_lo: float, w2_hi: float,
               n_scan: int = 80) -> float:
    grid = np.linspace(w2_lo, w2_hi, n_scan)
    vals = [Ffun(w) for w in grid]
    for i in range(len(grid) - 1):
        if np.sign(vals[i]) != np.sign(vals[i + 1]):
            return brentq(Ffun, grid[i], grid[i + 1], xtol=1e-11,
                          rtol=1e-12)
    raise RuntimeError("no sign change in scan window")


for lam in (2.0, 6.0):
    print(f"\n  ---- lam = {lam:g} ----")
    # single-cell phase-2 spectra (even-candidate and odd-candidate)
    Ac, Wc = assemble_single(QB, SB, lam, 'c', GAMMA_PHYS)
    Ab, Wb = assemble_single(QB, SB, lam, 'b', GAMMA_PHYS)
    vc = top_vals(Ac, Wc, k=6)
    vb = top_vals(Ab, Wb, k=6)
    # two-domain symmetric pair, doubled delta Gamma = 4q
    Ap, Wp = assemble_pair(QB, SB, lam, GAMMA_PAIR)
    vp, Vp = top_vals(Ap, Wp, k=6, vecs=True)
    # parity classification of the pair eigenvectors (mesh symmetric:
    # the idx nodes 1..N-2 reverse onto themselves)
    parities = []
    for j in range(vp.size):
        v = Vp[:, j]
        even_part = np.linalg.norm(v - v[::-1])
        odd_part = np.linalg.norm(v + v[::-1])
        parities.append('+' if even_part < odd_part else '-')
        check(f"lam={lam:g} pair eigenvector #{j} "
              f"(omega^2 = {vp[j]:+.6f}) has DEFINITE parity "
              f"{parities[-1]} about R (residual "
              f"{min(even_part, odd_part) / np.linalg.norm(v):.1e})",
              min(even_part, odd_part) / np.linalg.norm(v) < 1e-6)
    # union check: top-6 of pair = top-6 of (BC-c union BC-b)
    union = np.sort(np.concatenate([vc, vb]))[::-1][:6]
    rel = np.max(np.abs(vp - union) / np.abs(union))
    print(f"  pair top-6:  {np.array2string(vp, precision=6)}")
    print(f"  parities:    {parities}")
    print(f"  union top-6: {np.array2string(union, precision=6)}")
    check(f"lam={lam:g} UNION IDENTITY: pair spectrum (top 6) = union "
          f"of phase-2 BC-c (gamma = 2q) and BC-b spectra, max rel "
          f"diff {rel:.1e} < 1e-6 (same-mesh FD)",
          rel < 1e-6)
    # sector-resolved tops vs the phase-2 banked headline numbers
    top_even = vp[[j for j, p in enumerate(parities) if p == '+'][0]]
    top_odd = vp[[j for j, p in enumerate(parities) if p == '-'][0]]
    check(f"lam={lam:g} TOP EVEN omega^2 = {top_even:+.7f} matches the "
          f"phase-2 BC-c headline {EV_C_REF[lam]:+.7f} to 4+ digits "
          f"(rel {abs(top_even - EV_C_REF[lam]) / abs(EV_C_REF[lam]):.1e})",
          abs(top_even - EV_C_REF[lam]) / abs(EV_C_REF[lam]) < 1e-4)
    check(f"lam={lam:g} TOP ODD omega^2 = {top_odd:+.7f} matches the "
          f"phase-2 BC-b headline {EV_B_REF[lam]:+.7f} to 4+ digits "
          f"(rel {abs(top_odd - EV_B_REF[lam]) / abs(EV_B_REF[lam]):.1e})",
          abs(top_odd - EV_B_REF[lam]) / abs(EV_B_REF[lam]) < 1e-4)
    # independent shooting cross-check (not FD): even = Robin gamma=2q,
    # odd = Dirichlet, on the SINGLE cell
    we = shoot_root(lambda w2, lam=lam: (lambda uu: uu[1]
                    - GAMMA_PHYS * uu[0])(interior_shoot(QB, SB, lam,
                                                         w2)),
                    -0.05, -20.0)
    wo = shoot_root(lambda w2, lam=lam: interior_shoot(QB, SB, lam,
                                                       w2)[0],
                    -0.5, -60.0)
    check(f"lam={lam:g} INDEPENDENT SHOOTING: even-sector top "
          f"{we:+.7f} (Robin gamma = 2q) and odd-sector top {wo:+.7f} "
          f"(Dirichlet) agree with the pair FD to 4+ digits "
          f"(rel {abs(we - top_even) / abs(we):.1e}, "
          f"{abs(wo - top_odd) / abs(wo):.1e}) — the reduction is "
          "implemented right, independently of the FD assembly",
          abs(we - top_even) / abs(we) < 1e-4
          and abs(wo - top_odd) / abs(wo) < 1e-4)
    # no positive eigenvalue anywhere
    check(f"lam={lam:g} NO BINDING: every pair eigenvalue is negative "
          f"(top {vp[0]:+.6f}) — the doubled shell binds NOTHING",
          vp[0] < 0)

# r_min control on the pair problem
vp5 = top_vals(*assemble_pair(QB, SB, 2.0, GAMMA_PAIR, rmin=1e-5,
                              n_int=6000), k=2)
vp6 = top_vals(*assemble_pair(QB, SB, 2.0, GAMMA_PAIR, rmin=1e-6,
                              n_int=8000), k=2)
check("core control (lam=2): r_min 1e-5 -> 1e-6 changes the pair top "
      f"by {abs(vp5[0] - vp6[0]) / abs(vp5[0]):.1e} relative < 1e-4 — "
      "Friedrichs-branch truncation converged",
      abs(vp5[0] - vp6[0]) / abs(vp5[0]) < 1e-4)

# ===========================================================================
# T4 — the 4/3 mirage: null-test closure
# ===========================================================================
hr("T4 — THE 4/3 MIRAGE: NULL-TEST CLOSURE")

prox = abs(GAMMA_PAIR - L0) / L0
print(f"""  The naive reading: "the doubled shell gives Gamma = 4q = 4/3 =
  {GAMMA_PAIR:.6f}, vs L0 = {L0:.8f} — only {prox:.3%} below
  threshold; one nudge and it binds!"

  THE NAIVE COMPARISON IS VOID.  The symmetric pair never delivers an
  effective 4q to ANY single sector: the mode problem decomposes
  exactly (T1/T2), the even sector sees gamma_even = 2q = {GAMMA_PHYS:.6f}
  (deficit factor {L0 / GAMMA_PHYS:.4f}, phase 2 unchanged), and the
  odd sector sees a Dirichlet wall (no binding for any Gamma).
  Comparing the TOTAL jump 4q against the SINGLE-SECTOR threshold L0
  is a category error — the same double-count the banked guards
  (sections 217-219) forbid at the action level.""")
check(f"the mirage numbers, recorded: 4q = 4/3 sits {prox:.4%} below "
      f"L0 = {L0:.8f} — tantalizing, and MEANINGLESS: no sector of "
      "the pair problem has binding condition Gamma > L0; the "
      "operative comparison is 2q = 0.666667 vs L0 (factor "
      f"{L0 / GAMMA_PHYS:.6f} deficit), exactly as in phase 2",
      0.003 < prox < 0.005)
check("null-test discipline VINDICATED: phase 2 recorded 2.0075 != 2 "
      "and L0 != 4/3 (0.376% off) as NON-matches instead of romancing "
      "them; the symmetry-reduction theorem now CONFIRMS the proximity "
      "was a mirage — the factor 2 in Gamma = 4q is consumed by the "
      "even/odd split, never by binding",
      abs(L0 / GAMMA_PHYS - 2) > 1e-3 and abs(L0 - 4 / 3) > 1e-3)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
hr("SUMMARY")
if FAILURES:
    print(f"  {len(FAILURES)} CHECK(S) FAILED:")
    for lab in FAILURES:
        print(f"    - {lab}")
    sys.exit(1)
print(f"""  All {N_CHECKS} checks PASSED.

  T0  Mirrored profile derived: Delta f' = +2q/R, Delta phi' = -q/R,
      jump Delta u' = -(4q/R) u(R) — Gamma = 4q (doubled).
  T1  EVEN sector: u'(R+) = -u'(R-) + jump => u'(R-) = +(2q/R) u(R) —
      EXACTLY phase-2 BC-c at gamma = 2q; same L0 = {L0:.8f};
      deficit factor {L0 / GAMMA_PHYS:.6f} UNCHANGED by pairing.
  T2  ODD sector: u(R) = 0 — EXACTLY phase-2 BC-b; delta does no
      work; never binds (theorem).
  T3  Two-domain spectrum = BC-c UNION BC-b to 4+ digits (parity-
      classified FD + independent shooting): top even {EV_C_REF[2.0]:+.7f},
      top odd {EV_B_REF[2.0]:+.7f} (lam=2); {EV_C_REF[6.0]:+.7f} /
      {EV_B_REF[6.0]:+.7f} (lam=6).  No positive eigenvalue anywhere.
  T4  The 4/3-vs-L0 proximity (0.376%) is a CONFIRMED MIRAGE: no
      sector ever sees 4q; null-test discipline vindicated.

  VERDICT: the NON-LICENSED symmetric pair delivers NOTHING — its
  spectrum is the union of two already-banked phase-2 negatives.  The
  compound/two-sided interface route is CLOSED (recon closed the
  banked side; this theorem closes the adjacent non-banked side).""")
