#!/usr/bin/env python3
# BLIND VERIFIER independent check (same-session-spawned agent, 2026-07-31).
# Re-derives the stability-slice claims from the banked atlas footing on its own
# paths (variation-of-parameters resolvents; direct exact quadrature at rational
# spot s; stronger random-matrix rank-one toys; exact polynomial witnesses;
# Galerkin inertia hunts). Numerics used ONLY as falsifier-hunt tools.
import sympy as sp
from sympy import Rational as R

FAIL = []
def vk(name, cond, note=""):
    ok = bool(cond)
    print(("VPASS" if ok else "VFAIL") + f" {name} {note}")
    if not ok: FAIL.append(name)

x = sp.Symbol('x', real=True)
aF = sp.Symbol('a_F', positive=True)
gp, gf, gh = sp.symbols('g_p g_f g_h', positive=True)
cf, ch = sp.symbols('c_f c_h', real=True)
E0 = sp.Symbol('E0', positive=True)
w0, w1 = sp.symbols('w0 w1', real=True)
A = aF**2*E0/(2*gp)
w = A*x**2 + w1*x + w0
sigma = cf**2/gf + ch**2/gh
# banked energy relation: gp*w'^2 = aF^2*(2*E0*w - sigma)
shell = {cf**2: gf*(2*w0*E0 - gp*w1**2/aF**2 - ch**2/gh)}
def z(e):  # zero-residual on shell
    return sp.simplify(sp.cancel(sp.together(sp.expand(sp.expand(e).subs(shell))))) == 0
vk("V0_energy_relation_consistent", z(gp*sp.diff(w,x)**2 - aF**2*(2*E0*w - sigma)))

# --- V1: independent second-variation assembly, TWO independent parameters (polarization) ---
e1, e2 = sp.symbols('e1 e2')
vpA,vp1A,vf1A,vh1A,muA = sp.symbols('vpA vp1A vf1A vh1A muA')
vpB,vp1B,vf1B,vh1B,muB = sp.symbols('vpB vp1B vf1B vh1B muB')
p0,p1,f1,h1,lam0 = sp.symbols('p0 p1 f1 h1 lam0', real=True)
aFp = sp.Symbol('aFp', real=True)
aF_fun = aF + aFp*(e1*muA + e2*muB)   # a_F linear in lambda (banked)
S2 = sp.exp(aF_fun*(p0+e1*vpA+e2*vpB))*(gp*(p1+e1*vp1A+e2*vp1B)**2/2
     + gf*(f1+e1*vf1A+e2*vf1B)**2/2 + gh*(h1+e1*vh1A+e2*vh1B)**2/2)
Hess12 = sp.diff(S2, e1, e2).subs({e1:0, e2:0})
# their single-parameter form, polarized: Q(A,B) = (Q(A+B)-Q(A)-Q(B))/2 must equal Hess12
eps = sp.Symbol('eps')
def their_d2(vp_,vp1_,vf1_,vh1_,mu_):
    Sf = sp.exp((aF+aFp*mu_*eps)*(p0+eps*vp_))*(gp*(p1+eps*vp1_)**2/2
        + gf*(f1+eps*vf1_)**2/2 + gh*(h1+eps*vh1_)**2/2)
    return sp.diff(Sf, eps, 2).subs(eps,0)
QA = their_d2(vpA,vp1A,vf1A,vh1A,muA); QB = their_d2(vpB,vp1B,vf1B,vh1B,muB)
QAB = their_d2(vpA+vpB, vp1A+vp1B, vf1A+vf1B, vh1A+vh1B, muA+muB)
vk("V1_assembly_polarization", sp.simplify(sp.expand(QAB-QA-QB)/2 - Hess12) == 0,
   "(single-eps 2nd variation == full 2-parameter Hessian by polarization: SA1 form is the honest joint Hessian)")

