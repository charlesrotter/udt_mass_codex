# External Adversarial Review — G325

## Authentication

I authenticated the intake before reading scientific claims.

- `REVIEW_MANIFEST.sha256` matches the SHA-256 of `REVIEW_MANIFEST.tsv`.
- All 26 manifest payloads are present, with exact byte counts and SHA-256 matches.
- This includes `REVIEW_SCOPE.json`, the four replay scripts, the banked JSON artifacts, and the upstream source payloads listed in `SOURCE_SCOPE.tsv`.

## Independent derivation

Starting only from the sealed background metric

\[
g_0=-dT^2+\sum_{i=1}^3 C_i^2 T^{2p_i}(dx^i)^2,\qquad p=\left(-\frac13,\frac23,\frac23\right),
\]

and the diagonal synchronous perturbation

\[
g_{ii}=C_i^2T^{2p_i}[1+2\epsilon u_i(T)]+O(\epsilon^2),
\]

the diagonal Bianchi-I Ricci tensor is

\[
R_{00}=-\sum_i(\dot H_i+H_i^2),\qquad \frac{R_{ii}}{g_{ii}}=\dot H_i+\theta H_i,
\]

with `H_i=\dot a_i/a_i`, `a_i=C_iT^{p_i}(1+\epsilon u_i)`, and `theta=sum_i H_i`.
Linearizing the adopted trace-free Ricci equation and using contracted Bianchi on a connected regular region gives

\[
\delta R_{ab}=\lambda (g_0)_{ab},\qquad \delta R=4\lambda,
\]

so the exact first-order ODEs are

\[
\dot v_i+\frac{v_i}{T}+\frac{p_iV}{T}=\lambda,\qquad v_i=\dot u_i,\quad V=\sum_i v_i,
\]

plus the time/Hamiltonian relation

\[
\frac{V-\sum_i p_i v_i}{T}=\lambda.
\]

Solving these directly gives

\[
u_i(T)=c_i+q_i\log(T/T_{\mathrm{ref}})-\frac{p_i\tau}{T}+\frac{1-p_i}{4}\lambda T^2,
\]

with

\[
\sum_i q_i=0,\qquad \sum_i p_i q_i=0.
\]

For `p=(-1/3,2/3,2/3)`, the `q_i` space is one-dimensional:

\[
(q_1,q_2,q_3)=q(0,1,-1).
\]

Hence the complete declared sector has exactly six constants:

- `tau`: one residual time-origin gauge constant;
- `c_1,c_2,c_3`: three fixed-quotient lattice-modulus constants;
- `q`: one genuine local Kasner-shear constant;
- `lambda`: one connected scalar-curvature constant.

There is no seventh independent integration constant. The two linear constraints on the logarithmic coefficients remove the extra candidate anisotropy, and `T_ref` only reabsorbs into the `c_i`.

## Classification checks

The time-shift mode is genuine residual synchronous gauge. For constant `xi^0=tau`, `xi^i=0`,

\[
(\mathcal L_\xi g_0)_{ii}=tau\,\partial_T(g_0)_{ii}=2g_{0,ii}\frac{p_i tau}{T},
\]

which is exactly the `p_i/T` mode up to the passive/active sign convention.

The constant strains are not fixed-torus gauge. On the universal cover, `xi^i=c_i x^i` gives the constant diagonal strain, but on a quotient circle of period `L_i`,

\[
\xi^i(x^i+L_i)-\xi^i(x^i)=c_iL_i.
\]

For a periodic vector field this jump must vanish, so nonzero `c_i` do not descend to legal gauge on the fixed quotient. Discrete lattice automorphisms, including `y-z` exchange, do not remove these infinitesimal directions; they identify exact quotient presentations only discretely. In the diagonal slice these three constants are continuous fixed-quotient moduli.

The Kasner-shear mode is locally nontrivial even though first-order scalar invariants are blind to `y-z` exchange. For `q(0,\log T,-\log T)`,

\[
\delta R=0,
\]

but the orthonormal electric-curvature split is

\[
\delta(E_y-E_z)=-\frac{2q}{3T^2}\neq 0,
\]

so the mode is not gauge and is not an artifact of scalar blindness.

The scalar mode is the unique connected scalar-curvature direction:

\[
u_i^{(\lambda)}=\frac{1-p_i}{4}\lambda T^2,\qquad \delta R=4\lambda.
\]

It is local, curvature-changing, and not a new source or action term.

## Replay, provenance, and boundaries

I ran the four registered commands literally in a writable ephemeral copy under `/work`. After correcting the copied file permissions so the ephemeral copy was actually writable, all four commands succeeded, and the first three regenerated artifacts exactly matched the banked JSON outputs. The independent verifier does not import production code or read production results, and its tensor engine reconstructs Christoffels, Riemann, Ricci, scalar curvature, and the trace-free residual directly.

I did find one non-load-bearing vacuity: `derive_modes.py:146-147` records `time_shift_lie_derivative_witness` as the tautology `2 * P[index] == 2 * P[index]`. That assertion should not be cited as evidence. This does not overturn the census because the same point is genuinely checked by the independent tensor route in `verify_independent.py:221-227`, and my own derivation also confirms it. The hostile proofs are serviceable but lightweight: some checks in `verify_independent.py:229-240` and `run_catch_proofs.py:44-56` are arithmetic witnesses rather than deep mutation-hard tests. I treat those as evidence-quality caveats, not as scientific refutations.

Native provenance stayed inside the sealed scope. I found no introduction of a new UDT equation, action, source, observation, fit, selected scale, or `X_max`. The active equation remains the previously scoped trace-free Ricci law, the background metric and quotient provenance come from the listed upstream G323/G324 materials, and the written G325 boundary remains controlled first variation only. I reject any promotion to full linear stability, nonlinear stability, other topologies, off-diagonal modes, nonzero Fourier modes, occupancy, or physical scale.

On the exact preregistered question, the answer is yes in the stated bounded category.

ACCEPT__G325_BOUNDED_MODE_CENSUS
