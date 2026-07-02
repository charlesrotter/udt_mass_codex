"""verify_f2d_reduction.py -- CAS / high-accuracy cross-check that the DISCRETE operators of
cell_solver_f2d.py reduce to the symbolic EOMs of the derived frame. Prints PASS/FAIL per check.

Checks (per the build charter, f_rtheta_free_field_MAP.md sec.9 item 5):
  (a) discretized theta-moments I_r, I_4th (and I_th, I_s, I_4r) match their symbolic/high-accuracy
      values on >=2 test profiles f: f=theta (exact) and a band-limited deformed profile (spectral).
  (b) the discrete radial 2nd-derivative + the ASSEMBLED residual, on a smooth manufactured
      (phi,rho,f), match the SYMBOLIC EOM residual (phi-ODE, rho-ODE, f-PDE) to spectral accuracy.
  (c) the rigid f=theta residual == xi(1-N^2)cos(theta), discretely (N=1 -> 0; N=2 -> -3 cos theta).

It IMPORTS cell_solver_f2d and tests the ACTUAL discrete operators (fields()/residual()), not a
reimplementation. Symbolic side = sympy; moment reference = high-accuracy scipy quad.
"""
import numpy as np
import sympy as sp
from scipy.integrate import quad
import torch
torch.set_default_dtype(torch.float64)
import cell_solver_f2d as M

PASSES = []
def report(name, ok, detail=""):
    PASSES.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}   {detail}")


# =======================================================================================
# (a) theta-moments on 2 profiles
# =======================================================================================
print("(a) theta-moment operators vs symbolic / high-accuracy reference")
Nr, Nth = 6, 8
ctx = M.make_ctx(Nr, Nth, rc=0.5)
Z, XI, KAP, N = 8.0, 1.0, 1.0, 1
prm = (Z, XI, KAP, N)
L = 1.3

# ---- profile 1: f = theta (uf = 0) -> exact analytic moments Ir=0, Ith=1, Is=1, I4th=1, I4r=0 ----
u0 = M.pack(torch.zeros(Nr), 0.7 * torch.ones(Nr), torch.zeros(Nr, Nth), L)
Q0 = M.fields(u0, ctx, prm)
e = lambda a, v: float((a - v).abs().max())
ok1 = (e(Q0["Ir"], 0.0) < 1e-13 and e(Q0["Ith"], 1.0) < 1e-13 and e(Q0["Is"], 1.0) < 1e-13
       and e(Q0["I4th"], 1.0) < 1e-13 and e(Q0["I4r"], 0.0) < 1e-13)
report("f=theta moments == (Ir,Ith,Is,I4th,I4r)=(0,1,1,1,0)", ok1,
       f"maxerr Ir={e(Q0['Ir'],0.):.1e} Ith={e(Q0['Ith'],1.):.1e} Is={e(Q0['Is'],1.):.1e} "
       f"I4th={e(Q0['I4th'],1.):.1e} I4r={e(Q0['I4r'],0.):.1e}")

# ---- profile 2: band-limited deformation u = alpha*(1-mu^2)*zeta  (mu=cos theta) ----
alpha = 0.12
zeta = ctx["zeta"].numpy(); mu = ctx["mu"].numpy()
uf2 = alpha * (1.0 - mu[None, :] ** 2) * zeta[:, None]
u2 = M.pack(torch.zeros(Nr), 0.7 * torch.ones(Nr), torch.as_tensor(uf2), L)
Q2 = M.fields(u2, ctx, prm)

def moments_ref(zi, rho=0.7):
    """High-accuracy reference moments at radial coord zeta=zi for the analytic band-limited f."""
    fr = lambda t: (2.0 / L) * alpha * (np.sin(t) ** 2)            # (2/L) du/dzeta, du/dzeta=alpha(1-mu^2)
    fth = lambda t: 1.0 + alpha * zi * (2.0 * np.sin(t) * np.cos(t))
    f = lambda t: t + alpha * (np.sin(t) ** 2) * zi
    Ir = 0.5 * quad(lambda t: np.sin(t) * fr(t) ** 2, 0, np.pi)[0]
    Ith = 0.5 * quad(lambda t: np.sin(t) * fth(t) ** 2, 0, np.pi)[0]
    Is = 0.5 * quad(lambda t: np.sin(f(t)) ** 2 / np.sin(t), 0, np.pi)[0]
    I4th = 0.5 * quad(lambda t: np.sin(f(t)) ** 2 / np.sin(t) * fth(t) ** 2, 0, np.pi)[0]
    I4r = 0.5 * quad(lambda t: np.sin(f(t)) ** 2 / np.sin(t) * fr(t) ** 2, 0, np.pi)[0]
    return np.array([Ir, Ith, Is, I4th, I4r])

