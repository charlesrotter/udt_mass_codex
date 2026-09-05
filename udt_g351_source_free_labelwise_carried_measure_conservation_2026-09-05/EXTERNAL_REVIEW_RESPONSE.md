# External G351 adversarial review

Date: 2026-09-05
Review mode: fresh, sealed-intake-only, no network, no repository or protected-package access

## Executive finding

The exact bounded mathematical claim is correct, provided “measure” has its standard measure-theoretic meaning of a countably additive nonnegative measure and the regular-cut statement is confined to the nonzero absolutely continuous component. The conservation premise itself is not derived. It supplies a cut-independent measure on labels; the inverse-area density law is then a Radon–Nikodym consequence. In G350's deliberately chosen full independent positive character domain, the two coordinate directions separately force the frequency exponent to equal the already-declared observer weight and the area exponent to be `-1`. They do not choose the observer weight.

The singular and caustic qualifications are essential and are now stated correctly. A finite conserved label measure can lack an ordinary area density even on regular cuts, and a regular density can diverge or become singular under rank loss while the label measure and its pushforward remain finite. Multiplicity is retained by preimages under pushforward; geometric image-union area is not a substitute and no detector or cross-label composition law follows.

The registered replay and sealed-package integrity checks pass. Those checks are useful regression evidence, not the analytic proof. Several checks are tautological, text-token based, or implementation-distinct without being proof-independent. The claimed preregistration chronology is documentary rather than cryptographically time-authenticated. These are evidence-grade limitations, but they do not defeat the independently reconstructed bounded theorem.

## 1. Intake authentication and handling

Before substantive inspection or execution, I copied the complete mounted intake to:

```text
/work/g351-review-copy.AF5nwK
```

The sealed `/intake` was not edited. All execution occurred in the `/work` copy.

Authentication results:

- `REVIEW_MANIFEST.sha256` authenticates the supplied `REVIEW_MANIFEST.tsv`: its declared manifest digest is `47db44c00d8d6ea7cb882bcafb0239cd86d4b732e719c2dedf07d39e98edde01`, and `sha256sum` returned `OK`.
- The manifest contains 42 payload rows. Every payload exists and matches both its declared byte count and SHA-256 digest.
- `REVIEW_SCOPE.json` declares 42 payloads, contains 42 distinct paths, and agrees exactly with the manifest in both order and set.
- The mounted intake contains exactly 44 regular files: the 42 payloads, `REVIEW_MANIFEST.tsv`, and `REVIEW_MANIFEST.sha256`. There are no undeclared files, missing files, symlinks, or special filesystem entries.
- The `/work` copy initially had the exact same file set and payload digests. After replay it still matched all 44 sealed files by size and SHA-256, and contained no bytecode.
- The four frozen initial-preregistration hashes and all five frozen source hashes match the corresponding sealed payloads.

This establishes internal byte consistency relative to the supplied digest root. It does not turn the co-sealed unsigned checksum into a trusted signature, remote receipt, or external timestamp.

## 2. Independent analytic reconstruction

### 2.1 Regular absolutely continuous density

On a two-dimensional regular label chart, let `dλ` be coordinate Lebesgue measure. Pull the metric sheet-area measure at cut `i` back to label space:

```text
dα_i = J_i dλ,    J_i > 0.
```

Because `J_i` is finite and strictly positive on the regular stratum, `α_i` and `λ` are mutually absolutely continuous. Decompose the finite conserved label measure by Lebesgue decomposition:

```text
μ = μ_ac + μ_s,
dμ_ac = s dλ,
μ_s ⟂ λ.
```

The same singular part is singular relative to every regular `α_i`. The Radon–Nikodym derivative of only the absolutely continuous part is

```text
n_i = dμ_ac/dα_i = s/J_i.
```

For two regular cuts,

```text
A_ji = J_j/J_i,
n_j = s/J_j = (J_i/J_j)n_i = A_ji^-1 n_i                 (1)
```

almost everywhere. Equation (1), not a density ratio, is the universally valid form. On the support where `n_i` is nonzero it is equivalent to `n_j/n_i=A_ji^-1`. This proves the area weight of a nonzero absolutely continuous regular-density component is `q=-1`, conditional on the conserved-label-measure premise.

