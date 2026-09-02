# External Adversarial Review Response — G326

## Scope compliance

I inspected only the sealed intake at `/intake`, used `/work` only for ephemeral writable copies and mutation tests, did not edit intake evidence, did not continue the research, did not access any repository or protected package, and did not use network access beyond Codex transport.

## Authentication

I authenticated the intake before reading the scientific claims.

- `REVIEW_MANIFEST.sha256` contains `420738a871941dfd92ddd21d8d026e26e94c06dc853a0f7bead8209a6c9a90c9`.
- `sha256sum /intake/REVIEW_MANIFEST.tsv` returned the same hash.
- I then verified every row of `REVIEW_MANIFEST.tsv` against the actual byte count and SHA-256 of the corresponding payload.
- Result: all 30 manifest payloads matched exactly, including `REVIEW_SCOPE.json`.

## Independent derivation

I treated the landing as false until established from the adopted G324 background

\[
g_0=-dT^2+a_1(T)(dx^1)^2+a_2(T)(dx^2)^2+a_3(T)(dx^3)^2,
\qquad
a_i=C_i^2T^{2p_i},
\qquad
p=\left(-\frac13,\frac23,\frac23\right).
\]

For a general homogeneous synchronous spatial metric `gamma(T)`, the only nonzero Christoffel symbols are

\[
\Gamma^0{}_{ij}=\frac12\dot\gamma_{ij},
\qquad
\Gamma^i{}_{0j}=\frac12\gamma^{ik}\dot\gamma_{kj},
\]

with all purely spatial Christoffels zero because there is no spatial dependence. Direct contraction gives

\[
R_{00}
=-\frac12\operatorname{tr}(\gamma^{-1}\ddot\gamma)
+\frac14\operatorname{tr}(\gamma^{-1}\dot\gamma\gamma^{-1}\dot\gamma),
\]

\[
R_{0i}=0,
\qquad
R_{ij}
=\frac12\ddot\gamma_{ij}
+\frac14\operatorname{tr}(\gamma^{-1}\dot\gamma)\dot\gamma_{ij}
-\frac12(\dot\gamma\gamma^{-1}\dot\gamma)_{ij}.
\]

Now perturb only the off-diagonal sector,

\[
\gamma_{ij}=a_i\delta_{ij}+\epsilon k_{ij}(T),\qquad i<j.
\]

At first order:

- `delta R_00=0`: every trace term has one background diagonal factor and one off-diagonal factor, so the linear trace vanishes.
- `delta R_0i=0`: the homogeneous synchronous momentum components stay zero.
- `delta R_ii=0`: the diagonal variation vanishes because `delta gamma_ii=0`, `delta tr(gamma^{-1} dot gamma)=0`, and the quadratic term has no diagonal linear contribution from a single off-diagonal mode.
- Since the background is Ricci-flat by adopted G324 and `delta R_ii=delta R_00=0`, it follows that

\[
\delta R=0.
\]

So there is no new first-order scalar-curvature mode in this sector.

For `i<j`, the linearized off-diagonal equation is

\[
\delta R_{ij}
=\frac12\ddot k_{ij}
+\left(\frac{1}{2T}-\frac{p_i+p_j}{T}\right)\dot k_{ij}
+\frac{2p_ip_j}{T^2}k_{ij},
\]

hence

\[
\boxed{
\ddot k_{ij}
+\frac{1-2(p_i+p_j)}{T}\dot k_{ij}
+\frac{4p_ip_j}{T^2}k_{ij}=0 }.
\]

This matches the claimed exact ODE.

## Exact solutions and six-constant count

With `k=T^m`, the indicial polynomial is

\[
m(m-1)+(1-2(p_i+p_j))m+4p_ip_j
=m^2-2(p_i+p_j)m+4p_ip_j
=(m-2p_i)(m-2p_j).
\]

Therefore:

- `(1,2)` and `(1,3)` have roots `m=-2/3, 4/3`, so

\[
k_{12}=A_{12}T^{-2/3}+B_{12}T^{4/3},
\qquad
k_{13}=A_{13}T^{-2/3}+B_{13}T^{4/3}.
\]

