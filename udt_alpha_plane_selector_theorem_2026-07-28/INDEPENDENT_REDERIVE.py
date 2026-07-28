#!/usr/bin/env python3
"""
BLIND INDEPENDENT RE-DERIVATION of the alpha plane selector theorem.
Written from the metric definition only; does NOT reuse the package script.

Part A: jet-symbol algebra (my own construction of the Gram matrices from
        the one-form expansion of g, not copied).
Part B: honest 4D coordinate model on R x S3 (Hopf coordinates), general
        profiles u(eta), w(eta), symbolic alpha -- tests the Gram entries,
        the D matrices, the Killing property of Y, L_Y A = 0, and the
        Cartan identity df = -i_Y F(X) against the jet formalism.
Part C: witness control and the parent sec.6 identity (general stratum
        version with 1/S, and the witness version without).
Part D: F-D covariance checks done my way.
"""
import sympy as sp

fails = []
def chk(name, expr_zero):
    if hasattr(expr_zero, '__iter__'):
        ok = all(sp.simplify(sp.cancel(sp.together(sp.expand(e)))) == 0 for e in expr_zero)
    elif isinstance(expr_zero, bool):
        ok = expr_zero
    else:
        e = sp.cancel(sp.together(sp.expand(expr_zero)))
        ok = (e == 0) or (sp.simplify(e) == 0) or (sp.simplify(sp.trigsimp(e)) == 0)
    print(("PASS" if ok else "FAIL"), name)
    if not ok:
        fails.append(name)
    return ok

# ---------------------------------------------------------------- Part A
u, b = sp.symbols('u b', positive=True)
f, df, db, chi, alpha = sp.symbols('f df db chi alpha', real=True)
cE = sp.Symbol('c_E', real=True, nonzero=True)

def Xd(e):
    e = sp.sympify(e)
    return sp.expand(-2*chi*u*sp.diff(e, u) + df*sp.diff(e, f) + db*sp.diff(e, b))

# Build Gram entries MYSELF from g = -u(cE dt + alpha A)^2 + u^-1 A^2 + q_B
# with dt(K)=1, dt(V)=dt(Y)=0, A(K)=0, A(V)=1, A(Y)=f,
# q_B(K,.)=q_B(V,.)=0, q_B(Y,Y)=q_B(H,H)=b  (H=Y-fV, q_B(V,.)=0).
def gpair(dtx, Ax, qx, dty, Ay, qxy):
    return -u*(cE*dtx + alpha*Ax)*(cE*dty + alpha*Ay) + Ax*Ay/u + qxy

gKK = gpair(1, 0, 0, 1, 0, 0)          # -> -cE^2 u
gKV = -u*(cE*1 + alpha*0)*(cE*0 + alpha*1) + 0*1/u + 0
gVV = -u*(alpha*1)**2 + 1/u + 0
gKY = -u*(cE*1)*(alpha*f) + 0 + 0
gVY = -u*(alpha)*(alpha*f) + f/u + 0    # not needed but built for sanity
gYY = -u*(alpha*f)**2 + f*f/u + b

chk("A0_gram_entries", [gKK + cE**2*u, gKV + alpha*cE*u,
                        gVV - (1/u - alpha**2*u), gKY + alpha*cE*u*f,
                        gYY - ((1/u - alpha**2*u)*f**2 + b)])

GKV = sp.Matrix([[gKK, gKV], [gKV, gVV]])
GKY = sp.Matrix([[gKK, gKY], [gKY, gYY]])
S = b*u + f**2

chk("A1_detGKV", GKV.det() + cE**2)
chk("A2_detGKY", GKY.det() + cE**2*S)

DKV = sp.simplify(GKV.inv() * GKV.applyfunc(Xd))
chk("A3_DKV_lower_zero", DKV[1, 0])
chk("A3_DKV_00", DKV[0, 0] + 2*chi)
chk("A3_DKV_11", DKV[1, 1] - 2*chi)
chk("A3_DKV_01", DKV[0, 1] + 4*alpha*chi/cE)