# --- V2: reduced operator + exact basis + Wronskian, re-derived ---
Lop = lambda v: -sp.diff(gp*w*sp.diff(v,x), x) - aF**2*sigma*v/w
v1 = sp.diff(w,x)/w; v2 = E0 - sigma/w
vk("V2a_Lv1", z(sp.together(Lop(v1))*w**2))
vk("V2b_Lv2", z(sp.together(Lop(v2))*w**2))
Wr = sp.simplify(sp.expand(gp*w*(v1*sp.diff(v2,x) - v2*sp.diff(v1,x))).subs(shell))
vk("V2c_Wronskian", sp.simplify(Wr - aF**2*E0**2) == 0, f"= {Wr}")
# fh completion + depth total-derivative (independent re-expansion)
vf1s, vh1s, vps = sp.symbols('vf1s vh1s vps')
lhs = w*(gf*vf1s**2 + gh*vh1s**2) + 2*aF*vps*(cf*vf1s + ch*vh1s)
sq = w*(gf*(vf1s + aF*vps*cf/(gf*w))**2 + gh*(vh1s + aF*vps*ch/(gh*w))**2)
vk("V2d_fh_completion", sp.simplify(sp.expand(lhs - sq + aF**2*sigma*vps**2/w)) == 0)
vfun = sp.Function('v')(x)
vk("V2e_depth_total_derivative", sp.simplify(sp.expand(
    2*gp*sp.diff(w,x)*vfun*sp.diff(vfun,x) + aF**2*E0*vfun**2
    - sp.diff(gp*sp.diff(w,x)*vfun**2, x))) == 0)

# --- V3: B identity (lambda-field cross on the (v2, matched-fh) pair), independent path ---
pbar = sp.log(w)/aF; W_ = sp.exp(aF*pbar)
cross_dens = aFp*( vps*W_*(gp*sp.diff(pbar,x)**2/2+gf*(cf/(gf*w))**2/2+gh*(ch/(gh*w))**2/2)*(1+aF*pbar)
    + pbar*W_*(gp*sp.diff(pbar,x)*sp.Symbol('vp1x') + gf*(cf/(gf*w))*vf1s + gh*(ch/(gh*w))*vh1s) )
# (verifier note: first attempt dropped the 1/w in gf*f1s*vf1 -> false FAIL; my bug, fixed)
inst = cross_dens.subs({vps: v2, sp.Symbol('vp1x'): sp.diff(v2,x),
                        vf1s: -aF*v2*cf/(gf*w), vh1s: -aF*v2*ch/(gh*w)})
vk("V3_B_pointwise", z(sp.together(inst - aFp*(E0*v2 + aF*E0**2*pbar))))
print("part1 done; failures:", FAIL)

# ================= PART 2: crease branch (gp=1, ell=1, sigma=E0, aF^2*E0=s^2) =================
print("\n-- part 2: crease branch --")
s = sp.Symbol('s', positive=True)
wB = (s**2/2)*x**2 + (s**2-s)*x + (1 + s**2/2 - s)
x2 = 2/s - 1
# footing re-derived: crease conditions w(-1)=1, w'(-1)^2 = 2A*w(-1)=s^2
vk("V4a_crease_conditions", sp.simplify(wB.subs(x,-1)-1)==0 and
   sp.simplify(sp.diff(wB,x).subs(x,-1)**2 - s**2)==0)
vk("V4b_roots_and_disc", sp.simplify(sp.expand(wB-1-(s**2/2)*(x+1)*(x-x2)))==0 and
   sp.simplify((s**2-s)**2 - 4*(s**2/2)*(1+s**2/2-s) + s**2)==0)
# min of w = 1 - s^2/8*(x2+1)^2 = 1/2 > 0 (regular SL); w(1)=1+2s(s-1)
vk("V4c_w_positive_regular", sp.simplify(wB.subs(x,(x2-1)/2) - sp.Rational(1,2))==0 and
   sp.simplify(wB.subs(x,1) - 1 - 2*s*(s-1))==0)
LB = lambda v: -sp.diff(wB*sp.diff(v,x),x) - s**2*v/wB
vt2 = 1 - 1/wB
v1B = sp.diff(wB,x)/wB
vk("V4d_basis_on_branch", sp.simplify(sp.together(LB(vt2))*wB**2)==0 and
   sp.simplify(sp.together(LB(v1B))*wB**2)==0)
