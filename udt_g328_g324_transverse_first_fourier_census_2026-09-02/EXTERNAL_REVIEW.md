Fresh adversarial review of sealed intake `/intake`, performed with no repository access, no package installation, no web access, no evidence edits, and no scientific extension beyond the declared G328 primitive transverse tile.

## 1. Intake authentication

I authenticated the sealed intake at the file level before using any scientific output.

- `sha256(REVIEW_MANIFEST.tsv)` = `ce5dc552238749cf3dcf535c2f9355ee28b24dfb790cc1295db37c3d9346cac1`
- `REVIEW_MANIFEST.sha256` contains exactly that digest.
- `sha256(REVIEW_SCOPE.json)` = `cf200f2704b4a729d8fbe828b6ae8c2b8efc333abc997b1d815d0dd894e43383`, matching its manifest row.
- All 40 manifest payloads matched both registered byte counts and registered SHA-256 hashes.
- After the replay step below, I rehashed the full manifest set again and found `0` post-replay mismatches.

One bookkeeping nuance is worth stating explicitly: `REVIEW_MANIFEST.tsv` is not self-listed inside `REVIEW_MANIFEST.tsv`, so the detached seal authenticates the manifest and the manifest authenticates the payloads. That is normal detached-manifest structure, not a scientific defect.

## 2. Writable replay and vendored runtime

I created one ephemeral writable copy at `/work/g328_review_copy` and ran the four registered commands literally there:

```bash
python3 -S derive_transverse_modes.py --output .review_runtime/DERIVATION_RESULT.json
python3 -S verify_independent.py --output .review_runtime/INDEPENDENT_VERIFICATION.json
python3 -S run_catch_proofs.py --output .review_runtime/CATCH_PROOF_RESULT.json
python3 -S verify_package.py --output .review_runtime/PACKAGE_VERIFICATION_RESULT.json
```

The first attempt failed only because `cp -a` preserved the read-only mode bits from `/intake`; after making the copy writable, the literal replays succeeded unchanged. This touched only the copy, not the intake.

Replay findings:

- The first three generated JSON files matched the intake versions byte-for-byte.
- The fourth replay returned `status = PASS_INTERNAL_PENDING_EXTERNAL_REVIEW`.
- That aggregate verifier also reported:
  - `vendored_runtime_used = true`
  - `registered_replay_count = 4`
  - `literal_fourth_command_replayed = true`
  - `banked_evidence_overwritten = false`
- Its runtime probe verified `sympy 1.13.1` and `mpmath 1.3.0` loaded from `VENDORED_SYMPY_RUNTIME.zip`, not from host site-packages.

I separately rehashed the intake after replay and again found all manifest payload hashes unchanged. I therefore confirm that the intake-local vendored runtime was used in the writable copy and that no intake evidence file was modified.

## 3. Independent mathematical attack

I did not rely only on the banked JSON assertions. I separately reconstructed the key symbolic steps from the full ten-component perturbation using the copied vendored SymPy runtime.

### 3.1 Full ten-component sector and parity

Using the background

\[
g_0=-dT^2+C_1^2T^{-2/3}dX^2+C_\perp^2T^{4/3}(dy^2+dz^2),
\]

and the Fourier factor `exp(i k y)`, I recomputed the first variation from:

- odd block: `h_03 = b N`, `h_13 = a b H_o`, `h_23 = b^2 Q`;
- even block: `h_00 = -2A`, `h_01 = aB`, `h_02 = bC`, `h_11 = 2a^2U`, `h_12 = abV`, `h_22 = 2b^2W`, `h_33 = 2b^2Z`.

This is the full `3 + 7 = 10` symmetric metric content. Off-parity Ricci components vanish exactly, so the `z -> -z` split is complete at first order in this tile.

### 3.2 Bianchi step and the `k>0` scalar

I independently checked the linearized Bianchi identity in the `y` component for the even block:

\[
\nabla^a \delta S_{a y} - \frac14 \partial_y \delta R = 0.
\]

The symbolic residual is exactly zero. Hence on shell, `ik delta R = 0`. Because the tile is declared with `k > 0`, this forces `delta R = 0` in the nonzero transverse sector.

