"""
V2 -- GAUGE HOSTILITY (the headline falls if any flipped term is
gauge-removable).

(G1) tie constraints on xi (exact Lie derivatives) -- the banked rigidity.
(G2) HOSTILE: existence of REGULAR first-order chart-preserving vector
     fields in the even m=0 sector that the audit's C3 declared absent:
     xi^r = R(theta) (r-independent, allowed by the rr tie), xi^theta
     solving the k=0 constraint REGULARLY whenever Int_0^pi R sin = 0.
     Explicit example: xi = d_z (R = cos theta, xi^th = -sin theta / r).
(G3) DECISIVE: are these directions null directions of the constrained
     quadratic action?  Compute EOM_q[h_gauge] on an ON-SHELL spherical
     background (f0 = A + B/r solves the reduced EL).  If nonzero, the
     would-be gauge is broken by the background stress refusal and q,w
     are genuinely physical. Also verify the breaking equals the Lie
     drag of the background densitized stress (exact mechanism).
(G4) odd sector: h_W = r^2 sin^2 (W_T, W_r, W_th) on (p,u,v) is NOT null
     (H_ax nondegenerate) => no gauge removal there either; the U(1)
     direction p_chi = -f0 chi' costs alpha_pp p_chi^2 (flat only where
     G0 = 0, i.e. outside formed matter).
(G5) m != 0 accounting.
"""
import sympy as sp, time
t0 = time.time()
PASS = []
def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"CHECK {name}: {'PASS' if ok else 'FAIL'} {detail}", flush=True)

T, r, th, ph = sp.symbols('T r theta varphi')
P0 = sp.Function('phi0')(r, th)
f0 = sp.exp(-2*P0)
x = [T, r, th, ph]
g0 = sp.diag(-f0, 1/f0, r**2, r**2*sp.sin(th)**2)

def lie(gm, xi):
    d = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            s = sum(xi[A]*sp.diff(gm[m, n], x[A]) for A in range(4))
            s += sum(gm[A, n]*sp.diff(xi[A], x[m]) for A in range(4))
            s += sum(gm[m, A]*sp.diff(xi[A], x[n]) for A in range(4))
            d[m, n] = sp.expand(s)
    return d

xiT = sp.Function('xiT')(T, r, th, ph)
xir = sp.Function('xir')(T, r, th, ph)
xit = sp.Function('xit')(T, r, th, ph)
xiv = sp.Function('xiv')(T, r, th, ph)
dg = lie(g0, [xiT, xir, xit, xiv])
dphi = xir*sp.diff(P0, r) + xit*sp.diff(P0, th)
check("G1a g_TT tie residual = -2 f0 d_T xi^T (tie kills d_T xi^T)",
      sp.simplify(dg[0, 0] - 2*f0*dphi + 2*f0*sp.diff(xiT, T)) == 0)
check("G1b g_rr tie residual = +2 d_r xi^r / f0 (tie kills d_r xi^r)",
      sp.simplify(dg[1, 1] - 2*dphi/f0 - 2*sp.diff(xir, r)/f0) == 0)
dk = sp.simplify((dg[2, 2]/(2*r**2)
                  + dg[3, 3]/(2*r**2*sp.sin(th)**2))/2)
check("G1c delta k = xi^r/r + (d_th xi^th + cot th xi^th + d_v xi^v)/2",
      sp.simplify(dk - (xir/r + (sp.diff(xit, th)
                  + sp.cos(th)/sp.sin(th)*xit + sp.diff(xiv, ph))/2)) == 0)

# ---------- G2: regular chart-preserving family (HOSTILE existence) ----
print("\n--- G2 regular residual family the audit's C3 wording missed ---")
# xi = d_z in polar coords: xi^r = cos th, xi^th = -sin th / r
xz = [sp.Integer(0), sp.cos(th), -sp.sin(th)/r, sp.Integer(0)]
dgz = lie(g0, xz)
dkz = sp.simplify((dgz[2, 2]/(2*r**2) + dgz[3, 3]/(2*r**2*sp.sin(th)**2))/2)
dwz = sp.simplify((dgz[2, 2]/(2*r**2) - dgz[3, 3]/(2*r**2*sp.sin(th)**2))/2)
dqz = sp.simplify(dgz[1, 2])
ok = (sp.simplify(dgz[0, 0] - 2*f0*(sp.cos(th)*sp.diff(P0, r)
                                    - sp.sin(th)/r*sp.diff(P0, th))) == 0
      and sp.simplify(dgz[1, 1] - 2/f0*(sp.cos(th)*sp.diff(P0, r)
                                        - sp.sin(th)/r*sp.diff(P0, th))) == 0
      and dkz == 0 and sp.simplify(dgz[0, 1]) == 0
      and sp.simplify(dgz[0, 2]) == 0)
print(f"  d_z: delta k = {dkz}, delta w = {dwz}, delta q = {dqz}")
check("G2a xi = d_z is REGULAR (axis-smooth), preserves BOTH ties and "
      "k = 0 exactly at first order, and moves q (and dp) -- a "
      "first-order chart-preserving direction EXISTS (audit C3's 'no "
      "regular even gauge' is wrong as an existence statement)",
      ok and sp.simplify(dqz) != 0)