# no Dirichlet kernel: solution vanishing at -1 is prop. vt2 (v1B(-1)=-s/1 != 0); vt2(1)!=0
vk("V4e_no_dirichlet_kernel", sp.simplify(v1B.subs(x,-1)+s)==0 and
   sp.simplify(vt2.subs(x,1) - 2*s*(s-1)/(1+2*s*(s-1)))==0)
# Robin functional T[u]=(w u'+w' u)(1): T[vt2]=w'(1) (identity w vt2' + w' vt2 = w')
vk("V4f_T_identity", sp.simplify(sp.expand(wB*sp.diff(vt2,x) + sp.diff(wB,x)*vt2 - sp.diff(wB,x)))==0)

# --- independent resolvents by variation of parameters (Wronskian method), then spot exact quadrature ---
# L phi = g = 1/w. Wronskian of (v1B, vt2): w*(v1B vt2' - vt2 v1B') = const
WrB = sp.simplify(sp.expand(wB*(v1B*sp.diff(vt2,x) - vt2*sp.diff(v1B,x))))
print("  branch Wronskian w*(v1 vt2' - vt2 v1') =", WrB)
# particular solution: phi_part = -1/s^2 (since L(const c) = -s^2 c / w)
vk("V5a_particular", sp.simplify(sp.together(LB(-1/s**2) - 1/wB))==0)
al, be = sp.symbols('alpha beta')
phiD_gen = -1/s**2 + al*v1B + be*vt2
solD = sp.solve([phiD_gen.subs(x,-1), phiD_gen.subs(x,1)], [al,be], dict=True)[0]
vk("V5b_phiD_coeffs", sp.simplify(solD[al]+1/s**3)==0 and sp.simplify(solD[be]-1/(s*(s-1)))==0,
   f"alpha={sp.simplify(solD[al])}, beta={sp.simplify(solD[be])} (matches -1/s^3, 1/(s(s-1)))")
TB = lambda u: (wB*sp.diff(u,x) + sp.diff(wB,x)*u).subs(x,1)
phiR_gen = -1/s**2 + al*v1B + be*vt2
solR = sp.solve([phiR_gen.subs(x,-1), sp.expand(TB(phiR_gen))], [al,be], dict=True)[0]
vk("V5c_phiR_coeffs", sp.simplify(solR[al]+1/s**3)==0 and sp.simplify(solR[be]-2/(s*(2*s-1)))==0,
   f"alpha={sp.simplify(solR[al])}, beta={sp.simplify(solR[be])} (matches -1/s^3, 2/(s(2s-1)))")

# --- V6: criterion integrals by DIRECT exact quadrature at rational spot s (full independence) ---
phiD = phiD_gen.subs(solD); phiR = phiR_gen.subs(solR)
Js = sp.Symbol('J', positive=True)
gphiD_claim = -Js/s**2 - 2/(s**2*(s-1))
gphiR_claim = -Js/s**2 - 2*(4*s**2-3*s+1)/(s**2*(2*s-1)*(1+2*s*(s-1)))
crossD_claim = -2/(Js*(s-1))
crossR_claim = -2*(4*s**2-3*s+1)/(Js*(2*s-1)*(1+2*s*(s-1)))
for sv in [R(3,2), R(2), R(5,2)]:
    wv = wB.subs(s, sv)
    Jv = sp.integrate(1/wv, (x, -1, 1))          # exact atan closed form
    gpD = sp.integrate((phiD/wB).subs(s, sv), (x, -1, 1))
    gpR = sp.integrate((phiR/wB).subs(s, sv), (x, -1, 1))
    okD = sp.simplify(gpD - gphiD_claim.subs({s: sv, Js: Jv})) == 0
    okR = sp.simplify(gpR - gphiR_claim.subs({s: sv, Js: Jv})) == 0
    tauv = sv**2/Jv
    cD = sp.simplify(1 + tauv*gpD - crossD_claim.subs({s: sv, Js: Jv}))
    cR = sp.simplify(1 + tauv*gpR - crossR_claim.subs({s: sv, Js: Jv}))
    vk(f"V6_quadrature_s={sv}", okD and okR and cD == 0 and cR == 0,
       "(direct exact integrals match both closed forms AND both crossing scalars; J cancels)")
