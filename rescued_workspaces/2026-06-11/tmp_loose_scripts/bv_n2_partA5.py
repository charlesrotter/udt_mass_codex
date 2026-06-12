"""A5: distributional covariance at a weld (f cont., f' jumps).
Weld model consistent with claimed weights: collar f0=y^-q (y<1) -> flat f=1 (y>1), y_w=1.
Checks:
 1. Pi_phi = -2 f Pi_f identically  =>  Delta Pi_phi = -2 f(y_w) Delta Pi_f (f cont.)
 2. chain rule EL_phi = -2 f EL_f distributionally (multiplier -2f continuous: no delta x jump)
 3. mollifier limits of the delta weights: f-slot -q/2, phi-slot +q  (EL := dL/dfield - d/dy Pi)
"""
import sympy as sp
import numpy as np

y, q = sp.symbols('y q', positive=True)
f = sp.Function('f', positive=True)(y)
phi = sp.Function('phi')(y)

# 1. momenta
L_f = sp.Rational(1,4)*y**2*sp.diff(f, y)**2
Pi_f = sp.diff(L_f, sp.diff(f, y))
L_p = L_f.subs(f, sp.exp(-2*phi)).doit()
Pi_p = sp.diff(sp.expand(L_p), sp.diff(phi, y))
rel = sp.simplify(Pi_p - (-2*sp.exp(-2*phi))*Pi_f.subs(f, sp.exp(-2*phi)).doit())
print("A5  Pi_phi + 2 f Pi_f == 0:", "PASS" if rel == 0 else rel)

# 2. chain rule for the full EL (variational): dS/dphi = (df/dphi) dS/df = -2f dS/df
n = sp.Symbol('n')
cn = sp.Function('c')(y)
Ltot_f = L_f + cn*f**n
EL_f = sp.diff(Ltot_f, f) - sp.diff(sp.diff(Ltot_f, sp.diff(f, y)), y)
Ltot_p = Ltot_f.subs(f, sp.exp(-2*phi)).doit()
EL_p = sp.diff(Ltot_p, phi) - sp.diff(sp.diff(sp.expand(Ltot_p), sp.diff(phi, y)), y)
chain = sp.simplify(EL_p - (-2*sp.exp(-2*phi))*EL_f.subs(f, sp.exp(-2*phi)).doit())
print("A5  EL_phi + 2 f EL_f == 0 (smooth pts):", "PASS" if chain == 0 else chain)

# 3. mollifier numerics, q = 1/3
qv = 1.0/3.0
def run(eps):
    # phi_eps = (q/2)*(-eps*log(1+exp(-log(y)/eps)))' ... softmin(ln y, 0)
    ys = np.linspace(0.6, 1.6, 2000001)
    ly = np.log(ys)
    # smooth min(ln y, 0) = -eps*log(exp(-ly/eps)+1)  (stable form)
    m = -eps*np.logaddexp(0.0, -ly/eps)
    phiv = (qv/2.0)*m
    fv = np.exp(-2.0*phiv)
    dy = ys[1]-ys[0]
    fp = np.gradient(fv, dy); php = np.gradient(phiv, dy)
    Pif = 0.5*ys**2*fp
    Pip = 2.0*ys**2*php*fv**2
    i0, i1 = np.searchsorted(ys, 0.8), np.searchsorted(ys, 1.3)
    # delta weight of EL = (src) - d/dy Pi  ->  -[Pi]_jump as eps->0 (regular parts vanish off-weld
    # in the jump bracket because both one-sided solutions are smooth/critical there; we take the
    # raw bracket minus the smooth-side bracket of the unwelded collar continuation)
    wf  = -(Pif[i1]-Pif[i0])
    wp  = -(Pip[i1]-Pip[i0])
    # smooth reference brackets (pure collar continued, no weld), same window
    phic = (qv/2.0)*ly
    fc = np.exp(-2*phic); fcp = np.gradient(fc, dy); pcp = np.gradient(phic, dy)
    wf_ref = -(0.5*ys[i1]**2*fcp[i1] - 0.5*ys[i0]**2*fcp[i0])
    wp_ref = -(2*ys[i1]**2*pcp[i1]*fc[i1]**2 - 2*ys[i0]**2*pcp[i0]*fc[i0]**2)
    return wf - wf_ref, wp - wp_ref

for eps in (1e-2, 1e-3, 1e-4):
    wf, wp = run(eps)
    print(f"A5  eps={eps:g}:  f-slot weight={wf:+.6f} (target {-qv/2:+.6f})   "
          f"phi-slot weight={wp:+.6f} (target {+qv:+.6f})   ratio={wp/wf:+.4f} (target -2)")
