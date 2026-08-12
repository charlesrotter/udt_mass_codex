# Curvature-principal reciprocal/angular split ownership audit

Date: 2026-08-12  
Branch: `grok`  
Grade: **VERIFIED-WITH-CAVEATS**  
Primary landing:

```text
CURVATURE_OWNS_REGISTERED_SPLIT_ONLY_ON_A_PROPER_SUBSET_OF_TESTED_STRATA
```

## What was tested

An external proposal suggested that the Weyl tensor might already derive the reciprocal/angular
`2+2` split used by the complete coframe. This package tests that proposal directly rather than
promoting it from analogy.

The production route computes the full Riemann, Weyl, and Ricci tensors from every supplied metric
jet using double-precision automatic differentiation. It then classifies the complete self-dual
Weyl operator, including Jordan/nilpotent cases, and tests the **registered** split by direct
eigenbivector/projector and Ricci-invariance residuals. Its frame-covariance control is restricted
to frame changes preserving the registered `2+2` split; it is not a general moving-projector test.
A separately coded fourth-order
finite-difference implementation independently repeats every tensor and classification.

The bounded arena contains:

- the exact conditional founding spherical metric family;
- all 14 G63 complete-metric witnesses at their `p/q/r` tiles: 42 local jets;
- all 196 G85 profile identities in each of three regular constructive completion classes at three
  frozen controls: 1,764 provenance rows. The zero-shift Kruskal-local A05 subcase remains an
  explicit `INSUFFICIENT_OWNED_JET` scope row and receives no numerical Petrov type.

The G85 A05 construction is locally profile-independent at the chosen equatorial `h=0` band.
Consequently, the full census contains 1,806 provenance rows but only **1,221 distinct local metric
jets**. The repeated rows preserve source provenance and are not counted as independent evidence.

## Exact founding-family result

Write

```text
f(r) = exp[-2 phi(r)]
```

so that the conditional founding spherical metric is

```text
ds^2 = -f c_E^2 dt^2 + f^-1 dr^2 + r^2 dOmega^2.
```

Its magnetic Weyl tensor vanishes. The electric Weyl eigenvalues are

```text
w, -w/2, -w/2,

w = [r^2 f'' - 2 r f' + 2 f - 2] / (6 r^2).
```

Therefore:

- if `w != 0`, the metric is Petrov D and the temporal-radial versus angular split is the unique
  Weyl-principal `2+2` split;
- if `w = 0`, the local family is exactly `f=1+a r+b r^2` and the Weyl tensor is type O;
- on that type-O family, the pair/screen Ricci eigenvalue gap is `a/r`, so Ricci still recovers the
  split when `a != 0`;
- only when `w=0` and `a=0` do neither of the tested pointwise curvature operators own the split.

This directly rejects the proposed shortcut “Petrov O implies a new preferred flag field.” Weyl
degeneracy alone is insufficient; Ricci can retain the split. Even joint Weyl/Ricci degeneracy is
only a no-owner result for the tested **pointwise** operators, not proof of an aether or a new
postulate.

## Complete-metric census

| Bounded stratum | Rows | Petrov / registered-split result |
|---|---:|---|
| G63 R17 | 27 | all I; registered split misaligned and not Ricci-invariant |
| G63 complete time-live | 15 | all I; registered split misaligned and not Ricci-invariant |
| G85 A03, nonconstant profile | 576 | all I; misaligned |
| G85 A03, constant profile | 12 | I; Weyl aligns with one of three candidates and Ricci owns the registered split |
| G85 A04, nonconstant profile | 576 | all I; misaligned |
| G85 A04, generic constant profile | 9 | I; Weyl aligns with one of three candidates and Ricci owns the registered split |
| G85 A04, constant `q=1/2` | 3 | D; curvature-aligned, but Ricci has no pair/screen gap |
| G85 A05 shift-supported taper | 588 | D; Weyl and Ricci agree on the split; only 3 distinct jets |

Aggregate Petrov count:

```text
D = 591
I = 1,215
```

Aggregate ownership count:

```text
WEYL_AND_RICCI_AGREE_ON_SPLIT               588
RICCI_DERIVED_WITH_WEYL_ALIGNMENT             21
CURVATURE_ALIGNED_BUT_NOT_UNIQUE                3
SPLIT_MISALIGNED_WITH_CURVATURE_PRINCIPALS   1,194
```

The census falsifies the universal **Weyl** version of the external proposal. In particular, none of the 42
G63 points—including the R17 controls—has its registered split recovered by the tested pointwise
curvature operators. The strong positive A05 count is not 588 independent confirmations: it is
three local metric jets repeated across 196 retained profile identities.

## What this means

Curvature is a genuine metric-native source of reciprocal/angular structure on a proper subset of
the tested metric arena. It can uniquely own the split on nondegenerate founding spherical type-D
strata and can retain it through Ricci when Weyl degenerates in part of the exact type-O family.

But the complete orchestra can rotate or mix the registered coframe split away from every
pointwise curvature-principal plane. Type I often reduces the metric to three finite principal
candidate planes, but that is not the same as recovering the registered one. Petrov classification
therefore narrows the ownership problem; it does not solve it universally.

Nothing here selects a physical metric history, observer query, pair realization, action, source,
bootstrap law, `X_max`, SNe history, CMB history, or global flag section. Petrov type is a
classification of supplied geometry, not a physical-admissibility law.

## Verification gates

1. **Preregistered:** yes; question and numerical controls were committed before outcomes.
2. **Full space or bounded scope justified:** bounded local pointwise tile, explicitly delimited;
   all numerically evaluable preregistered G63/G85 rows retained; the missing zero-shift A05 second
   jet is explicitly returned as `INSUFFICIENT_OWNED_JET` outside the numerical atlas.
3. **Independently verified:** yes; separately coded finite differences reproduce 1,806/1,806
   classifications. Maximum relative tensor errors are `5.75e-9` (Weyl) and `7.06e-9` (Ricci),
   below the preregistered `2e-5` gate.
4. **Every premise audited:** yes; all constructive amplitudes and controls remain
   `pinned-by-HABIT`, and no physical selection is inferred.

Fourteen of fourteen catch proofs pass. Repository-wide gates are recorded separately in
`REPOSITORY_GATES.json`.

## Next justified question

Do not return to AM seam selection and do not install a preferred flag. The bounded next move is to
ask whether any **other metric-natural local concomitant**—for example a joint curvature-derivative
algebra—recovers the registered split specifically on the robustly misaligned strata, or whether
split ownership there is genuinely history/query/realization-relative. That question must again be
preregistered and must retain a no-owner return.
