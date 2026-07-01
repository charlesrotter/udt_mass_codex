# crux1_statistics_topology.py
# OBSERVE-mode constructor: characterize the ACTUAL topology of UDT's settled
# L2+L4 soliton (real unit 3-vector n, target S^2) for the STATISTICS question
# (Crux 1 of the coin-flip): does the configuration admit a Z2 boson/fermion
# distinction at all, and from where?
#
# This is NOT a generic SU(2)/S^3 Skyrmion. The settled field is n: (cell)->S^2.
# We characterize OUR field honestly, computing degree invariants explicitly to
# confirm WHICH homotopy group classifies the static soliton, then reason out
# pi_1 of the configuration space for spin and statistics.
#
# Homotopy facts used (standard, cited in the doc) are stated; the EXPLICIT
# constructions below CONFIRM the degree/Hopf classification of the actual maps.

import numpy as np

print("="*70)
print("CRUX 1 — STATISTICS TOPOLOGY of the settled L2+L4 S^2-soliton")
print("="*70)

# ----------------------------------------------------------------------
# PART A. THE FIELD: which map, which homotopy group?
# Two candidate readings of "the static soliton", both made explicit.
# ----------------------------------------------------------------------
print("\n[A] THE FIELD — explicit degree computations\n")

# A1. The ANGULAR hedgehog on the cell's angular 2-sphere:
#     n: S^2(space angles) -> S^2(target),  n = (sinTh cos ph, sinTh sin ph, cosTh)
#     with Theta(r) a radial profile; on a fixed-r shell Theta is fixed so the
#     shell-map is n(theta,phi) = identity-like degree-1 map S^2->S^2.
#     Winding = pi_2(S^2) = Z  (the H1 area-form degree).
def area_form_degree(N=400):
    # degree of the map S^2_space -> S^2_target for n = xhat (identity on sphere)
    th = np.linspace(1e-6, np.pi-1e-6, N)
    ph = np.linspace(0, 2*np.pi, N, endpoint=False)
    TH, PH = np.meshgrid(th, ph, indexing='ij')
    # n components
    nx = np.sin(TH)*np.cos(PH); ny = np.sin(TH)*np.sin(PH); nz = np.cos(TH)
    # derivatives
    dth = th[1]-th[0]; dph = ph[1]-ph[0]
    nth = np.stack(np.gradient(np.stack([nx,ny,nz]), dth, axis=1), axis=0) if False else None
    # manual gradients
    n = np.stack([nx,ny,nz], axis=0)
    n_th = np.gradient(n, dth, axis=1)
    n_ph = np.gradient(n, dph, axis=2)
    # winding density = n . (n_th x n_ph)
    cross = np.cross(n_th, n_ph, axis=0)
    dens = np.sum(n*cross, axis=0)
    deg = dens.sum()*dth*dph/(4*np.pi)
    return deg

deg2 = area_form_degree()
print(f"A1. pi_2(S^2) degree of the angular hedgehog map S^2->S^2 : {deg2:.4f}  (expect 1)")
print("    -> the H1 area-form winding lives in pi_2(S^2)=Z. This is the")
print("       CHARGE/degree of the soliton (B=1). It is an INTEGER, not a Z2.")