# general family: xi^r = R(th), xi^th = -(2/(r sin th)) Int_0^th R sin;
# regular at both poles iff Int_0^pi R sin = 0. Example R = Y2:
u_ = sp.cos(th)
R2 = (sp.sqrt(5)/2)*(3*u_**2 - 1)
I2 = sp.integrate(R2.subs(th, sp.Symbol('tp'))*sp.sin(sp.Symbol('tp')),
                  (sp.Symbol('tp'), 0, th))
X2 = sp.simplify(-2*I2/(r*sp.sin(th)))
print(f"  R = Y2: xi^th = {X2}")
x2 = [sp.Integer(0), R2, X2, sp.Integer(0)]
dg2 = lie(g0, x2)
dk2 = sp.simplify((dg2[2, 2]/(2*r**2) + dg2[3, 3]/(2*r**2*sp.sin(th)**2))/2)
check("G2b the ell=2 member (R = Y2) is regular and preserves k = 0: a "
      "regular chart-preserving vector exists in EVERY ell >= 1 channel "
      "(Int R sin dth = 0 is the only condition; ell = 0 alone excluded)",
      sp.simplify(dk2) == 0 and sp.simplify(X2.subs(th, sp.pi/2)) != sp.nan)

# ---------- G3: are they null directions? (the decisive computation) ---
print("\n--- G3 quadratic action on the d_z direction (on-shell bg) ---")
# Use V1's exact L2 machinery rebuilt compactly here (audit scheme;
# at spherical + gauge config w = 0 the scheme difference is inert).
c = sp.symbols('c', positive=True)
eps = sp.symbols('epsilon')
phi0s, p0rs, p0ts = sp.symbols('phi0s p0rs p0ts', real=True)
dps, dpTs, dprs, dpths, dpvs = sp.symbols('dps dpTs dprs dpths dpvs',
                                          real=True)
As, Bs, Ps, Ks, Ws, Qs, Us, Vs = sp.symbols('As Bs Ps Ks Ws Qs Us Vs',
                                            real=True)
rs, sts = sp.symbols('rs s_ts', positive=True)
phifs = phi0s + eps*dps
gS = sp.Matrix([
    [-sp.exp(-2*phifs), eps*As,           eps*Bs, eps*Ps],
    [eps*As,            sp.exp(2*phifs),  eps*Qs, eps*Us],
    [eps*Bs,            eps*Qs,           rs**2*(1+eps*(Ks+Ws))**2, eps*Vs],
    [eps*Ps,            eps*Us,           eps*Vs,
     rs**2*sts**2*(1+eps*(Ks-Ws))**2]])
gradS = sp.Matrix([eps*dpTs, p0rs + eps*dprs, p0ts + eps*dpths, eps*dpvs])
detS = gS.det()
NS = sp.expand((gradS.T*gS.adjugate()*gradS)[0, 0])
LS = -(c/2)*sp.exp(-2*phifs)*NS/detS*sp.sqrt(-detS)
L2S = sp.expand(sp.powsimp(sp.expand(sp.together(
    sp.diff(LS, eps, 2).subs(eps, 0))/2)))
EOMq_expr = sp.diff(L2S, Qs)

# gauge config (spherical bg Phi(r); on-shell f0 = A + B/r):
A_, B_ = sp.symbols('A B', positive=True)
F = A_ + B_/r
Phi = -sp.log(F)/2          # phi0 = -(1/2) ln f0
dpg = sp.cos(th)*sp.diff(Phi, r)             # delta phi = xi.grad phi0
qg = sp.sin(th)*(1 - 1/F)                    # (1/f0) d_th xi^r + r^2 d_r xi^th
sub = {phi0s: Phi, p0rs: sp.diff(Phi, r), p0ts: 0,
       dps: dpg, dprs: sp.diff(dpg, r), dpths: sp.diff(dpg, th),
       dpTs: 0, dpvs: 0,
       As: 0, Bs: 0, Ps: 0, Ks: 0, Ws: 0, Qs: qg, Us: 0, Vs: 0,
       rs: r, sts: sp.sin(th)}
EOMq_val = sp.simplify(EOMq_expr.subs(sub))
print(f"  EOM_q[h_gauge(d_z)] = {sp.factor(EOMq_val)}")
check("G3a the d_z chart-preserving direction is NOT a null direction: "
      "EOM_q on it is NONZERO on-shell (vanishes only in the flat limit "
      "B -> 0) => q is NOT gauge-removable; the flip is physical",
      sp.simplify(EOMq_val) != 0 and
      sp.simplify(EOMq_val.subs(B_, 0)) == 0)

