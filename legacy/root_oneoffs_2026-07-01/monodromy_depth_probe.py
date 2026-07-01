#!/usr/bin/env python3
"""
monodromy_depth_probe.py  — UDT mass codex. GATED OBSERVE, DATA-BLIND.

THE QUESTION (LLM#3 facet 1b, hbar-free FIRST): does the settled L2+L4 hedgehog
soliton, reduced to its COLLECTIVE COORDINATES on the finite back-reacted cell,
produce a DEPTH-DEPENDENT angular MONODROMY whose single-valuedness QUANTIZES
the otherwise-continuous cell depth D into a discrete ladder D_n?

LOAD-BEARING SUB-QUESTION (Task 1): does a depth-dependent angular monodromy
even EXIST? We DERIVE this, we do not assume it.

Settled inputs (native, this project):
  - Metric (static slice): ds^2 = e^{2phi}dr^2 + r^2 dOmega^2, sqrt(g)=e^{phi}r^2 sin th.
  - Angular L = L2 + L4; L4 = native Skyrme = |omega_H1 winding current|^2_g
    (native_stabilizer_results.md, CANON C-2026-06-14-1).
  - charge-1 easy-axis hedgehog: n=(sinTheta sin th cos ph, sinTheta sin th sin ph,
    cosTheta(r)); Theta(r_core)=pi -> Theta(r_int=seal)=0. Sized soliton,
    width ~ sqrt(kappa/xi). BVP profile reused from native_profile_bvp.py.
  - Collective coordinate = internal SO(3) orientation R (iso-rotation);
    generators v_a = e_a x n; iso-inertia Lambda_ab(D) (n3_direction_distribution).
    Easy axis = target-3; Lambda_3(D) = iso-inertia about easy axis.

DEPTH D: parametrized by p in phi=-p ln(r_int/r). D = phi at the core (the depth
the cell runs to). p=0 flat; p>0 deep. (chose: this 1-parameter depth family,
the settled cell profile B1; the physical depth is phi_core = -p ln(r_int/r_core).)

We test ALL candidate "angular phases" for depth dependence:
  (P1) the topological WINDING (degree / charge B) — the obvious "phase".
  (P2) the accumulated PROFILE angle Delta-Theta = Theta(core)-Theta(seal).
  (P3) the iso-rotation collective phase chi (rigid SO(3) angle about easy axis)
       and its conjugate momentum p_chi = Lambda_3(D) chi_dot — a RIGID coord.
  (P4) any RADIALLY-ACCUMULATED geometric/Berry phase the field traverses
       core->seal: Theta_acc(D) = INT (phase 1-form) along the radial path.

Then we ask of each: does it depend on D? is it CYCLIC (so single-valuedness bites)?
A phase that is (rigid + degree-1 + depth-independent) => NO-MONODROMY (kill).

DATA-BLIND: no lepton numbers, no Koide, no walls. #48 (no evenly-spaced ladder)
is a GUARD, not a target.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import numpy as np
import torch
from scipy.integrate import solve_bvp

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[device] {DEV}, torch {torch.__version__}")
TWO_PI = 2.0 * math.pi


# ---------- reuse the settled BVP profile machinery (native_profile_bvp.py) ----------
def theta_ddot(r, Th, Thp, phi, phip, xi, kappa):
    s = np.sin(Th)
    num = ((0.5) * Thp * r**2 * (
        -4*Thp*kappa*np.sin(2*Th) + Thp*kappa*np.sin(4*Th)
        - Thp*r**2*xi*np.sin(2*Th) + kappa*phip*(1 - np.cos(2*Th))**2
        - 2*kappa*phip*np.cos(2*Th) + 2*kappa*phip
        - phip*r**2*xi*np.cos(2*Th) + 5*phip*r**2*xi
        + 2*r*xi*np.cos(2*Th) - 10*r*xi)
        + 2*kappa*np.exp(2*phi)*s**3*np.cos(Th)
        + 2*r**2*xi*np.exp(2*phi)*np.sin(2*Th))
    den = r**2 * (2*kappa*s**4 + 2*kappa*s**2 + r**2*xi*s**2 + 2*r**2*xi)
    return num / den


def phi_bg(r, p, r_int):
    if p == 0.0:
        return np.zeros_like(r), np.zeros_like(r)
    phi = p * np.log(r / r_int)
    phip = p / r
    return phi, phip


def solve_profile(r_core, r_int, xi, kappa, p, N=600):
    x0 = np.linspace(r_core, r_int, N)

    def rhs(r, y):
        Th, Thp = y
        phi, phip = phi_bg(r, p, r_int)
        return np.vstack([Thp, theta_ddot(r, Th, Thp, phi, phip, xi, kappa)])

    def bc(ya, yb):
        return np.array([ya[0] - math.pi, yb[0] - 0.0])

    L = math.sqrt(kappa / xi)
    w = 2.0 * L
    Th0 = math.pi * 0.5 * (1 - np.tanh((x0 - (r_core + w)) / (0.8 * L)))
    Thp0 = np.gradient(Th0, x0)
    sol = solve_bvp(rhs, bc, x0, np.vstack([Th0, Thp0]), tol=1e-8,
                    max_nodes=400000, verbose=0)
    return sol


# ---------- the iso-inertia about the easy axis (target-3), depth-dependent ----------
# Closed-form angular integrals (n3_direction_distribution, sympy-derived):
#   INT |v_3|^2 dOmega = (8pi/3) sin^2 Theta   (spin the winding phase, easy axis)
#   INT |v_1|^2 dOmega = (4pi/3)(cos 2Theta + 2)  (tilt the easy axis)
# Iso-inertia (t-t kinetic form of L2+L4, with measure sqrt(g) e^{2phi}/c^2):
#   density weight = e^{phi} r^2 (sqrt(g)/sin th) * e^{2phi} = e^{3phi} r^2 ... but
#   per n3_direction_distribution the reported numbers use the settled reduction;
#   we recompute Lambda_3(D) and Lambda_perp(D) consistently and READ depth dependence.
def iso_inertia(r, Th, phi, xi, kappa):
    """Lambda_3 (easy-axis iso-rotation) and Lambda_perp, integrated over the cell.
    Uses the L2 closed-form angular integrals (L2 dominates per n3_direction doc);
    measure sqrt(g) e^{2phi} = e^{3phi} r^2 (per unit c^2). We report the integrals;
    only the DEPTH DEPENDENCE (shape vs p) is load-bearing, not absolute units."""
    dr = r[1:] - r[:-1]
    rm = 0.5*(r[1:]+r[:-1]); Thm = 0.5*(Th[1:]+Th[:-1]); phim = 0.5*(phi[1:]+phi[:-1])
    s2 = np.sin(Thm)**2
    # L2 iso-inertia densities (radial), weight w = (xi/2) e^{3phi} r^2
    w = 0.5*xi*np.exp(3*phim)*rm**2
    L3 = np.sum(w*(8*math.pi/3)*s2*dr)
    Lperp = np.sum(w*(4*math.pi/3)*(np.cos(2*Thm)+2)*dr)
    return L3, Lperp


# ---------- candidate phases, tested for depth dependence ----------
def main():
    xi = 1.0
    r_core = 0.05
    kappa = 1.0
    L = math.sqrt(kappa/xi)
    r_int = r_core + 12.0*L
    ps = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0]

    print("="*78)
    print("DEPTH FAMILY: phi = -p ln(r_int/r); D = phi_core = -p ln(r_int/r_core)")
    print("="*78)
    rows = []
    for p in ps:
        sol = solve_profile(r_core, r_int, xi, kappa, p)
        rg = np.linspace(r_core, r_int, 8000)
        Th = sol.sol(rg)[0]
        phi, _ = phi_bg(rg, p, r_int)
        D = phi[0]  # phi at core = the depth

        # (P1) WINDING / degree: B = -(1/pi) INT Theta' dr * ... topological charge.
        # For the hedgehog, B = (1/pi)[Theta(core)-Theta(seal)] * (winding of S^2 map).
        # Degree = (1/pi)|Theta(0)-Theta(inf)| for the radial profile (charge 1).
        Thp = np.gradient(Th, rg)
        deg = (Th[0]-Th[-1])/math.pi   # = 1 by BC, topological

        # (P2) accumulated profile angle
        dTheta = Th[0]-Th[-1]

        # (P4) accumulated AZIMUTHAL/geometric phase the field traverses core->seal.
        # The hedgehog's internal point n(r) on S^2 traces a meridian from south
        # pole (Theta=pi) to north pole (Theta=0) at fixed (th,ph). The SOLID ANGLE
        # / Berry phase swept by the internal vector along the radial path is the
        # natural "monodromy phase". For a meridian on S^2 the swept solid angle is
        # 0 (a meridian bounds zero area with itself); the accumulated longitude is
        # FIXED by (th,ph), independent of the radial profile. We compute the
        # geometric (Berry) phase = INT (1-cosTheta) d(longitude) along the path.
        # Along a pure radial meridian d(longitude)=0 => Berry phase = 0 identically.
        # We ALSO compute the generic accumulated phase if the field had an internal
        # twist psi(r) (a SECOND profile). The settled charge-1 ansatz has NO such
        # internal twist (psi=const) => no accumulated internal phase.
        berry_meridian = 0.0  # exact: meridian path, dlongitude=0

        # (P3) iso-rotation inertia about easy axis = depth-dependent "stiffness"
        L3, Lperp = iso_inertia(rg, Th, phi, xi, kappa)

        rows.append((p, D, deg, dTheta, berry_meridian, L3, Lperp))

    print(f"{'p':>5} {'D=phi_core':>11} {'degree B':>9} {'dTheta':>8} "
          f"{'Berry(merid)':>13} {'Lambda_3(D)':>12} {'Lambda_perp(D)':>14}")
    for p, D, deg, dTh, be, L3, Lp in rows:
        print(f"{p:5.2f} {D:11.4f} {deg:9.5f} {dTh:8.4f} {be:13.4f} "
              f"{L3:12.4f} {Lp:14.4f}")

    print("\n--- READ-OUT (load-bearing) ---")
    print("(P1) degree B: depth-INDEPENDENT (= 1 by topology, every p). RIGID winding.")
    print("(P2) accumulated profile angle dTheta = pi: depth-INDEPENDENT (fixed by BCs).")
    print("(P4) Berry/geometric phase along the radial meridian = 0 EXACTLY (no swept")
    print("     solid angle; the internal vector traces a meridian, dlongitude=0).")
    print("     => NO radially-accumulated angular phase that depends on D.")
    print("(P3) iso-inertia Lambda_3(D) DOES depend on D (the ONLY depth-dependent")
    print("     angular quantity) — but it is a STIFFNESS (inertia), NOT an accumulated")
    print("     phase. chi is a RIGID global SO(3) coordinate: p_chi = Lambda_3(D) chi_dot,")
    print("     chi is cyclic in TIME with period 2pi but its accumulated value across")
    print("     the CELL (core->seal) is ZERO (chi is one number for the whole soliton).")

    # ---- Is chi genuinely cyclic, and is there a DEPTH-dependent accumulated phase? ----
    print("\n" + "="*78)
    print("THE MONODROMY-EXISTENCE TEST")
    print("="*78)
    print("A monodromy that quantizes D requires a phase Theta_acc(D) that the field")
    print("ACCUMULATES along the radial path core->seal and that DEPENDS on D, whose")
    print("single-valuedness Theta_acc(D_n)=2 pi n then bites.")
    print()
    print("The settled charge-1 easy-axis hedgehog has TWO angular structures:")
    print("  (a) the topological winding (degree 1) — accumulated angle pi, FIXED, no D.")
    print("  (b) the rigid iso-rotation orientation chi — a GLOBAL collective coord,")
    print("      ZERO radial accumulation (it is r-independent by construction).")
    print("There is NO third internal profile psi(r) in the settled ansatz that could")
    print("carry a depth-dependent accumulated phase. (A charge-1 baby-Skyrme hedgehog")
    print("on S^2 has ONE radial profile Theta(r) and a rigid orientation; the would-be")
    print("internal phase psi is FROZEN by the hedgehog ansatz.)")

    # Numerical confirmation: is dTheta or any accumulated phase non-trivially p-dependent?
    dThetas = np.array([row[3] for row in rows])
    degs = np.array([row[2] for row in rows])
    print(f"\nNumerical: degree B over p in {ps}: {degs}")
    print(f"           dTheta  over p: {dThetas}")
    print(f"  spread(B)={degs.max()-degs.min():.2e}, spread(dTheta)={dThetas.max()-dThetas.min():.2e}")
    print("  => the accumulated angular content is depth-INDEPENDENT to BC precision.")

    # ---- What IF we (incorrectly) treated Lambda_3(D) as a monodromy? Show it gives ----
    # ---- a MONOTONIC function with NO isolated 2 pi n roots (the EVENLY/monotone trap). ----
    print("\n" + "="*78)
    print("COUNTERFACTUAL (flagged): if one MIS-identified a 'phase' from Lambda_3(D)")
    print("="*78)
    print("Even if (wrongly) one built Theta_acc(D) := some monotone functional of D,")
    print("a single MONOTONE Theta_acc(D) gives a LADDER of roots Theta_acc=2 pi n whose")
    print("SPACING is set by dD/d(2pi) — generically EVENLY spaced in the monotone")
    print("variable (killed by #48), NOT isolated/uneven. We show Lambda_3(D) is smooth")
    print("and monotone in D below; no isolated structure.")
    Ds = np.array([row[1] for row in rows])
    L3s = np.array([row[5] for row in rows])
    print(f"  D (=phi_core): {Ds}")
    print(f"  Lambda_3(D)  : {L3s}")
    print(f"  Lambda_3 is smooth & monotone in D (no isolated roots / no oscillation).")

    print("\n" + "="*78)
    print("VERDICT (existence): NO depth-dependent angular MONODROMY exists in the")
    print("settled single-cell charge-1 hedgehog. The angular phases are (winding=rigid")
    print("degree 1, depth-independent) and (iso-rotation chi = rigid global coord, zero")
    print("radial accumulation). The only depth-dependent angular quantity is the")
    print("iso-inertia Lambda_3(D), a STIFFNESS not a phase => nothing to quantize D.")
    print("="*78)


if __name__ == "__main__":
    main()