ref = np.array([moments_ref(float(z)) for z in zeta])              # (Nr,5)
dis = np.stack([Q2["Ir"].numpy(), Q2["Ith"].numpy(), Q2["Is"].numpy(),
                Q2["I4th"].numpy(), Q2["I4r"].numpy()], axis=1)
errs = np.abs(dis - ref).max(axis=0)
# I_r: integrand sin(th)f_r^2 is polynomial in mu (deg 4) -> GL EXACT (machine). I_4th/I_s/I_4r carry
# sin^2(f) (non-polynomial) -> GL spectral accuracy (small, converges with Nth). Report both.
report("deformed-profile I_r == reference (GL exact; integrand poly in mu)", errs[0] < 1e-13,
       f"maxerr I_r = {errs[0]:.2e}")
report("deformed-profile I_4th == reference (spectral GL quadrature)", errs[3] < 1e-6,
       f"maxerr I_4th = {errs[3]:.2e}  (I_th={errs[1]:.1e} I_s={errs[2]:.1e} I_4r={errs[4]:.1e})")
# spectral convergence of I_4th (the non-polynomial moment): Nth 8 -> 16
ctx16 = M.make_ctx(Nr, 16, rc=0.5)
mu16 = ctx16["mu"].numpy()
uf16 = alpha * (1.0 - mu16[None, :] ** 2) * zeta[:, None]
Q16 = M.fields(M.pack(torch.zeros(Nr), 0.7 * torch.ones(Nr), torch.as_tensor(uf16), L), ctx16, prm)
err16 = np.abs(Q16["I4th"].numpy() - ref[:, 3]).max()
report("I_4th quadrature CONVERGES with Nth (8 -> 16)", err16 <= errs[3] + 1e-15,
       f"err(Nth=8)={errs[3]:.2e} -> err(Nth=16)={err16:.2e}")


# =======================================================================================
# (b) manufactured smooth (phi,rho,f): discrete assembled residual == symbolic EOM residual
# =======================================================================================
print("\n(b) assembled residual vs symbolic EOM residual on a manufactured smooth field")
Nr, Nth = 7, 8
ctx = M.make_ctx(Nr, Nth, rc=0.5)
Lb = 1.4
zeta = ctx["zeta"].numpy(); th = ctx["th"].numpy(); mu = ctx["mu"].numpy()

# manufactured: poly(deg<=2) in zeta (Cheb exact) x band-limited(deg2) in mu (Dth exact)
phi_np = 0.10 + 0.05 * zeta + 0.02 * zeta ** 2
rho_np = 0.70 + 0.03 * zeta + 0.01 * zeta ** 2
uf_np = 0.08 * (1.0 - mu[None, :] ** 2) * (0.5 + 0.3 * zeta[:, None])
uman = M.pack(torch.as_tensor(phi_np), torch.as_tensor(rho_np), torch.as_tensor(uf_np), Lb)
Qm = M.fields(uman, ctx, prm)

# symbolic side
t, T = sp.symbols('t theta', real=True)
Zs, XIs, KAPs, Ns, Ls = sp.Integer(8), sp.Integer(1), sp.Integer(1), sp.Integer(1), sp.Rational(14, 10)
phi_s = sp.Rational(1, 10) + sp.Rational(5, 100) * t + sp.Rational(2, 100) * t ** 2
rho_s = sp.Rational(70, 100) + sp.Rational(3, 100) * t + sp.Rational(1, 100) * t ** 2
u_s = sp.Rational(8, 100) * (1 - sp.cos(T) ** 2) * (sp.Rational(5, 10) + sp.Rational(3, 10) * t)
f_s = T + u_s
dr = lambda ex: sp.Rational(2, 1) / Ls * sp.diff(ex, t)          # d/dr = (2/L) d/dt

