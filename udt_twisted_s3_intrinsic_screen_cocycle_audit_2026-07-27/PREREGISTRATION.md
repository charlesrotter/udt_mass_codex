# Preregistration — twisted `S3` intrinsic screen and same-branch cocycle

Date: 2026-07-27

Base: `fe44d27bd7650de1eff923249f4fa73e75206935`

Question type: **METRIC-LED, BOUNDED SAME-CONFIGURATION JOIN AUDIT**.

## Whole question

The earlier observer-optical and path-cocycle audits derived the transverse Jacobi machinery, but
the registered complete branches then had trivial clocks.  The new twisted `R x S3` family contains
complete configurations whose metric intrinsically identifies a nontrivial clock line and whose
clock twist identifies the reciprocal ruler line.  Does that same metric now supply:

1. a unique transverse two-plane and its local area density;
2. an exact endpoint clock ratio equal to the founded depth difference for the intrinsic stationary
   observers;
3. the complete transverse Jacobi phase-space propagator on the same supplied geodesic; and
4. one nontrivial same-branch longitudinal/transverse path cocycle, without splicing branches?

The audit must also determine whether the local transverse coframe area can honestly be identified
with the WR-L/SNe vertex angular-distance law.  It may not fit `lambda`, choose a path, or assume that
the local area density is an optical Jacobi determinant.

## Premise stamps carried unchanged

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

Co-presence is not used as a signalling law or field equation.  The result must survive if that
interpretive frame is later replaced.

## Frozen metric family and candidate universe

Use only the parent-audited complete coframe

```text
tau     = dt + a sigma_3
theta_0 = exp(-phi) tau
theta_1 = exp(+phi) sigma_3
theta_2 = exp(lambda phi) sigma_1
theta_3 = exp(lambda phi) sigma_2
g       = -theta_0^2 + theta_1^2 + theta_2^2 + theta_3^2,
d sigma_3 = kappa sigma_1 wedge sigma_2,  kappa=-2.
```

Candidates C01–C06 and controls C07–C08 are frozen in `CANDIDATE_UNIVERSE.tsv`.  No profile,
amplitude, twist, topology, `lambda`, scale, event, or invariant certificate may be retuned.

For C01–C06 the parent result may be used exactly as frozen:

- the unique continuous timelike Killing line is `span(K)`, `K=partial_t`;
- `g(K,K)=-exp(-2 phi)` in the registered units;
- the nonzero Killing twist spans the reciprocal ruler line `theta_1`;
- the metric is smooth and Lorentzian on `R x S3`, with the displayed slice spacelike.

This audit must not promote those off-shell configurations into selected solutions.

## Objects to derive

Let `u=K/sqrt(-g(K,K))`.  Let `n` be either unit representative of the unoriented twist line.
With signature `(-,+,+,+)`, test the metric-derived screen projector and screen metric

```text
H^a_b = delta^a_b + u^a u_b - n^a n_b,
q_ab  = g_ab + u_a u_b - n_a n_b.
```

Test uniqueness only up to the unavoidable signs of `u`, `n`, and screen orientation.  The
orientation-free area density is primary.  If an orientation is supplied, test

```text
epsilon_perp = i_n i_u epsilon_g.
```

In the displayed coframe, independently check whether

```text
q = theta_2^2 + theta_3^2,
epsilon_perp = plus_or_minus theta_2 wedge theta_3,
d(theta_2 wedge theta_3) = 2 lambda dphi wedge theta_2 wedge theta_3.
```

The last identity is a local coframe-area transport statement, not yet an optical-distance law.

For a supplied affinely parametrized geodesic with tangent `k`, test conservation of
`E=-g(K,k)` and the frequency measured by the intrinsic stationary observers,
`omega=-g(u,k)`.  With the frozen convention `Q_pq=omega_q/omega_p`, determine whether

```text
log Q_pq = phi(q)-phi(p)
```

holds on every such path segment whose endpoints lie on the stationary congruence.  This does not
select which geodesic or event pairing is physical.

On that same supplied path, retain the full transverse state `Y=(xi,Dxi/ds)` and its metric Jacobi
fundamental matrix `M_gamma`.  Test only the already established pathwise properties—symplecticity,
composition, inversion, screen-frame covariance, and continuation through projected caustics—and
whether

```text
C_gamma = S(log Q_gamma) direct_sum M_gamma
```

is now realized nontrivially in one complete same-metric branch.  Do not infer an irreducible
off-diagonal solder merely from the common metric.

## WR-L/SNe non-conflation test

The preserved SNe readout uses

```text
1+z=exp(phi),
D_A/X = 1-exp(-2 phi),
d_L=(1+z)^2 D_A.
```

The audit must compare this only after the intrinsic screen derivation.  It must test whether any
constant real `lambda` can make a normalized raw local screen length `A exp(lambda phi)` equal to
`1-exp(-2 phi)` on an open interval containing `phi=0`.  Failure means only that local coframe area
is not the vertex Jacobi area.  It does not refute the SNe result or the possibility that the full
Jacobi equation in a selected macro branch yields that law.

No SNe fitting, cosmological parameter import, density bracket, or observational selection of
`lambda` is authorized.

## Verification contract

- CPU only.
- Production derivation: exact SymPy exterior/projector and algebra checks.
- Independent derivation: standard-library symbolic-coefficient/exterior algebra with no import of
  the production module.
- Use at least two exact nonconstant depth substitutions and all eight frozen candidate types.
- Exercise every row of `FALSIFICATION_CONTRACT.tsv`.
- Recheck source hashes, six frozen packages, current paths, frontier targets, tests, and dirty
  checkout metadata.
- Do not edit startup controls, current registries, prior evidence, research artifacts, or
  `CANON.md`.

## Falsification and maximum conclusion

If C01–C06 retain the parent intrinsic pair, the projector/area identities and endpoint depth law
are exact, and the established Jacobi propagator can be formed on the same supplied path, the
maximum positive conclusion is:

```text
ONE_COMPLETE_TWISTED_S3_CONFIGURATION_FAMILY_REALIZES_A_METRIC_INTRINSIC_CLOCK_RULER_SCREEN_SPLIT;
FOUNDED_DEPTH_EQUALS_THE_INTRINSIC_STATIONARY_ENDPOINT_CLOCK_LOG_RATIO_IN_THIS_BRANCH;
A_NONTRIVIAL_REDUCIBLE_LONGITUDINAL_TRANSVERSE_COCYCLE_EXISTS_ON_EACH_SUPPLIED_GEODESIC_WITHOUT_BRANCH_SPLICING;
LOCAL_SCREEN_AREA_IS_NOT_IDENTIFIED_WITH_THE_WRL_SNE_VERTEX_JACOBI_AREA;
NO_PATH_ON_SHELL_BRANCH_LAMBDA_ACTION_OR_PHYSICAL_OBSERVABLE_SELECTED.
```

If any join fails, the maximum negative is scoped to the failed object in this frozen family.  It
is not a universal UDT no-go.

## Completeness map

Covered: C01–C06, C07–C08 controls, the intrinsic stationary congruence, the twist-selected ruler,
the orthogonal rank-two screen, its local metric and area density, endpoint Killing-frequency ratio,
and the full transverse Jacobi cocycle on supplied geodesics.

Dropped: path/event selection, cut-locus selection, explicit all-path Jacobi solutions for the
nonhomogeneous metric, optical distance as an observed scalar, physical `lambda`, on-shell equations,
action, variation domain, source, carrier, matter, boundary completion, bootstrap, density, mass,
`X_max`, dynamics, and operational signalling.
