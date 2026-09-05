# External adversarial review of bounded G347

Date: 2026-09-04  
Role: fresh zero-context mathematical-relativity, causal-geometry, null-screen, and observer-covariance review

## Executive finding

The bounded G347 endpoint-observer covariance result is mathematically correct on the sealed premises. The load-bearing statements follow from Lorentzian tangent-space algebra plus the accepted G343/G345/G346 quotient-screen and determinant identities. I found no sign error in the null-rotation term, no missing or extraneous endpoint-frequency factor, no target-observer factor in either directional area, and no failure for transverse or oblique finite observer changes.

The result is covariance, not numerical observer invariance. It remains an infinitesimal metric angular-area statement on each supplied labelled null ray. It is not a finite-beam, radiative-transfer, detector, brightness, flux, luminosity, probability, distance-selection, observer-selection, route-selection, matter, stability, scale, `X_max`, or canon result.

## 1. Intake authentication and handling

Before reading any substantive payload, I copied the complete mounted intake from `/intake` to the fresh writable directory `/work/g347-review.jXYrT6`. All executions were made in that copy. I did not edit the mounted intake or any copied evidence payload.

Authentication results:

- The SHA-256 of `REVIEW_MANIFEST.tsv` is `727492d6f4d21d315cff136d2289f452a864397df78f13d02eff8b660587891f`, exactly the value in `REVIEW_MANIFEST.sha256`.
- The manifest contains exactly 28 payload entries, matching `REVIEW_SCOPE.json`.
- The actual payload path set, after excluding the manifest and its detached seal, equals the declared set exactly: no missing and no undeclared payload.
- All 28 payload byte lengths and SHA-256 digests match their manifest rows in both `/intake` and the `/work` copy.
- The total file count is 30: 28 payloads plus `REVIEW_MANIFEST.tsv` and `REVIEW_MANIFEST.sha256`.
- All filesystem objects in the intake are ordinary files or directories; there are no symlinks or special objects.
- The source and copied scope, manifest, and detached-seal files are byte-identical.
- A post-replay authentication again found 28/28 matching payloads, the same manifest seal, the exact 30-file total, and no `__pycache__` or other added evidence-tree object.

This authenticates internal consistency and exact sealed-intake identity. The checksum file is unkeyed and therefore is not an external signer identity or provenance trust anchor. Likewise, `GIT_PREREGISTRATION_PROOF.txt` is authenticated as a sealed payload and contains the preregistration commit/diff record, but, under the prohibition on repository and network access, I treated it as documentary evidence rather than independently consulting a Git remote. The two live-orientation paths named in `SOURCE_SCOPE.tsv` but absent from the sealed manifest were not accessed and were not used; the bounded derivation and replay depend on the four included exact source derivations instead.

No web access, downloads, package installation, protected packages, or repository access were used.

## 2. Evidence classification and replay

The registered aggregate was run from the writable copied `g347` directory as:

```text
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_package.py
```

It returned `19/19`, including fresh subprocess replays of the production derivation (`73924/73924`), implementation-distinct verifier (`23547/23547`), and hostile-mutation suite (`22/22`). An independent before/after digest snapshot and the subsequent full manifest check showed no payload-byte change.

I also wrote a separate standard-library-only reconstruction outside the evidence copy at `/work/g347_scratch_reconstruction.py`. It imports nothing from the intake. It directly tested Lorentz products, quotient shifts, screen projection, inverse and transitive observer changes, five-point celestial derivatives in both tangent directions, longitudinal/transverse/oblique and near-null velocities, arbitrary `GL(2)` frames, affine changes, reversal, the inverse-G345 mean, and stationary sewing. It passed 10,831 checks with maximum normalized numerical error `2.4771164354994268e-08`, below the declared `8e-8` near-null/general-frame tolerance. Its SHA-256 is `f56d943e13b9569d8c3ec6aa3995562ebe4df0b754dc88eae12cedbb267eb393`.

These evidence classes must not be conflated:

