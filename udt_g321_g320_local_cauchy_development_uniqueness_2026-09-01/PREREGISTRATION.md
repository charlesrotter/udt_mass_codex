# G321 preregistration — conditional local development uniqueness

Date: 2026-09-01
Status: `PREREGISTERED_BEFORE_OUTCOME_SCRIPTS_OR_RESULTS`

## 1. Frozen bounded frame

Retain the exact G320 family reconstructed from the G319 flat marked-`T^3`, one-coordinate,
diagonal-TT, smooth positive periodic, sign-definite `B!=0` slice. Do not change the active
owner-provisional response equation, metric, reciprocal kernel, angular interface, or data.

## 2. Fixed mathematical question

For each complete datum `(Sigma,gamma,K)`, determine whether all smooth local developments solving
the active equation are equivalent by a spacetime diffeomorphism that commutes with the initial
embedding. This is geometric Cauchy uniqueness. It is not the selection of initial data.

## 3. Theorem hypotheses to be audited

The conditional imported local theorem may be applied only if all of the following pass:

1. `Sigma=T^3` is a smooth compact boundary-free three-manifold;
2. `gamma=psi^4 delta` is smooth and positive definite;
3. reconstructed `K` is smooth and symmetric on the regular `B!=0` branch;
4. the Hamiltonian and momentum constraints hold;
5. the Hamiltonian value is spatially constant and fixes one `Lambda` sector;
6. after harmonic reduction the equation has the full metric-wave principal operator;
7. gauge constraints have homogeneous propagation;
8. lapse, shift, and harmonic-coordinate data are presentation choices, not extra physical data.

Failure of any item blocks the uniqueness landing.

## 4. Registered controls

Use only the already registered G320 controls

```text
psi_n=3/2+(1/5)cos(nx), n in {1,2,3,4},
d=0, Lambda=0, J0=100, epsilon in {-1,+1}.
```

These numbers are diagnostic, not physical pins. The exact G319 compactness theorem, rather than
finite sampling, carries the extension to each positive integer mode after a sufficiently large
free `J0` is supplied.

## 5. Initial evolution map

For the presentation control `N=1`, `beta=0`, compute without integrating in time

```text
partial_t gamma_ij = -2 K_ij,
partial_t K_ij = R3_ij + K K_ij - 2 K_i^k K_kj
```

at `Lambda=0`. A fixed complete datum must produce exactly one right-hand side. This is a local
consistency check, not by itself a proof of PDE uniqueness; the latter remains conditional on the
declared harmonic well-posedness theorem.

## 6. Time reversal

The two registered signs must satisfy

```text
(gamma,K) -> (gamma,-K),
partial_t gamma -> -partial_t gamma,
partial_t K -> partial_t K
```

in the unit-lapse zero-shift presentation. They are two different full data sets related by time
reversal, not two futures emitted by the same `(gamma,K)` datum.

## 7. Marked-development distinction

If a data-preserving isometry identified modes `n!=m`, it would pull back their initial metrics and
preserve G320's `Q_R`. Since `Q_R(n)=n^2 Q_R(1)`, no such marked equivalence exists. Do not infer
that the unmarked maximal spacetimes cannot contain the data as different hypersurfaces.

## 8. Possible landings

1. `G320_DATA_HAVE_CONDITIONAL_UNIQUE_LOCAL_MARKED_DEVELOPMENTS` if every theorem hypothesis,
   constraint, gauge quotient, and independent check passes;
2. `G320_DATA_FAIL_LOCAL_WELLPOSEDNESS_HYPOTHESES` if a registered datum is unlawful or irregular;
3. `LOCAL_DEVELOPMENT_NONUNIQUENESS_FOUND` if one fixed datum has inequivalent local solutions;
4. `G321_INCONCLUSIVE` if implementations or theorem-hypothesis audits disagree.

## 9. Certification and falsification contract

- Production independently reconstructs the registered data, constraints, intrinsic Ricci tensor,
  and first ADM right-hand side without importing G319/G320 code or outputs.
- An implementation-distinct verifier uses different modes, amplitudes, sample count, and direct
  connection/Ricci loops; it must not import production functions or read production results.
- Hostile checks must reject wrong Hamiltonian sign, nonconstant inferred `Lambda`, omitted momentum,
  treating lapse/shift as physical branches, collapsing `K` signs, wrong time-reversal parity,
  calling first-jet determinism a PDE proof, erasing the imported-theorem caveat, and upgrading
  marked-local uniqueness to unmarked or global history selection.
- Run the exact premise verifier and full repository test suite.
- Require fresh external adversarial review before an externally accepted grade.

Maximum conclusion: conditional on the already declared smooth local well-posedness import, each
registered G320 datum has one local marked development up to diffeomorphism, so the demonstrated
breadth is ordinary initial-data freedom inside this bounded arena rather than a missing local
equation. No physical occupancy, complete global history, unmarked-spacetime classification,
topology, population, scale, observation, source, matter/mass, `X_max`, metric change, or kernel
change may be claimed.
