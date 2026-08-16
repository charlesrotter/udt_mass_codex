# Exact derivation — source-free UDT kaleidoscope forward operator

Date: 2026-08-15

## 1. Result first

The preregistered outcome-blind landing is

```text
FACTORIZED_REGULAR_KALEIDOSCOPE_NULL_DERIVED
__SELECTION_REFERENCE_MISMATCH_AND_CORRELATED_MULTIIMAGE_TERMS_EXACT
__CURRENT_COMPLETE_METRIC_PERMITS_BUT_DOES_NOT_OWN_A_NONZERO_CONNECTED_MODE
__ALL_FOUR_COEFFICIENT_HOMES_DORMANT__BOSS_AND_CMB_UNREAD
```

The kaleidoscope interpretation survives, but its exact mathematical burden is now visible. A
simple independent distortion of every source is only a lens. A genuine pattern from an otherwise
uncorrelated source population requires either a physical one-point modulation not represented by
the survey randoms or a connected two-relation operator. Current complete-metric equations permit
both homes conditionally but select neither.

This is not a no-go against future global, critical, holonomy, bootstrap, or joint source-history
structure.

## 2. Null source premise

Let `lambda` be a smooth positive source intensity on source-label space `Sigma`. G104 explicitly
posits the factorial null

```text
lambda_2^! = lambda tensor lambda
```

off the diagonal. It means no intrinsic connected BAO-like source pattern. It does not remove the
galaxies, their smooth one-point density, survey selection, or finite-catalog noise.

The premise is `POSIT_WORKING_OBSERVATIONAL_BASELINE`, not a metric derivation.

## 3. The simple-lens theorem

Let `K_1` be any measurable deterministic or independently marked one-source response. It includes
the complete supplied relation

```text
E=[[B,0],[QS,Q]],
J=[Y;Zeta],
Psi(a)=(Z_a,n_a),
```

with the entire orchestra entering before the observer readout. Write

```text
nu_1=K_1[lambda].
```

If the two-source response factorizes,

```text
K_2=K_1 tensor K_1,
```

then exactly

```text
nu_2=K_2[lambda tensor lambda]
    =nu_1 tensor nu_1,

C_obs=nu_2-nu_1 tensor nu_1=0.                 (1)
```

Equation (1) is independent of how nonlinear the one-source map is. A source may select one branch
randomly with source-local probabilities; the resulting marked Poisson map is still one `K_1`, so
the factorial output remains factorized. Merely turning on more `B,Q,S,Y,Zeta` activity does not
change this statistical type.

The production witness uses a nonidentity stochastic `3 x 3` kernel and exact rational source
weights. The connected matrix is identically zero. A separate Fraction implementation uses
different weights and a different kernel and obtains the same theorem.

## 4. What the survey randoms subtract

Let `p` be the normalized physical observed one-point measure and `q` the normalized random-catalog
measure for the registered selection. For a symmetric bin kernel `I_k`, the expectation of the
normalized Landy--Szalay numerator under the factorized null is

```text
N_k
 = integral I_k [p tensor p - p tensor q - q tensor p + q tensor q]
 = integral I_k [(p-q) tensor (p-q)].           (2)
```

Therefore

```text
w_k=N_k / integral I_k(q tensor q).             (3)
```

Two cases are exact.

### 4.1 Full one-point selection represented

If `q=p`, then every `w_k=0`. A regular independent complete relation does not produce a connected
pair pattern after its entire one-point intensity is represented by the random reference.

### 4.2 Physical modulation omitted from the selection randoms

If

```text
p=q(1+m),
integral m dq=0,
```

then

```text
w_k
 = [integral I_k q(x)q(y)m(x)m(y)]
   /[integral I_k q(x)q(y)].                    (4)
```

Thus a geometry-induced one-point modulation can create an apparent pair curve relative to
mask/selection randoms that intentionally do not contain that physical modulation. The curve is the
binwise autocorrelation of `m`; it is not an irreducible two-source effect.

The exact finite witness has

```text
p=(1/2,1/3,1/6),
q=(1/3,1/3,1/3),
```

and returns the nonzero matrix `(p-q)(p-q)^T`. If `q` is replaced by `p`, it returns zero.