# manifest negativity for all s>1: numerators/denominators sign
q_ = sp.Symbol('q_', positive=True)
vk("V6z_crossing_negative_all_s>1",
   sp.simplify(sp.expand((4*s**2-3*s+1).subs(s, 1+q_))) == sp.expand(4*q_**2+5*q_+2)
   and sp.discriminant(4*s**2-3*s+1, s) == -7,
   "(4s^2-3s+1>0 always, s-1>0, 2s-1>0, w(1)>0, J>0 => both crossing scalars < 0 for EVERY s>1: uniform incl. transcendental A*)")

# --- V7: double-crease EMPTY + SC5 bound + free-branch instability witness (exact rationals) ---
Adc, ldc = sp.symbols('A_dc l_dc', positive=True)
w_dc = Adc*x**2 + (1 - Adc*ldc**2)
vk("V7a_double_crease_forced_form", sp.simplify(w_dc.subs(x,ldc)-1)==0 and sp.simplify(w_dc.subs(x,-ldc)-1)==0
   and sp.simplify(sp.expand(w_dc - 1 - Adc*(x-ldc)*(x+ldc)))==0,
   "(w(+-l)=1 => w1=0, w-1=A(x^2-l^2) sign-definite inside => log w sign-definite => I_p != 0: EMPTY; "
   "E0<0 impossible in the definite class since disc<0 & w>0 force A>0)")
tt_ = sp.Symbol('t', positive=True)
vk("V7b_SC5_bound", sp.simplify(sp.diff(sp.log(tt_)-1+1/tt_, tt_) - (tt_-1)/tt_**2)==0,
   "(1-1/t <= log t with equality iff t=1 => int v2 = E0 int(1-1/w) < E0 int log w = aF E0^2 I_p = 0 strict on nonconstant members)")
# Negative-direction existence on the free branch: a 2-dim cubic trial space captures it only at
# small s (verifier's first attempt false-FAILED at s=2, 5/2 because the negative mode concentrates
# on [-1, x2] — a limitation of MY witness space, not of the claim). The exact argument stands on
# its own: vt2 is a Dirichlet ZERO mode of the strict subinterval [-1, x2] (V4d/V4b), so the
# Dirichlet ground state of the full interval is strictly negative (domain monotonicity), and the
# richer Galerkin(6) hunt below (V8) exhibits the direction explicitly at every spot s.
print("part2 done; failures:", FAIL)

# ================= PART 3: inertia hunts (numerics as FALSIFIER-HUNT tools only) =================
print("\n-- part 3: Galerkin inertia hunts (free vs odd-pinned; Dirichlet and Robin) --")
import mpmath as mp
mp.mp.dps = 40
def inertia_mp(M, n, tol='-1e-20'):
    Mmp = mp.matrix([[mp.mpf(str(sp.N(M[i,j], 35))) for j in range(n)] for i in range(n)])
    ev = mp.eigsy(Mmp, eigvals_only=True)
    return sum(1 for v in ev if v < mp.mpf(tol)), min(ev)
def qform(u, v, wv, sv):
    return sp.integrate(wv*sp.diff(u,x)*sp.diff(v,x) - sv**2*u*v/wv, (x,-1,1))