- The quotient, observer-screen, celestial differential, endpoint factors, reversal, mean, sewing, affine, and coordinate laws below are algebraic identities.
- The production and independent programs provide broad numerical and implementation-distinct verification. They remain premise-sharing checks, not premise-independent proofs.
- Token searches, wording gates, the sealed Git transcript, result JSON, and hostile documentary mutations are integrity guards. They do not prove the mathematics.
- The local screen theorem can be proved directly in any four-dimensional time-oriented Lorentz tangent space. The bilocal conclusion still conditionally imports the supplied G343/G345/G346 objects and does not establish their premises, the adopted spacetime, or any owner-provisional equation independently.

## 3. Null quotient and observer-screen representatives

Fix signature `(-,+,+,+)`, a nonzero future null vector `k`, and a future unit timelike vector `u`. Put

\[
\omega_u=-g(k,u)>0,\qquad k=\omega_u(u+s_u),
\]

where `s_u` is unit spacelike and orthogonal to `u`.

For `X` in `k^perp`, write `X=a u+x` with `x` in `u^perp`. The equation `g(X,k)=0` gives `x dot s_u=a`. Hence

\[
g(X,X)=|x|^2-a^2=|x-a s_u|^2\geq0.
\]

Equality holds exactly when `x=a s_u`, which means `X=(a/omega_u)k`. Thus the radical of the restricted form on `k^perp` is precisely `span(k)`, and the induced form on

\[
Q_k=k^\perp/\operatorname{span}(k)
\]

is positive definite. Its definition contains no observer; `u` was only a convenient proof decomposition.

The representative

\[
\pi_u[X]=X+\frac{g(X,u)}{\omega_u}k
\]

lies in both `u^perp` and `k^perp`. Under `X -> X+c k`, the extra `c k` cancels because `g(k,u)=-omega_u`; thus the map is well defined on the quotient. Uniqueness follows because an affine class `X+span(k)` has only one member orthogonal to `u`. Nullity of `k` and `g(X,k)=0` give

\[
g(\pi_u[X],\pi_u[Y])=g(X,Y),
\]

so this is an isometric identification of `Q_k` with the observer screen `S(u,k)`.

For `X` in `S(u,k)`, the change to observer `v` is

\[
I_{v\leftarrow u}X=X+\frac{g(X,v)}{\omega_v}k.
\]

The plus sign is forced by `g(k,v)=-omega_v`. If its coefficient is called `a_v`, then applying the reverse projection adds `g(X+a_vk,u)k/omega_u=-a_vk`, proving the inverse. For a third observer `w`,

\[
\frac{g(X+a_vk,w)}{\omega_w}
=\frac{g(X,w)}{\omega_w}-a_v,
\]

which cancels the first null shift and proves

\[
I_{w\leftarrow v}I_{v\leftarrow u}=I_{w\leftarrow u}.
\]

This also verifies every sign in the null-rotation term.

## 4. Full celestial tangent and solid-angle transformation

Represent a projective-null tangent at fixed `u`-frequency by `delta k=omega_u theta_u`, with `theta_u` in `S(u,k)`. Since `s_v=k/omega_v-v` and `delta omega_v=-g(delta k,v)`, direct differentiation gives

\[
\delta s_v
=\frac{\omega_u}{\omega_v}
\left(\theta_u+\frac{g(\theta_u,v)}{\omega_v}k\right)
=\frac{\omega_u}{\omega_v}I_{v\leftarrow u}\theta_u.
\]

Because `I` is an isometry, both celestial tangent directions receive the same scale. Therefore the tangent metric scales by `(omega_u/omega_v)^2` and the unoriented two-dimensional metric solid angle scales by

\[
d\Omega_v=\left(\frac{\omega_u}{\omega_v}\right)^2d\Omega_u.
\]

This is the full differential, not merely a collinear frequency calculation.

To make the generality explicit, decompose the relative velocity as `beta=beta_parallel s_u+beta_perp`. Every future unit observer has the unique pointwise tangent-space chart