DKY = sp.simplify(GKY.inv() * GKY.applyfunc(Xd))
chk("A4_DKY_off", DKY[1, 0] + alpha*cE*df*u**2/S)
chk("A5_trace", sp.trace(DKY) - Xd(S)/S)
chk("A6_XdetGKY", Xd(GKY.det()) + cE**2*Xd(S))
chk("A7_XS", Xd(S) - (db*u - 2*chi*u*b + 2*f*df))

# alpha = 0 sub-case
D0 = sp.simplify(DKY.subs(alpha, 0))
chk("A8_diag", [D0[0, 1], D0[1, 0]])
chk("A8_rate0", D0[0, 0] + 2*chi)
chk("A8_rate1_minus_2chi", D0[1, 1] - 2*chi - Xd(S)/S)
E = f**2/u + b
chk("A8_rate1_logE", D0[1, 1] - Xd(E)/E)

# T6 general line W = mV + nY (my own gram build)
m, n = sp.symbols('m n', real=True)
AW = m*1 + n*f
qWW = n**2*b                      # q_B(mV+nY, mV+nY) = n^2 b
gKW = -u*(cE)*(alpha*AW)
gWW = -u*(alpha*AW)**2 + AW**2/u + qWW
GKW = sp.Matrix([[gKK, gKW], [gKW, gWW]])
chk("A9_T6_det", GKW.det() + cE**2*((m + n*f)**2 + n**2*b*u))
chk("A9_T6_Xdet", Xd(GKW.det()) + cE**2*(2*m*n*df + n**2*Xd(S)))

# stratum identity (general, WITH 1/S) -- my own derivation route:
# impose X(S)=0 by db -> (2*chi*u*b - 2*f*df)/u
dbs = (2*chi*u*b - 2*f*df)/u
Dc = sp.simplify(DKY.subs(db, dbs))
chk("A10_stratum_identity_generalS",
    Dc.det() + 4*chi**2 - alpha**2*u**2*df**2/S)
# and confirm the WITNESS form (no 1/S) is NOT a general-stratum identity:
resid = sp.simplify(Dc.det() + 4*chi**2 - alpha**2*u**2*df**2)
num = resid.subs({u: 2, b: 1, f: 1, chi: sp.Rational(1, 3),
                  df: 1, alpha: 1, cE: 1})
chk("A10b_witnessform_fails_off_S1", bool(sp.simplify(num) != 0))

# ---------------------------------------------------------------- Part B
# Honest 4D model: coords (t, eta, xi1, xi2); A = cos^2(eta) dxi1 + sin^2(eta) dxi2
t, eta, x1, x2 = sp.symbols('t eta xi1 xi2', real=True)
U = sp.Function('U', positive=True)(eta)      # u(eta)
W = sp.Function('W', positive=True)(eta)      # w(eta), b = w^2
P = sp.Function('P', positive=True)(eta)      # q_B radial coefficient
al = sp.Symbol('alpha', real=True)

coords = [t, eta, x1, x2]
# one-form components in coordinate basis:
dt_c = sp.Matrix([1, 0, 0, 0])
A_c = sp.Matrix([0, 0, sp.cos(eta)**2, sp.sin(eta)**2])
mu_c = sp.Matrix([0, 0, sp.Rational(1, 2), -sp.Rational(1, 2)])   # mu(H)=1, mu(V)=0
de_c = sp.Matrix([0, 1, 0, 0])

theta = cE*dt_c + al*A_c
g4 = (-U*theta*theta.T + (A_c*A_c.T)/U + P**2*(de_c*de_c.T)
      + W**2*(mu_c*mu_c.T))
g4 = sp.simplify(g4)

Kv = sp.Matrix([1, 0, 0, 0])
Vv = sp.Matrix([0, 0, 1, 1])
Yv = sp.Matrix([0, 0, 1, -1])