- `(2,3)` has repeated root `m=4/3`, so the full solution is

\[
k_{23}=T^{4/3}\left(L_{23}+M_{23}\log(T/T_{\rm ref})\right).
\]

The repeated-root logarithmic branch is real and indispensable. There are exactly six integration constants in the complete off-diagonal homogeneous sector. I found no extra homogeneous off-diagonal solution and no missing one.

## Cover-coordinate image, kernel, and quotient legality

Take a constant linear cover-coordinate generator

\[
\xi^i=A^i{}_j x^j.
\]

Its local metric image is

\[
(\mathcal L_\xi g_0)_{ij}=a_jA^j{}_i+a_iA^i{}_j.
\]

In the off-diagonal sector this yields:

- `12`: independent images from `A^1{}_2` and `A^2{}_1`.
- `13`: independent images from `A^1{}_3` and `A^3{}_1`.
- `23`: image from the single combination `a_3A^3{}_2+a_2A^2{}_3`.

Because `a_2` and `a_3` share the same `T^{4/3}` power, the orthogonal combination

\[
a_3A^3{}_2+a_2A^2{}_3=0
\]

is a one-dimensional kernel: the local transverse rotation in the `2-3` plane. So the off-diagonal constant-linear cover image has rank exactly five and kernel dimension one.

Those five cover generators do not descend to legal gauge on the fixed torus. If `x^j` has period `L_j`, then

\[
\xi^i(x^j+L_j)-\xi^i(x^j)=A^i{}_jL_j.
\]

For a vector field on the fixed quotient, the values at identified points must agree. A nonzero affine jump fails that test. Thus:

- local affine cover changes explain five modes locally;
- none of those five are quotient-legal gauge on the fixed `T3`;
- they survive globally as five fixed-quotient lattice/frame moduli.

The only quotient-legal homogeneous synchronous residual gauge I found is the known G325 time translation plus spatial translations. Spatial translations are Killing in this background and add no off-diagonal perturbation. G326 therefore adds no new legal gauge mode.

## Local tidal witness modulo Lie transport

For the `23` sector, write

\[
k_{23}=T^{4/3}(L+M\log(T/T_{\rm ref})).
\]

The coordinate curvature component satisfies

\[
\delta R_{0203}
=\frac{2}{9T^2}k_{23}-\frac{M}{6}T^{-2/3}.
\]

The electric tidal operator is mixed-index, so one must include the inverse-metric variation:

\[
\delta E^2{}_3
=g_0^{22}\delta R_{0203}+\delta g^{23}R^0_{0303}.
\]

Since `R^0_{0303}=(2/9)a_3/T^2` and `\delta g^{23}=-k_{23}/(a_2a_3)`, the `L` contribution cancels exactly with the metric-raising term. Hence the constant `23` mode has no intrinsic transverse mixed tidal split. It is locally pure Lie transport inside the degenerate transverse eigenspace.

For the logarithmic branch, normalize

\[
M=2C_2C_3 q_\times.
\]

Then the cancellation leaves

\[
\delta E^{\hat y}{}_{\hat z}
=\delta E^{\hat z}{}_{\hat y}
=-\frac{q_\times}{3T^2}\neq0.
\]

So the repeated-root logarithmic mode is a genuine local curvature-changing transverse Kasner-shear mode modulo Lie transport. This is the sixth mode and the only local off-diagonal physical one.

## Reconciliation with G325

Using the accepted G325 diagonal census as an external dependency only at the comparison stage:

- G325 contributes `1` residual time gauge, `3` diagonal lattice/frame moduli, `1` diagonal shear component, and `1` scalar-curvature constant.
- G326 contributes `5` off-diagonal lattice/frame moduli, `1` transverse cross-shear component, and `0` new gauge or scalar modes.

Combined count:

- residual time gauge: `1`
- lattice/frame moduli: `3+5=8`
- local shear components: `1+1=2`
- scalar-curvature constants: `1`
- total homogeneous synchronous first-variation integration constants: `12`

I found no double-counting between the diagonal and off-diagonal lattice directions and no extra quotient-legal generator.