This result is chart invariant: both `s` and `J_i` acquire the same coordinate Jacobian, so `s/J_i` does not.

### 2.2 Frequency weight and the G350 character domain

The bare density `n_i` is observer-neutral. A frequency exponent appears only after declaring a readout type. With one arbitrary fixed positive reference frequency `ω_*`, define a component of declared observer weight `p` by

```text
C_i = (ω_i/ω_*)^p n_i.
```

Then (1) gives

```text
C_j/C_i = (ω_j/ω_i)^p (J_i/J_j)
        = R_ji^p A_ji^-1.                                (2)
```

The common `ω_*` makes arbitrary real powers dimensionless and cancels from every transfer ratio. It is a mathematical reference, not a selected physical scale.

To test uniqueness without assuming the answer, take the general G350 character

```text
T(R,A)=R^a A^q
```

and require the observer-weight-stripped sheet measure to be conserved. The residual multiplier is

```text
R^(a-p) A^(q+1).
```

G350's registered character problem quantifies over the full abstract domain of independent positive `(R,A)`. Setting `A=1` and varying `R>0` forces `a=p`; setting `R=1` and varying `A>0` forces `q=-1`. Conversely `(a,q)=(p,-1)` makes the residual identically one. Thus `q` is uniquely fixed inside that declared class, while `p` remains whichever observer representation type was supplied.

This does not assert that one metric history realizes every positive pair. It uses G350's abstract classification domain. On a smaller realized subgroup, uniqueness could weaken. It also does not rule out G350's broader endpoint coboundaries, nonlocal laws, field-valued transfers, or other classes outside the bounded two-ratio character problem.

There is no covert derivation of `p`: multiplying an observer-neutral density by `(ω/ω_*)^p` defines a typed readout. Conservation neither requires that a physical readout exist nor selects its type.

## 3. Algebraic and covariance claims

For three cuts, the metric ratios obey

```text
R_ki=R_kj R_ji,    A_ki=A_kj A_ji.
```

Therefore `T_ki^(p)=T_kj^(p)T_ji^(p)`. At identity, `(R,A)=(1,1)` and `T=1`. Reversal replaces both ratios by their inverses and hence replaces `T` by `T^-1`. These are exact character identities and introduce no new physics.

For independent finite endpoint-observer changes `ω_i -> D_iω_i`, the ratio transforms as

```text
R_ji -> (D_j/D_i)R_ji.
```

Assigning the already-declared component type `C_i -> D_i^p C_i` makes (2) covariant and leaves `C_iJ_i/(ω_i/ω_*)^p` unchanged. Covariance verifies a chosen representation weight; it does not select one. Demanding an observer-invariant component would be the additional choice `p=0`, not a consequence made in G351.

## 4. Singular counterexample and the R1 repair

Take the in-domain two-dimensional label chart `[0,1]^2`, regular constant Jacobians `J_i=1` and `J_j=2`, and

```text
μ = δ_(1/2,1/2).
```

The singleton has zero `α_i`- and `α_j`-area but `μ`-mass one. If an ordinary density `h` represented `μ`, then

```text
1 = μ({point}) = ∫_{point} h dα_i = 0,
```

which is impossible. Allowing `h=∞` on the singleton does not help: a nonnegative Lebesgue integral over a null set is still zero. Thus the full finite measure need not possess an ordinary area density, and its singular component has no ordinary density exponent `q`.

The original scope was therefore overbroad. R1 correctly repaired it by:

- applying the density theorem only to `μ_ac`;
- retaining `μ_s` as a measure without an ordinary exponent;
- replacing a universal ratio by the division-free equality (1);
- observing that an identically zero component remains zero but supplies no exponent witness.

R2 correctly changed `dμ/dArea` to `dμ_ac/dArea` and retained the dimensionless frequency reference. R3 correctly moved the atom from a one-dimensional shorthand into the two-dimensional screen-label chart. These repairs are mathematically substantive in precision but do not change the repaired theorem.

The executable atomic checks test selected finite candidate densities and then report a hard-coded scope field. They do not prove nonexistence of every Radon–Nikodym density. The singleton null-set argument above is the proof.

