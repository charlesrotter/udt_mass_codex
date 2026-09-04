# External Review Response

Reviewer mode: fresh zero-context adversarial review, bounded to the sealed `/intake` evidence and
its byte-identical `/work/intake` copy.

## Findings By Severity

No defects found at high, medium, or low severity within the bounded G342 claim set.

## Authentication

I authenticated the intake before using any payload content.

- `REVIEW_MANIFEST.tsv` matched the detached seal in `REVIEW_MANIFEST.sha256`.
- The manifest listed 30 payloads; `find` showed exactly 32 files in `/intake`, namely those 30
  payloads plus `REVIEW_MANIFEST.tsv` and `REVIEW_MANIFEST.sha256`.
- Every listed payload matched the sealed SHA-256 and byte count, including `REVIEW_SCOPE.json`,
  all G342 files, and all sealed source files.
- The `/work/intake` copy preserved the same file set and layout before replay.

## Review Answers

### 1. Fixed-affine source-sky map

Yes.

Using the sealed G341 endpoint formulas

\[
Q_X(T,\lambda)=\frac1{C_X}\int_{T_e}^T \frac{u^{4/3}}{\sqrt{u^2+\lambda^2}}\,du,
\qquad
Q_\perp(T,\lambda)=\frac{\lambda}{C_\perp}\int_{T_e}^T \frac{u^{-2/3}}{\sqrt{u^2+\lambda^2}}\,du,
\]

the fixed-`T` derivatives are

\[
\partial_\lambda Q_X=-\frac{\lambda}{C_X}I,
\qquad
\partial_\lambda Q_\perp=\frac1{C_\perp}I,
\qquad
I=\int_{T_e}^T \frac{u^{4/3}}{(u^2+\lambda^2)^{3/2}}\,du.
\]

Projecting the physical endpoint derivative onto the in-plane unit screen
`S=(-s)e_1+ce_2`, with `a=C_XT^{-1/3}`, `b=C_\perp T^{2/3}`, `c=T/sqrt(T^2+\lambda^2)`,
`s=\lambda/sqrt(T^2+\lambda^2)`, gives

\[
a(-s)\partial_\lambda Q_X+b\,c\,\partial_\lambda Q_\perp
=T^{-1/3}\sqrt{T^2+\lambda^2}\,I.
\]

At the source, `tan(theta_e)=lambda/T_e`, hence

\[
\frac{d\lambda}{d\theta_e}=T_e\sec^2\theta_e=\frac{T_e^2+\lambda^2}{T_e}.
\]

Therefore

\[
D_\parallel=\frac{T_e^2+\lambda^2}{T_e}\,T^{-1/3}\sqrt{T^2+\lambda^2}\,I,
\]

which is the stated diagonal in-plane response.

For azimuth, the physical endpoint azimuth displacement is `b Q_\perp d varphi`, while the unit
source-sky parameter is `d eta = sin(theta_e) d varphi` with
`sin(theta_e)=\lambda/\sqrt{T_e^2+\lambda^2}`. Dividing gives

\[
D_Z=\sqrt{T_e^2+\lambda^2}\,T^{2/3}
\int_{T_e}^T \frac{u^{-2/3}}{\sqrt{u^2+\lambda^2}}\,du,
\]

so the `sin(theta_e)` normalization is necessary and correctly retained.

The fixed-affine endpoint-time correction is legitimately removed only at screen level: at fixed
affine parameter the extra endpoint displacement is proportional to the spatial ray tangent
`n=ce_1+se_2`, hence orthogonal to `S` and also to `Z`. It is not deleted by coordinate choice;
it is a tangent/null-gauge term whose quotient-screen projection vanishes.

My own scratch finite-difference check on 40 random mixed rays, done separately from package code,
matched the stated `D_\parallel` with maximum relative error `1.1846524220453898e-10` and matched
the azimuth normalization with maximum relative error `2.2069409231241003e-16`.

### 2. Levi-Civita/Riemann screen tide

Yes.

From the exact metric

\[
g=-dT^2+a(T)^2dX^2+b(T)^2(dY^2+dZ^2),
\qquad
a=C_XT^{-1/3},\quad b=C_\perp T^{2/3},
\]

the orthonormal frame `e_0=\partial_T`, `e_1=a^{-1}\partial_X`, `e_2=b^{-1}\partial_Y`,
`e_3=b^{-1}\partial_Z` has expansion rates

