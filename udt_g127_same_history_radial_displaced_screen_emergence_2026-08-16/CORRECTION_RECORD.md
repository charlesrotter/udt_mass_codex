# G127 correction record

Date: 2026-08-16

Repairs made after the first blind verdict:

1. Added `PREREGISTRATION_SCOPE_CORRECTION.md`; all reports now distinguish the shared
   finite-radius symmetry-radial control from G119's separate center-vertex query.
2. Replaced every load-bearing “shear equals `sin(alpha)^2 Xi`” statement with the precise tidal
   contrast and Jacobi-map contrast. Added the optical deformation derivation
   `B=D'D^-1=I/lambda-lambda Rperp/3+O(lambda^2)` and its trace-free shear.
3. Reclassified `Xi` as a spherically adapted curvature contrast.
4. Replaced the hard-coded production tilt by symbolic `sin(alpha), cos(alpha)` contractions and
   a genuine `alpha -> -alpha` check. The `3/5,4/5` direction remains only an exact witness.
5. Expanded production verification from 23 to 26 checks and independent verification from 14 to
   17 checks, including three independent optical-shear checks. Updated all status and evidence
   bookkeeping.

No metric history, angular coefficient, `mu`, observation, second history, or protected package
was introduced.