This implication does not survive at `k = 0`; it degenerates to `0 = 0`. That is exactly why the G325 homogeneous connected scalar branch remains available. I found no illicit step that erases the zero mode.

### 3.3 Gauge reach, periodicity, and residual quotient

From a direct Lie derivative of the background by

\[
\xi=(P,G_X,G_y,G_z)e^{iky},
\]

I recovered the gauge image

\[
A=P',\quad B=aG_X',\quad C=bG_y'-ikP/b,
\]
\[
U=-P/(3T),\quad V=ik(a/b)G_X,\quad W=2P/(3T)+ikG_y,\quad Z=2P/(3T),
\]
\[
N=bG_z',\quad Q=ikG_z,\quad H_o \mapsto 0.
\]

Therefore `H_o` is gauge invariant, and so is `H_e := 2U + Z`.

Synchronous reach requires solving

\[
P'=A,\quad G_X'=B/a,\quad G_z'=N/b,\quad G_y'=C/b+ikP/b^2.
\]

On every compact interval inside `T>0`, the coefficients `1`, `a^{-1}`, `b^{-1}`, `b^{-2}` are smooth, so there is no local obstruction to reaching synchronous gauge.

Periodicity is handled correctly. Constant and smooth same-mode gauge functions are quotient-legal; affine cover generators are not. The hostile control rejecting the affine fake gauge is valid, and I found no hidden use of a nonperiodic generator.

For the claimed fully fixed representatives, the residual-gauge matrix has determinant

\[
\det = \frac{i C_1 k^3}{3 C_\perp T^2},
\]

which is nonzero for `k>0`, so the stated residual removal is complete in the declared tile.

### 3.4 Odd block

My direct recomputation gives:

\[
i\,b\,Q' + k N = 0,
\]

and

\[
H_o''+\frac1T H_o'+\left(\nu^2T^{-4/3}-\frac1{T^2}\right)H_o=0,\qquad \nu=k/C_\perp.
\]

In synchronous gauge, `N=0`, so `Q' = 0`. The remaining `23` equation then becomes identically redundant, and constant `G_z` removes the constant `Q`. I found no lost odd constraint branch and no extra odd physical mode.

### 3.5 Even vector block

The exact vector constraint is

\[
T V' + V - \frac{i k T^{1/3}}{C_\perp} B = 0.
\]

In synchronous gauge `B=0`, hence `V = c_X/T`. A constant residual `G_X` generates exactly that profile, so the block is pure gauge. I found no exceptional surviving vector branch.

### 3.6 Even scalar/tensor block

In synchronous gauge `A=C=0`, the raw exact components reduce to:

\[
R_{0y} = -ik\left(U' + Z' - \frac{U}{T}\right),
\]

\[
\frac{R_{XX}}{a^2}
=
U''+\frac{2}{3T}U'
-\frac{1}{3T}(W'+Z')
\nu^2 T^{-4/3} U,
\]

\[
\frac{R_{zz}}{b^2}
=
Z''+\frac{2}{3T}U'
\frac{2}{3T}W'
\frac{5}{3T}Z'
\nu^2 T^{-4/3} Z.
\]

The momentum constraint gives

\[
U'+Z'-\frac{U}{T}=0.
\]

With `H_e = 2U + Z`, this is `U' = H_e' - U/T`. Solving `R_{XX}=0` for `W'` yields the stated formula, equivalently

\[
W'=3T U'' + 3U' - \frac{U}{T} + 3\nu^2 T^{-1/3} U.
\]

Substituting the constraint and this `W'` relation into `R_{zz}` gives exactly

\[
H_e''+\frac1T H_e'+\nu^2T^{-4/3}H_e=0.
\]

The remaining exact equations reduce to propagation identities:

\[
R_{yy} \propto 3T E' + 5E,\qquad
R_{00} \propto 3T E' + 4E,
\]

with `E = H_e'' + H_e'/T + \nu^2 T^{-4/3} H_e`.

I explicitly checked these reductions from the raw synchronous Ricci components. I found no dropped constraint, no hidden rank jump, and no exceptional even branch omitted by the quotient.