## 5. Caustics, pushforward, and multiplicity

For any supplied measurable cut map `X_i`, the pushforward is

```text
(X_i)_*μ(B)=μ(X_i^-1(B)).
```

If `μ` is finite, the pushforward is finite regardless of the differential rank of `X_i`. Rank loss can nevertheless destroy absolute continuity with respect to two-dimensional image area.

An explicit limiting witness is `X_t(x,y)=(tx,ty)` on the unit label square with uniform label measure. For `t>0`, `J_t=t^2` and the image-area density is `t^-2`; it diverges as `t -> 0`. At `t=0`, the pushforward is a finite unit atom at the origin. The finite measure survives while an everywhere-finite inverse-area density does not. G351 claims only the former.

If two labels `λ_1,λ_2` with masses `m_1,m_2` map to the same endpoint `y`, then

```text
(X_*μ)({y}) = m_1+m_2
```

for that atomic example. On regular overlapping sheets, the pushforward density analogously sums sheet contributions over preimages. The geometric image union counts the image location once and therefore cannot recover the carried label measure. This is mathematical preimage accounting, not a selected rule for detector resolution, incoherent addition, cancellation, phase, or interference.

The pointwise formula `n=s/J` belongs to the labelled regular sheet. At a globally many-to-one image it must not be confused with a single-sheet-free density on the geometric union; that image density, when it exists, includes the preimage sum. The package preserves this distinction.

## 6. Scope and hidden-physics audit

I found no covert selection of:

- a nonzero source magnitude or angular/source distribution;
- populated labels or path probabilities;
- `p`;
- cross-label physical aggregation, phase, or interference;
- emission, absorption, light, photon, energy, flux, luminosity, detector response, or observational distance;
- metric history, occupancy, topology, matter model, mass, physical scale, `X_max`, or canon.

The homogeneous law sends zero measure to zero measure. It cannot populate labels or create content. Nonzero `μ` and its support remain supplied data. “Source-free” is entirely part of the owner-adopted conservation premise; it is not derived from the metric, reciprocity, or a field equation.

The supplied G348/G349 records retain rank strata and distinguish multiplicity-weighted sheet area from image-union area. The supplied G350 record retains the full abstract character domain and explicitly says inverse area requires a new conservation premise. The five frozen upstream/source digests match their sealed files. The current registry's G312, G348, G349, and G350 rows retain their prior metric, reciprocal-kernel, angular-sector, and bounded-response boundaries. G351 adds no replacement metric, kernel, angular equation, or response equation.

That last conclusion is necessarily intake-relative: repository access was forbidden, so I verified non-alteration against the sealed frozen sources and registry, not against an external live repository state.

## 7. Registered replay

I ran the registered aggregate from the copied G351 directory with:

```text
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_package.py
```

It exited zero and reproduced:

- aggregate: `45/45`;
- production exact arithmetic: `60,325/60,325`;
- implementation-distinct arithmetic: `11,290/11,290`;
- hostile mutations: `12/12` caught;
- saved production, independent, hostile, and aggregate JSON exactly;
- frozen preregistration and source hashes;
- package-builder containment and registered-command guards.

An external snapshot around the replay covered all 36 G351 package files. Before and after snapshots were identical in file count, path-set digest, content digest, and a size/mtime/ctime/mode digest; bytecode count remained zero. A second full-copy comparison showed all 44 copied intake files still byte-identical to `/intake` and no added files.

The replay used only the system standard library under `-S`. Direct source inspection found no dynamic import, socket, HTTP, package-manager, download, or network-capable call. `verify_package.py` invokes only the three fixed local child scripts. The builder can write a new package under `/tmp`, but the registered aggregate parses it and does not execute it.

## 8. Evidence-integrity attacks and grading

### Analytic proof versus regression evidence

