# G331 preregistration — nonsymmetric Ricci-eigenline and fibration perturbations

Date: 2026-09-03

## Frozen question

Let

```text
gamma_0 = a^2 (sigma_1^2 + sigma_2^2) + c^2 sigma_3^2,
a > 0, c > 0, a != c,
```

be a supplied non-round Berger metric on `S3`. For the complete class of smooth positive metrics
`gamma` in a sufficiently small `C2` neighborhood of `gamma_0`, determine exactly which parts of
G330 survive:

1. a smooth global rank-one spatial-Ricci eigenline;
2. a global unit representative up to sign;
3. closed leaves forming the Hopf circle fibration;
4. G330's period-normalized absolute helicity; and
5. conditional local carry under the active provisional vacuum equation.

The geometric neighborhood is the full bounded perturbation class, not one Fourier mode or one
symmetry ansatz. A separate explicit bump is only a witness/control inside that class.

## Candidate outcomes

1. `EIGENLINE_AND_HOPF_FIBRATION_ARE_BOTH_GAP_OPEN`: a uniform simple Ricci gap forces both the
   global line and closed Hopf fibres for every sufficiently close metric.
2. `EIGENLINE_IS_GAP_OPEN__HOPF_FIBRATION_NEEDS_EXTRA_ORBIT_STRUCTURE`: the global smooth line
   persists, but gap and topology do not force periodic leaves or the fibre-period normalization.
3. `EVEN_THE_GLOBAL_EIGENLINE_IS_NOT_PERTURBATION_OPEN`: arbitrarily small smooth perturbations can
   destroy the rank-one Ricci spectral cluster despite the registered uniform gap hypothesis.

No outcome selects a physical history.

## Exact gates

1. **Base-gap gate.** Reuse only the externally accepted G330 algebra
   `Delta_0 = abs(4(c^2-a^2)/a^4) > 0` for `a != c`. The round case remains a required boundary,
   not a failed datum.
2. **Common-bundle gate.** Compare the Ricci endomorphisms of `gamma` and `gamma_0` after a canonical
   positive metric identification. No subtraction of matrices in unrelated orthonormal frames is
   accepted.
3. **Uniform spectral gate.** Prove that a self-adjoint operator perturbation smaller than half the
   base separation preserves one rank-one spectral cluster at every point. Use compactness to make
   the neighborhood uniform.
4. **Regularity gate.** Record the exact derivative loss: Ricci depends on the metric through two
   derivatives. `C2` controls continuity of the projector; a smooth perturbed metric with an open
   simple gap gives a smooth projector and line.
5. **Gauge gate.** Express the continued object as a spectral projector/line, never as a retained
   component direction. Verify covariance under orthogonal frame changes and invariance under line
   reversal.
6. **Global-line gate.** Distinguish existence of the rank-one subbundle from choice of sign. Use
   `H1(S3;Z2)=0` only as an imported mathematical theorem to show every real line bundle on `S3` is
   trivial; report that neither sign is selected.
7. **Nonsymmetric-tilt gate.** For `gamma_epsilon=exp(2 epsilon f) gamma_0`, choose a global smooth
   bump with, at a point `p`, `f(p)=0`, `df(p)=0`, and
   `Hess(f)(e_1,e_3) != 0`. Apply the exact 3D conformal Ricci formula and verify that the original
   Berger vertical line is not a Ricci eigenline at `p` for sufficiently small nonzero `epsilon`.
   The witness must be nonhomogeneous and must stay positive without a cutoff or fitted value.
8. **Orbit-closure gate.** Exhibit smooth nonvanishing line fields arbitrarily close to the Hopf
   field whose generic invariant-torus orbits have irrational slope and hence are not closed. This
   establishes only that closeness plus line topology cannot prove fibration. It must not be
   mislabeled as a metric-owned Ricci eigenline.
9. **Normalization gate.** Audit G330's normalization. If no common closed fibre period exists,
   `eta=(2 pi/ell_fibre) alpha` and its registered integer are unavailable without a new choice.
   No alternative helicity may be inserted to rescue the claim.
10. **Conditional-dynamics gate.** For every smooth constraint-compatible datum whose spatial
    metric is in the gap-open neighborhood, conditional smooth local Cauchy development preserves
    the rank-one cluster for some nonzero interval by continuity. Do not claim the explicit bump
    solves the constraints unless that is independently established.
11. **Controls.** Retain: round gap closure; diffeomorphic pullbacks; common homotheties; both line
    signs; perturbations tangent to and transverse to the old line; and non-`S3` topology as a
    nonuniversality control.
12. **Provenance gate.** No historical `S2` carrier, `L2+L4` action, EH selection argument, source,
    matter, mass, observation, fit, absolute scale, physical `X_max`, or protected local work may
    enter.

## Falsification contract

- Outcome 2 fails if gates 2--7 do not establish a global smooth rank-one line for the full declared
  gap-open neighborhood.
- Its fibration boundary fails if gap plus `S3` line-bundle topology alone mathematically forces all
  nearby leaves to be closed, or if the orbit-closure control is singular or not arbitrarily close.
- The tilt witness fails if it is only a coordinate/diffeomorphism artifact, homogeneous, or uses an
  approximate Ricci law where the exact conformal formula is available.
- Any purported active-equation consequence fails if it treats an unconstrained spatial metric as
  lawful initial data or relies on G330's `U(2)` symmetry inheritance after that symmetry is broken.

No failed gate may be repaired by adding a carrier, action, boundary condition, observational
filter, or desired physical mechanism.

## Evidence contract

- one direct symbolic/exact implementation;
- one implementation-distinct verifier that does not import the production module or read its
  result;
- hostile mutations of the gap threshold, conformal-Ricci sign, global topology statement,
  orbit-rationality classification, and constraint-compatibility wording;
- aggregate package replay;
- fresh external adversarial review before any scientific verdict is banked.

## Maximum conclusion

The maximum grade is a `DERIVED_CONDITIONAL` perturbation-boundary theorem scoped to smooth spatial
metrics near a supplied non-round Berger `S3` datum and, dynamically, only to the constraint-compatible
members under the owner-provisional response equation. It is not a stability, occupancy, matter,
mass, scale, `X_max`, or canon result.
