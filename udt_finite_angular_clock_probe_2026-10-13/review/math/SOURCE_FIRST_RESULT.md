# Source-first independent result

Frozen before any FAC1 author result/script or RECOVERY content was read.
TPS1 source_first_run01 completed successfully in 0.847s, 54,832KiB maximum
RSS, 2GiB virtual-memory cap, one thread, no wall/CPU timeout, empty stderr.
Python3.10.12 and SymPy1.13.1 performed exact rational polynomial operations.

For the analytic supplied metric and preparation in SOURCE_FIRST.md, define
D=nx²-ny² and T=nx²+ny²=1-z². Independent world-function calculation gives

    log p_plus  = D L²/4 +(D²-T z²-4T z)L⁴/96+O(L⁶),
    log p_minus = D L²/4 +(D²-T z²+4T z)L⁴/96+O(L⁶).

Thus each **full preparation-sphere mean** is

    M_plus=M_minus=L⁴/720+O(L⁶).

The displayed equality concerns the two coefficients; the exact equality of
the full means is suggested by z reflection and is not required for the sign
witness. There are directional blueshifts at leading order. The positive mean
does not imply all-direction positivity or positional attribution. Restoring
plane-wave amplitude a gives a²L⁴/720 at quartic order.

Independent checks passed: both perturbed incidence roots through L⁵,
two arrangements of the implicit clock derivative through L⁴, flat reduction,
and exact angular moments. The incidence equation's flat scaled derivative is
-2 on either future root, uniformly in direction. The entire functions S,C and
removable z=0 and Δu=0 expressions give analytic coefficients across S² for a
small common neighborhood. Compactness then makes the O(L⁶) remainder uniform,
so both means are strictly positive for sufficiently small nonzero L. This does
not furnish a numeric radius, finite-amplitude certification, or all-observer
classification.

No independent finite numerical null solver was run at this stage. No author
checks were imported. The independently derived positive witness is compatible
with there being other Ricci-flat controls of either sign; it establishes no
general sign theorem. Source pins and this stage's output hash are recorded in
SOURCE_FIRST_PINS.json; hashes bind bytes rather than prove correctness or time.
