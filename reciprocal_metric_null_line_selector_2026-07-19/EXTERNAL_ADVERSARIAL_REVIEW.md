# Fresh Adversarial Reviews

Date: 2026-07-19
Mode: three isolated read-only contexts, no package edits

## Overall ruling

`VERIFIED-WITH-CAVEATS`

No adversary refuted a load-bearing mathematical claim. The two algebra reviews independently reproduced the
conclusion that the reciprocal kinematics do not currently select one global conformal null line.

## Review A — causal gradient and anisotropic counterfamily

This review independently inverted a fully general positive two-dimensional angular metric and
obtained

\[
 g^{-1}(d\phi,d\phi)=
 -e^{2\phi}\phi_t^2/c^2+e^{-2\phi}\phi_r^2
 +q^{AB}\phi_A\phi_B.
\]

It confirmed:

- every nonzero static gradient is spacelike;
- null time-live gradients solve an optional two-sign eikonal equation;
- the positive angular term cannot be omitted;
- the static seal supplies either a spacelike gradient or no gradient line;
- the anisotropic metric
  `diag(-exp(-2r), exp(2r), exp(4r), exp(6r))` is nondegenerate on every finite interval and obeys
  the reciprocal temporal/radial identity.

Using an orthonormal-frame curvature calculation separate from the constructor, it reproduced

```text
Psi0 = Psi4 = -5/4 E
Psi1 = Psi3 = 0
Psi2 = -13/12 E
Q(z) = -E (z^2+5)(5z^2+1)/4
I^3-27 J^2 = 2025 E^6/16
```

and therefore exact Petrov I with four simple PNDs. It explicitly limited the counterfamily to a
kinematic local metric, not a complete on-shell universe. This frame calculation was reported by the
read-only review; the checked-in verifier supplies a separate runnable coordinate implementation.

## Review B — complete round/common-warp family

This review independently analyzed the nondegenerate warped product

\[
 g=h_{ab}(x)dx^a dx^b+R(x)^2\gamma_{AB}(y)dy^A dy^B.
\]

It reduced the Weyl tensor to one scalar,

\[
 \mathcal W={}^{(2)}R[h]/2+(\Box_hR)/R+(K-|\nabla R|_h^2)/R^2,
\]

and independently contracted a full coordinate Christoffel-Riemann-Ricci-Weyl calculation with an
adapted null tetrad. The result was

```text
Psi0 = Psi1 = Psi3 = Psi4 = 0
Psi2 = mathcal_W/6
```

up to an overall convention sign. It confirmed that the family is D when `mathcal_W` is nonzero and
O when it vanishes. It also caught the projective-infinity subtlety: `6 Psi2 z^2` contains a second
double PND at infinity and must never be read as one selected ray. II, III, and N cannot occur in
this common-warp family.

The package's banked runnable claim was subsequently narrowed to the static reciprocal round-sphere
subfamily directly computed by its constructor. The broader reduction above is retained as the
fresh review's analytic result, not silently substituted for checked-in executable coverage.

## Review C — final package consistency

The final zero-context review returned `VERIFIED-WITH-CAVEATS`. It reproduced the full causal norm,
explicit eikonal solution, static round D/O classification, projective-infinity root, anisotropic NP
scalars and invariants, and smooth-positive conformal typing. It found no scientific refutation. It
required evidence corrections before freezing:

- narrow the executable round-family claim to the static family actually computed;
- distinguish the reported frame check from the checked-in coordinate verifier;
- derive the angular norm from an explicit matrix inverse and display its positive complete-square
  form rather than count a definitional equality as evidence;
- rename zero-substitution and duplicate-discriminant checks as controller guards rather than
  necessity proofs;
- qualify conformal statements by smooth positive nondegenerate rescaling;
- build and verify `SHA256SUMS.txt` only after all corrections.

All requested evidence corrections were completed before the final package-manifest freeze and
replay.

## Required caveats retained

1. The general static `d phi` result is complete only within the positive-spatial, block-diagonal,
   gradient-adapted reciprocal representative.
2. The round-warped D/O theorem is conditional on that angular ansatz; it is not a universal UDT
   theorem.
3. The anisotropic Petrov-I family establishes present kinematic underdetermination. The missing
   action and boundary equations could later reject it.
4. Petrov algebra alone does not make a PND geodesic or physically solder it to a carrier.
5. Local exact classifications do not provide a globally smooth section through folds, zeros,
   degeneracies, or type transitions.
6. Mechanical check totals are not counts of independent physical facts.
7. Conformal claims apply only for smooth positive nondegenerate Common-Scale rescalings.

No repository files were changed by either review context.
