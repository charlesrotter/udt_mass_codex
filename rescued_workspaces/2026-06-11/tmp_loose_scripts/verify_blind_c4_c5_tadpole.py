"""BLIND VERIFIER C4/C5 + tadpole.

C4: V_a1a1 = P_a/(4a) exactly  (=> m=+-1 zero mode iff background a-eq holds).
C5: ell<=2 Hessian m-block structure {u,a0,g0},{a1,g1},{g2}; nonzero couplings
    V_a1g1 = -sqrt5 k/(2F) + O(k^3), V_a0g0 = -sqrt15 k/(3F) + O(k^3)?? (verify)
Tadpole: T_g0 = -sqrt(5pi) k^2/3 (which normalization? test dQ/dg0 and /4).
All via exact angular quadrature of Q[f] = Int dOmega |grad f|^2/f.
"""
import numpy as np
from scipy import integrate

c = np.sqrt(3/(4*np.pi))

def Y(lm, th, ph):
    x = np.cos(th); s = np.sin(th)
    return {
      'Y00': 0.5/np.sqrt(np.pi)+0*th,
      'Y10': np.sqrt(3/(4*np.pi))*x,
      'Y11': np.sqrt(3/(4*np.pi))*s*np.cos(ph),
      'Y20': np.sqrt(5/(16*np.pi))*(3*x*x-1),
      'Y21': np.sqrt(15/(4*np.pi))*s*x*np.cos(ph),
      'Y22': np.sqrt(15/(16*np.pi))*s*s*np.cos(2*ph)}[lm]

def dYth(lm, th, ph):
    x = np.cos(th); s = np.sin(th)
    return {
      'Y00': 0*th,
      'Y10': -np.sqrt(3/(4*np.pi))*s,
      'Y11': np.sqrt(3/(4*np.pi))*x*np.cos(ph),
      'Y20': -np.sqrt(5/(16*np.pi))*6*x*s,
      'Y21': np.sqrt(15/(4*np.pi))*(x*x-s*s)*np.cos(ph),
      'Y22': np.sqrt(15/(16*np.pi))*2*s*x*np.cos(2*ph)}[lm]

def dYph(lm, th, ph):
    x = np.cos(th); s = np.sin(th)
    return {
      'Y00': 0*th, 'Y10': 0*th,
      'Y11': -np.sqrt(3/(4*np.pi))*s*np.sin(ph),
      'Y20': 0*th,
      'Y21': -np.sqrt(15/(4*np.pi))*s*x*np.sin(ph),
      'Y22': -np.sqrt(15/(16*np.pi))*2*s*s*np.sin(2*ph)}[lm]

def Q(F, k, coeffs):
    def ig(th, ph):
        f   = F*(1+k*np.cos(th)); fth = -F*k*np.sin(th); fph = 0.0
        for lm, cc in coeffs.items():
            f += cc*Y(lm, th, ph); fth += cc*dYth(lm, th, ph); fph += cc*dYph(lm, th, ph)
        s = np.sin(th)
        g2 = fth**2 + (fph/np.where(s == 0, 1.0, s))**2
        return g2/f*s
    v, _ = integrate.dblquad(ig, 0, 2*np.pi, 0, np.pi, epsabs=1e-12, epsrel=1e-12)
    return v

def d2(F, k, m1, m2, h=2e-4):
    if m1 == m2:
        return (Q(F,k,{m1:h}) - 2*Q(F,k,{}) + Q(F,k,{m1:-h}))/h**2
    return (Q(F,k,{m1:h,m2:h}) - Q(F,k,{m1:h,m2:-h})
            - Q(F,k,{m1:-h,m2:h}) + Q(F,k,{m1:-h,m2:-h}))/(4*h*h)

def d1(F, k, m, h=2e-4):
    return (Q(F,k,{m:h}) - Q(F,k,{m:-h}))/(2*h)

print("=== C4: V_a1a1 = P_a/(4a) ===")
fails = 0
for F, k in [(1.0, 0.2), (1.5, 0.6), (0.8, 0.85)]:
    a = k*F/c
    V11 = d2(F, k, 'Y11', 'Y11')/4
    Pa  = d1(F, k, 'Y10')          # dQ/da0 at background
    ok = abs(V11 - Pa/(4*a)) < 1e-5*max(1, abs(V11))
    fails += (not ok)
    print(f"  F={F} k={k}: V_a1a1={V11:.8f}  P_a/(4a)={Pa/(4*a):.8f} {'OK' if ok else 'FAIL'}")
    # claimed closed form 3U/(8k^3 F)
    L = np.log((1+k)/(1-k)); U = (1+k*k)*L - 2*k
    print(f"            closed form 3U/(8k^3F) = {3*U/(8*k**3*F):.8f}")

print("\n=== C5: m-block zeros (couplings that must vanish) ===")
F, k = 1.3, 0.45
zero_pairs = [('Y00','Y11'), ('Y00','Y21'), ('Y00','Y22'), ('Y10','Y11'),
              ('Y10','Y21'), ('Y10','Y22'), ('Y11','Y20'), ('Y11','Y22'),
              ('Y20','Y21'), ('Y20','Y22'), ('Y21','Y22')]
for p in zero_pairs:
    v = d2(F, k, *p)/4
    ok = abs(v) < 1e-5
    fails += (not ok)
    print(f"  V_{p[0]},{p[1]} = {v:+.2e} {'OK(0)' if ok else 'FAIL(nonzero)'}")

print("\n=== C5: nonzero O(k) couplings ===")
print("claimed: V_a1g1 = -sqrt5 k/(2F),  V_a0g0 = -sqrt15 k/(3F)  (leading order)")
for kk in [0.02, 0.05, 0.1, 0.2]:
    F = 1.0
    v11 = d2(F, kk, 'Y11', 'Y21')/4
    v00 = d2(F, kk, 'Y10', 'Y20')/4
    print(f"  k={kk}: V_a1g1={v11:+.8f} claimed={-np.sqrt(5)*kk/(2*F):+.8f} "
          f"ratio={v11/(-np.sqrt(5)*kk/(2*F)):.5f}")
    print(f"        V_a0g0={v00:+.8f} claimed={-np.sqrt(15)*kk/(3*F):+.8f} "
          f"ratio={v00/(-np.sqrt(15)*kk/(3*F)):.5f}")

print("\n=== tadpole T_g0: dQ/dg0 (and /4) at small k; claimed -sqrt(5pi)k^2/3 ===")
for kk in [0.05, 0.1, 0.2, 0.4]:
    F = 1.0
    t = d1(F, kk, 'Y20')
    cl = -np.sqrt(5*np.pi)*kk*kk/3
    print(f"  k={kk}: dQ/dg0={t:+.8f}  (dQ/dg0)/4={t/4:+.8f}  claimed={cl:+.8f} "
          f"ratio(full)={t/cl:.5f} ratio(/4)={t/4/cl:.5f}")

# sign of effect on degeneration: does sourced g0 raise or lower f at th=pi pole?
print("\n  Y20(pi) =", np.sqrt(5/(16*np.pi))*2, " > 0; negative tadpole means the")
print("  sourced gamma0 is NEGATIVE => f at both poles is LOWERED;")
print("  the degenerating pole (th=pi, f_min) is pushed FURTHER toward f=0.")
print("  (Direction of relaxation: energy decreases along -T direction, g0<0.)")

print(f"\nC4/C5 zero-structure FAILS: {fails}")