### 3.7 Full reconstructed residuals

I independently rechecked the claimed representatives:

- even: `A=-3H_e`, `C=-3 i C_\perp T^{2/3} H_e'/k`, `U=H_e`, `Z=-H_e`, `B=V=W=0`;
- odd: `N=Q=0`, only `h_13 = a b H_o`.

Substituting these directly into the full first-variation Ricci tensor, together with their master ODEs, makes all `16` matrix entries vanish exactly. In the even case the linearized scalar also vanishes on shell. I therefore found no reconstruction error and no residual hidden gauge remainder.

### 3.8 Curvature witnesses

I independently recovered the intrinsic slice-curvature witnesses

\[
2\frac{\delta R^{(3)}_{XX}}{a^2}+\frac{\delta R^{(3)}_{zz}}{b^2}
=
\frac{k^2}{b^2} H_e,
\]

\[
\frac{\delta R^{(3)}_{Xz}}{ab}
=
\frac{k^2}{2b^2} H_o.
\]

Because these are proportional to the gauge invariants, the two physical families are not periodic Lie derivatives.

### 3.9 Bessel bases, branch structure, and dimension count

With `zeta = 3 nu T^(1/3)`, I independently checked:

- `J0(zeta)` and `Y0(zeta)` solve the even master exactly;
- `J3(zeta)` and `Y3(zeta)` solve the odd master exactly;
- the transformed `T`-Wronskian is
  \[
  W_T = \frac{2}{3\pi T} \neq 0;
  \]
- past behavior is exactly:
  - even: finite `J0`, logarithmic `Y0`;
  - odd: `J3 ~ (9/16) nu^3 T`, `Y3 ~ -(16/(27 pi nu^3)) T^{-1}`;
- future common relative envelope is `T^(-1/6)`.

No branch was missing, no repeated/logarithmic branch was lost, and the stated dimension count

\[
2 \text{ masters} \times 2 \text{ time constants} \times 2 \text{ real phases} = 8
\]

is correct.

## 4. Evidence non-circularity and provenance

I specifically attacked the possibility that the package merely republishes prior answers or imports unregistered structure.

- The executable scripts import only standard-library modules, `sealed_runtime`, and vendored `sympy`.
- `verify_independent.py` does not import `derive_transverse_modes.py` and does not read `DERIVATION_RESULT.json`.
- `verify_package.py` includes canned-answer substitution attacks for the three generating scripts; all were rejected on source-integrity grounds during replay.
- The preregistration proof authenticates commit `96298482a035a6ffa9103d3949c6aa4fee987c75` and the five preregistered path-object identities.
- `SOURCE_SCOPE.tsv` registers exactly eight upstream dependencies, all intake-local, with no archive or protected paths.

I also searched the intake specifically for imports of action, source, matter model, observation, fit, scale, selected history/topology/population, physical `X_max`, or an unregistered field equation.

Result:

- I found no such live imports into the G328 derivation.
- The only active equation used is the explicitly declared owner-provisional `Ric-(R/4)g=0`, with provenance tied to G310/G312.
- The many occurrences of words like `source`, `action`, `matter`, `scale`, `history`, `topology`, and `X_max` are boundary statements that exclude those imports, not places where G328 smuggles them in.

## 5. Boundary enforcement

The intake consistently respects the declared limit. The claim is one primitive `y`-directed nonzero Fourier tile on compact intervals inside `T>0`, modulo periodic same-mode gauge, and not:

- the full nonzero Fourier spectrum;
- oblique covectors;
- multimode coupling;
- endpoint admissibility;
- full linear stability;
- nonlinear stability.

I found no inflation of the claim beyond that boundary.

## 6. Conclusion

I did not find an exact falsifier for the bounded landing. The symbolic closure, gauge quotient, Bianchi scalar step, parity split, residual reconstruction, curvature witnesses, Bessel bases, branch classification, eight-real-constant count, evidence non-circularity, and intake-local provenance all survive hostile review within the declared primitive transverse sector.

ACCEPT__G328_BOUNDED_TRANSVERSE_CENSUS