fw = sp.cos(2*eta)                    # A(Y) in this model
bw = W**2                             # q_B(H,H)
chk("B0_AY_is_cos2eta", (A_c.T*Yv)[0] - fw)
Hv = Yv - fw*Vv
chk("B0_b_is_w2", (Hv.T*g4*Hv)[0] - (-U*(al*(A_c.T*Hv)[0])**2
                                     + ((A_c.T*Hv)[0])**2/U + bw))
chk("B0_AH_zero", (A_c.T*Hv)[0])

gKK4 = (Kv.T*g4*Kv)[0]
gKV4 = (Kv.T*g4*Vv)[0]
gVV4 = (Vv.T*g4*Vv)[0]
gKY4 = (Kv.T*g4*Yv)[0]
gYY4 = (Yv.T*g4*Yv)[0]
chk("B1_gram_vs_family", [
    gKK4 + cE**2*U,
    gKV4 + al*cE*U,
    gVV4 - (1/U - al**2*U),
    gKY4 + al*cE*U*fw,
    gYY4 - ((1/U - al**2*U)*fw**2 + bw)])

# Killing check for K, V, Y (coordinate Lie derivative of the metric matrix)
def lie_g(vec):
    L = sp.zeros(4, 4)
    for iA in range(4):
        for jA in range(4):
            s = sum(vec[k]*sp.diff(g4[iA, jA], coords[k]) for k in range(4))
            s += sum(g4[k, jA]*sp.diff(vec[k], coords[iA]) for k in range(4))
            s += sum(g4[iA, k]*sp.diff(vec[k], coords[jA]) for k in range(4))
            L[iA, jA] = sp.simplify(s)
    return L

chk("B2_K_killing", list(lie_g(Kv)))
chk("B2_V_killing", list(lie_g(Vv)))
chk("B2_Y_killing", list(lie_g(Yv)))

# L_Y A = 0 directly (components of A are eta-only, Y has no eta component):
LYA = sp.Matrix([sum(Yv[k]*sp.diff(A_c[iA], coords[k]) for k in range(4))
                 + sum(A_c[k]*sp.diff(Yv[k], coords[iA]) for k in range(4))
                 for iA in range(4)])
chk("B3_LYA_zero", list(LYA))

# Cartan: df(X) = -F(Y, X) with F = dA, X = d/deta
Fcomp = sp.zeros(4, 4)
for iA in range(4):
    for jA in range(4):
        Fcomp[iA, jA] = sp.diff(A_c[jA], coords[iA]) - sp.diff(A_c[iA], coords[jA])
FYX = sum(Yv[iA]*Fcomp[iA, jA]*(sp.Matrix([0, 1, 0, 0]))[jA]
          for iA in range(4) for jA in range(4))
chk("B4_cartan_df", sp.diff(fw, eta) + FYX)
chk("B4_df_value", sp.diff(fw, eta) + 2*sp.sin(2*eta))
# i_V F = 0 (F basic)
iVF = sp.Matrix([sum(Vv[iA]*Fcomp[iA, jA] for iA in range(4)) for jA in range(4)])
chk("B4_F_basic", list(iVF))

# D matrices from the 4D model via d/deta vs the jet formulas
chi4 = -sp.diff(U, eta)/(2*U)
subjet = {u: U, f: fw, b: bw, chi: chi4, df: sp.diff(fw, eta),
          db: sp.diff(bw, eta), alpha: al}
GKV4 = sp.Matrix([[gKK4, gKV4], [gKV4, gVV4]])
GKY4 = sp.Matrix([[gKK4, gKY4], [gKY4, gYY4]])
DKV4 = sp.simplify(GKV4.inv()*GKV4.diff(eta))
DKY4 = sp.simplify(GKY4.inv()*GKY4.diff(eta))
chk("B5_DKV_model_vs_jet", list(sp.simplify(DKV4 - DKV.subs(subjet))))
chk("B5_DKY_model_vs_jet", list(sp.simplify(DKY4 - DKY.subs(subjet))))
chk("B6_T2_off_model",
    sp.simplify(DKY4[1, 0] + (al*cE*sp.diff(fw, eta)*U**2
                              / (bw*U + fw**2))))