- The analytic Radon–Nikodym argument and the two independent character-coordinate probes prove the bounded theorem.
- Production constructs `c_i=pw_i-j_i+σ` and then checks identities that largely follow by substitution. Its large assertion count demonstrates exact arithmetic execution and regression coverage, not independent discovery.
- The implementation-distinct verifier imports no production module and reads no production result. That is genuine code independence. It still instantiates the same proposed formula `px-y`, so it is not proof-independent and cannot replace the analytic derivation.
- The finite caustic loops show exact conservation and monotone density growth over a finite grid; analytic limiting reasoning is needed for unboundedness and the rank-loss statement.
- The multiplicity executable check is only positivity of `s1+s2`, not an implementation of a pushforward or area formula. The measure-theoretic preimage argument is load-bearing.
- The 12 hostile checks explicitly flip fields in a baseline dictionary and test corresponding conditions. The wrong-coefficient witnesses have mathematical content; most other catches are contract/semantic regression guards, not searches over documents or theories.
- Many aggregate gates are substring checks. They establish that expected phrases and saved states are present, not that the prose is true.

### Circularity and vacuity

No circularity infects the independent analytic proof. There is substantial circularity if the executable counts are advertised as that proof: proposed formulas are constructed and then algebraically rechecked; several result fields are literal constants; semantic mutations are rejected by validators written to reject those exact Boolean changes. The package mostly acknowledges this by calling the arithmetic routes witnesses and regression guards. The audit should continue to preserve that grading.

### Preregistration and provenance

The four initial preregistration files match `FROZEN_PREREGISTRATION_HASHES.tsv`, and the five declared sources match `FROZEN_SOURCE_HASHES.tsv`. No internal alteration or stale-file mismatch is present relative to those tables.

However, the hash tables, Git narrative, payloads, and manifest are all co-sealed. `GIT_PREREGISTRATION_PROOF.txt` is documentary text, not a verifiable Git object graph, signed attestation, remote receipt, or trusted timestamp. The aggregate's `preregistered_before_outcomes` gate merely finds a commit string in prose. Its R1–R5 preregistration gates similarly confirm titles and selected phrases, not chronology. Because repository access was prohibited, I cannot independently establish that commit `42e48241` was pushed before execution, that repair files predated repair runs, or that the frozen sources are current relative to an external repository. These claims must be graded as documentary provenance.

This limitation is not a reason to reject the theorem because the result has been independently proved from the stated assumptions here. It would be a reason to reject any stronger claim of cryptographically authenticated outcome-unseen chronology.

### No-write and dependency limits

The package's internal no-write check covers G351 package bytes and omits bytecode from its digest; its separate no-bytecode gate closes the latter gap at completion. My external snapshot additionally covered metadata and the entire copied intake. Neither method can rule out a hypothetical transient write restored before the after-snapshot or writes to arbitrary external paths. Direct source inspection found no such behavior, and the actual registered replay left no observed change.

The static standard-library audit is bounded: `subprocess` is allowed and static import inspection cannot generally exclude every runtime effect. In these exact sealed scripts the subprocess targets are fixed local Python files and no network path is present.

## 9. Boundary conditions on acceptance

The accepted statement means only:

1. `μ` is a standard finite nonnegative countably additive measure on the supplied measurable label space and is assumed unchanged between the relevant source-free cuts.
2. `q=-1` applies only to a nonzero absolutely continuous density on the regular positive-Jacobian stratum.
3. Zero density obeys the division-free law but does not identify an exponent.
4. Singular content has no ordinary area-density exponent.
5. `p` is an arbitrary declared observer type for a readout, not a selected physical value.
6. The character uniqueness is relative to G350's full independent positive abstract `(R,A)` class.
7. Through caustics, the finite label measure and its measurable pushforward survive; an everywhere-finite inverse-area scalar does not.
8. Pushforward retains preimage contribution/multiplicity mathematically; no physical cross-label law follows.
9. The owner-adopted conservation premise remains provisional, non-derived, and non-canonical.

If “additive” were intended to mean merely finitely additive rather than the standard countably additive meaning of “measure,” the invoked Lebesgue decomposition and Radon–Nikodym theorem would not follow in this generality. The package's terminology and proof machinery clearly use the standard meaning; no wider finitely additive claim is accepted.

No value of `p`, source, population, cross-label physics, light transfer, distance, history, scale, `X_max`, matter model, or canon is selected by this review.

ACCEPT_G351_BOUNDED_CARRIED_MEASURE_CONSERVATION