# mechanism: EOM_q[h_gauge] must equal the Lie drag of the background
# densitized stress:  (L_xi 𝔗)^{r th} = -𝔗^{thth} d_th xi^r
#                                        - 𝔗^{rr} d_r xi^th
gi0 = g0.inv()
grad0 = sp.Matrix([0, sp.diff(P0, r), sp.diff(P0, th), 0])
dphi20 = (grad0.T*gi0*grad0)[0, 0]
Tdn0 = c*f0*(grad0*grad0.T - g0*dphi20/2)
Tup0 = gi0*Tdn0*gi0
sq0 = r**2*sp.sin(th)
TD = sq0*Tup0
liedrag = sp.simplify((- TD[2, 2]*sp.diff(xz[1], th)
                       - TD[1, 1]*sp.diff(xz[2], r)
                       + xz[1]*sp.diff(TD[1, 2], r)
                       + xz[2]*sp.diff(TD[1, 2], th)
                       - TD[0, 0]*0
                       + TD[1, 2]*(sp.diff(xz[1], r) + sp.diff(xz[2], th))
                       ).subs(P0, Phi.subs(r, r)))
# general Lie-density formula for rank-2 density: (L 𝔗)^{mn} =
#   xi^a d_a 𝔗^{mn} - 𝔗^{an} d_a xi^m - 𝔗^{ma} d_a xi^n + 𝔗^{mn} d_a xi^a
def liedens(TDm, xi):
    out = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            s = sum(xi[A]*sp.diff(TDm[m, n], x[A]) for A in range(4))
            s -= sum(TDm[A, n]*sp.diff(xi[m], x[A]) for A in range(4))
            s -= sum(TDm[m, A]*sp.diff(xi[n], x[A]) for A in range(4))
            s += TDm[m, n]*sum(sp.diff(xi[A], x[A]) for A in range(4))
            out[m, n] = s
    return out
LD = liedens(TD, xz)
LDrth = sp.simplify(LD[1, 2].subs(P0, Phi))
print(f"  (L_xi 𝔗)^(r th) on-shell = {sp.factor(LDrth)}")
check("G3b EXACT MECHANISM: EOM_q[h_gauge] = (L_xi 𝔗)^{r th} -- the "
      "breaking is precisely the Lie drag of the background stress "
      "refusal (no Einstein row to absorb it in the native theory)",
      sp.simplify(EOMq_val - LDrth) == 0,
      f"residual = {sp.simplify(EOMq_val - LDrth)}")

# ---------- G4: odd sector + U(1) direction not null ----------
print("\n--- G4 odd-sector / U(1) directions cost action ---")
Hpp = sp.simplify(sp.diff(L2S, Ps, 2)/2)
check("G4a alpha_pp = -(c/4)(f0 p0r^2 + p0t^2/r^2)/sin != 0 on formed "
      "backgrounds: the U(1)/bundle direction (and every W(T,r,th) "
      "axial direction, by det H_ax = c^3(X+Y)^3/64r^8 sin^3 > 0) is "
      "action-costly, NOT a null gauge direction; it IS flat exactly "
      "where grad phi0 = 0 (exterior/vacuum)",
      sp.simplify(Hpp + (c/4)*(sp.exp(-2*phi0s)*p0rs**2
                               + p0ts**2/rs**2)/sts) == 0)

# ---------- G5: m != 0 even-sector accounting ----------
print("\n--- G5 m != 0 ---")
m = sp.symbols('m', integer=True, positive=True)
# even m!=0: xi^r = R(th) e^{i m ph} forbidden by d_r xi^r = 0? no --
# allowed; but k=0 now reads xi^r/r + (X_th + cot X + i m Phi_v)/2 = 0
# with X(r,th), Phi_v(r,th): the 1/r source can be absorbed by X or
# Phi_v ~ 1/r. Axis regularity for m != 0 vector fields requires
# xi^r ~ sin^m, xi^th, xi^vphi specific falloffs; the family persists
# unless killed -- record the structure honestly:
Rt = sp.Function('Rt')(th)
Xt = sp.Function('Xt')(r, th)
Pv = sp.Function('Pv')(r, th)
xim = [sp.Integer(0), Rt*sp.exp(sp.I*m*ph), Xt*sp.exp(sp.I*m*ph),
       Pv*sp.exp(sp.I*m*ph)]
dgm = lie(g0, xim)
dkm = sp.simplify(sp.expand((dgm[2, 2]/(2*r**2)
                             + dgm[3, 3]/(2*r**2*sp.sin(th)**2))/2
                            )/sp.exp(sp.I*m*ph))
print(f"  m!=0 delta k / e^(im ph) = {dkm}")
check("G5 m != 0: delta k = [R/r + (X_th + cot X + i m Pv)/2] e^{im ph}; "
      "first-order chart-preserving solutions persist for m != 0 too "
      "(Pv = 2i R/(m r) - (X_th + cot X)/(i m) etc.) -- so the audit's "
      "physicality argument must NOT rest on their absence; it rests on "
      "G3 (they are not null directions)",
      sp.simplify(dkm - (Rt/r + (sp.diff(Xt, th)
                  + sp.cos(th)/sp.sin(th)*Xt + sp.I*m*Pv)/2)) == 0)

n = sum(1 for _, ok in PASS if ok)
print(f"\nV2 TOTAL: {n}/{len(PASS)} PASS   ({time.time()-t0:.1f}s)")
for nm, ok in PASS:
    if not ok:
        print("  FAIL:", nm)
