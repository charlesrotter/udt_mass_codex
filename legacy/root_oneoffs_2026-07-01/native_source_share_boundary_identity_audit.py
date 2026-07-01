#!/usr/bin/env python3
"""
native_source_share_boundary_identity_audit.py

Audit of the last open link of P_domain (negative_phi_native_geometry.md,
verdict 382, ~line 27542): the H1 collar source law s(q) = q/3.

What this script does: an independent single-file re-derivation (sympy)
of the chain through which, on the self-similar branch, the function-valued
law s(q)=q/3 collapses to a single phi0 boundary identity

    collar source DEMANDED by self-similar transport  =  H1-projected
    spatial curvature share SUPPLIED by the phi0 geometry,

which is EXACTLY equivalent to q = 1/3 (supply = demand uniqueness on the
nontrivial branch).

VERIFIER AMENDMENT (2026-06-10): this "supply = demand" framing is a
RESTATEMENT of content already in negative_phi_native_geometry.md --
sections 270 (lines 19297-19326), 285 (lines 20475-20570, verdict 270
"endpoint/collar self-consistency"), 286 (verdict 271), 375, 377, 393,
397/verdict 382, including the generalization q(1-q)/2 = q/N
=> q = 1 - 2/N (lines 29383, 29927). It is banked here as an independent
re-derivation confirming sections 270/285-287, NOT as a new sharpening.
The genuinely new artifact in this file is CHECK E (numerical exclusion
of the pointwise share law).

All checks are exact sympy except the explicitly numerical CHECK E (RK4).

Background facts banked in the repo (verified there, re-verified here where
they enter):
  - radial collar equation:  f_xx + f_x + 2 s f = 0  in x = ln r
  - exact q-flow:            dq/dx = q^2 - q + 2 s,   q = -d ln f / d ln r
  - curvature share:         R3/R2 = 1 - f - r f'  (R3 = 2(1-f-rf')/r^2,
                             R2 = 2/r^2), equal to q exactly at f = 1
  - H1 isotropic projection: <n_a n_b> = delta_ab / 3 (exact)
  - finite C1 action:        S_C1 = (1/4) Int r^2 (f')^2 dr needs p < 1/2
  - no-go: local bulk scalar action cannot produce a q-dependent source
    coefficient (native_curvature_share_action_no_go.py)
"""

import sympy as sp

PASS = []
FAIL = []


