# Frozen source-first reconstruction result

This note was prepared before any candidate/code/results exposure.
The source-first check completed successfully on Python 3.10.12 / SymPy 1.13.1,
0.2171s wall, 47088 KiB reported child maximum RSS, within 512 MiB/60s limits.
Exact captured argv, times, resource ceiling and stdout/stderr are in
source_first.json/.stdout/.stderr. The script imports SymPy and standard
library only, with no campaign scientific import or source-result replay.

The generic symmetric bivector form has 21 parameters; first Bianchi and
Einstein equations have joint rank 10, leaving 11. The declared 24 symmetric
record entries have rank 11 on that space, with a 13-dimensional exact left
annihilator. Six null screens alone have rank 10; E alone has rank 6.
Deleting the mixed-curvature block reduces full rank from 11 to 6. These
exact ranks are checked independently of an electric/magnetic parametrization.
All 256 component Bianchi relations and all six null trace identities vanish.
A constant-curvature tensor has E=-I and all null tides zero. A symmetric,
trace-free changed pair of null records can fail joint image membership.

The exact observation matrix and its left annihilator establish a finite
linear-algebra compatibility criterion: records lie in the annihilator's
kernel iff they belong to the 11-dimensional observation image; full rank
makes the algebraic Einstein tensor unique. This is not a sufficiency theorem
for an already supplied metric, a Cauchy datum/development, or physical data.

Analytic parity reconstruction can alternatively define
F_mj=(1/2)epsilon_mab R_ab0j, where F is symmetric trace-free in the Einstein
subspace. For cyclic (i,a,b)=(1,2,3),(2,3,1),(3,1,2), let
Delta_i=(T_i^+-T_i^-)/2 in screen (a,b). Then
Delta_i,aa=-2F_ab, Delta_i,bb=2F_ab,
Delta_i,ab=F_aa-F_bb. The three offdiagonal F entries and three diagonal
differences with one cyclic dependence recover all five F degrees of freedom.
The sign follows the explicitly declared R_abcd=g(R(ea,eb)ec,ed) ordering;
other component conventions must be translated, not assumed to agree.

Omissions: no full registry verifier, source-package reruns, formal proof
assistant, PDE realization/existence proof, spacetime extension, laboratory
readout/finite-time approximation, observations, GPU, archive, network,
different-model or human-specialist review. This is a fresh source-first
argument with implementation-distinct algebraic checks, not independent
physical premises. No verdict on the candidate has yet been issued.
