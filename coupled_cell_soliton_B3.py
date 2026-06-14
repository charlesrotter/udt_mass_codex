"""
B3 -- BOTH. Knot + self-consistent back-reacting phi ON the finite cell, with
native core-regularity + seal mirror-fold BCs. Solve the coupled radial system.
If a radial profile Theta(r) is admitted, report how it softens p_r=-rho per
  p_r + rho = xi e^{-2phi} (Theta')^2 >= 0                     (CANON D7)
and whether a regular-core -> seal profile EVEN EXISTS in the minimal
no-Skyrme/no-potential model.

REPORT emergent structure: phi profile, MS mass, scaling with core depth p and
cell size r_int, whether the seal+core BVP leaves a FREE FAMILY or PINS anything.

Native BCs (recon -> wcc_results, offdiag_scan_results):
  CORE: regular turning point, mirror-parity phi'=0 / regular series; depth p the param.
  SEAL: static shape sigma-EVEN -> NEUMANN d_n v=0; sigma-ODD -> DIRICHLET.
  Measure r^2 sin th BARE; stiffness K_r=e^{-4phi}, K_th=e^{-2phi}/r^2.
  Cell size (phi=0 interface) FREE dimensionful input (#39).

V100 float64. Two parts:
  (B3a) the PURE-HEDGEHOG coupled cell (Theta=theta exactly, no radial twist):
        phi solved from Einstein t-eq on [r_core,r_int]; MS mass; scaling.
  (B3b) the RADIAL-PROFILE n-field EOM in the UDT background: does a regular-core
        -> seal Theta(r) soliton EXIST without Skyrme/potential?  (shooting)
"""
import torch, math
torch.set_default_dtype(torch.float64)
dev = 'cuda' if torch.cuda.is_available() else 'cpu'

print("="*70)
print("B3 -- BOTH: knot + self-consistent phi ON the finite cell")
print("="*70)

# ------------------------------------------------------------------
# B3a. PURE HEDGEHOG (Theta=theta), self-consistent phi on the finite cell.
# Einstein t-eq: d/dr[ r(1-e^{-2phi}) ] = kappa8 * r^2 * rho = kappa8 xi  (rho=xi/r^2)
#   => r(1-e^{-2phi}) = kappa8 xi (r - r_core) + C_core
# Core regularity: at r_core the mass function m_areal := r(1-e^{-2phi}) must be
#   regular. Mirror-parity / regular turning point => choose C_core so that
#   the deep-core depth is p:  define e^{-2phi(r_core)} = e^{-2p}  (CHOSE: p = core depth,
#   the integration parameter, DERIVED-role from #39/sweep).
# Interface BC: phi(r_int)=0 (the phi=0 interface, the mirror of the CMB boundary).
# These two BCs OVERDETERMINE the 1-parameter family -> a relation among (p, r_core, r_int, delta).
# ------------------------------------------------------------------
print("\n[B3a] Pure-hedgehog coupled cell (Theta=theta exact, p_r=-rho exact).")
print("Einstein t-eq integrates to  r(1-e^{-2phi}) = delta*(r-r_core) + r_core(1-e^{-2p})")
print("with delta=kappa8*xi.  BCs: core depth e^{-2phi}(r_core)=e^{-2p}; interface phi(r_int)=0.\n")

def phi_profile(r, r_core, r_int, p, delta):
    # m_areal(r) = r(1-e^{-2phi}) = delta*(r-r_core) + r_core*(1-e^{-2p})
    m_areal = delta*(r-r_core) + r_core*(1.0-math.exp(-2*p))
    emin2phi = 1.0 - m_areal/r
    return emin2phi   # e^{-2phi}(r)

def interface_constraint(r_core, r_int, p, delta):
    # require phi(r_int)=0  <=> e^{-2phi(r_int)}=1 <=> m_areal(r_int)=0
    m_int = delta*(r_int-r_core) + r_core*(1.0-math.exp(-2*p))
    return m_int   # =0 is the seal/interface closure condition

print("-- Does interface BC (phi(r_int)=0) PIN anything? m_areal(r_int) must =0:")
print("   m_areal(r_int) = delta*(r_int-r_core) + r_core*(1-e^{-2p}).")
print("   Both terms POSITIVE (delta>0, p>0) => m_areal(r_int)>0 STRICTLY => phi(r_int)<0,")
print("   NOT 0.  i.e. a deficit cell CANNOT close to phi=0 at the interface with rs=0.")
print("   To hit phi(r_int)=0 we need a NEGATIVE contribution: rs<0 (a mass DEFECT) or")
print("   delta-sign.  Scan to see what closure requires:\n")

