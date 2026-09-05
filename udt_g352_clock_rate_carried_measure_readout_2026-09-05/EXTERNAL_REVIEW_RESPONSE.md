# External G352 adversarial review

Date: 2026-09-05  
Review mode: fresh, sealed-intake-only, no network, no repository or protected-package access

## Executive finding

The regular-cut algebra is correct after conditioning on a suitably defined **continuous phase-count intensity** and on a phase-independent copy of G351's label measure. In that repaired model,

\[
\Gamma_i={\omega_i\over\Delta\Theta}{s\over J_i},
\qquad
{\Gamma_j\over\Gamma_i}=R_{ji}A_{ji}^{-1},
\]

on nonzero absolutely continuous regular support. The pair `(p,q)=(1,-1)` is then unique only in G350's declared full independent positive character domain and only for this typed readout. The `p=0` G351 density and other readout types remain distinct. Observer covariance, common positive phase scaling, identity, algebraic reversal, sewing, and the frequency-integrable pushforward statement all close within their stated domains.

The package nevertheless needs repair. A literal fixed-increment **discrete sequence** does not have the ordinary instantaneous counting rate `omega/DeltaTheta`; its proper-time counting measure is atomic. The smooth expression is instead the density of total phase variation, an averaged/random-offset event intensity, or a continuously interpolated phase-count coordinate. Those are additional assumptions. Moreover, with the package's chosen future orientation, `dTheta/dtau=-omega`, so the displayed alleged nonnegative product measure

```text
dXi=(dTheta/DeltaTheta)dmu
```

has the unrepaired orientation sign. It must use the total-variation phase measure, or be replaced by an explicitly atomic level-counting measure. R1 correctly repaired the scalar rate but did not repair this product-measure formula. These defects do not invalidate the conditional `R A^-1` algebra; they prevent acceptance of the current claim that an unqualified supplied fixed-increment sequence itself yields the displayed smooth positive crossing measure.

## 1. Intake authentication and handling

Before substantive review or execution, I copied the complete mounted intake to:

```text
/work/g352_external_review.s7PAhk
```

The sealed `/intake` was not edited. All registered execution occurred inside the copied G352 directory.

Authentication results:

- `REVIEW_MANIFEST.sha256` validates `REVIEW_MANIFEST.tsv`. The manifest digest is `bc8247c6fdaa6c6a50762a092f457475b5efa288571d0ab8fba8c5500004e29d`.
- The manifest has 36 payload rows. `REVIEW_SCOPE.json` declares 36 payloads and lists 36 paths. Its list, the manifest paths, and the actual payload file set agree exactly.
- Every one of the 36 payloads matches both its declared byte count and SHA-256 digest. The authenticated scope payload has digest `90458838b1f95c1d8e370331199a65eae2cf71c47af2e8e5062ff69b9d6db2e1`.
- The full intake has exactly 38 regular files: the 36 payloads plus `REVIEW_MANIFEST.tsv` and `REVIEW_MANIFEST.sha256`. There are no symlinks or special filesystem entries.
- A recursive comparison showed that the initial `/work` copy was byte-identical to `/intake`.
- After all registered checks, the copy still had exactly 38 files, remained byte-identical to `/intake`, and contained no `.pyc` files.

This authenticates internal byte consistency relative to the co-sealed manifest digest. The unsigned checksum, scope, Git narrative, and payloads were supplied together, so they do not establish an external signature, trusted timestamp, or independently authenticated preregistration chronology.

## 2. Independent reconstruction of the bounded claim

The usable mathematical data are:

1. a smooth time-oriented Lorentzian metric of signature `(-,+,+,+)`;
2. a nonzero supplied null phase covector `k_a=nabla_a Theta`, with its raised vector future-directed;
3. future unit timelike observer tangents `u_i` and `omega_i=-u_i^a k_a>0`;
4. a common fixed `DeltaTheta>0`;
5. G351's finite nonnegative countably additive label measure `mu`, unchanged between the relevant cuts;
6. on a regular label chart, `dmu_ac=s dlambda` and `dArea_i=J_i dlambda`, with `J_i>0`;
7. the additional factorization that the same label measure is attached independently of phase.

For any observer worldline tangent to `u_i`,

\[
{d\Theta\over d\tau_i}=u_i^a\nabla_a\Theta=u_i^ak_a=-\omega_i.
\]

If the readout is explicitly defined using continuous total phase variation, its positive local intensity is