def check(label, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    (PASS if ok else FAIL).append(label)
    print(f"  [{tag}] {label}" + (f"  -- {detail}" if detail else ""))
    return ok


def hr(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# symbols
x, t = sp.symbols('x t', real=True)
r = sp.symbols('r', positive=True)  # collar radius r > 0
q, s, p = sp.symbols('q s p', real=True)
R, r_in = sp.symbols('R r_in', positive=True)
A, B, Ap, Bp = sp.symbols('A B Aprime Bprime', real=True)
f = sp.Function('f')

# ---------------------------------------------------------------------------
hr("CHECK A (DEMAND): self-similar profile forces s = q(1-q)/2")
# ---------------------------------------------------------------------------
# f = (R/r)^q  =>  in x = ln r (up to normalization R^q): f = e^{-q x}
f_ss = sp.exp(-q * x)
collar_residual = sp.diff(f_ss, x, 2) + sp.diff(f_ss, x) + 2 * s * f_ss
collar_residual = sp.simplify(collar_residual / f_ss)   # e^{-qx} never zero
print(f"  collar residual / f  =  {collar_residual}")
sol_s = sp.solve(sp.Eq(collar_residual, 0), s)
print(f"  solve for s          =>  s = {sol_s}")
check("A1: collar eq on f=e^{-qx} reduces to q^2 - q + 2s = 0",
      sp.simplify(collar_residual - (q**2 - q + 2 * s)) == 0)
check("A2: unique demanded source s = (q - q^2)/2 = q(1-q)/2",
      len(sol_s) == 1 and sp.simplify(sol_s[0] - q * (1 - q) / 2) == 0,
      f"s = {sp.factor(sol_s[0])}")
# also confirm in r-variable: f=(R/r)^q satisfies the same equation with
# x = ln r, i.e. r^2 f'' + 2 r f' ... -> use d/dx = r d/dr
f_r = (R / r) ** q
lhs_r = (r * sp.diff(r * sp.diff(f_r, r), r)) - r * sp.diff(f_r, r) \
        + r * sp.diff(f_r, r) + 0  # f_xx = r d/dr (r d/dr f)... build directly
f_xx_r = r * sp.diff(r * sp.diff(f_r, r), r)
f_x_r = r * sp.diff(f_r, r)
res_r = sp.simplify((f_xx_r + f_x_r + 2 * (q * (1 - q) / 2) * f_r) / f_r)
check("A3: same statement in r-variable, f=(R/r)^q with s=q(1-q)/2 on-shell",
      res_r == 0, f"residual = {res_r}")

# ---------------------------------------------------------------------------
hr("CHECK B (SUPPLY): phi0 geometry supplies R3/R2 = q, H1 share = q/3")
# ---------------------------------------------------------------------------
fsym, fpsym = sp.symbols('f fprime', real=True)
R3 = 2 * (1 - fsym - r * fpsym) / r**2
R2 = 2 / r**2
share = sp.simplify(R3 / R2)
print(f"  R3/R2 = {share}")
share_phi0 = share.subs({fsym: 1, fpsym: -q / R, r: R})
share_phi0 = sp.simplify(share_phi0)
print(f"  at phi0 (f=1, f'=-q/R, r=R):  R3/R2 = {share_phi0}")
check("B1: R3/R2 = 1 - f - r f' identically",
      sp.simplify(share - (1 - fsym - r * fpsym)) == 0)
check("B2: at phi0 boundary (f=1, f'=-q/R): R3/R2 = q", share_phi0 == q)
# H1 isotropic projection: <n_a n_b> = delta_ab/3; one channel takes 1/3.
n1, n2, n3 = sp.symbols('n1 n2 n3', real=True)
# exact angular average over S^2 of n_a n_b: diagonal entries
theta, phi_ang = sp.symbols('theta phi_ang', real=True)
nvec = sp.Matrix([sp.sin(theta) * sp.cos(phi_ang),
                  sp.sin(theta) * sp.sin(phi_ang),
                  sp.cos(theta)])
area = 4 * sp.pi
avg = sp.Matrix(3, 3, lambda i, j: sp.integrate(
    sp.integrate(nvec[i] * nvec[j] * sp.sin(theta), (theta, 0, sp.pi)),
    (phi_ang, 0, 2 * sp.pi)) / area)
check("B3: <n_a n_b> = delta_ab/3 (exact S^2 average, banked projection)",
      sp.simplify(avg - sp.eye(3) / 3) == sp.zeros(3, 3))
h1_share = share_phi0 / 3
check("B4: H1-projected single-channel share at phi0 = q/3",
      sp.simplify(h1_share - q / 3) == 0,
      "this is the source the phi0 geometry SUPPLIES to the H1 sector")

# ---------------------------------------------------------------------------
hr("CHECK C (SUPPLY = DEMAND): boundary identity <=> q = 1/3 "
   "[independent re-derivation confirming doc sections 270/285-287]")
# ---------------------------------------------------------------------------
identity = sp.Eq(q * (1 - q) / 2, q / 3)
sols = sp.solve(identity, q)
print(f"  q(1-q)/2 = q/3  =>  q in {sorted(sols)}")
check("C1: exact solution set is {0, 1/3}",
      set(sols) == {sp.Integer(0), sp.Rational(1, 3)})
print()
print("  EQUIVALENCE (both directions), on the self-similar branch f=(R/r)^q:")
print("   (=>) If the boundary identity holds [collar source demanded by")
print("        self-similarity = H1-projected curvature share at phi0, i.e.")
print("        q(1-q)/2 = q/3], then q = 0 or q = 1/3; on the nontrivial")
print("        branch (q != 0) necessarily q = 1/3.")
print("   (<=) If q = 1/3, then demand q(1-q)/2 = (1/3)(2/3)/2 = 1/9 and")
print("        supply q/3 = 1/9 coincide, so the boundary identity holds.")
print()
print("  STATUS (verifier amendment): this is NOT new content. It is an")
print("  independent re-derivation confirming negative_phi_native_geometry.md")
print("  sections 270/285-287 (verdicts 270/271), 375, 377, 393, 397/382,")
print("  including the general-N form q(1-q)/2 = q/N => q = 1-2/N")
print("  (doc lines 29383, 29927).")
check("C2: (<=) direction explicitly: at q=1/3 both sides equal 1/9",
      sp.Rational(1, 3) * sp.Rational(2, 3) / 2 == sp.Rational(1, 9)
      and sp.Rational(1, 3) / 3 == sp.Rational(1, 9))
# self-coupled flow form from the doc: substitute s = q/3
flow = q**2 - q + 2 * (q / 3)
flow_target = q * (q - sp.Rational(1, 3))
check("C3: s=q/3 in flow gives dq/dt = q(q - 1/3)",
      sp.simplify(flow - flow_target) == 0, f"flow = {sp.factor(flow)}")
fps = sp.solve(sp.Eq(flow, 0), q)
check("C4: fixed points of self-coupled flow are {0, 1/3}",
      set(fps) == {sp.Integer(0), sp.Rational(1, 3)})

# ---------------------------------------------------------------------------
hr("CHECK D (CHAIN TO P_domain): each link exact")
# ---------------------------------------------------------------------------
print("-- D1: general on-shell solution at constant s = 1/9 --")
s19 = sp.Rational(1, 9)
m = sp.symbols('m', real=True)
char = m**2 + m + 2 * s19
roots = sp.solve(sp.Eq(char, 0), m)
print(f"  characteristic roots of m^2 + m + 2/9 = 0:  m = {sorted(roots)}")
check("D1a: roots m = -1/3, -2/3, i.e. q = -m in {1/3, 2/3}",
      set(roots) == {sp.Rational(-1, 3), sp.Rational(-2, 3)})
q1, q2 = sp.Rational(1, 3), sp.Rational(2, 3)
check("D1b: q-roots are the two flow fixed points of q^2 - q + 2s = 0 (s=1/9)",
      set(sp.solve(sp.Eq(q**2 - q + 2 * s19, 0), q)) == {q1, q2})
check("D1c: Vieta: q1 + q2 = 1 and q1*q2 = 2s = 2/9",
      q1 + q2 == 1 and q1 * q2 == 2 * s19)
f_gen = A * r ** sp.Rational(-1, 3) + B * r ** sp.Rational(-2, 3)
res_gen = sp.simplify(r * sp.diff(r * sp.diff(f_gen, r), r)
                      + r * sp.diff(f_gen, r) + 2 * s19 * f_gen)
check("D1d: f = A r^{-1/3} + B r^{-2/3} solves the collar equation exactly",
      res_gen == 0, f"residual = {res_gen}")

print("-- D2: h-residual decomposition f = (R/r)^p h, p = 1/3 --")
pval = sp.Rational(1, 3)
h_expr = sp.simplify(f_gen / (R / r) ** pval)
h_expr = sp.expand(h_expr)
print(f"  h(r) = f / (R/r)^(1/3) = {h_expr}")
Ap_val = A * R ** sp.Rational(-1, 3)
Bp_val = B * R ** sp.Rational(-1, 3)
h_form = Ap_val + Bp_val * r ** sp.Rational(-1, 3)
check("D2a: on-shell h(r) = A' + B' r^{p - q2} = A' + B' r^{-1/3} "
      "(A'=A R^{-1/3}, B'=B R^{-1/3})",
      sp.simplify(h_expr - h_form) == 0)
check("D2b: exponent p - q2 = 1/3 - 2/3 = -1/3",
      pval - q2 == sp.Rational(-1, 3))
hR = h_form.subs(r, R)
check("D2c: normalization h(R) = 1 reads A' + B' R^{-1/3} = 1",
      sp.simplify(hR - (Ap_val + Bp_val * R ** sp.Rational(-1, 3))) == 0,
      f"h(R) = {sp.simplify(hR)} = 1 imposed")
delta_h = sp.simplify((-r * sp.diff(sp.log(h_form), r)).subs(r, R))
delta_h = sp.simplify(delta_h.subs(A, (1 - Bp_val * R ** sp.Rational(-1, 3))
                                   * R ** sp.Rational(1, 3) / 1))
# recompute cleanly with normalization h(R)=1:
h_norm = (1 - Bp * R ** sp.Rational(-1, 3)) + Bp * r ** sp.Rational(-1, 3)
delta_h_norm = sp.simplify((-r * sp.diff(sp.log(h_norm), r)).subs(r, R))
print(f"  delta_h = -d ln h/d ln r |_R = {delta_h_norm}")
check("D2d: delta_h = (1/3) B' R^{-1/3}, nonzero iff B' != 0 iff B != 0",
      sp.simplify(delta_h_norm - Bp * R ** sp.Rational(-1, 3) / 3) == 0)

print("-- D3 (dependent route -- see verifier finding): value-pinning "
      "algebra --")
print("  VERIFIER FINDING (2026-06-10): D3 is WITHDRAWN as an independent")
print("  route. The decomposition f = (R/r)^p h has gauge freedom in p: for")
print("  ANY B != 0, choosing p* = ln f(r_in) / ln(R/r_in) satisfies y = 0")
print("  at BOTH ends with delta_h != 0, and q_phi0 = p* + delta_h still")
print("  carries the B-mode. The algebra below forces B = 0 only because p")
print("  was frozen at 1/3 FIRST, which presupposes either the finite-action")
print("  filter (making D3 collapse into D4) or an underived two-point")
print("  Dirichlet datum (doc line 30128, section 424, stated only")
print("  conditionally: 'If the endpoint profile normalization absorbs h at")
print("  the inner end'). The two-end pinning argument itself is prior art:")
print("  doc sections 429 (lines 30584-30690), 430, 432. The algebra is")
print("  kept below because it is correct GIVEN p = 1/3 fixed.")
# y = ln h vanishing at both ends <=> h(r_in) = h(R) = 1  (with p frozen
# at 1/3; see gauge-freedom caveat above)
eq_R = sp.Eq(Ap + Bp * R ** sp.Rational(-1, 3), 1)
eq_in = sp.Eq(Ap + Bp * r_in ** sp.Rational(-1, 3), 1)
diff_eq = sp.simplify((eq_in.lhs - eq_R.lhs))
print(f"  h(r_in) - h(R) = {diff_eq} = 0")
check("D3a: subtracting: B'(r_in^{-1/3} - R^{-1/3}) = 0",
      sp.simplify(diff_eq - Bp * (r_in ** sp.Rational(-1, 3)
                                  - R ** sp.Rational(-1, 3))) == 0)
sol_pin = sp.solve([eq_R, eq_in], [Ap, Bp], dict=True)
check("D3b: with r_in != R the unique solution is A'=1, B'=0, hence h == 1",
      len(sol_pin) == 1 and sol_pin[0][Ap] == 1 and sol_pin[0][Bp] == 0,
      f"solution: {sol_pin[0]}")
check("D3c: B'=0 => B=0 (B' = B R^{-1/3}, R > 0)",
      sp.solve(sp.Eq(B * R ** sp.Rational(-1, 3), 0), B) == [0])

print("-- D4: finite C1 action endpoint filter (the carrying route) --")
# f ~ r^{-p}: integrand r^2 (f')^2 ~ p^2 r^{-2p}
f_p = r ** (-p)
integrand = sp.simplify(r**2 * sp.diff(f_p, r) ** 2)
print(f"  r^2 (f')^2 for f = r^-p:  {integrand}")
check("D4a: endpoint integrand = p^2 r^{-2p}",
      sp.simplify(integrand - p**2 * r ** (-2 * p)) == 0)
# Int_0 r^{-2p} dr: antiderivative r^{1-2p}/(1-2p) (p != 1/2);
# finite at r -> 0+ iff exponent 1 - 2p > 0 iff p < 1/2
antider = sp.integrate(r ** (-2 * p), r)
print(f"  antiderivative of r^(-2p): {antider}")
# generic branch (p != 1/2) of the Piecewise antiderivative
antider_generic = antider.args[0][0] if isinstance(antider, sp.Piecewise) \
    else antider
check("D4b: antiderivative exponent 1-2p; endpoint r->0 finite iff "
      "1-2p > 0 iff p < 1/2",
      sp.simplify(antider_generic - r ** (1 - 2 * p) / (1 - 2 * p)) == 0
      and sp.solve_univariate_inequality(1 - 2 * p > 0, p)
      == (p < sp.Rational(1, 2)),
      f"generic branch {antider_generic}; "
      f"solve(1-2p>0) -> {sp.solve_univariate_inequality(1 - 2 * p > 0, p)} "
      f"(p=1/2 marginal branch log r also diverges at r->0)")
check("D4c: q1 = 1/3 < 1/2 finite;  q2 = 2/3 >= 1/2 divergent",
      bool(q1 < sp.Rational(1, 2)) and bool(q2 >= sp.Rational(1, 2)))
# divergence of the q2 mode explicitly:
I_q2 = sp.integrate(r ** (-2 * q2), (r, 0, 1))
check("D4d: Int_0^1 r^{-4/3} dr = oo (q2-mode endpoint action diverges)",
      I_q2 == sp.oo, f"integral = {I_q2}")
# B-mode dominates as r -> 0: |B r^{-2/3}| / |A r^{-1/3}| = |B/A| r^{-1/3}
absA, absB = sp.symbols('absA absB', positive=True)  # |A|, |B| with A,B != 0
ratio_limit = sp.limit((absB * r ** (-q2)) / (absA * r ** (-q1)), r, 0, '+')
check("D4e: B-mode dominates endpoint: lim_{r->0} |B|r^{-2/3}/(|A|r^{-1/3}) "
      "= oo for any B != 0",
      ratio_limit == sp.oo,
      f"limit = {ratio_limit}; ratio = |B/A| r^{{-1/3}}")
print("  => B != 0 forces the endpoint exponent to 2/3 > 1/2,")
print("     hence infinite endpoint C1 action; the finite-action filter")
print("     independently rejects the B-mode.")

print("-- D5: conclusion chain --")
print("  on-shell  +  finite-action filter [D4]")
print("    =>  B = 0  =>  h == 1  =>  delta_h = 0          [D2d]")
print("    =>  q_phi0 = p = 1/3 exactly (no residual exponent)")
print("    =>  the elementary branch IS the mixed-Hodge harmonic")
print("        representative: P_domain content, conditional on the")
print("        premises ledgered in CHECK F.")
print("  NOTE (verifier amendment): the rejection of the B-mode rests on")
print("  D4 (finite action) ALONE. D3 is not an independent second route:")
print("  it is gauge-dependent (p-freedom) and collapses into D4 or into an")
print("  underived two-point Dirichlet datum (doc line 30128, conditional),")
print("  unless that datum is independently derived.")
d_fail = [lbl for lbl in FAIL if lbl.startswith('D')]
check("D5: chain links D1-D4 all verified above",
      not d_fail,
      "all D-links passed" if not d_fail else f"failed: {d_fail}")

# ---------------------------------------------------------------------------
hr("CHECK E (NEW ARTIFACT): numerical exclusion of the pointwise share law, "
   "supporting banked verdicts 267/268")
print("  [This is the genuinely new content of this audit: the LOCAL share")
print("   law s_loc = (1/3)(1 - f(1-q)) does not hold off phi0 and cannot")
print("   sustain s = 1/9 along the collar.]")
# ---------------------------------------------------------------------------
# symbolic part: local share along the collar
q_loc = sp.symbols('q_loc', real=True)
local_share = 1 - fsym - r * fpsym
# with q = -d ln f/d ln r:  r f' = -q f
local_share_q = local_share.subs(fpsym, -q_loc * fsym / r)
local_share_q = sp.simplify(local_share_q)
print(f"  local share R3/R2 = 1 - f - r f' = {local_share_q}  (using rf'=-qf)")
check("E1: local share = 1 - f(1 - q) identically",
      sp.simplify(local_share_q - (1 - fsym * (1 - q_loc))) == 0)
gap = sp.factor(local_share_q - q_loc)
print(f"  (local share) - q = {gap}")
sol_f = sp.solve(sp.Eq(local_share_q, q_loc), fsym)
check("E2: local share = q  <=>  (1-f)(1-q) = 0; solving for f gives f = 1",
      sp.simplify(gap - (1 - fsym) * (1 - q_loc)) == 0 and sol_f == [1],
      "note: the factorization also admits the degenerate root q = 1; "
      "for the physical branch q != 1 the identity holds ONLY at f = 1")
print()
print("  Numerical integration of the LOCAL self-coupled system (RK4):")
print("    dq/dt = q^2 - q + (2/3)(1 - f(1-q)),   df/dt = -q f")
print("    [system as specified; note: as written this is the flow in")
print("     t = +ln r, since q = -d ln f/d ln r gives df/d(ln r) = -qf and")
print("     dq/d(ln r) = q^2 - q + 2s; integrating inward in t = -ln r")
print("     flips both signs. The drift conclusion is direction-independent;")
print("     both runs are reported.]")


def rk4(deriv, y0, t0, t1, n, blowup=1e6):
    """RK4 with a blow-up guard; returns (trajectory, t_stop or None)."""
    hstep = (t1 - t0) / n
    tcur, y = t0, list(y0)
    traj = [(tcur, tuple(y))]
    for _ in range(n):
        k1 = deriv(tcur, y)
        k2 = deriv(tcur + hstep / 2, [y[i] + hstep / 2 * k1[i] for i in range(len(y))])
        k3 = deriv(tcur + hstep / 2, [y[i] + hstep / 2 * k2[i] for i in range(len(y))])
        k4 = deriv(tcur + hstep, [y[i] + hstep * k3[i] for i in range(len(y))])
        y = [y[i] + hstep / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
             for i in range(len(y))]
        tcur += hstep
        if any(abs(v) > blowup or v != v for v in y):
            return traj, tcur
        traj.append((tcur, tuple(y)))
    return traj, None


def s_loc_of(qv, fv):
    return (1.0 / 3.0) * (1.0 - fv * (1.0 - qv))


def run_local(sign, label):
    # sign=+1: system exactly as specified; sign=-1: inward t=-ln r flow
    def deriv(_, y):
        qv, fv = y
        return [sign * (qv * qv - qv + 2.0 * s_loc_of(qv, fv)),
                sign * (-qv * fv)]
    n_steps = 60000  # dt = 1e-4, fine RK4
    traj, t_blow = rk4(deriv, [1.0 / 3.0, 1.0], 0.0, 6.0, n_steps)
    print()
    print(f"  -- {label} --")
    print(f"  {'t':>5} {'q(t)':>14} {'f(t)':>14} {'s_loc(t)':>14} {'s_loc-1/9':>12}")
    marks = [0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    out = {}
    for tm in marks:
        idx = round(tm / 6.0 * n_steps)
        if idx >= len(traj):
            print(f"  {tm:5.1f} {'(blown up)':>14}")
            continue
        tv, (qv, fv) = traj[idx]
        sl = s_loc_of(qv, fv)
        out[tm] = (qv, fv, sl)
        print(f"  {tv:5.1f} {qv:14.8f} {fv:14.6g} {sl:14.8f} {sl - 1/9:12.4e}")
    if t_blow is not None:
        print(f"  ** finite-t blow-up: |q| exceeded 1e6 at t ~ {t_blow:.4f} "
              f"(q'' ~ q^2 growth) **")
    s_vals = [s_loc_of(qq, ff) for _, (qq, ff) in traj]
    drift = max(abs(sv - 1.0 / 9.0) for sv in s_vals)
    sign_change = (min(s_vals) - 1.0 / 9.0) * (max(s_vals) - 1.0 / 9.0) < 0 \
        or min(s_vals) < 0
    q_drift = max(abs(qq - 1.0 / 3.0) for _, (qq, _) in traj)
    print(f"  max |s_loc - 1/9| over run: {drift:.6g}   "
          f"max |q - 1/3|: {q_drift:.6g}   "
          f"s_loc crosses/leaves the s=1/9 level: {sign_change or drift > 0.01}")
    return drift, q_drift, out


drift1, qd1, _ = run_local(+1, "system as specified "
                               "(dq/dt=q^2-q+2s_loc, df/dt=-qf; t = +ln r, outward)")
drift2, qd2, _ = run_local(-1, "sign-flipped inward run (t = -ln r increasing)")
check("E3: local law does NOT sustain s = 1/9: q and s_loc drift off the "
      "fixed point in both directions",
      drift1 > 1e-3 and drift2 > 1e-3 and qd1 > 1e-3 and qd2 > 1e-3,
      f"outward max|s_loc-1/9|={drift1:.4f}, inward={drift2:.4f}")
print()
print("  READING: the start point (f=1, q=1/3) has dq/dt=0 but df/dt != 0;")
print("  once f leaves 1 the local source s_loc=(1/3)(1-f(1-q)) departs from")
print("  1/9 and q is dragged away from 1/3. The LOCAL share law therefore")
print("  cannot be the mechanism that holds s = 1/9 along the collar. The")
print("  working reading must be boundary-anchored: s is SET at phi0 by the")
print("  H1-projected share q/3, and held constant along the collar by a")
print("  transport / scale-covariance premise. That constancy is a SEPARATE")
print("  premise, not a consequence of the local geometry (this check).")

# ---------------------------------------------------------------------------
hr("CHECK F (CIRCULARITY LEDGER)")
# ---------------------------------------------------------------------------
rows = [
    ("(1) stationarity / on-shell",
     "definition of a branch (collar equation imposed)",
     "INDEPENDENT: constitutive; no q=1/3 content by itself"),
    ("(2) constant s along collar",
     "REQUIRES transport premise; NOT independently derived (CHECK E: "
     "local share law drifts, cannot supply constancy)",
     "OPEN PREMISE (ii): separate physical premise, must be banked as such"),
    ("(3) finite-action filter",
     "banked native filter S_C1 = (1/4) Int r^2 (f')^2 dr finite, p < 1/2",
     "INDEPENDENT: already banked; rejects q2 = 2/3 companion (D4); this "
     "is the SOLE carrying route for B=0 (D3 withdrawn, see D5 note)"),
    ("(4) value-pinning BCs y=0 at both ends",
     "OUTER end only: doc lines 29996-30010 state the phi0 normalization "
     "h(R)=1, y(R)=0. The INNER-end statement is doc line 30128 "
     "(section 424) and is CONDITIONAL ('If the endpoint profile "
     "normalization absorbs h at the inner end'). Two-end pinning prior "
     "art: sections 429 (lines 30584-30690), 430, 432",
     "NOT independent (verifier): D3 has gauge freedom in p; the two-point "
     "Dirichlet datum is underived, so D3 is unavailable and D4 must carry "
     "the rejection alone"),
    ("(5) boundary identity s(phi0) = q/3 (source product rule)",
     "re-derived equivalence (CHECK C, confirming doc sections "
     "270/285-287): given self-similarity it is EQUIVALENT to q = 1/3",
     "OPEN PREMISE (i): NOT an independent derivation of q=1/3; it cannot "
     "close P_domain unless derived from the variational principle "
     "(cf. native_curvature_share_action_no_go.py: a local bulk scalar "
     "action cannot produce the q-dependent coefficient)"),
    ("(6) self-similarity p = q on the collar",
     "assumed throughout CHECKs A and C; the doc's section 393 "
     "Alternative B (split boundary layer) is a live alternative",
     "OPEN PREMISE (iii): separate premise, not derived here"),
]
w1 = max(len(rw[0]) for rw in rows)
print(f"  {'premise':<{w1}} | provenance | independence status")
print("  " + "-" * 76)
for name, prov, indep in rows:
    print(f"  {name:<{w1}}")
    print(f"  {'':<{w1}} | provenance:   {prov}")
    print(f"  {'':<{w1}} | independence: {indep}")
    print("  " + "-" * 76)
print()
print("  OPEN-PREMISE COUNT (verifier amendment): THREE premises remain")
print("  between the banked geometry and P_domain, not one:")
print("    (i)   the source product rule s(phi0) = q/3 from the UDT")
print("          variational principle  [row 5]")
print("    (ii)  collar constancy / transport of s  [row 2; CHECK E shows")
print("          the local geometry cannot supply it]")
print("    (iii) self-similarity p = q  [row 6; vs section 393")
print("          Alternative B, split boundary layer]")

# ---------------------------------------------------------------------------
hr("SUMMARY")
# ---------------------------------------------------------------------------
print(f"  checks passed: {len(PASS)}   checks failed: {len(FAIL)}")
if FAIL:
    print("  FAILED CHECKS:")
    for lbl in FAIL:
        print(f"    - {lbl}")

hr("FINAL VERDICT")
print(
    "P_domain is NOT closed by this audit. The conditional statement "
    "[boundary identity + self-similar transport + finite action + "
    "stationarity] => P_domain is a single-file COMPOSITION of banked "
    "verdicts (178 + 267/268 + 270/271/272 + 382), reconfirming the "
    "existing localization in negative_phi_native_geometry.md -- it is not "
    "a new theorem and does not narrow the gap. THREE open premises stand "
    "between the banked geometry and P_domain: (i) the source product rule "
    "s(phi0)=q/3 from the UDT variational principle; (ii) collar "
    "constancy/transport of s (CHECK E: cannot come from the local "
    "geometry); (iii) self-similarity p=q (vs section 393 Alternative B, "
    "split boundary layer). The genuinely new artifact here is CHECK E's "
    "numerical exclusion of the pointwise share law, supporting banked "
    "verdicts 267/268."
)