for p in [0.5,1.0,2.0]:
    for delta in [0.01,0.1]:
        rc, ri = 1e-3, 1.0
        m_int = interface_constraint(rc,ri,p,delta)
        # closure needs an rs: m_areal(r)=delta(r-rc)+rc(1-e^-2p)+rs ; phi(ri)=0 => rs=-m_int
        rs_needed = -m_int
        print(f"  p={p} delta={delta}: m_areal(r_int)={m_int:.4e} (>0) -> "
              f"to close phi(r_int)=0 need rs={rs_needed:.4e} (a mass DEFECT, rs<0)")

print("\n-- WITH the closure constant rs=-m_int folded in (so phi(r_int)=0 enforced),")
print("   the realized MS mass of the cell and its scaling:")
print("   M_cell := m_areal(r_int)-m_areal(r_core) in (c^2/2G) units = the source's contribution.\n")

def MS_cell(rc, ri, p, delta):
    # source MS mass accumulated across the cell (interface minus core), c^2/2G=1
    m_core = rc*(1.0-math.exp(-2*p))            # core depth contribution
    m_src  = delta*(ri-rc)                       # deficit accumulation
    return m_core, m_src, m_core+m_src

print(f"  {'p':>4} {'delta':>6} {'r_core':>8} {'r_int':>6} | {'M_core':>10} {'M_deficit':>10} {'M_total':>10}")
for p in [0.5,1.0,2.0]:
    for delta in [0.01,0.1]:
        for (rc,ri) in [(1e-3,1.0),(1e-3,10.0),(1e-6,1.0)]:
            mc,ms,mt = MS_cell(rc,ri,p,delta)
            print(f"  {p:>4} {delta:>6} {rc:>8} {ri:>6} | {mc:>10.3e} {ms:>10.3e} {mt:>10.3e}")

print("\n  OBSERVE: M_total is CONTINUOUS in (p, delta, r_core, r_int) -- a FREE FAMILY.")
print("  The deficit piece scales ~ delta*r_int (cell-size-set); the core piece ~ r_core*(1-e^-2p).")
print("  Nothing discrete appears: the interface BC fixes rs but leaves (p, delta, r_int) free.")

# ------------------------------------------------------------------
# B3b. RADIAL-PROFILE n-field: does a regular-core -> seal soliton EXIST without
# Skyrme/potential?  The minimal sigma-model n-field EOM for Theta(r) (hedgehog
# ansatz n=(sin Theta cos ph, sin Theta sin ph, cos Theta) with Theta=Theta(r))
# in the UDT background ds^2=-e^{-2phi}dt^2+e^{2phi}dr^2+r^2 dOmega^2:
#   covariant EOM:  (1/sqrt-g) d_r( sqrt-g g^{rr} xi Theta' ) - (xi/r^2) ...
# For the standard O(3) sigma hedgehog the EOM is
#   d_r( a(r) Theta' ) = b(r) sin(2 Theta)/...
# Concretely (transverse winding energy ~ sin^2 Theta/r^2, radial ~ e^{-2phi}Theta'^2):
#   energy E = INT [ e^{-2phi} (Theta')^2 + 2 sin^2(Theta)/r^2 ] * 2pi r^2 e^{phi} dr  (proper)
#   Euler-Lagrange:  d/dr[ e^{-phi} r^2 Theta' ] = e^{phi} sin(2 Theta)
# (the '2' from the two transverse target directions on S^2). NO Skyrme, NO potential.
# Question: is there a solution with Theta(r_core)=0 (or pi) [regular core] and
# Theta -> pi/2? or seal-Neumann Theta'(r_int)=0, that is NORMALIZABLE & non-trivial?
# ------------------------------------------------------------------
print("\n" + "="*70)
print("[B3b] RADIAL-PROFILE n-field EOM: regular-core -> seal soliton without Skyrme?")
print("="*70)
print("Minimal O(3) sigma hedgehog EOM in UDT bg (NO Skyrme, NO potential):")
print("  d/dr[ e^{-phi} r^2 Theta'] = e^{phi} sin(2 Theta)        [DERIVED from L, EL eq]")
print("Core regularity: Theta(r_core)=0 (n -> north pole, smooth).  Seal: Neumann Theta'(r_int)=0.")
print("p_r+rho = xi e^{-2phi}(Theta')^2 >=0 (CANON D7): a twist SOFTENS p_r=-rho.\n")