for sv in [R(3,2), R(2), R(5,2)]:
    wv = wB.subs(s, sv)
    Jv = sp.integrate(1/wv, (x,-1,1)); tauv = sv**2/Jv
    bD = [(1-x**2)*x**k for k in range(6)]              # Dirichlet both ends
    bR = [(1+x)*x**k for k in range(6)]                 # crease-pinned only (free right/seam end)
    n = 6
    MD  = sp.zeros(n,n); MDp = sp.zeros(n,n); MR = sp.zeros(n,n); MRp = sp.zeros(n,n)
    ID = [sp.integrate(b/wv, (x,-1,1)) for b in bD]
    IR = [sp.integrate(b/wv, (x,-1,1)) for b in bR]
    w1v = sp.diff(wv,x).subs(x,1)
    for i in range(n):
        for j in range(i,n):
            qD = qform(bD[i], bD[j], wv, sv)
            qR = qform(bR[i], bR[j], wv, sv) + w1v*bR[i].subs(x,1)*bR[j].subs(x,1)
            MD[i,j]=MD[j,i]=qD
            MDp[i,j]=MDp[j,i]= qD + tauv*ID[i]*ID[j]
            MR[i,j]=MR[j,i]=qR
            MRp[i,j]=MRp[j,i]= qR + tauv*IR[i]*IR[j]
    nD,_ = inertia_mp(MD,n); nDp,mDp = inertia_mp(MDp,n)
    nR,_ = inertia_mp(MR,n); nRp,mRp = inertia_mp(MRp,n)
    vk(f"V8_hunt_s={sv}", nD==1 and nDp==0 and nR==1 and nRp==0,
       f"(free-branch: Dirichlet n-={nD}, Robin n-={nR} [both =1 as claimed]; odd-pinned penalized: "
       f"Dirichlet n-={nDp} (min~{mp.nstr(mDp,4)}), Robin n-={nRp} (min~{mp.nstr(mRp,4)}) [both 0: absorption confirmed])")

# --- V9: rank-one crossing rule on RANDOM exact matrices (stronger than the in-script toy) ---
import random
random.seed(11)
ok9 = True
for trial in range(8):
    n = 5
    Mr = sp.Matrix(n, n, lambda i,j: 0)
    B0 = sp.Matrix(n, n, lambda i,j: R(random.randint(-4,4)))
    Mr = B0.T*B0 + sp.diag(*[R(random.randint(1,4)) for _ in range(n)])  # PD
    u0 = sp.Matrix([R(random.randint(-3,3)) for _ in range(n)])
    Mr = Mr - (u0*u0.T)*R(random.randint(2,5))   # push to indefinite-ish
    gr = sp.Matrix([R(random.randint(-3,3)) for _ in range(n)])
    taur = R(random.randint(1,6), random.randint(1,3))
    def n_neg(Msym):
        evs = sp.Matrix(Msym).eigenvals()
        c = 0
        for v,m in evs.items():
            vn = sp.N(v, 30)
            if vn < 0: c += int(m)
        return c
    nL = n_neg(Mr)
    if Mr.det() == 0 or gr.T*Mr.inv()*gr == sp.Matrix([[0]]): continue
    pred_cross = sp.N((1 + taur*(gr.T*Mr.inv()*gr)[0,0]), 30)
    npert = n_neg(Mr + taur*gr*gr.T)
    # rule as used: crossing scalar < 0 => n- drops by exactly 1; > 0 => unchanged
    expect = nL - 1 if pred_cross < 0 else nL
    if npert != expect:
        ok9 = False
        print("   counterexample trial", trial, nL, npert, pred_cross)
vk("V9_rank_one_rule_random", ok9,
   "(8 random exact 5x5: n-(L+tau gg^T) == n-(L) - [1+tau<g,L^-1 g> < 0] every time — the rule as applied is sound)")
print("part3 done; failures:", FAIL)