# phi-ODE symbolic
phir, phirr = dr(phi_s), dr(dr(phi_s))
rhor, rhorr = dr(rho_s), dr(dr(rho_s))
phi_ode_s = phirr - (4 * sp.exp(-2 * phi_s) * rhor ** 2 / (Zs * rho_s ** 2) - 2 * phir * rhor / rho_s)
phi_ode_fn = sp.lambdify(t, phi_ode_s, 'numpy')
err_phi = float(np.abs(phi_ode_fn(zeta[1:-1]) - Qm["phi_ode"].numpy()[1:-1]).max())
report("phi-ODE  discrete == symbolic (Cheb 2nd-deriv exact on poly)", err_phi < 1e-10,
       f"maxerr = {err_phi:.2e}")

# f-PDE symbolic (conservative form; discrete uses the analytically-equivalent EXPANDED form)
fr_s, fth_s = dr(f_s), sp.diff(f_s, T)
A_s = XIs * rho_s ** 2 * sp.sin(T) + KAPs * Ns ** 2 * sp.sin(f_s) ** 2 / sp.sin(T)
B_s = XIs * sp.sin(T) + KAPs * Ns ** 2 * sp.sin(f_s) ** 2 / (rho_s ** 2 * sp.sin(T))
pot_s = (Ns ** 2 * sp.sin(f_s) * sp.cos(f_s) / sp.sin(T)) * (XIs + KAPs * fr_s ** 2 + KAPs * fth_s ** 2 / rho_s ** 2)
resf_s = dr(A_s * fr_s) + sp.diff(B_s * fth_s, T) - pot_s
resf_fn = sp.lambdify((t, T), resf_s, 'numpy')
TT, ZZ = np.meshgrid(th, zeta[1:-1], indexing='ij')             # (Nth, Nr-2)
resf_ref = resf_fn(ZZ, TT).T                                    # -> (Nr-2, Nth)
err_f = float(np.abs(resf_ref - Qm["res_f"].numpy()[1:-1]).max())
report("f-PDE  discrete(expanded) == symbolic(conservative)", err_f < 1e-9, f"maxerr = {err_f:.2e}")

# rho-ODE symbolic: analytic derivatives + high-accuracy quad moments (I_r, I_4th)
def Ir_I4th_ref(zi):
    fr = lambda tt: (2.0 / Lb) * 0.08 * (0.3) * np.sin(tt) ** 2
    fth = lambda tt: 1.0 + 0.08 * (0.5 + 0.3 * zi) * (2 * np.sin(tt) * np.cos(tt))
    fv = lambda tt: tt + 0.08 * np.sin(tt) ** 2 * (0.5 + 0.3 * zi)
    Ir = 0.5 * quad(lambda tt: np.sin(tt) * fr(tt) ** 2, 0, np.pi)[0]
    I4th = 0.5 * quad(lambda tt: np.sin(fv(tt)) ** 2 / np.sin(tt) * fth(tt) ** 2, 0, np.pi)[0]
    return Ir, I4th
phir_fn = sp.lambdify(t, phir, 'numpy'); phirr_fn = sp.lambdify(t, phirr, 'numpy')
rhor_fn = sp.lambdify(t, rhor, 'numpy'); rhorr_fn = sp.lambdify(t, rhorr, 'numpy')
phiv_fn = sp.lambdify(t, phi_s, 'numpy'); rhov_fn = sp.lambdify(t, rho_s, 'numpy')
rho_ode_ref = []
for zi in zeta[1:-1]:
    Ir, I4th = Ir_I4th_ref(float(zi))
    pv, rv = float(phiv_fn(zi)), float(rhov_fn(zi))
    e2p = np.exp(2 * pv)
    val = rhorr_fn(zi) - (2 * phir_fn(zi) * rhor_fn(zi) - (8 / 4) * rv * e2p * phir_fn(zi) ** 2
                          + (e2p / 4) * (1.0 * rv * Ir - 1.0 * 1 ** 2 * I4th / rv ** 3))
    rho_ode_ref.append(val)
err_rho = float(np.abs(np.array(rho_ode_ref) - Qm["rho_ode"].numpy()[1:-1]).max())
report("rho-ODE discrete(GL moments) == symbolic (spectral; I_4th via quad)", err_rho < 1e-6,
       f"maxerr = {err_rho:.2e}")


