# External Review Response — G329

## Scope and method

I treated this as a fresh hostile mathematical review of the sealed intake at `/intake` only. I did
not browse the web, access any repository, install packages, or modify evidence files. Writable
checks used `/work` and `/tmp` only.

## 1. Authentication of scope, seal, manifest, and payloads

- `REVIEW_SCOPE.json` authenticated through `REVIEW_MANIFEST.tsv`: the manifest row for
  `REVIEW_SCOPE.json` matched both byte count `600` and SHA-256
  `d87b71b0eedf41f3501ccff982fdd6062c6ac57fe3b512bd1d1c61e866bc4cfc`.
- The detached manifest seal in `REVIEW_MANIFEST.sha256` is exactly
  `a19494b0f447e8d1e9148cef4447c50130f1b59e5da9d11592f4fa420c322679`.
- Independent `python3 -S` hashing of `/intake/REVIEW_MANIFEST.tsv` reproduced that exact seal.
- I verified every listed payload in `REVIEW_MANIFEST.tsv` against its recorded byte count and
  SHA-256. All `41/41` payloads matched.

Conclusion: the review scope, manifest, detached seal, and all manifest payloads authenticate
cleanly.

## 2. Literal replay in one writable ephemeral copy

- I created one writable ephemeral copy at `/work/g329_review.MhlI4h` from `/intake`.
- I verified the intake-local vendored runtime under `python3 -S` by importing
  `sealed_runtime.activate_runtime()` from the ephemeral copy. It loaded
  `/work/g329_review.MhlI4h/VENDORED_SYMPY_RUNTIME.zip` and imported `sympy 1.13.1` and
  `mpmath 1.3.0`.
- I then ran the four registered commands literally, in that copy, with no edits:

```bash
python3 -S derive_oblique_modes.py --output /tmp/G329_DERIVATION_RESULT.json --raw-output /tmp/G329_RAW_RESIDUALS.json
python3 -S verify_independent.py --output /tmp/G329_INDEPENDENT_VERIFICATION.json
python3 -S run_catch_proofs.py --output /tmp/G329_CATCH_PROOF_RESULT.json
python3 -S verify_package.py --output /tmp/G329_PACKAGE_VERIFICATION_RESULT.json
```

- All four commands exited `0`.
- The `/tmp` replay outputs matched the sealed intake JSON files byte-for-byte:
  `DERIVATION_RESULT`, `RAW_RESIDUALS`, `INDEPENDENT_VERIFICATION`, `CATCH_PROOF_RESULT`,
  `PACKAGE_VERIFICATION_RESULT`.
- After replay, I rechecked the authenticated intake manifest hashes. `/intake` remained
  byte-identical to its manifest.

Conclusion: the sealed package replays exactly in a writable copy under `python3 -S`, using the
vendored runtime, with no evidence-file changes.

## 3. Independent mathematical review

### 3.1 Full ten-component first variation and parity split

The declared strict-oblique mode uses the background

\[
g_0=-dT^2+T^{-2/3}dx^2+T^{4/3}(dy^2+dz^2),
\qquad q=\alpha\,dx+\beta\,dy,
\qquad \alpha\beta\neq 0.
\]

The perturbation content is complete:

- odd under `z -> -z`: `N,H,Q`;
- even under `z -> -z`: `A,B,C,U,V,W,Z`.

That is `3+7=10` unrestricted metric amplitudes. The raw residual record preserves all ten
upper-triangle components. There is no hidden tensor-only or scalar-only truncation.

### 3.2 Linearized Bianchi identity and the zero mode

The load-bearing point is the inference `delta R=0`. I attacked this directly because it is where
the nonzero spatial covector matters.

- In the strict-oblique tile, the exact linearized identity is
  `∇^a δS_ab = (1/4) ∇_b δR`.
- Since `q` has nonzero spatial components, the `x` or `y` component gives
  `i alpha delta R = 0` or `i beta delta R = 0`.
- Therefore `delta R=0` follows in the declared stratum `alpha beta != 0`.
- This argument fails at the spatial zero mode. I checked the intake source lineage for that
  exception. The G325 homogeneous source explicitly retains a connected scalar branch
  `delta R = 4 lambda` at `alpha=beta=0`.

Conclusion: the package uses the Bianchi step correctly inside the strict-oblique tile and does not
legitimately erase the zero mode.

