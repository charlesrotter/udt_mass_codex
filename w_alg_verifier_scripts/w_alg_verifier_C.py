#!/usr/bin/env python3
"""INDEPENDENT verifier for CLAIM C (integrability) + E elliptic.
Substitution only; no shared machinery."""
import sympy as sp
PASS, FAIL = [], []
def ck(tag, cond, note=""):
    (PASS if cond else FAIL).append(tag)
    print(f"VC-{tag}: {'PASS' if cond else 'FAIL'}  {note}")

xi,eta = sp.symbols('xi eta', real=True)

# ---- C1. Liouville general solution, BOTH sign branches ----
F=sp.Function('F')(xi); G=sp.Function('G')(eta)
# V_xe = +(1/4) e^-2V ; claim e^-2V = -4 F' G'/(F+G)^2
A = -4*sp.diff(F,xi)*sp.diff(G,eta)/(F+G)**2
# V = -(1/2) ln A.  Check V_xe = (1/4) A (since e^-2V = A by construction):
res = sp.simplify(sp.diff(-sp.log(A)/2, xi, eta) - A/4)
ck("C1a", res==0, "OFF Liouville: e^-2V=-4F'G'/(F+G)^2 solves V_xe=+(1/4)e^-2V (general soln)")
A2 = 4*sp.diff(F,xi)*sp.diff(G,eta)/(F+G)**2
res2 = sp.simplify(sp.diff(-sp.log(A2)/2, xi, eta) + A2/4)
ck("C1b", res2==0, "opposite branch: e^-2V=+4F'G'/(F+G)^2 solves V_xe=-(1/4)e^-2V")

# ---- C2. Tzitzeica exponent identification ----
# ON slice S_on ~ (e^v - gam e^-2v); shift v=V+(1/3)ln gam:
V=sp.Symbol('V',real=True); gam=sp.Symbol('gamma',positive=True); lam=sp.Symbol('lam',positive=True)
sh = V + sp.log(gam)/3
lhs = lam*(sp.exp(sh) - gam*sp.exp(-2*sh))
rhs = lam*gam**sp.Rational(1,3)*(sp.exp(V)-sp.exp(-2*V))
ck("C2", sp.simplify(lhs-rhs)==0, "ON slice -> Tzitzeica exponent pair (+1,-2) exactly (DBM)")

# ---- C3. WTC resonances {-1,+2} for U U_xe - U_x U_e = k(U^3-1) ----
z=sp.Symbol('z'); k=sp.Symbol('k',positive=True)
eta_s=sp.Symbol('eta',real=True); psi=sp.Function('psi')(eta_s); ps1=sp.diff(psi,eta_s)
def op(U,kk):
    Uz=sp.diff(U,z); Ue=ps1*Uz+sp.diff(U,eta_s)
    Uze=ps1*sp.diff(U,z,2)+sp.diff(Uz,eta_s)
    return sp.expand((U*Uze-Uz*Ue-kk*(U**3-1)).doit())
a0=sp.Function('a0')(eta_s)
lead=op(a0*z**-2,k)
c6=sp.simplify(lead.coeff(z,-6))
sol=[s for s in sp.solve(c6,a0) if s!=0]
ck("C3a", len(sol)==1 and sp.simplify(sol[0]-2*ps1/k)==0, "leading: a0=2psi'/k unique (double pole)")
a0v=2*ps1/k
b_,j_=sp.symbols('b j')
pert=op(a0v*z**-2+b_*z**(j_-2),k)
linb=sp.expand(sp.diff(pert,b_).subs(b_,0))
res_poly=sp.simplify(linb.coeff(z**(j_-6)))
fact=sp.factor(sp.simplify(res_poly/(a0v*ps1)))
ck("C3b", sp.simplify(res_poly-a0v*ps1*(j_-2)*(j_+1))==0, f"resonance poly ~ (j-2)(j+1) => j=-1,+2 BOTH integer; factored={fact}")
# compatibility at j=2:
c1,c2=sp.Function('c1')(eta_s),sp.Function('c2')(eta_s)
EQ=op(a0v*z**-2+c1*z**-1+c2,k)
o5=sp.simplify(EQ.coeff(z,-5)); sc1=sp.solve(o5,c1)
o4=sp.simplify(sp.expand(EQ.coeff(z,-4)).subs(c1,sc1[0]))
ck("C3c", sp.simplify(sp.diff(o4,c2))==0 and sp.simplify(o4)==0,
   "j=2 compatibility holds identically (c2 free, residual 0): ON slice PASSES Painleve")