# =======================================================================================
# (c) rigid f=theta residual == xi(1-N^2) cos(theta), discretely
# =======================================================================================
print("\n(c) rigid f=theta f-PDE residual == xi(1-N^2) cos(theta)")
Nr, Nth = 6, 10
ctx = M.make_ctx(Nr, Nth, rc=0.5)
th = ctx["th"].numpy()
for Nv in (1, 2, 3):
    prmv = (8.0, 1.0, 1.0, Nv)
    ur = M.pack(0.1 * torch.ones(Nr), 0.7 * torch.ones(Nr), torch.zeros(Nr, Nth), 1.0)
    resf = M.fields(ur, ctx, prmv)["res_f"].numpy()               # (Nr,Nth)
    target = 1.0 * (1 - Nv ** 2) * np.cos(th)[None, :]            # xi(1-N^2)cos th, all r rows
    err = float(np.abs(resf - target).max())
    report(f"N={Nv}: rigid residual == {1-Nv**2}*cos(theta)", err < 1e-11, f"maxerr = {err:.2e}")


# =======================================================================================
# (d) vacuum-P scale symmetry [OBS-1] (MAP sec.4 / sec.9.5; ported from verify_f2d_virial_step0 V3)
#     Under (r, rho) -> lambda(r, rho), f(r) -> f(r/lambda): the geometry + the whole xi-sector are
#     scale-COVARIANT (each Lagrangian density piece has lambda-weight 0 -> vacuum P invariant); the
#     kappa (quartic) sector BREAKS it (weight lambda^-2). => kap/xi sets the absolute cell length;
#     only RATIOS are unit-free (consistent with the ratios-only data-blind rule).
# =======================================================================================
print("\n(d) vacuum-P scale symmetry [OBS-1]: geo+xi scale-invariant, kappa breaks (lam^-2)")
rr, lam, uu = sp.symbols('r lambda u', positive=True)
Zc, xic, kapc, Nc = sp.symbols('Z xi kappa N', positive=True)
phic = sp.Function('phi')(rr); rhoc = sp.Function('rho')(rr); fc = sp.Function('f')(rr, T)
Pc, Rc, Fc = sp.Function('P')(uu), sp.Function('R')(uu), sp.Function('F')(uu, T)
subs_sc = {phic: Pc.subs(uu, rr / lam), rhoc: lam * Rc.subs(uu, rr / lam), fc: Fc.subs(uu, rr / lam)}
def _weight(term):
    return sp.simplify(term.subs(subs_sc).doit().subs(rr, lam * uu))
pieces = {
    'geo_kin_phi': (Zc / 2) * rhoc ** 2 * sp.diff(phic, rr) ** 2,
    'geo_R2': sp.Integer(2),
    'geo_K': -2 * sp.exp(-2 * phic) * sp.diff(rhoc, rr) ** 2,
    'mat_xi_r': (xic / 2) * rhoc ** 2 * sp.diff(fc, rr) ** 2,
    'mat_xi_th': (xic / 2) * sp.diff(fc, T) ** 2,
    'mat_xi_s': (xic / 2) * Nc ** 2 * sp.sin(fc) ** 2,
    'mat_k_r': (kapc * Nc ** 2 / 2) * sp.sin(fc) ** 2 * sp.diff(fc, rr) ** 2,
    'mat_k_th': (kapc * Nc ** 2 / 2) * sp.sin(fc) ** 2 * sp.diff(fc, T) ** 2 / rhoc ** 2,
}
W = {k: _weight(v) for k, v in pieces.items()}
geoxi = ['geo_kin_phi', 'geo_R2', 'geo_K', 'mat_xi_r', 'mat_xi_th', 'mat_xi_s']
kappa = ['mat_k_r', 'mat_k_th']
geoxi_invariant = all(not W[k].has(lam) for k in geoxi)                       # weight 0
kappa_breaks = all((not sp.simplify(W[k] * lam ** 2).has(lam)) and W[k].has(lam) for k in kappa)  # weight -2
report("(d) vacuum-P scale symmetry: geo+xi invariant, kappa breaks (lam^-2)",
       geoxi_invariant and kappa_breaks,
       f"geo+xi weight-0={geoxi_invariant}; kappa weight-(-2)={kappa_breaks}")


print("\n" + "=" * 60)
print(f"RESULT: {sum(PASSES)}/{len(PASSES)} checks PASS")
print("=" * 60)