\[
v=\gamma(u+\beta),\qquad
D_{v\leftarrow u}=\frac{\omega_v}{\omega_u}
=\gamma(1-\beta_\parallel)>0.
\]

For a screen tangent `theta`,

\[
I_{v\leftarrow u}\theta
=\theta+\frac{\theta\mathbin\cdot\beta_\perp}{1-\beta_\parallel}(u+s_u).
\]

Thus a transverse component gives a nonzero plus-signed null rotation even though the quotient length is unchanged. Longitudinal motion has `beta_perp=0`; purely transverse motion has `D=gamma` and a generally nonzero null shift; the oblique case contains both. The solid-angle factor follows after the entire isometric null rotation, so all finite longitudinal, transverse, and oblique changes are covered.

“Finite boost” and “rapidity” here name coordinates on the future-unit hyperboloid in one tangent space. No worldline dynamics, inertial-frame postulate, special-relativistic propagation model, electromagnetic law, or optical-reciprocity theorem is imported.

## 5. Directional areas: source factor only

The G343 position block is a map between intrinsic quotient screens. Replacing an endpoint observer changes only its representative plane through an isometry. Consequently the target quotient-screen metric area is unchanged. At a source endpoint, however, the same projective angular patch obeys `dOmega_v=D^{-2}dOmega_u`. Therefore

\[
\mathscr A'_{1\leftarrow0}=D_0^2\mathscr A_{1\leftarrow0},\qquad
\mathscr A'_{0\leftarrow1}=D_1^2\mathscr A_{0\leftarrow1}.
\]

There is no target factor: changing only the target observer applies an isometry to the numerator area. A target-observer factor would require extra structure such as a material detector plane, which is not in the sealed premises.

The same conclusion follows from the coordinate formula

\[
\mathscr A_{1\leftarrow0}
=\omega_0^2|\det B_{10}|\sqrt{\det q_1\det q_0}.
\]

The intrinsic determinant/metric-area combination is observer-screen invariant, while only the source frequency changes. If `D_i` is not one, the corresponding numerical area ordinarily changes; the claim is covariant, not invariant.

## 6. Reversal, G345 mean, and stationary sewing

Using the accepted common-affine relation `B_01=-B_10^T`, the changed directional ratio is

\[
\frac{\mathscr A'_{1\leftarrow0}}{\mathscr A'_{0\leftarrow1}}
=\frac{D_0^2}{D_1^2}
\left(\frac{\omega_{u_0}}{\omega_{u_1}}\right)^2
=\left(\frac{\omega_{v_0}}{\omega_{v_1}}\right)^2.
\]

Its form is unchanged while its numerical value is observer dependent.

G345's scalar can be written

\[
\widehat\Delta_{10}
=\frac{1}{|\det B_{10}|\omega_0\omega_1
\sqrt{\det q_0\det q_1}}.
\]

The observer isometries leave the determinant/metric-area part invariant, so

\[
\widehat\Delta'_{10}=\frac{\widehat\Delta_{10}}{D_0D_1}.
\]

It follows exactly that