\[
H_1=-\frac1{3T},
\qquad
H_\perp=\frac2{3T}.
\]

Direct Levi-Civita/Riemann reconstruction gives the needed orthonormal curvature channels

\[
g(e_1,R(e_1,e_0)e_0)=-\frac4{9T^2},
\]

\[
g(e_2,R(e_2,e_0)e_0)=g(e_3,R(e_3,e_0)e_0)=\frac2{9T^2},
\]

\[
g(e_1,R(e_1,e_2)e_2)=g(e_1,R(e_1,e_3)e_3)=-\frac2{9T^2},
\qquad
g(e_2,R(e_2,e_3)e_3)=\frac4{9T^2}.
\]

Contracting with `ell=alpha(e_0+n)`, `n=ce_1+se_2`, `S=-se_1+ce_2`, `Z=e_3`, yields

\[
T_{SS}=-\frac{2\alpha^2 s^2}{3T^2},
\qquad
T_{ZZ}=+\frac{2\alpha^2 s^2}{3T^2},
\qquad
T_{SZ}=T_{ZS}=0.
\]

Since

\[
\alpha^2\frac{s^2}{T^2}
=\frac{\lambda^2 T_e^{4/3}}{(T_e^2+\lambda^2)T^{10/3}},
\]

this is exactly

\[
T_{\text{screen}}=\operatorname{diag}(-q,+q),
\qquad
q=\frac{2\lambda^2 T_e^{4/3}}{3(T_e^2+\lambda^2)T^{10/3}}>0.
\]

The cross term is zero by the metric's axial reflection symmetry about the ray plane: the metric
and chosen mixed ray are invariant under `Z -> -Z`, while `Z` changes sign and `S` does not.
Nothing in this derivation uses the Jacobi map to define the tide, so there is no circularity.

### 3. Full affine Jacobi equation, vertex data, and normalization constants

Yes.

The displayed responses

\[
D_\parallel=\frac{T_e^2+\lambda^2}{T_e}\,T^{-1/3}\sqrt{T^2+\lambda^2}\,I(T,\lambda),
\]

\[
D_Z=\sqrt{T_e^2+\lambda^2}\,T^{2/3}K(T,\lambda),
\qquad
K(T,\lambda)=\int_{T_e}^T \frac{u^{-2/3}}{\sqrt{u^2+\lambda^2}}\,du,
\]

obey

\[
\ddot D_\parallel-qD_\parallel=0,
\qquad
\ddot D_Z+qD_Z=0,
\]

with affine generator `d/dv = alpha d/dT`, and the source normalization gives
`D(T_e)=0`, `dot D(T_e)=I_2`.

The source-normalized screen map is independent of `C_X` and `C_\perp`: they enter the endpoint
coordinates and physical orthonormal projection factors but cancel exactly in both screened
responses after the `theta_e` and azimuth source-sky normalizations.

My separate scratch RK4/integral replay, coded independently from the intake scripts, matched the
closed-form `D_\parallel` and `D_Z` on 40 random cases with maximum relative difference
`1.5633272454351754e-11`.

### 4. Global positivity, affine rates, area, expansion, shear, and Raychaudhuri signs

Yes.

- `I(T,\lambda)>0` and `K(T,\lambda)>0` for all `T>T_e`, so `D_\parallel>0`, `D_Z>0`, and
  `A=D_\parallel D_Z>0`.
- `D_Z` is a product of positive increasing factors, so `dot D_Z>0`.
- `ddot D_\parallel=qD_\parallel>=0` with unit vertex slope, so `dot D_\parallel>0` for every
  future regular point.
- Hence both eigenrates `beta_\parallel=dot D_\parallel/D_\parallel` and
  `beta_Z=dot D_Z/D_Z` are positive, and `Theta=beta_\parallel+beta_Z>0`.
- The determinant/area increases because `dot A = A Theta > 0`.

For the shear gap `w=beta_\parallel-beta_Z`, the two scalar Riccati equations imply

\[
\dot w+\Theta w = 2q.
\]

Using `A(v) ~ v^2` at the vertex,

\[
w(v)=\frac{2}{A(v)}\int_0^v q(s)A(s)\,ds.
\]

Therefore `w>0` on every nonlongitudinal ray (`lambda>0`) because then `q>0` on the whole regular
segment; `w=0` only on the longitudinal symmetry family (`lambda=0`) or at the vertex limit.

For the total expansion,

