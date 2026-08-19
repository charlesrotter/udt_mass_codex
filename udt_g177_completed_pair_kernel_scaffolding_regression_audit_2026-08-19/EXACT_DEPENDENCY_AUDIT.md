# G177 exact dependency audit

Date: 2026-08-19

## Minimal reconstruction

The complete bounded scalar kernel needs exactly four layers:

```text
primary metric
-> supplied regular pair germ
-> complete pair pullback
-> completed-pair Dual Reciprocity.
```

For a raw symmetric Lorentzian pair matrix

\[
h_\sigma=
\begin{pmatrix}
h_{00}&h_{01}\\
h_{01}&h_{11}
\end{pmatrix},
\qquad h_{00}<0,\quad \det h_\sigma<0,
\]

the unique regular decomposition is

\[
T^2=-h_{00},\qquad
\beta=\frac{h_{01}}{h_{00}},\qquad
L_\sigma^2=h_{11}-\frac{h_{01}^2}{h_{00}}.
\]

The identity

\[
T^2L_\sigma^2=-\det h_\sigma
\]

holds directly. Completed-pair Dual Reciprocity then gives

\[
m^2=T^2L_\sigma^2=-\det h_\sigma,
\qquad
\Phi=-\log T.
\]

No path, dimensionful position, score, carry, observer-only potential, fitted profile, or physical
mechanism appears in the proof.

## Orchestra audit

The entries \(h_{00},h_{01},h_{11}\) are read only after the complete pullback. Therefore every
angular, screen, mixing, and shift contribution that the metric and supplied germ place in the pair
tensor is upstream.

- Changing \(h_{11}\) at fixed \(h_{00},h_{01}\) changes \(m^2=-\det h_\sigma\): spatial orchestra
  changes the reciprocal tape.
- Changing \(h_{00}\) changes \(T\) and hence \(\Phi\): clock-side orchestra changes depth.
- Nonzero \(h_{01}\) gives nonzero \(\beta\); determinant normalization does not erase shift.

No additive angular term is appended after \(\Phi\).

## Executable dependency census

The G176 production AST imports only `__future__`, `hashlib`, `json`, `pathlib`, and `sympy`. None of
the registered scaffold identifiers occurs as an executable identifier. Source-hash and reporting
strings are evidence plumbing, not mathematical dependencies.

## Deletion audit

Twenty-eight preregistered catches remove or prohibit:

- `X_max`, paths, connections, holonomy, Jacobi, and universal cocycles;
- G142--G160 score/carry/torsor/history machinery;
- observer-only potentials and arbitrary triangle closure;
- post-readout angular terms, scalar `mu`, and frozen orchestra coefficients;
- arclength or hidden ruler densities;
- fits, radiative transfer, actions, sources, matter, bootstrap, and dynamics;
- co-presence selection and signal-speed claims.

The generic matrix reconstruction is unchanged after every deletion because none is an antecedent
of the theorem.

## Boundary

The supplied pair germ remains genuinely supplied. G177 does not turn scalar normalization into an
event-pairing or global-realization theorem. Non-scalar route/frame channels also remain separate.

## Landing

```text
SCAFFOLD_FREE_BOUNDED_KERNEL
__ONLY_METRIC_GERM_PULLBACK_AND_DUAL_RECIPROCITY_LOAD_BEARING
```

This landing is conditional on the G176 `WORKING_FOUNDATIONAL_CLARIFICATION`, is local to regular
rank-two completed pairs, and is not canon.