chk("B7_detGKY_model", sp.simplify(GKY4.det() + cE**2*(bw*U + fw**2)))

# ---------------------------------------------------------------- Part C
eps = sp.Symbol('epsilon', positive=True)
uw_ = 1 + eps*(1 - fw**2)
bw_ = (1 - fw**2)/uw_
chk("C0_witness_on_stratum", sp.simplify(bw_*uw_ + fw**2 - 1))
chiw_ = -sp.diff(uw_, eta)/(2*uw_)
# both planes, alpha=0, direct d/deta:
GKVw = sp.Matrix([[-cE**2*uw_, 0], [0, 1/uw_]])
GKYw = sp.Matrix([[-cE**2*uw_, 0], [0, fw**2/uw_ + bw_]])
chk("C1_planes_equal_gram", list(sp.simplify(GKVw - GKYw)))
for nm, GG in (("KV", GKVw), ("KY", GKYw)):
    DD = sp.simplify(GG.inv()*GG.diff(eta))
    chk(f"C2_{nm}_det_const", sp.simplify(sp.diff(GG.det(), eta)))
    chk(f"C2_{nm}_offs", [DD[0, 1], DD[1, 0]])
    chk(f"C2_{nm}_rates", [sp.simplify(DD[0, 0] + 2*chiw_),
                           sp.simplify(DD[1, 1] - 2*chiw_)])
# parent sec.6 identity ON the witness with symbolic alpha (via my jet DKY):
wsub = {u: uw_, f: fw, b: bw_, chi: chiw_, df: sp.diff(fw, eta),
        db: sp.diff(bw_, eta)}
DKYw_a = DKY.subs(wsub)
chk("C3_parent6_on_witness",
    sp.simplify(sp.trigsimp(sp.simplify(DKYw_a.det()) + 4*chiw_**2
                            - alpha**2*uw_**2*(sp.diff(fw, eta))**2)))
# df on witness interior: -2 sin 2eta, zero only at eta = 0, pi/2
sols = sp.solveset(sp.sin(2*eta), eta, sp.Interval.open(0, sp.pi/2))
chk("C4_df_nonzero_interior", sols is sp.S.EmptySet or len(list(sols)) == 0)

# ---------------------------------------------------------------- Part D
sig, lam, cc = sp.symbols('sigma lam c', real=True, nonzero=True)
B = sp.Matrix([[1, sig], [0, lam]])
Gp = B.T*GKY*B
Dp = sp.simplify(Gp.inv()*Gp.applyfunc(Xd))
chk("D1_det_scale", sp.simplify(Gp.det() - lam**2*GKY.det()))
chk("D2_similarity", list(sp.simplify(Dp - B.inv()*DKY*B)))
chk("D3_off_scale", sp.simplify(Dp[1, 0] - DKY[1, 0]/lam))
Dsc = DKY.subs({chi: cc*chi, df: cc*df, db: cc*db}, simultaneous=True)
chk("D4_X_rescale", list(sp.simplify(Dsc - cc*DKY)))
# K rescale K -> aK: certificate invariance (det scales const, line property)
a_ = sp.Symbol('a', real=True, nonzero=True)
BK = sp.Matrix([[a_, 0], [0, 1]])
GpK = BK.T*GKY*BK
DpK = sp.simplify(GpK.inv()*GpK.applyfunc(Xd))
chk("D5_K_rescale_det", sp.simplify(GpK.det() - a_**2*GKY.det()))
chk("D5_K_rescale_sim", list(sp.simplify(DpK - BK.inv()*DKY*BK)))
# Y -> -Y sign: f -> -f, df -> -df; certificate quantities invariant
chk("D6_Y_sign_S", sp.simplify(S.subs(f, -f) - S))
chk("D6_Y_sign_off", sp.simplify(DKY[1, 0].subs({f: -f, df: -df},
                                                simultaneous=True)
                                 + DKY[1, 0]))  # off entry flips sign only
print()
print("FAILURES:", fails if fails else "none -- all independent checks pass")