\[
\rho_i={|d\Theta/d\tau_i|\over\Delta\Theta}
       ={\omega_i\over\Delta\Theta}.
\]

Multiplication by the regular G351 density gives

\[
\Gamma_i=\rho_i{d\mu_{\rm ac}\over dA_i}
        ={\omega_i\over\Delta\Theta}{s\over J_i}.
\]

For the same retained label and common nonzero `s`,

\[
{\Gamma_j\over\Gamma_i}
= {\omega_j\over\omega_i}{J_i\over J_j}
=R_{ji}A_{ji}^{-1}.
\]

The division-free statement `Gamma_j=R_ji A_ji^-1 Gamma_i` also preserves zero density, but zero cannot witness exponents. A singular component of `mu` has no ordinary regular area density and is not covered by this pointwise formula.

## 3. Phase sign and R1

R1 correctly identifies the frozen preregistration's sign error. With the supplied orientation, `omega=dTheta/dtau>0` is false and `dTheta/dtau=-omega` is correct. Taking an absolute value gives a positive phase-variation rate.

Two qualifications remain:

- R1's statement that one may “equivalently” replace `Theta` by `-Theta` is not literally within the same convention: that replacement makes the raised gradient past-directed and makes `-u.k` negative unless the orientation convention or frequency definition is also changed. The positive-rescaling argument used later avoids this problem.
- Equation (3) in `EXACT_DERIVATION.md` still uses signed `dTheta`, even though it calls `Xi` a crossing measure built from nonnegative `mu`. Along every included future timelike worldline, this signed factor is negative. R1 therefore repairs equation (2) but not equation (3).

The nonnegative continuous version should be written as a product of measures, for example

\[
d\Xi={|d\Theta|\over\Delta\Theta}\otimes d\mu,
\]

with the product measurable structure stated. If orientation is intended, `Xi` is a signed measure and must not be called the positive crossing count.

## 4. A fixed-increment sequence versus a smooth rate

Let the actual supplied sheets be the discrete phase levels `Theta_n=Theta_0-n DeltaTheta`, and let `tau_n` be their intersections with an observer worldline. Nonzero future-null `k` and future timelike `u` imply `u.k<0`, so the intersections are transverse and locally ordered whenever the relevant phase levels lie in the worldline's phase range. This part holds for every finite future unit timelike observer; the excluded null limit need not be regular.

The literal count is nevertheless a step function,

\[
N(\tau)=\#\{n:\tau_n\leq\tau\},
\]

and its distributional derivative is the atomic measure

\[
dN=\sum_n\delta_{\tau_n}.
\]

It is not the ordinary function `omega(tau)/DeltaTheta`. Over a finite interval, the integer crossing count differs from total phase variation divided by `DeltaTheta` by endpoint/floor terms of less than one crossing. Between crossings its classical derivative is zero, and at a crossing it is not finite.

Thus `omega/DeltaTheta` is exact only after choosing one of the following meanings:

- the continuous phase-count coordinate `N_cont=-Theta/DeltaTheta` and its total-variation rate;
- a phase-averaged or random-offset expected count intensity;
- an asymptotic/coarse-grained rate with endpoint discrepancies discarded.

Alternatively, literal crossings require the phase-space counting measure

\[
\left(\sum_n\delta_{\Theta_n}\right)\otimes\mu,
\]

whose observer-time image is atomic. The package does not make this choice. Calling equation (2) the exact rate of a discrete fixed-increment sequence is therefore overbroad.

An endpoint observer vector by itself also does not supply a global observer worldline or guarantee that a specified finite set of levels lies in its phase range. It does determine the local phase derivative for every worldline extension with that tangent, which is all that the repaired local intensity needs.

## 5. Hidden assumptions in the product crossing measure

The factorization of a phase-label measure is not forced by G351 and does more work than the adoption sentence states. It requires at least:

1. a declared measurable phase domain and product sigma-algebra with the label space;
2. a choice between total-variation phase measure and atomic level-counting measure;
3. a common globally fixed positive spacing, independent of phase, label, and cut;
4. the same `mu` on every phase slice, so the label measure per crossing is phase-independent;
5. no phase-label correlation, phase-dependent support, or modulation;
6. factorization rather than a general measure `Xi(dTheta,dlambda)` or a family `mu_Theta`;
7. label-preserving comparison across cuts and no extra weights attached to individual phase levels;
8. measurability of every cut map and of the observer-frequency weight used later.

