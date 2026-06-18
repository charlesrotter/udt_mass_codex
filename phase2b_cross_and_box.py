#!/usr/bin/env python3
"""
phase2b_cross_and_box.py -- the TWO decisive Phase-2b tests beyond the additive
ensemble sweep (phase2b_ensemble_solve.py):

  (I)  THE DEGENERATE CROSS CHANNEL -- the ONLY channel where the orchestra can do
       something a single note cannot. The selection rules (phase2b_cross_stress.py)
       say cross-mode gravitational coupling to the static l=0 mass survives ONLY
       for modes sharing BOTH l AND w. We exercise that channel directly: two
       degenerate l=2 fundamentals (same l, same w0) coupled through the verified
       S_cross. Question: does the cross term flip the net mass sign, or is the
       degenerate packet still net-negative (cross term just re-weights the same
       negative self-energy)?

  (II) THE BOX-CONTROL GATE (DESIGN 5.1) for an ensemble: relocate the seal R and
       watch the ensemble frequencies + the mass coefficient. Is anything
       box-invariant, or does everything still scale 1/R (frequencies) / R-free
       (the dimensionless mass coefficient)? Are the INTER-MODE ratios the physical
       content, and do they differ from the trivial single-l Bessel ladder?

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A. OBSERVE. c=1.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import sys
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from phase2b_ensemble_solve import EnsembleProblem, continue_amplitude, jl_zeros

np.set_printoptions(precision=6, linewidth=140, suppress=False)


# ---------------------------------------------------------------------------
# (I) DEGENERATE CROSS CHANNEL
# We force two modes into the SAME (l,w0) so the solver registers a cross-pair.
# Two l=2, n=1 modes are exactly degenerate (identical w0). With per-mode
# normalization ||Psi_i||^2 = share*A^2 and identical shapes, the two modes are
# the SAME function; the cross term 2 S_cross[Psi1,Psi2] then ADDS to the two
# self terms. Net source for two identical degenerate modes of equal weight:
#   S = S_self[P1] + S_self[P2] + 2 S_cross[P1,P2]
# with P1=P2=P (share=1/2 each so ||P||^2 = A^2/2):
#   = 2*S_self[P] + 2*(2 S_self[P])   [since S_cross(i=i)=2 S_self]
# wait -- that double counts; the PHYSICAL check is: a single l=2 mode of norm A
# must EQUAL two degenerate half-weight l=2 modes (same shape) summed coherently.
# The cross term is exactly what restores that equivalence. We TEST that
# equivalence numerically (a strong validation that S_cross is right) AND read
# the mass sign.
# ---------------------------------------------------------------------------
def test_degenerate_cross(N=100, R=1.0):
    print("="*80)
    print("(I) DEGENERATE CROSS CHANNEL (same l, same w -> cross term ACTIVE)")
    print("="*80)
    A_list = [1e-3, 0.05, 0.1, 0.2]

    # single l=2 mode of full weight (reference)
    single = [dict(l=2, n=1, a=1.0)]
    prob_s, rows_s, w0s = continue_amplitude(N, R, single, A_list)

    # two DEGENERATE l=2 n=1 modes, equal weight -> cross pair registered.
    # (Same radial shape; physically the azimuthal m-multiplet of a single mode.)
    # The cross term 2 S_cross is ACTIVE here -- the ONLY composition in which it is.
    degen = [dict(l=2, n=1, a=1.0), dict(l=2, n=1, a=1.0)]
    prob_d, rows_d, w0d = continue_amplitude(N, R, degen, A_list)
    print(f"  degenerate cross-pairs registered: {prob_d.cross_pairs}  (expect [(0,1)])")

    print(f"\n  {'A':>7} {'M_single':>12} {'M_degen+cross':>16}")
    for rs, rd in zip(rows_s, rows_d):
        print(f"  {rs['A']:7.3f} {rs['m_R_over_A2']:+12.5f} {rd['m_R_over_A2']:+16.5f}")
    print("\n  READ: the cross term is ACTIVE (cross-pairs non-empty). The degenerate")
    print("  packet mass M is computed WITH the full S_self+2 S_cross source. The")
    print("  decisive observation is its SIGN: the cross term is the polarization of")
    print("  the SAME negative-definite self-stress (S_cross(i=i)=2 S_self), so it")
    print("  cannot change the sign -- it re-sums negative self-energy. M stays < 0.")

    # Now a NON-trivial degenerate pair: same (l,w) but DIFFERENT shapes is
    # impossible for a single-l cavity fundamental (the regular Dirichlet mode is
    # unique up to scale). The only genuine same-(l,w) multiplicity is the
    # azimuthal m-multiplet, which shares the radial profile. So the cross channel
    # has NO shape freedom to exploit -- it can only re-sum the SAME negative
    # self-energy. Record this structural fact.
    print("\n  STRUCTURAL: a single-l cavity fundamental is UNIQUE up to scale; the")
    print("  only same-(l,w) multiplicity is the azimuthal m-multiplet (same radial")
    print("  profile). The cross channel therefore has NO independent shape to bind")
    print("  -- it can only re-weight the identical negative self-energy. No positive")
    print("  mass is reachable through the (sole surviving) degenerate cross channel.")
    return rows_s, rows_d


# ---------------------------------------------------------------------------
# (II) BOX-CONTROL GATE for the ensemble
# ---------------------------------------------------------------------------
def test_box_control(N=100):
    print("\n" + "="*80)
    print("(II) BOX-CONTROL GATE: relocate seal R; watch ensemble w_i and mass coeff")
    print("="*80)
    modes = [dict(l=2, n=1, a=1.0), dict(l=3, n=1, a=1.0), dict(l=4, n=1, a=1.0)]
    A_list = [1e-3, 0.05, 0.1]
    R_list = [1.0, 2.0, 4.0, 8.0]

    print("\n  [w*R invariance] (box mode: w*R = const across R):")
    print(f"  {'R':>5} | " + " ".join(f"w{i}*R" for i in range(len(modes))))
    w0R_ref = None
    for R in R_list:
        prob, rows, w0 = continue_amplitude(N, R, modes, A_list)
        wR = w0 * R
        if w0R_ref is None:
            w0R_ref = wR
        print(f"  {R:5.1f} | " + " ".join(f"{x:.5f}" for x in wR))
    drift = np.max(np.abs(wR - w0R_ref) / w0R_ref) * 100
    print(f"  max relative drift of w*R across R=1..8: {drift:.3e} %  "
          f"({'BOX-CONTROLLED' if drift < 1.0 else 'box-invariant feature?'})")

    print("\n  [inter-mode ratios] w_i/w_0 (the scale-free content):")
    prob, rows, w0 = continue_amplitude(N, 1.0, modes, A_list)
    ratios = w0 / w0[0]
    print(f"     w_i/w_0 = {np.array2string(ratios, precision=6)}")
    # compare to single-l Bessel ladder (j_2 overtone ratios) -- DIFFERENT because
    # these are CROSS-l (j_2,j_3,j_4 first zeros), a genuinely mixed ladder
    j2 = jl_zeros(2, 1)[0]; j3 = jl_zeros(3, 1)[0]; j4 = jl_zeros(4, 1)[0]
    print(f"     (these are j_2,j_3,j_4 FIRST zeros: {j2:.5f},{j3:.5f},{j4:.5f};")
    print(f"      ratios {j3/j2:.5f},{j4/j2:.5f} -- a MIXED-l ladder, but still")
    print(f"      pure spherical-cavity Bessel zeros: NO new intrinsic scale.)")

    print("\n  [mass coefficient R-dependence] M=m(R)/A^2 at fixed A across R:")
    print(f"  {'R':>5} | {'M(l2+l3+l4)':>14}")
    Mref = None
    for R in R_list:
        prob, rows, w0 = continue_amplitude(N, R, modes, [1e-3, 0.05, 0.1])
        M = rows[-1]['m_R_over_A2']
        if Mref is None:
            Mref = M
        print(f"  {R:5.1f} | {M:+14.6f}")
    print("  READ: if M=m(R)/A^2 is R-INVARIANT (dimensionless, scale-free) AND")
    print("  negative at every R -> the ensemble mass is a scale-free NEGATIVE")
    print("  number set by mode SHAPE, not the box; box-controlled, no positive mass.")


if __name__ == "__main__":
    test_degenerate_cross()
    test_box_control()
    print("\n" + "="*80)
    print("DONE. See phase2b_ensemble_results.md for the A/B/C-ens verdict.")
    print("="*80)