### 3.3 Complete periodic gauge image and gauge fixing

I independently checked the four-function same-mode gauge image and the gauge determinant.

The stated same-mode Lie image formulas are consistent, and for the proposed complete gauge
conditions `U=V=Z=Q=0`, the gauge matrix has determinant

\[
-\frac{2i}{3}\alpha^2\beta.
\]

For `alpha beta != 0` this is nonzero on every compact interval in `T>0`, so the gauge fixing is
complete in the declared stratum. I also checked the purported orbit amplitudes:

\[
\mathcal E=
W-Z-\frac{\beta}{\alpha T}V
+\frac{\beta^2}{\alpha^2T^2}\left(U+\frac Z2\right),
\qquad
\mathcal O=H-\frac{\alpha T}{\beta}Q.
\]

Substituting a pure gauge perturbation makes both vanish identically. There is no residual same-mode
periodic gauge freedom left after `U=V=Z=Q=0`.

### 3.4 Odd block rederivation

Using the sealed raw residual formulas, not the narrative summary, I rederived the odd block in the
gauge `Q=0`.

From `R_03=0` one gets exactly

\[
N=-\frac{i\alpha T^{2/3}}{\alpha^2T^2+\beta^2}(TH'-H).
\]

Substituting this into the remaining nontrivial odd equations gives the single scalar equation

\[
H''
+\frac{\beta^2-\alpha^2T^2}{T(\alpha^2T^2+\beta^2)}H'
+\left[
(\alpha^2T^2+\beta^2)T^{-4/3}
+\frac{\alpha^2T^2-\beta^2}{T^2(\alpha^2T^2+\beta^2)}
\right]H=0.
\]

With `Psi_o = H / sqrt(alpha^2 T^2 + beta^2)`, this becomes

\[
\Psi_o''+\frac1T\Psi_o'
+\left[
(\alpha^2T^2+\beta^2)T^{-4/3}
+\frac{\beta^2(2\alpha^2T^2-\beta^2)}{T^2(\alpha^2T^2+\beta^2)^2}
\right]\Psi_o=0.
\]

I then checked the representative equations directly:

- `R_03=0`,
- `R_13=0`,
- `R_23=0`,

after substituting the representative and the master shell. All vanish exactly.

### 3.5 Even block rederivation

I independently reduced the even block from the raw residual equations in the complete gauge
`U=V=Z=0`.

Define

\[
D=\alpha^2T^2+\beta^2,
\qquad
d=4\alpha^2T^2+\beta^2,
\]

and the orthogonal shift combinations

\[
L=\beta B-\alpha T C,
\qquad
M=\alpha T B+\beta C.
\]

From the raw residual equations:

- `R_33=0` yields
  \[
  M=iT^{2/3}(A'-W').
  \]
- `R_01=0` yields
  \[
  L=\frac{2i\alpha T^{2/3}}{3\beta}(3TW'-4A+3W).
  \]
- `R_02=0` then forces
  \[
  A=\frac{3\alpha^2T^2(TW'+W)}{4\alpha^2T^2+\beta^2}.
  \]

Solving back for the shifts gives

\[
B=\frac{\beta L+\alpha T M}{D},
\qquad
C=\frac{-\alpha T L+\beta M}{D}.
\]

Substituting these reconstructions into the remaining nontrivial even residuals reduces them to the
single scalar master

\[
W''
+\frac{4\alpha^2T^2+5\beta^2}{T(4\alpha^2T^2+\beta^2)}W'
+\left[
(\alpha^2T^2+\beta^2)T^{-4/3}
+\frac{4\beta^2}{T^2(4\alpha^2T^2+\beta^2)}
\right]W=0.
\]

I then checked the representative equations directly, including the differentiated master shell for
the `B'` and `C'` terms:

- `R_33=0`,
- `R_01=0`,
- `R_02=0`,
- `R_11=0`,
- `R_22=0`,
- `R_00=0`.

All vanish exactly. The other even/odd matrix positions are identically zero by parity and were
already preserved in the raw residual evidence.

Conclusion: both master equations and the representative reconstruction are correct.

### 3.6 Residual closure, curvature witnesses, and dimension count

I found no dropped residual component. In the fixed representatives:

- the odd nontrivial residual entries vanish exactly on the odd master;
- the even nontrivial residual entries vanish exactly on the even master;
- the remaining matrix entries are identically zero by the parity block structure.

The orbit-curvature witnesses are also consistent:

\[
\widehat{\delta R}^{(3)}_{xx}=\alpha^2\mathcal E,
\qquad
\widehat{\delta R}^{(3)}_{xz}=\frac{\beta^2}{2T}\mathcal O.
\]

These are nonzero for nonzero physical families on open sets, so the two masters are not periodic
Lie derivatives.

The dimension count is also correct:

- two second-order complex master equations;
- two time constants each;
- reality adds the conjugate `-q` mode, equivalently cosine/sine phases.

That gives exactly `2 x 2 x 2 = 8` real physical constants.

### 3.7 Frozen-angle attack and exact decoupling

The exact decoupling is parity decoupling, not a frozen-angle shortcut.

The physical propagation angle is

\[
\tan\theta(T)=\frac{\beta}{\alpha T},
\qquad
\theta'(T)\neq 0.
\]

I checked that both master coefficients retain both `alpha` and `beta`, and the extra rational
terms depending on `D` and `d` are precisely the terms that would be lost if one silently replaced
the oblique direction by a constant-angle axial surrogate. I found no frozen-angle simplification.

### 3.8 G327/G328 limits, Wronskians, and endpoint branches

The component limits check out:

- `beta -> 0` gives the G327 axial equation in both sectors.
- `alpha -> 0` gives the G328 odd equation directly.
- `alpha -> 0` in the even sector is singular in `W`, but after the regular transverse
  normalization `E=T^2W` it gives the G328 even equation exactly.

I also checked the exact Wronskians:

\[
\mathcal W_e=C\frac{(4\alpha^2T^2+\beta^2)^2}{T^5},
\qquad
\mathcal W_o=\frac{C}{T}.
\]

They satisfy the exact first-order Wronskian equations and do not vanish on `T>0`. Therefore no
endpoint branch is being discarded by a hidden degeneracy.

Past branches:

- even, after `E=T^2W`: repeated indicial root `0`, so `E ~ 1, log T`;
- equivalently `W ~ T^{-2}, T^{-2} log T`;
- odd normalized: roots `+1,-1`, so `Psi_o ~ T, T^{-1}`.

Future branches:

- both masters have leading frequency `alpha T^{1/3}`;
- phase `~ (3/4) alpha T^{4/3}`;
- common relative envelope `T^{-2/3}`.

I found no missing exceptional compact-time branch in the strict-oblique stratum because the only
load-bearing denominators are `D` and `d`, both strictly positive for `T>0` when `alpha beta != 0`.

## 4. Forbidden-import audit and scientific boundary

I searched the intake for imported action, source, matter model, observation, fit, scale, selected
history, topology/population, physical `X_max`, and equation drift.

Findings:

- In the G329 evidence itself, the active equation remains only
  `delta(R_ab - (1/4) R g_ab) = 0`.
- The G329 derivation, audit, preregistration, and premise ledger repeatedly mark action/source/
  matter/observation/fit/scale/history/topology/population/`X_max` as absent or open.
- I found no new field equation introduced in G329 beyond the registered owner-provisional
  trace-free Ricci equation.
- Historical source-lineage files in `/intake/sources` mention earlier premises and background
  provenance, including the accepted zero-mode comparison. Those are registered lineage artifacts,
  not new imports into the G329 derivation.

Boundary enforcement:

- this is one primitive strict-oblique Fourier tile only;
- it is not full Fourier stability;
- it is not nonlinear stability;
- it does not select a physical universe, topology, population, history, scale, or `X_max`.

## 5. Verdict

I found no mathematical defect inside the bounded G329 claim as stated. The authentication,
literal replay, independent raw-equation reduction, gauge-rank analysis, zero-mode Bianchi
exception handling, exact residual reconstruction, curvature witnesses, component limits, Wronskian
checks, endpoint branch census, and boundary discipline all support the stated landing.

The acceptance is bounded and conditional exactly as the package says: it relies on the registered
G324 background and the owner-provisional trace-free response equation, and it does not promote the
result to full linear/nonlinear stability or physical selection.

ACCEPT__G329_BOUNDED_OBLIQUE_CENSUS
