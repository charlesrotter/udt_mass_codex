"""W4-B BLIND VERIFIER — attack A(ii)/(iii): is the fingerprint ratio
kappa_s/kappa_c an informative member-independent constant, or a
structurally insensitive functional?

Exact reduction (both edges live on the SAME weighted Sturm-Liouville
structure; t-variable, Dirichlet at t=1-end, Neumann at t=0-end):
  kappa_c = 3c/(16 mu1),  mu1 = min_v Int p v'^2 / Int b v^2
  kappa_s = c/(16 lam*),  lam* = fold of (p v')' = lam b e^{-2v}
  => ratio = kappa_s/kappa_c = mu1 / (3 lam*).
Substituting m = -2v this is the Gelfand/Bratu fold of
(p m')' + 2 lam b e^m = 0, so ratio = (2/3) mu1 / muG*, with muG* the
weighted Gelfand fold parameter. For CONSTANT weights the exact value
is (2/3) pi^2 / 3.513830719 = 1.87252 (computed below from scratch,
machinery validation).

This script maps ratio(p, b) over weight families far wider than the
library: if the spread is tiny everywhere, the observed 1.900 +- 0.002
across three members carries little evidence (insensitive functional);
if generic weights move the ratio substantially while members
coincide, member-independence is real information. Also tests the
exact-value candidates 19/10 and the flat constant.
Log: /tmp/w4b_verifier_1d.log. New file. 2026-06-12, verifier.
"""
import sys
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl


def log(*a):
    print(*a, flush=True)


class Toy:
    def __init__(self, p, b, Nt=4000):
        self.tg = np.linspace(0.0, 1.0, Nt)
        self.Nt = Nt
        self.p = np.column_stack([p(self.tg)])
        self.b = np.column_stack([b(self.tg)])
        self.c = 1.0


def ratio_of(p, b, Nt=4000):
    toy = Toy(p, b, Nt)
    kc, mu1 = vl.kappa_c_ray(toy, 0)
    lam, v = vl.fold_ray(toy, 0)
    ks = toy.c / (16 * lam)
    return ks / kc, mu1, lam, float(v.min())


log("=" * 72)
log("VALIDATION: constant weights (exact = 2 pi^2/(3*3.513830719))")
log("=" * 72)
r, mu1, lam, vmin = ratio_of(lambda t: np.ones_like(t),
                             lambda t: np.ones_like(t))
exact = 2 * np.pi**2 / (3 * 3.513830719)
log(f"flat ratio = {r:.6f} (exact {exact:.6f}; dev {abs(r-exact):.2e})"
    f"  [mu1={mu1:.6f} vs pi^2/4={np.pi**2/4:.6f}; "
    f"2lam*={2*lam:.6f} vs 3.513830719/4={3.513830719/4:.6f}; "
    f"min v at fold = {vmin:.4f} vs exact -? ]")
log(f"candidate 19/10 = 1.9000; flat = {exact:.5f}; "
    f"members claim 1.8999-1.9026")

log("=" * 72)
log("WEIGHT-FAMILY SCAN (ratio sensitivity)")
log("=" * 72)
rows = []


def scan(name, p, b):
    try:
        r, mu1, lam, vmin = ratio_of(p, b)
        rows.append((name, r))
        log(f"  {name:42s} ratio = {r:.5f}")
    except Exception as ex:
        log(f"  {name:42s} FAILED: {ex}")


one = lambda t: np.ones_like(t)
for x0 in (0.1, 0.3, 0.5, 0.7, 0.9):
    for sg in (0.05, 0.15):
        scan(f"b=gauss(x0={x0},sig={sg}), p=1",
             one, lambda t, x0=x0, sg=sg: 1e-4 + np.exp(
                 -((t - x0) / sg)**2))
for al in (-4, -2, 2, 4):
    scan(f"b=exp({al} t), p=1", one,
         lambda t, al=al: np.exp(al * t))
    scan(f"p=exp({al} t), b=1",
         lambda t, al=al: np.exp(al * t), one)
# seal-like: p decays toward the Dirichlet end by ~500x (f: 1 -> 0.002),
# b spikes near the Dirichlet end (f in the denominator)
scan("seal-like: p=exp(-6.2 t), b=exp(+5 t)",
     lambda t: np.exp(-6.2 * t), lambda t: np.exp(5 * t))
scan("seal-like sharper: p=exp(-6.2 t), b=exp(+6.2 t)",
     lambda t: np.exp(-6.2 * t), lambda t: np.exp(6.2 * t))
scan("p=(1-0.9 t)^2, b=1/(1-0.9 t)", lambda t: (1 - 0.9 * t)**2,
     lambda t: 1 / (1 - 0.9 * t))

# random smooth positive weights (Fourier log-fields), 40 draws
rng = np.random.default_rng(7)
rs = []
for i in range(40):
    a = rng.normal(0, 1, 6) / np.arange(1, 7)
    bcf = rng.normal(0, 1, 6) / np.arange(1, 7)

    def mk(cf):
        def f(t, cf=cf):
            s = np.zeros_like(t)
            for j, cj in enumerate(cf):
                s += cj * np.cos(np.pi * (j + 1) * t)
            return np.exp(1.5 * s)
        return f
    try:
        r, *_ = ratio_of(mk(a), mk(bcf))
        rs.append(r)
    except Exception:
        pass
rs = np.array(rs)
log(f"random smooth weights (n={len(rs)}): ratio min={rs.min():.4f} "
    f"max={rs.max():.4f} mean={rs.mean():.4f} std={rs.std():.4f}")

allr = np.array([r for _, r in rows] + list(rs))
log("=" * 72)
log(f"GLOBAL SPREAD over all scanned weights: [{allr.min():.4f}, "
    f"{allr.max():.4f}]  (claimed member band: 1.8999-1.9026; flat "
    f"{exact:.4f})")
log("=" * 72)
