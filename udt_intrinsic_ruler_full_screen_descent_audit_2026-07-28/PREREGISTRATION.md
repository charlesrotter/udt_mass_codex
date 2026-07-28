# Preregistration — intrinsic ruler under full-screen Hopf descent

Date: 2026-07-28

Fixed base: `97d85edb7da351e6a96bb8c55b4e969ea8e3a749`

## Whole question

In the stationary twisted `R x S3` control,

```text
theta0=exp(-phi)(c_E dt+alpha sigma3),
theta1=exp(+phi)sigma3,
(theta2,theta3)^T=P(sigma1,sigma2)^T,
P:S3->GL(2,R),
g=-theta0^2+theta1^2+theta2^2+theta3^2,
```

determine, without an action or desired Hopf outcome:

1. whether the earlier curvature-invariant certificate selecting the stationary clock line persists
   when both screen shears are released;
2. whether the twist of that metric-selected clock line still selects the founded ruler line for
   general `P`;
3. whether founded-depth normalization gives the same regular Hopf connection on the stationary
   orbit space;
4. the exact necessary and sufficient condition for the complete orbit metric to descend along the
   Hopf circle; and
5. whether the earlier unique-clock certificate and full Hopf-fiber descent can hold simultaneously.

This is metric-led. The Hopf bundle is not an acceptance target.

## Frozen regime and candidate strata

- `G00`: all smooth finite stationary `phi` and smooth invertible `P` on the chosen global `S3`.
- `G01`: open full-screen perturbations of the six prior exact rank-three intrinsic-pair witnesses.
- `G02`: arbitrary fiber-dependent `phi` and/or `P`.
- `G03`: fiber-invariant `phi` and screen metric, with both shear modes still allowed on the base.
- `G04`: coframe-equivariant screens whose metric is fiber-invariant.
- `G05`: screens with only discrete or exceptional fiber symmetry.
- `G06`: twist-off `alpha=0` control.
- `G07`: constant-depth control.
- `G08`: positive, zero, and negative displayed-slice strata retained separately.

No stratum may be filtered for failing to resemble a universe or particle.

## Frozen objects and definitions

- `K=partial_t` is the registered stationary field; whether its line is metric-selected is tested.
- `V` is the registered diagonal Hopf generator on the `S3` orbit space, normalized by
  `sigma3(V)=1` and period `2 pi`.
- The old strong intrinsic-clock certificate is rank three of three scalar-curvature-invariant
  spatial gradients, implying a one-dimensional continuous Killing algebra.
- The clock twist is `omega_K=star(K_flat wedge dK_flat)`.
- Ruler recovery means the unoriented line of `omega_K` equals the line of `theta1`.
- Founded-depth normalization means `exp(-phi) theta1=sigma3`; this is not strong local CSN.
- Full metric descent means the complete stationary-orbit metric is invariant under the supplied
  free Hopf circle, not merely that `sigma3` is a contact form.

## Preregistered decision logic

The audit must distinguish:

- open persistence of the rank-three certificate near the old witnesses;
- universal persistence across all `P`;
- ruler-line recovery conditional on a supplied versus metric-selected `K`;
- regularity of the normalized contact form;
- invariance of the complete orbit metric;
- and simultaneous compatibility of clock selection and fiber descent.

Possible outcomes include constructive overlap, disjoint strata, partial overlap with a weaker clock
selector, or an unresolved compatibility seam. A failure of the old rank-three certificate may not
be promoted to failure of every possible future metric-intrinsic clock characterization.

## Certification and falsification contract

Load-bearing exterior/Hodge algebra, perturbative rank persistence, Lie derivatives, and symmetry
implications must be independently reconstructed. Counterbranches remain in the atlas. Exact
identities use symbolic or rational arithmetic; topology/symmetry statements require their global
hypotheses.

The maximum allowed conclusion is a bounded classification of the clock/ruler/descent compatibility
inside this chosen stationary `S3` family. The audit cannot select `S3`, a physical branch, carrier,
action, source, boundary law, density/bootstrap fixed point, mass, scale, dynamics, operational
signalling, or canon.

No GPU, ODE/PDE, relaxation, time-live solve, observation fit, or repository reorganization is
authorized.
