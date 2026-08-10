# External review — normalized transcript

The original accepted raw response was SHA-256
`1d08a7247ed2f6f435bcaabb45f6fb1a665829f22bb74f49511c0560ec979a6f`. This transcription removes
only temporary-intake absolute links and condenses the displayed nonnormality matrix; the verdict
and every adjudicated claim are preserved below.

**Primary Verdict**

`GAUGE_GROUPOID_ALREADY_SUFFICIENT`

`RELATIVE_ORBIT_DERIVED__REPRESENTATIVE_OPEN` is a valid lower bound, but it is not the sharpest
object-type statement. The stronger representative-free object already derived in
`EXACT_DERIVATION.md` is the path-labelled `SO(2)` alignment bitorsor `M_gamma(q)`, not merely its
double-coset shadow.

**Load-Bearing Algebra**

1. Type and existence check out. `R_int(q)` and `R_car(gamma,q)` are two reductions in the same
Lorentz tangent space, not one tensor under two names. On every retained same-`lambda` stratum they
have one timelike clock line, one spacelike ruler line, and one positive screen plane, so some
`M0 in SO^+` exists with `M0 R_car M0^-1 = R_int`.

2. Uniqueness fails on all six strata. In the adapted frame,

```text
X_lambda=diag(-1,1,lambda,lambda),
B_01=[[5/4,3/4,0,0],[3/4,5/4,0,0],[0,0,1,0],[0,0,0,1]],
R_23(theta)=rotation in the screen plane.
```

With `X_car=B_01 X_lambda B_01^-1`, every

```text
M(theta)=R_23(theta) B_01^-1
```

satisfies `M(theta) X_car M(theta)^-1 = X_lambda` and aligns `P_u,P_n,H`. So the full-projector
alignment set is exactly `M_gamma(q)=H_int M0=M0 H_car`, a continuous `SO(2)` bitorsor. The grading
stabilizer dimensions `1,3,1,1,3,1` and full-projector dimension `1` are correct.

3. No hidden screen phase is selected. The metric intrinsically recovers the unique clock line and
the twist-selected ruler line, but only an unoriented ruler line and an oriented screen plane.
Writing

```text
sigma1' = cos(theta) sigma1 + sin(theta) sigma2,
sigma2' = -sin(theta) sigma1 + cos(theta) sigma2,
```

preserves both the Maurer-Cartan relations and the screen block `theta2^2+theta3^2`. So the complete
coframe, orientation, screen complex structure, twist, and global `S3` presentation do not
metric-select a screen axis.

4. The section claims need narrowing, and the package mostly does that correctly. Local gauges
exist. What fails is a universal natural selector: no left-equivariant section of `G -> G/SO(2)`
can exist because equivariance at the basepoint would force every `h in SO(2)` to fix `s(eH)`, hence
`h=1`. A global continuous universal section is also obstructed by the compact model
`SO(3)->S^2`. “Pure boost”, polar, Cartan, minimum-rotation, or geodesic representatives are gauges
requiring extra objective data, not forced by frozen premises.

5. The only substantive sharpening is object type. Under adapted-frame changes,
`R -> h_int^-1 R h_car`, so the double-coset class is frame-invariant. But the stronger owned object
is already the bitorsor `M_gamma(q)` itself. The double coset is only its orbit shadow and is not the
right compositional carrier. The nonnormality objection is correct: with `H=SO(2)_{23}` and

```text
B_02=[[5/4,0,3/4,0],[0,1,0,0],[3/4,0,5/4,0],[0,0,0,1]],
```

`B_02 R_23 B_02^-1` does not preserve `P_u` or `H`, so it is not in `H`. Hence naive multiplication
on `H\G/H` is ill-defined, while balanced composition of bitorsors/groupoid arrows is the correct
representative-free law.

6. Path labels cannot be erased. The frozen witness has exact local nonparallelism, full sampled
holonomy rank six, and 36/36 nonidentity loops with nonzero ordinary closure residual. So `M_B=I`
is refuted on the retained branch family.

7. No scalar or physical promotion is licensed. The carried/intrinsic alignment result does not
upgrade R17, `delta_RF`, terminal `c_E`, universal `c_eff`, or a physical pair relation beyond their
current conditional/open statuses. Projector alignment does not capture calibration density or
pair-surface realization.

The proposed next quotient/descent audit is the correct next deductive step, but it should start
from the already-derived `SO(2)` bitorsor/gauge-groupoid object and test whether `delta_RF`, the
terminal pair readout, and any calibration-density data descend through it. It should not keep
searching for a metric-forced screen-phase representative.
