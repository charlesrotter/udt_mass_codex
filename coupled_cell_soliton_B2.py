"""
B2 -- PHI ONLY. The n=x/r knot SOURCING a back-reacting phi via Einstein eqs,
on an INFINITE/unbounded domain (NO cell wall). Does the Misner-Sharp mass
M(r) CONVERGE as r->infinity (phi localizes the knot) or DIVERGE (phi gives
only the deficit, not finiteness)?

DERIVED (angular_lagrangian_results.md TASK 6, CANON C-2026-06-14-1):
  t-equation G^t_t = -kappa8 xi/r^2  =>  e^{-2phi} = 1 - kappa8 xi - rs/r
  (a SOLID-ANGLE DEFICIT (1-kappa8 xi) on top of Schwarzschild).
  Misner-Sharp:  m(r) = (c^2 r/2G)(1 - e^{-2phi}).

This is the GLOBAL MONOPOLE metric. We compute m(r) and ask its r->inf limit.
Numerics on V100 float64 (with a CPU/analytic cross-check).
"""
import torch, math
torch.set_default_dtype(torch.float64)
dev = 'cuda' if torch.cuda.is_available() else 'cpu'

print("="*70)
print("B2 -- PHI ONLY (back-reacting phi on UNBOUNDED domain)")
print("="*70)

# DERIVED back-reaction solution. delta := kappa8*xi (the solid-angle deficit),
# rs the Schwarzschild integration constant (CHOSE rs=0: pure monopole, no point mass).
# e^{-2phi} = 1 - delta - rs/r.   m(r) = (c^2 r/2G)(1-e^{-2phi}) = (c^2 r/2G)(delta + rs/r)
# Units: set c^2/2G = 1.  Then m(r) = r*delta + rs/2.

def m_MS(r, delta, rs):
    emin2phi = 1.0 - delta - rs/r          # DERIVED back-reaction
    return r*(1.0 - emin2phi)              # = r*delta + rs   (in c^2/2G=1 units)

print("\n-- Solve Einstein t-eq self-consistently (closed form), integrate M(r):")
print("   e^{-2phi}=1-delta-rs/r,  m(r)=(c^2 r/2G)(1-e^{-2phi})  [c^2/2G=1]\n")

for delta in [0.001, 0.01, 0.1]:
    rs = 0.0
    rgrid = torch.logspace(-3, 6, 1000000, device=dev)   # r from 1e-3 to 1e6
    m = m_MS(rgrid, delta, rs)
    print(f"  delta=kappa8*xi={delta:<6} rs={rs}: "
          f"m(r=1)={m_MS(torch.tensor(1.0),delta,rs):.4e}  "
          f"m(r=1e3)={m_MS(torch.tensor(1e3),delta,rs):.4e}  "
          f"m(r=1e6)={m_MS(torch.tensor(1e6),delta,rs):.4e}")
    # slope test: m(r)/r -> delta (linear growth, NO convergence)
    ratio = (m[-1]/rgrid[-1]).item()
    print(f"     m(r)/r -> {ratio:.6e}  (= delta exactly => m DIVERGES linearly)")

print("\n-- Also verify the ENERGY integral diverges (independent of the MS reading):")
print("   E_coord(R) = INT_0^R rho 4pi r^2 dr = INT 4pi xi dr = 4pi xi R -> inf")
for xi in [0.01,0.1]:
    for R in [1e1,1e3,1e6]:
        r = torch.linspace(1e-6, R, 2000000, device=dev)
        E = torch.trapz(xi/r**2 * 4*math.pi*r**2, r).item()
        print(f"  xi={xi} R={R:<6}: E_coord(R)={E:.4e}  (4pi*xi*R={4*math.pi*xi*R:.4e})")

print("\n-- Curvature / localization check: does the source decay so the knot is")
print("   LOCALIZED?  rho = xi/r^2 has NO intrinsic length -> NOT localized; it is")
print("   scale-free (power law), the hallmark of the global monopole. The deficit")
print("   is a global angular defect, not a finite lump.")

print("\nVERDICT B2: phi back-reaction ALONE does NOT finitize.")
print("M(r) = r*delta + rs/2 GROWS LINEARLY without bound (the solid-angle deficit")
print("is a long-range defect, not a localized mass). e^{-2phi}=1-delta is CONSTANT")
print("at large r (a conical/deficit geometry), so m(r)~(c^2/2G)*delta*r -> infinity.")
print("phi supplies the DEFICIT (the B=1/A EOS, the conical geometry) but NOT")
print("finiteness. Finiteness must come from elsewhere (the cell truncation).")