# ---- C4. obstruction closed form -psi'^2 (ln K)''/K^2 ----
# non-chiral k(x): k=k0+k1 z+k2 z^2; reuse op with kser.
k0=sp.Function('k0',positive=True)(eta_s); k1=sp.Function('k1')(eta_s); k2=sp.Function('k2')(eta_s)
kser=k0+k1*z+k2*z**2
a0x=2*ps1/k0
e1,e2=sp.Function('e1')(eta_s),sp.Function('e2')(eta_s)
EQx=op(a0x*z**-2+e1*z**-1+e2,kser)
o5x=sp.simplify(EQx.coeff(z,-5)); se1=sp.solve(o5x,e1)
o4x=sp.simplify(sp.expand(EQx.coeff(z,-4)).subs(e1,se1[0]))
obstr=sp.simplify(o4x - sp.diff(o4x,e2)*e2)
ck("C4a", sp.simplify(sp.diff(o4x,e2))==0 and obstr!=0, "non-chiral k(x): j=2 residual NONZERO (Painleve broken off-slice)")
# close to criterion with K(x): k0=K,k1=K'/2,k2=K''/8, chain rule dx/deta=(1-psi')/2
K=sp.Function('K',positive=True); x0=sp.Symbol('x0',real=True)
Kv,K1v,K2v=K(x0),sp.diff(K(x0),x0),sp.diff(K(x0),x0,2)
subK={k2:K2v/8, sp.diff(k1,eta_s):K2v*(1-ps1)/4, sp.diff(k0,eta_s):K1v*(1-ps1)/2, k1:K1v/2, k0:Kv}
obstrK=sp.simplify(obstr.subs(subK,simultaneous=True))
# criterion: obstr*K^4/psi'^2 + (K K'' - K'^2) == 0
ck("C4b", sp.simplify(sp.expand(obstrK*Kv**4/ps1**2 + (Kv*K2v-K1v**2)))==0,
   "obstruction CLOSES to -psi'^2 (K K''-K'^2)/K^4 = -psi'^2 (ln K)''/K^2")
# => passes iff (ln K)''=0 iff K exponential in x. independent confirmation:
print("   => integrable off-slice iff K = lam gam^{1/3} is EXPONENTIAL in tortoise x. Confirmed.")

# ---- E (statics elliptic): ON first integral + quartic ----
m=sp.Symbol('m',real=True); Phi=sp.Symbol('Phi',positive=True); E=sp.Symbol('E',real=True)
vf=sp.Function('v')(m)
Ham=sp.diff(vf,m)**2/2 + Phi/2*sp.exp(-2*vf) + Phi*sp.exp(vf)
dH=sp.simplify(sp.diff(Ham,m).subs(sp.diff(vf,m,2), Phi*(sp.exp(-2*vf)-sp.exp(vf))))
ck("E1", dH==0, "ON first integral v_m^2/2+(Phi/2)e^-2v+Phi e^v = E (exact)")
y=sp.Symbol('y',positive=True)  # y=e^-v
vm2 = 2*E - Phi*y**2 - 2*Phi/y   # v_m^2 from first integral
quart = -Phi*y**4 + 2*E*y**2 - 2*Phi*y
ck("E2", sp.simplify(y**2*vm2 - quart)==0, "y=e^-v: y_m^2 = -Phi y^4+2E y^2-2Phi y (elliptic quartic)")

print(f"\nVC: {len(PASS)} PASS / {len(FAIL)} FAIL")
if FAIL: print("FAILED:", FAIL)
