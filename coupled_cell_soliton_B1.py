"""
B1 -- CELL ONLY. The n=x/r hedgehog source on a FINITE cell [r_core, r_int],
phi held as a FIXED background (no back-reaction). Compute the total energy /
Misner-Sharp mass integral over the finite cell. Is it FINITE? What sets its
scale? Confirm p_r=-rho stays exact.

OBSERVE study (coupled_cell_soliton_results.md). Data-blind. No mass/ratio
extraction; xi, r_core, r_int are dimensionless dials we SCAN to see scaling.

DERIVED inputs (angular_lagrangian_results.md / CANON C-2026-06-14-1):
  rho = xi/r^2,  p_r = -xi/r^2,  p_theta = p_phi = 0   (hedgehog n=x/r)
  measure sqrt(-g) = c r^2 sin theta  (phi cancels)
  proper-volume energy uses the spatial measure e^{+phi} r^2 sin th (g_rr^{1/2})
"""
import torch, math
torch.set_default_dtype(torch.float64)
dev = 'cuda' if torch.cuda.is_available() else 'cpu'

# ---- chosen background phi(r): a FIXED monotone profile (no back-reaction).
# CHOSE: a generic fixed background to probe sensitivity. Two test forms.
def phi_flat(r):            # phi=0 everywhere (Minkowski background)  [CHOSE]
    return torch.zeros_like(r)
def phi_log(r, p, r_int):   # phi = -p * ln(r_int/r): deep (-> -inf-ish) at core
    return -p*torch.log(r_int/r)          # phi(r_int)=0, phi-> -p ln as r->small [CHOSE]

def energy_integrals(xi, r_core, r_int, phi_fn, N=200000):
    r = torch.linspace(r_core, r_int, N, device=dev)
    rho = xi/r**2                                   # DERIVED
    phi = phi_fn(r)
    # (a) BARE coordinate energy  E_coord = INT rho * 4pi r^2 dr  (sqrt-g, phi cancels)
    integ_coord = rho*4*math.pi*r**2                # = 4pi xi  (constant integrand!)
    E_coord = torch.trapz(integ_coord, r)
    # (b) PROPER-volume energy  E_proper = INT rho * 4pi r^2 e^{+phi} dr  (g_rr^{1/2}=e^{phi})
    integ_proper = rho*4*math.pi*r**2*torch.exp(phi)
    E_proper = torch.trapz(integ_proper, r)
    # p_r = -rho check
    p_r = -xi/r**2
    eos_resid = torch.max(torch.abs(p_r+rho)).item()
    return E_coord.item(), E_proper.item(), eos_resid

# Misner-Sharp mass of the fixed background (read off the metric, NOT the source):
def MS_mass(phi_at_r, r):   # m = (c^2 r/2G)(1-e^{-2phi}); report in (c^2/2G)=1 units
    return r*(1.0-math.exp(-2*phi_at_r))

print("="*70)
print("B1 -- CELL ONLY (phi fixed background, no back-reaction)")
print("="*70)

# (1) p_r = -rho exact, and coord-energy = 4 pi xi (r_int - r_core)? NO:
#     integrand 4pi xi is CONSTANT in r, so E_coord = 4 pi xi (r_int - r_core).
print("\n-- Coordinate energy is LINEAR in cell width (rho ~ 1/r^2 x r^2 = const):")
for xi in [0.01, 0.1]:
    for (rc, ri) in [(1e-3,1.0),(1e-6,1.0),(1e-3,10.0),(0.1,1.0)]:
        Ec,Ep,res = energy_integrals(xi, rc, ri, phi_flat)
        print(f"  xi={xi:>5} rc={rc:<7} ri={ri:<5} | E_coord={Ec:.6e}  "
              f"(4pi*xi*(ri-rc)={4*math.pi*xi*(ri-rc):.6e})  |p_r+rho|max={res:.1e}")

print("\n-- FINITENESS: E_coord = 4*pi*xi*(r_int - r_core). FINITE for any finite cell.")
print("   Scale set by: xi (coupling) and the cell WIDTH (r_int - r_core), both free dials.")
print("   No 1/r_core divergence in the COORDINATE energy (the 1/r^2 of rho is")
print("   exactly cancelled by the r^2 of the measure -> constant integrand).")

# (2) With a deep-phi background, does the PROPER-volume energy diverge at the core?
print("\n-- PROPER-volume energy with deep log background phi=-p ln(r_int/r):")
for p in [0.5, 1.0, 2.0]:
    xi=0.1; ri=1.0
    for rc in [1e-2,1e-4,1e-6]:
        Ec,Ep,res = energy_integrals(xi, rc, ri, lambda r: phi_log(r,p,ri))
        print(f"  p={p} rc={rc:<7} | E_coord={Ec:.4e}  E_proper={Ep:.6e}")
    # E_proper integrand ~ xi*4pi*e^{phi} = 4pi xi (r/ri)^p -> integrable at core for p>-1
    print(f"    (E_proper integrand ~ (r/r_int)^p -> 0 at core for p>0; FINITE)")

# (3) MS mass of the fixed background at the interface
print("\n-- MS mass of FIXED background at interface (read off metric):")
for p in [0.5,1.0,2.0]:
    ri=1.0
    # phi=0 at r_int by construction -> MS mass(r_int)=0 for the pure log bg (no rs term)
    print(f"  p={p}: phi(r_int)=0 => MS m(r_int)=0 (pure deficit bg has no rs; "
          f"mass is in the SOURCE energy, not the vacuum metric)")

print("\nVERDICT B1: cell makes the energy FINITE and CONTINUOUS in cell size.")
print("E_coord = 4*pi*xi*(r_int-r_core): finite, linear/continuous in width, no")
print("pinned value. p_r=-rho stays EXACT (|p_r+rho|=0). The CELL alone finitizes")
print("the COORDINATE energy by truncation; nothing pins the cell size (#39).")