\[
\dot\Theta=(q-\beta_\parallel^2)+(-q-\beta_Z^2)
=-\frac12\Theta^2-\frac12 w^2<0.
\]

So the expansion is positive but strictly decreasing at every finite regular point. This is the
correct Raychaudhuri sign structure for the bounded vacuum screen problem.

### 5. Principal projective limits

Yes.

For `R=T/T_e>1`:

- Longitudinal chart `lambda=0`:

\[
D_\parallel=D_Z=v=\frac{3T_e}{2}(R^{2/3}-1),
\]

with `q=0`, vanishing shear, and eigenrates `1/v`.

- Transverse projective chart `mu=1/lambda -> 0`:

\[
\frac{D_\parallel}{T_e}=\frac37\left(R^2-R^{-1/3}\right),
\qquad
\frac{D_Z}{T_e}=3\left(R-R^{2/3}\right),
\]

and the stated positive affine-rate formulas follow by applying
`beta = alpha d_R log(D/T_e) / T_e`.

The limits are nonsingular because the disappearing polar azimuth at `lambda=0` is only a
direction-chart degeneracy, while the transverse boundary is regular in `mu=1/lambda`.

### 6. Compact multiplicity and labelled per-lift maps

Yes.

The sealed G341 result proves that each nonzero universal-cover lift has one regular future null
solution and one arrival. G342 then attaches

\[
D_L=D(T_L,\lambda_L),
\qquad
A_L=\det D_L>0
\]

to each lift `L` separately. The package does not delete, weight, aggregate, or physically select
paths. It also distinguishes quotient cut ties from conjugate behavior on an individual lift.

This is supported by:

- the analytic G341 per-lift uniqueness proof;
- the explicit G342 statements that branches are not summed, weighted, or discarded;
- the hostile control `quotient_path_deletion`, which the replay caught.

### 7. Replay, independence, frozen sources, and initial finite-axis miss

Yes, with the required qualification about what is and is not independent.

I reran the registered no-write replay in `/work/intake/g342` with
`UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S`:

- `derive_full_null_jacobi.py`: `4720/4720`, `PASS`
- `verify_full_null_jacobi_independent.py`: `2080/2080`, `PASS`
- `run_catch_proofs.py`: `10/10`, all hostile mutations caught
- `verify_package.py`: `17/17`, `all_passed=true`

The aggregate replay also verified frozen source hashes and reported no byte changes in the copied
package during replay.

The implementation-distinct replay is genuinely implementation-distinct relative to the production
script: it rebuilds metric jets, Christoffels, Riemann, and the Jacobi ODE without importing the
production code. It is not premise-independent, and the intake says so explicitly. That is the
correct claim. Likewise, the aggregate verifier is an integrity gate, not the analytic proof; the
intake says that explicitly as well, so I found no false independence claim and no vacuous
substitution of integrity checks for mathematics.

The preserved initial finite-axis miss does not change the scientific criterion. The sealed note
records a chart-boundary approximation miss at `lambda/T_e=1e5`, then moves the finite check to
`1e6`, where the same preregistered transverse asymptotic is further into its declared
`O(lambda^-2)` regime, while keeping the original raw tolerance `5e-9`. No formula, sign claim,
selected alternative, or scientific landing changed.

### 8. Boundary discipline

Yes.

I found no silent promotion of geometric Jacobi area into brightness, luminosity, physical
distance, electromagnetic transfer, selected route/population, generic stability, scale, `X_max`,
or canon. The separation is consistent across:

- `g342/EXACT_DERIVATION.md`
- `g342/PREMISE_LEDGER.tsv`
- `g342/STATUS_LEDGER.tsv`
- `g342/LAY_REPORT.md`
- the hostile control `physical_readout_promotion`

The package repeatedly distinguishes:

- geometric beam area from any radiative observable;
- analytic proof from numerical replay;
- implementation independence from premise independence;
- per-lift response from any quotient aggregation.

## Conclusion

Within the sealed scope, the bounded G342 result survives fresh adversarial review. The exact
fixed-affine two-direction Jacobi map, direct metric-derived screen tide, full affine Jacobi
equation, global sign classifications, two projective limits, per-lift compact multiplicity, and
bounded no-physics/no-route/no-scale discipline are all supported. I found no scientific defect
that would force demotion to alternatives `B`, `C`, or `D`.

ACCEPT_G342_BOUNDED_FULL_NULL_JACOBI_BEAM_AREA