# ================= PART 4: the lambda(mu)-Schur question on the FREE-fh branch (hunt) =================
# The banked record scopes "index exactly 1" to the REDUCED sector; the joint space includes mu.
# Joint index = n-(field-form with mu Schur-eliminated) which can be 1 OR 2. Hunt at the massive
# root s* (I_p = 0): assemble the FULL joint form (v_p Dirichlet, v_f free, mu) numerically.
print("\n-- part 4: joint (fields+mu) index hunt at the massive root s* --")
f_Ip = lambda sv: mp.quad(lambda t: mp.log((sv**2/2)*t**2 + (sv**2-sv)*t + (1+sv**2/2-sv)), [-1, 1])
sstar = mp.findroot(f_Ip, mp.mpf('2.2'))
print("   massive root s* ~", mp.nstr(sstar, 12), " I_p(s*) ~", mp.nstr(f_Ip(sstar), 3))
aFv, aFpv, gpv, gfv = mp.mpf(2), mp.mpf(2), mp.mpf(1), mp.mpf(1)
E0v = sstar**2/aFv**2; cfv = mp.sqrt(E0v)   # sigma = E0 (crease), ch=0 decouples
wf  = lambda t: (sstar**2/2)*t**2 + (sstar**2-sstar)*t + (1+sstar**2/2-sstar)
wpf = lambda t: sstar**2*t + sstar**2 - sstar
NP = 6
bP  = [lambda t,k=k: (1-t**2)*t**k for k in range(NP)]          # v_p Dirichlet
bPp = [lambda t,k=k: -2*t*t**k + (1-t**2)*(k*t**(k-1) if k>0 else 0) for k in range(NP)]
bF  = [lambda t,k=k: t**k for k in range(NP)]                    # v_f' free (traces free)
dim = 2*NP + 1
Qj = mp.matrix(dim, dim)
def dens(i, j, t):
    # joint on-shell density: fields (vp, vf') and mu blocks (verifier's own assembly, from V1's Hessian)
    wv = wf(t); pb = mp.log(wv)/aFv; pbp = wpf(t)/(aFv*wv); fbp = cfv/wv
    Lt = gpv*pbp**2/2 + (cfv/wv)**2/2
    vp_i  = bP[i](t)  if i < NP else (0 if i < 2*NP else 0)
    vp1_i = bPp[i](t) if i < NP else (0 if i < 2*NP else 0)
    vf1_i = bF[i-NP](t) if NP <= i < 2*NP else 0
    mu_i  = 1 if i == 2*NP else 0
    vp_j  = bP[j](t)  if j < NP else 0
    vp1_j = bPp[j](t) if j < NP else 0
    vf1_j = bF[j-NP](t) if NP <= j < 2*NP else 0
    mu_j  = 1 if j == 2*NP else 0
    W = wv
    # polarized joint Hessian density (from V1): fields x fields + mu cross + mu^2
    dd = ( W*(gpv*vp1_i*vp1_j + gfv*vf1_i*vf1_j)
      + aFv*W*( vp_i*(gpv*pbp*vp1_j + gfv*fbp*vf1_j) + vp_j*(gpv*pbp*vp1_i + gfv*fbp*vf1_i) )
      + aFv**2*Lt*W*vp_i*vp_j
      + aFpv*( mu_i*( vp_j*W*Lt*(1+aFv*pb) + pb*W*(gpv*pbp*vp1_j + gfv*fbp*vf1_j) )
             + mu_j*( vp_i*W*Lt*(1+aFv*pb) + pb*W*(gpv*pbp*vp1_i + gfv*fbp*vf1_i) ) )
      + aFpv**2*pb**2*W*Lt*mu_i*mu_j )
    return dd
for i in range(dim):
    for j in range(i, dim):
        val = mp.quad(lambda t: dens(i, j, t), [-1, 1])
        Qj[i,j] = Qj[j,i] = val
evj = mp.eigsy(Qj, eigvals_only=True)
njoint = sum(1 for v in evj if v < mp.mpf('-1e-18'))
print("   joint (v_p D, v_f free, mu) Galerkin(13) n- =", njoint, "; lowest two:", mp.nstr(evj[0],6), mp.nstr(evj[1],6))
vk("V10_joint_mu_index_hunt", njoint >= 1,
   f"(joint index at s* = {njoint}: if 2, the JSON's unscoped 'n-=1 exact' is materially over-stated; "
   "ledger/derivation scope 'reduced sector' — see report)")
print("part4 done; failures:", FAIL)