## Compact-time and boundary discipline

The result is bounded to homogeneous first variation on compact intervals in `T>0`. I reject the following stronger readings:

- no endpoint-uniform control follows because the normalized amplitudes contain `T^{-1}`, `T`, or `log T` behavior;
- no full linear stability follows because all nonzero Fourier modes remain open;
- no nonlinear stability follows;
- no datum/topology/occupancy/scale selection follows;
- no physical `X_max`, source, action, observation, or fit enters.

On this point the intake remains disciplined enough. I found no improper promotion of the claim beyond the registered compact-time first-variation scope in the exact derivation.

## Native provenance audit

Within the intake, G326 keeps the adopted G324 metric and the adopted G310/G312 bounded trace-free Ricci equation. I found no import of a new metric, reciprocal-kernel rule, angular law, action, source, observation, fit, scale, or `X_max`. The provenance boundary is intact as stated, conditional on the already adopted prior premises recorded in the intake.

## Registered-command replay

I copied the sealed package into `/work` and ran the four registered commands literally in a writable ephemeral copy:

1. `python3 -S derive_offdiagonal_modes.py --output .review_runtime/DERIVATION_RESULT.json`
2. `python3 -S verify_offdiagonal_independent.py --output .review_runtime/INDEPENDENT_VERIFICATION.json`
3. `python3 -S run_catch_proofs.py --output .review_runtime/CATCH_PROOF_RESULT.json`
4. `python3 -S verify_package.py --output .review_runtime/PACKAGE_VERIFICATION_RESULT.json`

Results:

- The first copy made with archive-style permission preservation was still read-only and the commands failed because `.review_runtime` could not be created. That is a packaging weakness in the replay instructions.
- After making a genuinely writable ephemeral copy, all four commands ran successfully.
- The generated artifacts were byte-identical to the sealed intake artifacts.

## Circularity / vacuity / mutation-sensitivity findings

I found real tooling weaknesses, but they do not overturn the mathematical claim because the claim was independently rederived above.

1. `verify_package.py` does not truly replay the fourth registered command inside its own self-check. It replays the first three and only string-compares the fourth line via `fourth_command_self`.

2. The package replay is mutation-insensitive to loss of computation in the supposed independent and hostile scripts. In a separate writable mutation copy under `/work`, I replaced:

- `verify_offdiagonal_independent.py` with a vacuous script that simply rereads and re-emits `INDEPENDENT_VERIFICATION.json`;
- `run_catch_proofs.py` with a vacuous script that simply rereads and re-emits `CATCH_PROOF_RESULT.json`.

Then I ran

`python3 -S verify_package.py --output .review_runtime/PACKAGE_VERIFICATION_RESULT.json`

and it still passed unchanged. Therefore the package verifier does not certify that those scripts are still performing independent tensor reconstruction or actual hostile mutation checks; it certifies only artifact reproducibility plus a few static string conditions.

3. `derive_offdiagonal_modes.py` is not itself a derivation from the metric. It checks the announced roots, ranks, and counts after the ODE has already been fixed. That is acceptable as a production summary script, but it is not strong evidence by itself.

These are evidence-pipeline weaknesses. They are not mathematical counterexamples to the off-diagonal census.

## Bottom line

On the exact registered question, my independent derivation agrees with the claimed landing:

- the homogeneous off-diagonal synchronous sector closes at first order;
- `delta R=0` in that sector;
- the three exact ODEs are correct;
- the repeated-root logarithmic `23` solution is required;
- there are exactly six off-diagonal integration constants;
- five are locally affine cover-coordinate modes that fail torus periodicity and therefore survive as fixed-quotient lattice/frame moduli;
- one is a genuine local transverse Kasner-shear mode with nonzero mixed tidal witness modulo Lie transport;
- no new quotient-legal gauge mode and no new scalar-curvature mode appear.

Open boundaries remain exactly the stated ones: nonzero Fourier modes, full linear stability, nonlinear stability, endpoint-uniform control, other quotients/topologies, occupancy, scale, and `X_max`.

ACCEPT__G326_BOUNDED_OFFDIAGONAL_CENSUS