This result does not authorize treating an observational selection defect as UDT. The official
randoms retain their frozen footprint, completeness, and registered selection roles. A future
physical `m` must be derived from one complete history and distinguished from survey systematics.

## 5. The true connected kaleidoscope

A general two-source operator can be written

```text
K_2=K_1 tensor K_1 + H,                         (5)
```

where `H` is the connected pair response. Under the null source,

```text
C_obs=H[lambda tensor lambda].                  (6)
```

Equation (6) is the broad kaleidoscope home. It may arise from connected complete-pair data without
literal duplicate images. Current overlap and joint-Gram equations constrain which simultaneous
relations are legal, but they do not supply a probability kernel `H` or select its history.

### 5.1 Correlated multi-image construction

Multiple branches give one exact constructive subtype. Let one Poisson parent at `a` produce the
random image measure

```text
M_a=sum_b I_b(a) delta_{Psi_b(a)}.
```

Its observed intensity is

```text
nu_1(dx)=integral E[M_a(dx)] lambda(da).
```

The factorial second measure is

```text
nu_2(dx,dy)
 =nu_1(dx)nu_1(dy)
  +integral E[M_a^[2](dx,dy)] lambda(da),        (7)
```

where `M_a^[2]` contains distinct image pairs from the same parent. Hence

```text
C_branch
 =integral sum_(b!=c) E[I_b I_c]
    delta_(Psi_b(a),Psi_c(a)) lambda(da).        (8)
```

If each parent independently chooses exactly one branch, `M_a^[2]=0` and the output is again a
simple-lens null. If jointly retained branches exist, equation (8) is nonzero and its angular shape
is the pushforward of `lambda` by the relative branch maps.

The exact three-cell witness independently reconstructs a nonzero symmetric connected matrix.

## 6. What the complete metric currently owns

The frozen sources establish:

- `G102`: supplied branch maps and source/branch measures can be evaluated;
- `G103`: regular local zero- and first-jet data remain surjective after releasing `J`;
- complete overlap: shared clocks, transitions, and joint Gram data must be compatible;
- current global/history evidence: flat, monotone, and loud--quiet--loud continuations survive;
- G99: one conditional middle-regime endpoint coordinate is frozen observationally.

They do not establish:

- a physical one-point modulation field `m`;
- a nonzero connected operator `H`;
- a multi-image branch family, joint visibility, or branch weights;
- a global history producing any of those objects;
- a regime evolution function for a connected mode.

Therefore the complete metric currently **permits** kaleidoscope channels but does not yet **own**
the nonfactorizing score that makes them physical.

## 7. Coefficient disposition

The preregistered coefficient budget does not become fitting freedom merely because the algebra has
named possible homes:

| coefficient | disposition | exact reason |
|---|---|---|
| `a_conn` | `DORMANT` | `H` is typed but no physical nonzero mode is selected |
| `a_branch` | `DORMANT` | equation (8) is conditional; branch maps and joint weights are unowned |
| `a_area` | `DORMANT` | equation (4) is exact; no physical modulation field `m` is owned |
| `a_regime` | `DORMANT` | no active base mode has an owned continuation |

No two-to-four-parameter BOSS curve family is therefore scientifically available yet. Activating a
coefficient now would hide the missing geometry inside a fit.

## 8. Exact next joint

The smallest unresolved geometric question is no longer “can a smooth lens distort a sky?” It is:

```text
Does one complete UDT history derive either
  (a) a physical one-point density modulation m relative to survey selection, or
  (b) a nonfactorizing connected pair/branch operator H?
```

That question belongs to global relation-family assembly, critical/branch structure, or a joint
history-query rule. Bootstrap could later constrain it but remains inactive here.

## 9. Evidence

Production SymPy checks pass for the factorized null, exact Landy--Szalay mismatch identity, full
selection null, independent branch null, multi-image connected term, and general `H` recovery. A
separate standard-library Fraction implementation uses different inputs and imports no production
code. Twelve hostile mutations are caught. No BOSS or CMB outcome artifact is read.

## 10. Maximum conclusion

The kaleidoscope hypothesis has been sharpened, not rejected. UDT can produce an apparent pattern
from plain sources only if the complete observer relation contains more than independent per-source
distortion or if a genuine physical one-point modulation is deliberately absent from the survey
selection reference. The existing metric record does not yet select either nonzero field, so the
observational coefficient family must remain dormant.