\[
\sqrt{\mathscr A'_{1\leftarrow0}\mathscr A'_{0\leftarrow1}}
=\frac{1}{\widehat\Delta'_{10}}.
\]

This is an inverse-G345 geometric mean, not an arithmetic mean and not an observer-independent number.

At a stationary join, the invariant middle-screen determinant is normalized as

\[
\widehat h_1=\frac{|\det H_1|}{\omega_1^2\det q_1}.
\]

The quotient Hessian and metric screen area are unchanged by the observer isometry, whereas `omega_1` gains `D_1`. Hence

\[
\widehat h'_1=\frac{\widehat h_1}{D_1^2}.
\]

The right side of the sewn law then gains `D_1^{-2}` from the middle factor, `D_1^2` from the segment sourced at the middle endpoint, and `D_0^2` from the segment sourced at endpoint zero. The middle factors cancel and exactly reproduce the `D_0^2` change of the total area. Leaving `hhat_1` unchanged, multiplying it by `D_1^2`, or omitting stationary elimination is false.

## 7. Coordinate, affine, directional, coincidence, boundary, and label attacks

For passive endpoint coordinates `x_i'=R_i x_i`, with arbitrary `R_i` in `GL(2)`,

\[
B'_{10}=R_1B_{10}R_0^T,\qquad
q'_i=R_i^{-T}q_iR_i^{-1}.
\]

The determinant of `B` gains `|det R_1 det R_0|`, while the two metric-area coefficients gain its reciprocal. Thus both directional areas, G345's normalized scalar, and the normalized middle determinant are coordinate scalars. This passive freedom is distinct from the active isometric identification of two observer representative planes, and composing the two produces no extra frequency factor.

Under a common positive affine change `k -> a k`, each frequency gains `a`, each `B` gains `a^{-1}`, each two-dimensional `det B` gains `a^{-2}`, and every `D_i` is unchanged. The areas, changed reversal, mean, and sewing laws are therefore affine invariant.

The observer proof is independent of the projective ray direction. It applies unchanged to every mixed direction and both supplied principal families. As a cross-check, the sealed longitudinal G346 formulas have ratio `(T_0/T_1)^(2/3)`, matching the square of the G340 longitudinal frequency ratio, while the transverse formulas have ratio `(T_1/T_0)^(4/3)`, matching the square of the transverse frequency ratio. The mixed formula already factors as `G r` and `G/r`; multiplying its two sources by `D_0^2` and `D_1^2` gives the changed laws above without deleting either screen component.

At endpoint coincidence the supplied `B` has identity-chart behavior linear in endpoint separation, so each two-dimensional area is quadratic. Multiplication by a fixed finite positive `D_source^2` preserves this order. This statement is pointwise in a fixed included observer; it is not a uniform theorem for a correlated double limit in which the observer simultaneously runs to the null boundary.

For every `|beta|<1`, `D` is finite and strictly positive. Along a collinear chase with speed `b -> 1`,

\[
D=\sqrt{\frac{1-b}{1+b}}\longrightarrow0,
\]

so `dOmega_v/dOmega_u` diverges and the source directional area tends to zero. In the opposite collinear direction, `D` is the reciprocal and tends to infinity. General approaches to the null direction can be path dependent and need not have one uniform finite limit; this supports, rather than weakens, the stated singular-boundary classification. At `|beta|=1` there is no unit timelike observer and no finite normalization hidden by the formulas. The boundary is correctly excluded.

Every compact lift retains its own null generator, frequency factors, propagator, and directional-area pair. All covariance identities apply label by label. No sum, weight, interference rule, earliest-route rule, preferred lift, or physical population is introduced.

## 8. Scope and adversarial conclusion

The word “frequency” denotes the local scalar `-g(k,u)` and “solid angle” denotes the metric area on the celestial tangent. Those definitions support the stated geometry but do not supply an electromagnetic field, signal emission, finite bundle evolution, intensity, polarization, absorption, detector response, brightness, flux, luminosity, probability, or observational prediction.

Likewise, an angular-area Jacobian is not by itself a selected observational distance. The result chooses no preferred observer, worldline population, source, detector, route, compact lift, topology, physical scale, matter/mass model, `X_max`, or canon. It proves no generic-spacetime propagation or stability theorem. The local Lorentzian screen lemma is pointwise and broadly valid, but the bilocal G347 landing remains expressly conditional on the supplied spacetime, endpoints, labelled rays, accepted G343/G345/G346 inputs, and owner-provisional arena.

The only caveats found are non-blocking scope clarifications already respected by the package: checksum and Git transcripts are documentary rather than externally signed provenance; implementation diversity is not premise independence; coincidence scaling is for fixed finite observers; and null-boundary limits are nonuniform/path dependent. None changes a formula or requires repair of the bounded landing.

ACCEPT_G347_BOUNDED_ENDPOINT_OBSERVER_COVARIANCE