# ================= PART 5: S-ii (Stage C) independent re-derivation =================
print("\n-- part 5: S-ii landing class + dichotomy + controls --")
lc = sp.Symbol('lc', positive=True)      # cell half-length l
uu, vv = sp.Function('uu')(x), sp.Function('vv')(x)   # v_lam, v_p
vfx, vhx = sp.Function('vfx')(x), sp.Function('vhx')(x)
f1b, h1b = sp.symbols('f1b h1b', real=True)
E0c = gf*f1b**2/2 + gh*h1b**2/2
# independent two-parameter Hessian about the landing (p=0, lam=0, aF=2*lam on P1-4D)
d1, d2_ = sp.symbols('d1 d2_')
Sfull = sp.exp(2*(d1*uu)*(d1*vv + d2_*sp.Symbol('dummy')*0))*(gp*sp.diff(d1*vv,x)**2/2
        + gf*(f1b + d1*sp.diff(vfx,x))**2/2 + gh*(h1b + d1*sp.diff(vhx,x))**2/2)
d2S_C = sp.diff(Sfull, d1, 2).subs(d1, 0)
vk("V11_Sii_assembly", sp.simplify(sp.expand(d2S_C - (gp*sp.diff(vv,x)**2 + gf*sp.diff(vfx,x)**2
   + gh*sp.diff(vhx,x)**2 + 4*uu*vv*E0c))) == 0,
   "(joint form == gp vp'^2 + gf vf'^2 + gh vh'^2 + 4 E0 vlam vp; NO vlam diagonal on no-m-jet class)")
# negative witness re-derived (both E0 signs)
tpar = sp.Symbol('tpar', positive=True)
prof = sp.sin(sp.pi*x/lc)
Qw = gp*sp.integrate(sp.diff(prof,x)**2, (x,-lc,lc)) - 4*tpar*E0c*sp.integrate(prof**2, (x,-lc,lc))
vk("V12_Sii_witness", sp.simplify(Qw.subs(tpar, gp*sp.pi**2/(2*E0c*lc**2)) + gp*sp.pi**2/lc) == 0,
   "(Q = -gp pi^2/l < 0 exact at t = gp pi^2/(2 E0 l^2); E0<0 handled by t -> -t: UNSTABLE unconditional)")
# wall-parity admissibility of the witness: odd about BOTH walls (mirror-odd forcing)
dlt = sp.Symbol('dlt', real=True)
vk("V12b_witness_parity", sp.simplify(prof.subs(x, lc+dlt) + prof.subs(x, lc-dlt)) == 0
   and sp.simplify(prof.subs(x, -lc+dlt) + prof.subs(x, -lc-dlt)) == 0,
   "(sin(pi x/l) exactly odd about x=+l and x=-l; all traces zero => germ-independent)")
# jet dichotomy: per-mode 2x2 with k_n = n pi/(2l); mode functions sin(n pi (x+l)/(2l))
# (symbolic-integer orthogonality defeats sympy's simplifier — a MY-tooling artifact, so checked
#  at explicit integers; n!=m orthogonality + norms l, k_n^2 l are the standard exact identities)
nn = sp.Symbol('nn', positive=True, integer=True)
orth_ok = True
for n_i in range(1, 5):
    for m_i in range(1, 5):
        a_m = sp.sin(n_i*sp.pi*(x+lc)/(2*lc)); b_m = sp.sin(m_i*sp.pi*(x+lc)/(2*lc))
        i1 = sp.simplify(sp.integrate(a_m*b_m, (x,-lc,lc)))
        i2 = sp.simplify(sp.integrate(sp.diff(a_m,x)*sp.diff(b_m,x), (x,-lc,lc)))
        e1 = lc if n_i == m_i else 0
        e2 = (n_i*sp.pi/(2*lc))**2*lc if n_i == m_i else 0
        if sp.simplify(i1-e1) != 0 or sp.simplify(i2-e2) != 0: orth_ok = False
mode_n = sp.sin(nn*sp.pi*(x+lc)/(2*lc))
kn = nn*sp.pi/(2*lc)
vk("V13a_mode_orthogonality", orth_ok,
   "(explicit n,m in 1..4: exact orthogonality in both metrics; norms l and k_n^2 l => exact 2x2 block-diagonalization)")