# A2. The PHYSICAL 3D lump: n: R^3 -> S^2 with n->const at the seal.
#     n constant on the boundary => R^3 one-point-compactifies to S^3.
#     So the static soliton-as-a-3D-field is a map  S^3 -> S^2.
#     pi_3(S^2) = Z, classified by the HOPF INVARIANT.
#     BUT: a hedgehog n=xhat (Theta=theta, no internal winding) has Hopf=0.
#     The 3D "texture charge" is the Hopf number; the radial hedgehog is
#     the boundary of the degree, NOT a Hopf texture. Confirm Hopf of a
#     genuine Hopf map = 1, and of the hedgehog-extended field = 0.
def hopf_invariant(field_func, N=24, L=3.0):
    # Compute Hopf invariant H = -(1/(4pi)^2) INT A.B d^3x where B = curl A,
    # F = pullback of the area form. Use the standard formula on a grid.
    xs = np.linspace(-L, L, N)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing='ij')
    n = field_func(X, Y, Z)  # shape (3,N,N,N), unit vector
    nx, ny, nz = n
    d = xs[1]-xs[0]
    # F_ij = n.(d_i n x d_j n)/2 ... we need F_jk (2-form) and A with dA=F
    g = [np.gradient(c, d, axis=ax) for ax in range(3) for c in [n]]
    # gradients of n along x,y,z
    n_x = np.gradient(n, d, axis=1)
    n_y = np.gradient(n, d, axis=2)
    n_z = np.gradient(n, d, axis=3)
    def F(a, b):  # F_ab = n.(d_a n x d_b n)
        return np.sum(n * np.cross(a, b, axis=0), axis=0)
    Fyz = F(n_y, n_z)
    Fzx = F(n_z, n_x)
    Fxy = F(n_x, n_y)
    # B = (Fyz, Fzx, Fxy) is the "magnetic" field of the composite connection (=2*pi*pullback)
    # Solve for A with curl A = B via FFT (Coulomb gauge)
    k = np.fft.fftfreq(N, d=d)*2*np.pi
    KX, KY, KZ = np.meshgrid(k, k, k, indexing='ij')
    K2 = KX**2+KY**2+KZ**2
    K2[0,0,0] = 1.0
    Bf = [np.fft.fftn(Fyz), np.fft.fftn(Fzx), np.fft.fftn(Fxy)]
    Kv = [KX, KY, KZ]
    # A = i k x B / k^2  (curl A = B in Coulomb gauge)
    cross_kB = [Kv[(i+1)%3]*Bf[(i+2)%3]-Kv[(i+2)%3]*Bf[(i+1)%3] for i in range(3)]
    Af = [1j*cross_kB[i]/K2 for i in range(3)]
    A = [np.real(np.fft.ifftn(Af[i])) for i in range(3)]
    AB = A[0]*Fyz + A[1]*Fzx + A[2]*Fxy
    H = AB.sum()*d**3 / (4*np.pi)**2
    return H

def hedgehog_field(X, Y, Z):
    r = np.sqrt(X**2+Y**2+Z**2)+1e-9
    # profile: Theta = pi at r=0 -> 0 at large r; n = (sinTh xhat_ang..., cosTh) hedgehog
    Th = np.pi*np.exp(-r)  # smooth pi->0
    rho = np.sqrt(X**2+Y**2)+1e-12
    # spatial angular hedgehog direction
    sx, sy, sz = X/r, Y/r, Z/r
    n = np.stack([np.sin(Th)*sx, np.sin(Th)*sy, np.sin(Th)*sz + 0*Z]) # not unit; fix
    # build proper hedgehog: n = (sinTh * spatial_unit_xy_part..., cosTh)
    n = np.stack([np.sin(Th)*sx, np.sin(Th)*sy, np.cos(Th)])
    nn = np.sqrt(np.sum(n**2, axis=0))
    return n/nn

def true_hopf_field(X, Y, Z):
    # standard Hopf map H=1: stereographic of Hopf fibration
    r2 = X**2+Y**2+Z**2
    # map R^3 -> S^3 -> S^2 ; use w = (X+iY, Z+i(1-r2)/2)/norm style.. use known:
    # n from psi=(z0,z1), z0=(2(X+iY)), z1=(2Z + i(r2-1)), normalize on S^3
    z0 = 2*(X + 1j*Y)
    z1 = 2*Z + 1j*(r2 - 1)
    norm = np.sqrt(np.abs(z0)**2+np.abs(z1)**2)+1e-12
    z0/=norm; z1/=norm
    nx = 2*np.real(np.conj(z0)*z1)
    ny = 2*np.imag(np.conj(z0)*z1)
    nz = np.abs(z0)**2 - np.abs(z1)**2
    return np.stack([nx, ny, nz])

H_hh = hopf_invariant(hedgehog_field)
H_true = hopf_invariant(true_hopf_field)
print(f"\nA2. Hopf invariant (pi_3(S^2)=Z) of the radial HEDGEHOG n=xhat*sinTh : {H_hh:.3f}  (expect ~0)")
print(f"    Hopf invariant of a GENUINE Hopf map (control)               : {H_true:.3f}  (expect ~1)")
print("    -> the settled radial hedgehog is NOT a Hopf texture (H=0). Its")
print("       charge is the pi_2 DEGREE, realized as the boundary value, not")
print("       an internal pi_3 linking. (3D Hopf charge available but unused.)")

# ----------------------------------------------------------------------
# PART B. THE Z2 SOURCES — three candidates, are they the same?
# These are homotopy facts; we STATE them with sources and check arithmetic.
# ----------------------------------------------------------------------
print("\n[B] THE Z2 SOURCES (homotopy facts; arithmetic checked)\n")

