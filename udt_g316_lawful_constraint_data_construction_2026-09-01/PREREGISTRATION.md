# G316 preregistration — lawful constraint-data construction

Date: 2026-09-01
Status: `PREREGISTERED_BEFORE_DERIVATION_OR_OUTCOME_FILES`

## Whole bounded question

For the G315 constraints

\[
{}^{(3)}R+\frac23\tau^2-A_{ij}A^{ij}=2\Lambda,
\qquad
D_jA^{ij}-\frac23D^i\tau=0,
\]

determine:

1. an independent conformal construction of lawful spacelike data;
2. exactly which quantities are freely supplied seeds and which must be solved;
3. explicit existence, nonexistence, and degeneracy controls without claiming a full global
   solvability theorem;
4. the residual null-normal boost gauge at a two-sheet corner;
5. what a single null sheet cannot supply;
6. whether any of these constructions selects a physical history, scale, topology, or kernel.

## Preregistered conformal identities

In three spatial dimensions write

\[
\gamma_{ij}=\psi^4\bar\gamma_{ij},\qquad \psi>0,
\]

\[
K_{ij}=A_{ij}+\frac13\tau\gamma_{ij},
\qquad
A^{ij}=\psi^{-10}\bar A^{ij},
\]

and decompose

\[
\bar A^{ij}=\bar A_{TT}^{ij}+(\bar L W)^{ij},
\]

where

\[
(\bar L W)^{ij}=\bar D^iW^j+\bar D^jW^i
-\frac23\bar\gamma^{ij}\bar D_kW^k.
\]

Test the transformed system

\[
\boxed{
-8\bar\Delta\psi+\bar R\psi
-|\bar A_{TT}+\bar L W|_{\bar\gamma}^2\psi^{-7}
+\left(\frac23\tau^2-2\Lambda\right)\psi^5=0,
}
\]

\[
\boxed{
\bar D_j(\bar L W)^{ij}
=\frac23\psi^6\bar D^i\tau.
}
\]

The seed tuple is preregistered as the conformal geometry, a transverse-traceless tensor, mean
curvature, connected `Lambda`, and all topology/boundary/asymptotic choices. `psi` and the
longitudinal correction `W` are solved variables when a solution exists. Lapse and shift remain
evolution gauge and do not enter this construction.

Constant-mean-curvature (`bar D tau=0`) is a diagnostic subcase in which the vector and scalar
equations decouple. It is not promoted to a UDT premise or a complete chart on all lawful data.

## Preregistered solvability and degeneracy controls

On a connected compact slice without boundary, test:

1. the vector operator has conformal-Killing fields in its kernel; solvability requires the source
   to be orthogonal to that kernel, and `W` is nonunique modulo kernel elements while `bar L W`
   remains unchanged;
2. with `bar R=0`, `|bar A|^2=a^2>0`, and
   `C=(2/3)tau^2-2Lambda>0`, a constant positive solution obeys
   `psi^12=a^2/C`;
3. with the same nonzero `a^2` and `C<=0`, the integrated scalar equation forbids a positive
   solution;
4. with `bar A=0`, constant `bar R=R0`, and constant `C`, a nonzero constant solution requires
   `psi^4=-R0/C>0`;
5. with `bar R=0`, `bar A=0`, and `C=0`, every positive constant `psi` solves the scalar equation,
   displaying an unfixed homothety rather than a selected scale;
6. the round positive bounce and flat positive slicing from G315 are reconstructed as exact lawful
   controls, but are not selected over other data.

These controls establish that seed-to-data construction has real existence and degeneracy gates.
They do not constitute a global Yamabe/non-CMC/boundary classification.

## Preregistered null-corner identities

At a regular screen `S` where two null hypersurfaces intersect, choose null normals `ell,k` with
`g(ell,k)=-1`. Under the local boost

\[
\ell\mapsto e^f\ell,\qquad k\mapsto e^{-f}k,
\]

test:

\[
q_{AB}\mapsto q_{AB},
\quad
\theta_{(\ell)},\sigma^{(\ell)}_{AB}\mapsto
e^f\theta_{(\ell)},e^f\sigma^{(\ell)}_{AB},
\]

\[
\theta_{(k)},\sigma^{(k)}_{AB}\mapsto
e^{-f}\theta_{(k)},e^{-f}\sigma^{(k)}_{AB}.
\]

Thus the cross-products `theta_(ell) theta_(k)` and
`sigma_(ell):sigma_(k)` are boost invariant. For the normal-bundle connection in the registered
sign convention, test its inhomogeneous shift by a screen gradient and the invariance of its curl.
The mixed equation `Ric(ell,k)=-Lambda` is also boost invariant.

The maximum corner claim is only that cross-normalization leaves a local boost gauge and that one
null sheet does not determine the data/transport hierarchy on the transverse sheet. No
formalism-independent minimal characteristic list or global two-sheet existence theorem is claimed.

## Certification and falsification contract

Production must derive the registered powers, coefficients, seed roles, integral controls, and
boost weights from G315 plus stated mathematical identities. An implementation-distinct
standard-library verifier must rebuild the load-bearing algebra without importing production
functions or result files. Hostile mutations must catch at least:

- wrong conformal powers `4`, `-10`, `-7`, `5`, or `6`;
- wrong sign of `Lambda` or of the TT norm in the scalar equation;
- calling arbitrary seed data lawful before solving both constraints;
- promoting CMC, conformal flatness, topology, roundness, or a sign to UDT;
- hiding the conformal-Killing kernel or calling `W` unique;
- turning a positive constant `psi` into a derived physical scale;
- treating null-normal boost gauge as measured distance or clock calibration;
- declaring one null sheet complete;
- selecting a physical history, population, scale, topology, `X_max`, or kernel;
- importing an action, source, matter/mass model, observation, fit, or protected work.

Run the full premise verifier and repository tests before banking. A fresh external adversarial
review is required before any externally accepted grade.

## Preregistered landing classes

Exactly one maximum landing may be used:

1. `CONFORMAL_CONSTRUCTION_MAPS_A_LAWFUL_SUBSET_WITH_NONTRIVIAL_SOLVABILITY_AND_CORNER_GAUGE_BOUNDS__NO_PHYSICAL_DATA_SELECTION`
2. `CONFORMAL_CONSTRUCTION_UNIQUELY_PARAMETERIZES_ALL_LAWFUL_DATA_AND_SELECTS_ONE_HISTORY`
3. `REGISTERED_CONSTRUCTION_FAILS_THE_G315_CONSTRAINTS`
4. `CLASSIFICATION_INCONCLUSIVE_WITHIN_REGISTERED_SCOPE`

No landing changes the metric, reciprocal kernel, angular cancellation, observational interface,
or premise grades.