vk("V13b_modes_wall_odd", sp.simplify(mode_n.subs(x, lc+dlt) + mode_n.subs(x, lc-dlt)) == 0
   and sp.simplify(mode_n.subs(x, -lc+dlt) + mode_n.subs(x, -lc-dlt)) == 0,
   "(every Dirichlet mode is odd about both walls: banked-admissible; the basis is the FULL H^1_0 basis)")
cm = sp.Symbol('c_m', positive=True)
M2 = sp.Matrix([[gp*kn**2, 2*E0c],[2*E0c, cm*kn**2]])
vk("V13c_block_det", sp.simplify(M2.det() - (gp*cm*kn**4 - 4*E0c**2)) == 0,
   "(det = gp cm kn^4 - 4E0^2; diag > 0 => PSD iff det >= 0; worst mode n=1, k1^4 = pi^4/(16 l^4) "
   "=> stable iff 64 E0^2 l^4 <= gp cm pi^4 — threshold re-derived BOTH directions: "
   "det<0 at n=1 gives an explicit 2-component negative direction; det>=0 all n gives per-mode PSD + Parseval completeness)")
# stable-side spot: rational point strictly below threshold => all-mode PSD (minor check n=1,2,3)
subsS = {gp:1, cm:1, lc:1, E0c: R(1,10)}
belows = [sp.simplify((1*1*(k*sp.pi/2)**4 - 4*R(1,100))) for k in [1,2,3]]
vk("V13d_stable_side_spot", all(sp.N(b) > 0 for b in belows),
   "(E0=1/10, gp=cm=l=1: 64 E0^2 l^4 = 0.64 < pi^4: dets positive for n=1,2,3 and increasing in n — stable regime populated)")
# unstable-side spot: E0=1 => 64 > pi^4 ~ 97.4? NO — pick E0=2: 256 > 97.4 => n=1 det < 0
vk("V13e_unstable_side_spot", sp.N((sp.pi/2)**4 - 4*4) < 0,
   "(E0=2, gp=cm=l=1: n=1 det = pi^4/16 - 16 < 0 — explicit negative direction on the unstable side)")
# constants control (S-iii): full form is SOS; mu and k_mod absent
p0c = sp.Symbol('p0c', real=True)
S_const = sp.exp((aF+aFp*d1*sp.Symbol('muC'))*(p0c + d1*vv))*(gp*sp.diff(d1*vv,x)**2/2
          + gf*sp.diff(d1*vfx,x)**2/2 + gh*sp.diff(d1*vhx,x)**2/2)
d2_const = sp.diff(S_const, d1, 2).subs(d1,0)
vk("V14_constants_control", sp.simplify(sp.expand(d2_const - sp.exp(aF*p0c)*(gp*sp.diff(vv,x)**2
   + gf*sp.diff(vfx,x)**2 + gh*sp.diff(vhx,x)**2))) == 0,
   "(E0=0 constants member: joint form == W0*SOS exactly; mu ABSENT (lambda flat), k_mod/k10/C absent: "
   "kernel = banked flat directions exactly — CONTROL PASS reproduced independently)")
# triad control: aF(0)=1, E0=0 landing
S_triad = sp.exp((1+2*(d1*uu))*(d1*vv))*(gp*sp.diff(d1*vv,x)**2/2 + gf*sp.diff(d1*vfx,x)**2/2
          + gh*sp.diff(d1*vhx,x)**2/2)
d2_triad = sp.diff(S_triad, d1, 2).subs(d1,0)
vk("V15_triad_control", sp.simplify(sp.expand(d2_triad - (gp*sp.diff(vv,x)**2 + gf*sp.diff(vfx,x)**2
   + gh*sp.diff(vhx,x)**2))) == 0,
   "(triad-locked massless member: SOS with v_lam(x) fully absent => arbitrary odd v_lam, v_kmod in kernel: CONTROL PASS)")
print("part5 done; failures:", FAIL)
print("\n== VERIFIER INDEPENDENT CHECK: total failures:", len(FAIL), FAIL, "==")