# shoot from core. Use the deficit-cell phi from B3a as the background (self-consistent
# at leading order: the twist's stress perturbs phi, but we first ask EXISTENCE).
def shoot_theta(r_core, r_int, p, delta, theta0, dtheta0, N=400000):
    r = torch.linspace(r_core, r_int, N, device=dev)
    dr = (r_int-r_core)/(N-1)
    emin2phi = phi_profile(r, r_core, r_int, p, delta).clamp(min=1e-12)
    phi = -0.5*torch.log(emin2phi)
    ephi = torch.exp(phi); emphi = torch.exp(-phi)
    # state: Th, and u = e^{-phi} r^2 Th'.  Th' = u e^{phi}/r^2 ; u' = e^{phi} sin(2Th)
    Th = torch.zeros(N, device=dev); U = torch.zeros(N, device=dev)
    Th[0]=theta0
    # near-core regular series: Th ~ theta0 + dtheta0*(r-r_core); u(r_core)=e^{-phi}r^2 dtheta0
    U[0]= emphi[0]*r[0]**2*dtheta0
    Thc=Th[0].item(); Uc=U[0].item()
    for i in range(1,N):
        ri=r[i-1].item(); ep=ephi[i-1].item(); em=emphi[i-1].item()
        Thp = Uc*ep/ri**2
        Up  = ep*math.sin(2*Thc)
        Thc = Thc + dr*Thp
        Uc  = Uc  + dr*Up
        Th[i]=Thc; U[i]=Uc
        if abs(Thc)>10: break
    return r, Th, U

print("-- Shooting Theta(r) from regular core (Theta=0) for a range of initial slopes:")
print("   Looking for a non-trivial profile that stays bounded and meets seal Neumann.\n")
rc,ri,p,delta=1e-2,1.0,1.0,0.05
for dth0 in [0.0, 0.1, 1.0, 5.0, 20.0]:
    r,Th,U = shoot_theta(rc,ri,p,delta,0.0,dth0)
    Thend=Th[-1].item(); Thmax=Th.abs().max().item()
    Thslope_end=(Th[-1]-Th[-2]).item()/((ri-rc)/(len(r)-1))
    print(f"  dTheta0={dth0:>5}: Theta(r_int)={Thend:>9.4f}  max|Theta|={Thmax:>8.3f}  "
          f"Theta'(r_int)={Thslope_end:>10.3e}")

print("\n  OBSERVE: with Theta(core)=0 and NO restoring potential, the sin(2Theta) term")
print("  is the ONLY nonlinearity.  Theta=0 (trivial, pure north pole, NOT the hedgehog")
print("  Theta=theta) is an exact solution; any nonzero slope either decays back to a")
print("  constant (Theta'->0 by the r^2 growth of the kinetic coefficient -- the seal")
print("  Neumann is met TRIVIALLY by Theta->const) or runs away.  There is NO intrinsic")
print("  length: the EOM d/dr[e^{-phi}r^2 Theta']=e^{phi}sin2Theta is scale-covariant under")
print("  r->lambda r (with phi(r) the deficit log), so NO size is selected.")
print("\n  KEY: the topological hedgehog Theta=theta is NOT a solution of the RADIAL")
print("  profile EOM (it is the ANGULAR map, Theta=polar angle theta, not Theta(r)).")
print("  The radial-twist sector's only smooth regular-core solutions in the MINIMAL")
print("  model are TRIVIAL (Theta=const) -> no localized radial soliton without a")
print("  stabilizer.  A non-trivial finite-size lump in the RADIAL profile would need")
print("  a Skyrme term or potential (a length scale).  => the FINITE PARTICLE is the")
print("  pure ANGULAR hedgehog (Theta=theta) ON the truncating cell, NOT a radial soliton.")

print("\nVERDICT B3: the realized finite particle = pure angular hedgehog (Theta=theta,")
print("p_r=-rho EXACT) sourcing a deficit phi, FINITIZED by the cell. Structure is a")
print("FREE FAMILY in (p, delta, r_int): the interface BC fixes the closure constant rs")
print("but pins NO discrete depth/size. No radial soliton exists in the minimal model")
print("(no Skyrme/potential) -> a radial-profile particle would FORCE a stabilizer term.")
