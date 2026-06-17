# VERIF_matter_sector_potential_E34.py
# E3: effective radial operator -u'' + V_eff(r*) u = omega^2 u for the tangent
#     fluctuation eta (the matter guiding wave), with the angular-harmonic decomposition.
# E4 (CRUX): solve the eigenproblem under regularity-at-core + finite-cell/seal BC;
#     run the S4 BOX-CONTROL TRAP-TEST (vary the cell/wall size R, >=4 values, factor>10).
#
# We DERIVE the radial operator from the Jacobi operator (E1) on the static UDT metric.
# The L2 tangent-fluctuation wave equation (E1) is
#   D^m D_m eta + K[ |grad n0|^2 eta - <eta,grad n0> grad n0 ] = 0,  K=1.
# Static modes eta ~ e^{-i omega t} Y(angles) u(r):  the t-part of box_g gives the
# omega^2 e^{2phi} term (g^{tt}=-e^{2phi}); the spatial Laplacian gives the radial op +
# angular eigenvalue L=l(l+1); the curvature term gives V_curv = -|grad n0|^2 (attractive)
# acting on the transverse component.  We assemble V_eff in the tortoise/optical coord.

import numpy as np, pickle
import scipy.linalg as sla

with open('matter_sector_profiles.pkl','rb') as fh: prof = pickle.load(fh)

print("="*72)
print("E3/E4: EFFECTIVE RADIAL OPERATOR + BOX-CONTROL TRAP-TEST (CRUX, S4)")
print("="*72)

# ----------------------------------------------------------------------
# E3.  Build V_eff(r).  The static fluctuation eqn (frequencies via g^{tt}=-e^{2phi}):
#   - (1/sqrt-g) d_r( sqrt-g g^{rr} d_r u ) + [ L/r^2 + V_curv(r) ] u = omega^2 e^{2phi} u
# sqrt-g = e^{phi} r^2, g^{rr}=e^{-2phi}.  Angular eigenvalue L = l(l+1) (scalar harmonic;
# the transverse tangent fluctuation carries an additional winding shift from the U(1)
# connection -> we scan l and also include the m-winding centrifugal as the corpus' angular
# stiffness).  V_curv = -( e^{-2phi}Theta'^2 + 2 sin^2Theta/r^2 ) (the ATTRACTIVE Jacobi term).
#
# Reduce to Liouville/tortoise form -psi'' + V_eff psi = omega^2 psi.
# Define proper radial coord and Liouville substitution so the operator is self-adjoint.
# Operator:  H u = omega^2 m(r) u,  with
#   H u = -(1/(e^{phi} r^2)) d_r( e^{-phi} r^2 d_r u ) + Vbar(r) u   [since g^{rr}sqrt-g = e^{-phi} r^2]
#   m(r) = e^{2phi}  (the time-metric weight), Vbar = L/r^2 + V_curv.
# This is a generalized SL eigenproblem H u = omega^2 m u.  We solve it directly on a grid
# (finite differences, Dirichlet at core[regularity] and seal[finite cell]) -- the cleanest
# faithful discretization, and VARY the seal radius R (box-control trap-test).
# ----------------------------------------------------------------------

def build_interp(profile):
    rg = profile['r']
    return (lambda x: np.interp(x, rg, profile['Th']),
            lambda x: np.interp(x, rg, profile['Thp']),
            lambda x: np.interp(x, rg, profile['phi']),
            lambda x: np.interp(x, rg, profile['phip']))

def eig_on_cell(profile, R, l, N=2000, rc=1e-3, sign='attractive'):
    """Solve H u = omega^2 m u on r in [rc, R], Dirichlet both ends (regular core + seal)."""
    Th_f, Thp_f, phi_f, phip_f = build_interp(profile)
    # extend profile beyond its solved domain by holding seal value (Theta=0 outside) -> V_curv->0
    r = np.linspace(rc, R, N); h = r[1]-r[0]
    Thv = np.where(r <= profile['r'][-1], Th_f(r), 0.0)
    Thpv= np.where(r <= profile['r'][-1], Thp_f(r), 0.0)
    phv = np.where(r <= profile['r'][-1], phi_f(r), profile['phi'][-1])
    # weights
    A = np.exp(-phv)*r**2            # = e^{-phi} r^2  (the g^{rr} sqrt-g flux weight)
    mwt = np.exp(2*phv)              # time-metric weight m(r)
    sg  = np.exp(phv)*r**2           # sqrt-g
    Vcurv = np.exp(-2*phv)*Thpv**2 + 2*np.sin(Thv)**2/r**2     # = |grad n0|^2  (>0)
    if sign=='attractive': Vc = -Vcurv      # the DERIVED Jacobi sign (tachyonic/attractive)
    else:                  Vc = +Vcurv      # control: flipped sign (would-be repulsive barrier)
    Vbar = l*(l+1)/r**2 + Vc
    # assemble H (generalized, symmetric via mass weight): H_{ij} u_j = omega^2 (m sg) u
    # weak form: integral [ A u'^2 + sg Vbar u^2 ] = omega^2 integral [ sg m u^2 ]
    # FD: -d/dr(A du/dr)/sg + Vbar u = omega^2 m u  -> symmetric generalized eig with weight (sg)
    main = np.zeros(N); lower=np.zeros(N-1); upper=np.zeros(N-1)
    Ahalf = 0.5*(A[:-1]+A[1:])      # A at half-points
    for i in range(1,N-1):
        main[i]  = (Ahalf[i-1]+Ahalf[i])/h**2 + sg[i]*Vbar[i]
        lower[i-1] = -Ahalf[i-1]/h**2
        upper[i]   = -Ahalf[i]/h**2
    # Dirichlet ends
    main[0]=1e30; main[-1]=1e30
    H = np.diag(main)+np.diag(lower,-1)+np.diag(upper,1)
    Mw = np.diag(sg*mwt)
    w = sla.eigh(H, Mw, eigvals_only=True)
    w = np.sort(w[np.isfinite(w)])
    w = w[w < 1e20]
    return w[:6]