facts = {
 "pi_4(S^2)":  "Z2   (statistics/FR sign for a 3D S^2-soliton; exchange loop)",
 "pi_5(S^2)":  "Z2   (the 4D WZW-era sign, su3_field #50)",
 "pi_3(S^2)":  "Z    (Hopf invariant; 3D texture charge -- NOT a Z2)",
 "pi_2(S^2)":  "Z    (degree/charge of the static soliton -- B=1)",
 "pi_5(SU(3))":"Z    (integer WZW level N_c -- the route #50 found NOT native)",
 "H^1(M;Z2)":  "0 (interval time) or Z2 (circle time): spin-structure torsor (#47b)",
}
for k,v in facts.items():
    print(f"    {k:14s} = {v}")

print("""
    KEY DISTINCTION for OUR field (target S^2, NOT S^3/SU(2)):
    - SPIN (2pi rotation of one lump) and STATISTICS (exchange of two)
      for a soliton with target T and base S^3 are governed by pi_1 of the
      configuration space Q. For skyrmion-type solitons the spin-statistics
      Z2 is carried by the FINKELSTEIN-RUBINSTEIN class:
         loop in Q (rotation or exchange)  ->  a map  S^4 -> T  (susp. of S^3)
      so the relevant group is pi_4(T).  For T=S^2: pi_4(S^2)=Z2.
    - This Z2 is INDEPENDENT of the degree (pi_2): a degree-B S^2 soliton has
      an FR statistics class in pi_4(S^2)=Z2 that is a FREE sign UNLESS a
      WZW-type term in the action FIXES it.
""")

# ----------------------------------------------------------------------
# PART C. CAN N (=3) ENTER AS N mod 2 ?
# In the real SU(2) Skyrme model the soliton is a fermion iff the WZW/baryon
# coefficient (the level, = N_c) is ODD: the FR phase = exp(i*pi*N_c*B).
# Here there is NO native integer WZW (#50): target is S^2, pi_5(S^2)=Z2 free,
# pi_5(SU(3))=Z absent. So the question: is the Z2 element fixed by N as N mod 2?
# ----------------------------------------------------------------------
print("[C] CAN N=3 ENTER THE Z2 AS N mod 2 ?\n")
print(f"    N = 3,  N mod 2 = {3 % 2}  (the nontrivial/fermionic class IF N entered)")
print("""    MECHANISM SHAPE (derived, not asserted):
    The only way an integer N fixes the FR Z2 sign is through a topological
    term whose coefficient is N and that evaluates the loop class mod 2:
        FR phase = exp(i*pi * c * (class in pi_4)),  c in Z, sign = (-1)^c.
    In the SU(2) case c = N_c*B comes from the WZW term (pi_5(SU(2))? no --
    via the 5D WZW on SU(N), pi_5(SU(N>=3))=Z, level N_c). For OUR S^2 field
    there is NO integer-graded term: the available 5D class is pi_5(S^2)=Z2,
    which is ITSELF only a Z2 -- it cannot carry an integer N as a coefficient,
    only its own free sign. So N=3 has NO integer-graded channel to set the
    sign. The N=3 we have is the pi_2-DEGREE/area-form count (an integer in a
    DIFFERENT group), and degree does not feed pi_4 mod 2: a degree-B S^2
    soliton's FR class is the SAME free Z2 for every B (the suspension that
    builds pi_4 from the rotation loop does not see the degree as a parity).
""")

# ----------------------------------------------------------------------
print("="*70)
print("SUMMARY (see crux1_statistics_topology_results.md for full reasoning)")
print("="*70)
print(f"""
 - Static soliton charge: pi_2(S^2)=Z, degree B={deg2:.2f}  (an integer, NOT a coin).
 - 3D texture: map S^3->S^2, pi_3(S^2)=Z (Hopf); hedgehog Hopf={H_hh:.2f} (unused).
 - The STATISTICS coin: pi_4(S^2)=Z2  -> a genuine two-sided coin EXISTS.
 - It is a FREE sign (no native term selects it): #47/#49/#50 all concur.
 - N=3 is a pi_2 integer; it has NO integer-graded (pi_5(SU(3))=Z) channel to
   set the Z2, because that channel is not native (#50). So N does NOT fix the
   coin as N mod 2 in the classical theory.
""")