The G352 prose acknowledges that a phase-dependent profile would replace the product form, but acknowledgement is not derivation. The owner adoption record defines a readout on a “supplied conserved sequence”; it does not explicitly adopt the same full G351 measure independently at every phase level or choose continuous instead of atomic counting. Those conditions must be promoted to clearly labelled provisional premises. They must not be presented as a representation automatically implied by a fixed-increment sequence.

## 6. Character uniqueness and non-universality

Given the repaired intensity definition, the character calculation is sound. For a general G350 character `R^a A^q`, equality with `R A^-1` for every independent positive `(R,A)` gives

\[
R^{a-1}A^{q+1}=1.
\]

Taking `A=1` and varying `R>0` forces `a=1`; taking `R=1` and varying `A>0` forces `q=-1`. This is uniqueness only:

- in G350's full abstract independent positive domain;
- among its continuous positive multiplicative two-ratio characters;
- for the repaired clock-rate intensity readout.

It is not uniqueness on an arbitrary smaller set of ratio pairs realized by one geometry. Correlations such as `A=R^c` can leave only one linear constraint on `(a,q)`. It also does not cover G350's endpoint coboundaries, nonlocal rules, or field-valued laws.

No universal frequency exponent is selected. The observer-neutral G351 density remains a distinct `p=0` readout. Other declared observer types remain mathematically different and open. The package is correct on this point.

## 7. Normalization, observer covariance, identity, reversal, and sewing

These checks close with precise boundaries:

- Under one common positive affine rescaling `Theta -> b Theta` and `DeltaTheta -> b DeltaTheta`, `omega/DeltaTheta` and `Gamma` are invariant. A phase translation is also harmless. A general nonlinear reparameterization does not preserve fixed increments and is not covered.
- Under independent finite endpoint observer changes `omega_i -> D_i omega_i`, with `D_i>0`, the intrinsic sheet Jacobian is unchanged and `Gamma_i -> D_i Gamma_i`. Consequently `T_ji -> (D_j/D_i)T_ji`. This verifies observer weight one for the already-defined readout; it does not select a preferred observer.
- On a common regular retained label, frequency and area ratios are cocycles. Therefore identity, reciprocal comparison, and three-cut sewing follow exactly.
- Comparison reversal is algebraic. It does not construct a reversed causal process.

All of these conclusions presuppose common phase normalization and spacing, the same factored label measure, positive regular Jacobians at the compared cuts, and nonzero density if a ratio of `Gamma` values is written.

## 8. Caustic and weighted-pushforward statement

Define

\[
w_i(\lambda)={\omega_i(\lambda)\over\Delta\Theta},
\qquad
\nu_i=(X_i)_*(w_i\mu).
\]

For measurable nonnegative `w_i`, `nu_i` is finite exactly when

\[
\int_\Lambda w_i\,d\mu<\infty.
\]

Pointwise finiteness of every observer and finiteness of `mu` do not by themselves imply this integrability; `w_i` may be unbounded across the retained label patch. The package states the integrability condition, and it is essential.

Rank loss or many-to-one mapping does not prevent the pushforward from being a finite measure under that condition. It does not imply absolute continuity with respect to two-dimensional image area, a finite ordinary density, or a pointwise continuation of `A^-1` through `J=0`. On a regular labelled sheet, the absolutely continuous density is `w_i s/J_i`; on a many-to-one image, an image density, when it exists, includes a preimage sum. At a caustic it can diverge or acquire a singular part while `nu_i` remains finite.

This measure statement survives the phase-count repair if `w_i` is explicitly the continuous phase intensity. For literal atomic crossings, the relevant object is instead a measure on observer time and endpoint image; no everywhere-smooth instantaneous `Gamma_i` follows.

## 9. Forbidden-import audit

I searched the copied G352 materials for the prohibited interpretation terms and inspected their contexts. They occur in exclusion clauses, premise boundaries, upstream scope statements, filenames/status prose, and hard-coded negative regression fields. I found no affirmative mathematical dependency that assigns any prohibited physical identity or imports any detector rule, observational law, nonzero generating mechanism, metric history, matter model, absolute scale, `X_max`, or canonical status.

Two rhetorical phrases—“UDT's clock-first interpretation” in the lay report and references to an unchanged provisional response equation—are not used in the derivation. They should remain rhetoric only and cannot strengthen the bounded mathematical result.