# ---- E3 report: is there a repulsive near-core barrier? ----
print("""
E3: V_eff(r) = l(l+1)/r^2  +  V_curv(r),   V_curv = - ( e^{-2phi}Theta'^2 + 2 sin^2Theta/r^2 ).
The DERIVED S^2 curvature (Jacobi) term enters with a NEGATIVE (attractive) sign on the
transverse fluctuation.  The only POSITIVE (repulsive) near-core piece is the ordinary
centrifugal l(l+1)/r^2 (present for any wave, not special to the matter sector).  The
winding/curvature contribution sin^2Theta/r^2 is ATTRACTIVE here, NOT a repulsive barrier.
=> NO genuine repulsive near-core barrier from the matter-sector curvature term.
   (Contrast: conjecture-A's metric sector lacked any l(l+1)/r^2 winding term at all;
    here we DO have the ordinary centrifugal, but the curvature dressing is attractive.)
""")

# ---- E4 + S4 box-control trap-test ----
def trap_test(profile, label, l):
    print(f"\n--- BOX-CONTROL TRAP-TEST  [{label}], angular l={l} ---")
    print(f"{'R (seal)':>10} {'omega0^2':>14} {'omega0^2 * R^2':>16} {'omega1^2':>14}")
    Rs = [8.0, 25.0, 80.0, 250.0]   # factor ~30 range, 4 values (S4: >=4, factor>10)
    rows=[]
    for R in Rs:
        w = eig_on_cell(profile, R, l, N=3000)
        w0 = w[0]; w1 = w[1] if len(w)>1 else np.nan
        print(f"{R:>10.1f} {w0:>14.6e} {w0*R**2:>16.4f} {w1:>14.6e}")
        rows.append((R,w0,w1))
    # diagnose
    arr=np.array(rows)
    # if w0 ~ const/R^2 then w0*R^2 ~ const (box-controlled); if w0 asymptotes to const>0 -> intrinsic
    prod = arr[:,1]*arr[:,0]**2
    val  = arr[:,1]
    print(f"  omega0^2*R^2 spread: {prod.min():.3f}..{prod.max():.3f} (flat => BOX-CONTROL)")
    print(f"  omega0^2 values:     {val.min():.3e}..{val.max():.3e} (asymptote>0 => INTRINSIC)")
    if np.all(val>0) and (prod.max()/max(prod.min(),1e-300) < 5):
        verdict = "BOX-CONTROLLED (omega^2 ~ 1/R^2; wall artifact) -- NOT intrinsic"
    elif np.all(val<0):
        verdict = "NEGATIVE omega^2 (tachyonic instability), not a stable bound tower"
    elif val[-1] > 0.5*val[0] and prod.max()/max(prod.min(),1e-300) > 5:
        verdict = "INTRINSIC candidate (depth-controlled, asymptotes as R grows)"
    else:
        verdict = "ambiguous -- inspect"
    print("  VERDICT:", verdict)
    return verdict

print("\n### E4: regular-core + finite-cell(seal) Dirichlet eigenproblem ###")
v_flat = trap_test(prof['flat'], "flat phi=0, attractive Jacobi", l=1)
v_deep = trap_test(prof['deep'], "deep phi (p=1), attractive Jacobi", l=1)
v_flat0= trap_test(prof['flat'], "flat phi=0, l=0 (s-wave)", l=0)

# CONTROL: flip the curvature sign to +V_curv (would-be repulsive barrier) -- does a barrier bind?
print("\n### CONTROL: artificial REPULSIVE curvature (+V_curv) -- sanity that the solver CAN see binding/box behavior ###")
def trap_ctrl(profile,label,l):
    print(f"\n--- CONTROL +V_curv [{label}], l={l} ---")
    for R in [8.0,25.0,80.0,250.0]:
        w=eig_on_cell(profile,R,l,N=3000,sign='repulsive')
        print(f"  R={R:>6.1f}  omega0^2={w[0]:.6e}  omega0^2*R^2={w[0]*R**2:.4f}")
trap_ctrl(prof['flat'],"flat, repulsive",l=1)

print("\nDONE E3/E4.")
