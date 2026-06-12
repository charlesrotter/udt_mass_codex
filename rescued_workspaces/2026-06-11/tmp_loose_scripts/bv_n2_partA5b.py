"""A5 mollifier numerics, corrected: delta-weight of EL = (dL/dfield) - d/dy Pi over a
shrinking window [1-h,1+h], mollifier eps << h. Weld: collar f0=y^-q (y<1, sourced,
n=1: src coeff c_1 = J = -s y^-q) welded to flat vacuum f=1 (y>1, unsourced). q=1/3.
weight = -(Pi(1+h)-Pi(1-h)) + int_window (algebraic part of EL).
Targets: f-slot -q/2, phi-slot +q, ratio -2.
"""
import numpy as np
from scipy.integrate import quad

qv = 1.0/3.0
s = qv*(1-qv)/2

def fields(yarr, eps):
    ly = np.log(yarr)
    m = -eps*np.logaddexp(0.0, -ly/eps)          # smooth min(ln y, 0)
    sig = 1.0/(1.0+np.exp(ly/eps))               # d m / d ln y = sigma(-ly/eps)
    phi = (qv/2.0)*m
    php = (qv/2.0)*sig/yarr                      # phi'
    f = np.exp(-2*phi)
    fp = -2*php*f
    return phi, php, f, fp

def weights(h, eps):
    for ye in (1.0-h, 1.0+h):
        pass
    y0, y1 = 1.0-h, 1.0+h
    _, php0, f0_, fp0 = fields(np.array([y0]), eps)
    _, php1, f1_, fp1 = fields(np.array([y1]), eps)
    Pif0, Pif1 = 0.5*y0**2*fp0[0], 0.5*y1**2*fp1[0]
    Pip0 = 2*y0**2*php0[0]*f0_[0]**2
    Pip1 = 2*y1**2*php1[0]*f1_[0]**2
    # algebraic parts (n=1):
    #   f-slot:  dL/df = c_1(y) = J(y) = -s y^-q     (collar side only, y<1)
    #   phi-slot: dL/dphi = -4 y^2 phi'^2 f^2 - 2 c_1 f   (c_1 collar side only)
    Jf = lambda yy: -s*yy**(-qv) if yy < 1.0 else 0.0
    src_f = quad(lambda yy: Jf(yy), y0, y1, points=[1.0], limit=200)[0]
    def integrand_p(yy):
        ya = np.array([yy])
        _, php, f, _ = fields(ya, eps)
        return -4*yy**2*php[0]**2*f[0]**2 - 2*Jf(yy)*f[0]
    src_p = quad(integrand_p, y0, y1, points=[1.0], limit=200)[0]
    wf = -(Pif1 - Pif0) + src_f
    wp = -(Pip1 - Pip0) + src_p
    return wf, wp

print(f"targets: f-slot {-qv/2:+.6f}, phi-slot {+qv:+.6f}")
for h, eps in ((0.1, 1e-3), (0.05, 1e-3), (0.02, 1e-4), (0.01, 1e-5)):
    wf, wp = weights(h, eps)
    print(f"h={h:<5g} eps={eps:g}:  f-slot {wf:+.6f}   phi-slot {wp:+.6f}   ratio {wp/wf:+.5f}")