The scripts use only Python's standard library. The only subprocess use is in `verify_package.py`, which invokes the three fixed local registered scripts with `-B -S` and no-write environment variables. Direct inspection found no socket, HTTP, download, package-manager, dynamic-import, or network-capable call. The intake builder can write a new `/tmp` tree, but it was not a registered check and was not run.

## 10. Registered replay and evidence grading

I ran exactly the four commands registered in `COMMANDS.md`, from the copied G352 package, with `UDT_NO_WRITE=1`, `PYTHONDONTWRITEBYTECODE=1`, and `python3 -B -S`. All exited zero and reproduced the saved results:

- production: `96,444/96,444` assertions;
- implementation-distinct additive route: `73,887/73,887` assertions;
- semantic mutations: `13/13` rejected;
- aggregate: `36/36` gates.

These are regression results, not proof of the phase-count premise or the measure construction.

### Production route

The 2,400 advertised cases are generated entirely by indices modulo 9, so they contain only 9 distinct base data states, repeated many times. Most assertions substitute the proposed definitions of `gamma` and `transfer` back into identities. The sign witness sets `phase_derivative=-omega` and checks `abs(-omega)=omega`; it confirms the coded convention but does not reconstruct Lorentzian orientation. The coefficient grid is finite and cannot prove uniqueness for all real exponents. The 160 caustic steps prove 160 exact equalities and strict increases; unboundedness needs the analytic continuation `J_n=1/n^2` for arbitrary `n`. The many-to-one test is a useful explicit finite sum, not a general pushforward theorem. Several scientific result booleans are literal constants.

### Implementation-distinct route

The 2,700 advertised cases are determined modulo 19, so they contain only 19 distinct base coordinate states. The route is implementation-distinct in the limited sense that it imports no production module and reads no production result. It still constructs `log Gamma=x-y+sigma-d` and verifies consequences of that same ansatz. Its finite coefficient grid and finite caustic sequence do not establish functional-equation completeness or a limiting measure theorem.

### Hostile and aggregate routes

The hostile program mutates 13 fields in a baseline dictionary and uses a validator written to reject those exact changes. It is an honest semantic regression guard, as its saved result says, but it does not search for covert assumptions or test the discrete/continuous crossing distinction. The aggregate usefully verifies required files, frozen hashes, child no-write behavior, saved-output equality, and selected fields. Several gates are substring or hard-coded-result assertions. They show expected text and values are present, not that the text is mathematically true.

The aggregate's internal snapshot covers package file paths, sizes, and content hashes, not all metadata, transient writes, or arbitrary external paths. My external post-run recursive comparison covers the entire copied intake at completion and found no change. Direct source inspection found no attempted out-of-scope write in the registered paths.

### Provenance

The frozen preregistration and source hashes match the sealed files. `GIT_PREREGISTRATION_PROOF.txt` explicitly concedes that it is documentary. No Git objects, signed attestations, remote receipts, or trusted timestamps were available or permitted, so the claimed outcome-unseen commit/push chronology cannot be independently authenticated from this intake.

## 11. Required repair and narrowest defensible landing

No new scientific question is needed. The smallest repair is:

1. choose explicitly between literal atomic crossings and a continuous/averaged phase-count intensity;
2. if retaining `Gamma_i` as an ordinary local density, define it using the nonnegative total-variation phase measure `|dTheta|/DeltaTheta`, not the derivative of a discrete step count;
3. replace signed equation (3) by an actual nonnegative product-measure definition, including the product sigma-algebra;
4. state as an owner-adopted provisional premise that the same G351 label measure is attached independently to every phase increment, with no phase-label correlation or phase-dependent weighting;
5. confine the ratio formula to nonzero absolutely continuous regular support and retain the weighted pushforward only under measurability and frequency integrability;
6. preserve the current boundaries: `(p,q)=(1,-1)` only for this repaired readout in G350's full abstract character domain, with `p=0` and all other readout types still open.

After those repairs, the defensible conditional conclusion is exactly that the continuous phase-count clock-rate density transfers by `R A^-1`, is observer weight one, is invariant under common positive phase scaling, sews and reverses algebraically on regular cuts, and has a finite measure-valued caustic formulation only under frequency integrability. The current unqualified fixed-increment-sequence and product-measure formulation is not yet acceptable.

REPAIR_G352_BOUNDED_CLOCK_RATE_READOUT
