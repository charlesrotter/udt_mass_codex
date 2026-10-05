# Exact derivation — P4 Route B Stage 1: extension-stratum classification

Date: 2026-07-28. Branch: `p4-routeB`. Contract: `PREREGISTRATION.md` in this package
(frozen question §1, layers C1–C4, targets T1–T6, falsifiers F-A..F-E, ceiling §5).
Machine record: `derive_routeB_stage1.py` → `DERIVATION_RESULT.json` /
`DERIVATION_STDOUT.txt` — **47 checks, all zero-residual/exact-solve SymPy passes,
exit 0, runtime < 1 s**. Check names below in `[brackets]` refer to that JSON.

Banked inputs (CITED, cross-checked only, never re-derived): the 07-26 selector audit
(zero active selector rank; scalar-only centralizer/equivariance correction), the 07-27
metric-natural extension audit (conditional ±1 forcing; swap→λ=0 diagonal-only), the
07-28 joint no-go (so(1,3) perfect; centralizer dims 1/3/3/1), the 07-27 rank-closure
audit (orbit metric; V_q exponent 1+2λ), the 07-28 J-obligations TSV, and the 07-25
E02 extension-class package (parametrization reused verbatim).

## 0. Conventions and representation (the T1 representation-care clause)

- Coframe = COLUMN `e` of 4 one-forms, slots (clock, ruler, screen1, screen2) =
  indices (0,1,2,3); `eta = diag(-1,1,1,1)`.
- Extension operation: `e -> exp(phi X) e` (left multiplication), with
  `X = [[H,0],[C,K]]`, `H = diag(-1,+1)` fixed (G01/G02), `K = [[a,b],[0,d]]`
  (registered triangular chart), `C` the 2×2 mixing block. E07 = `diag(-1,+1,-k,+k)`;
  E08 = lower shift `s(1-e^{-phi})` — conventions byte-compatible with
  `udt_founded_phi_complete_coframe_extension_audit_2026-07-25/derive_extension_class.py`.
- Local Lorentz gauge: `e -> L e`, `L ∈ SO+(1,3)` connected; the SAME physical
  operation in the new gauge is `X -> L X L^{-1}`, infinitesimally
  `delta_lam X = [lam, X]` (adjoint in the defining representation). Gauge basis
  ordered `(B01, B02, B03, R12, R13, R23)` (boosts symmetric, rotations antisymmetric).
- Composition order: "phi1 then phi2" = matrix product `g2 * g1` (later action on the
  left).

HONESTY NOTE (recorded, not hidden): a first run asserted the triangularity
obstruction entry as `a - d` and FAILED on the sign; with the basis `R23 = E23 - E32`
the exact entry is `d - a`. The substantive claim (vanishes iff `a = d`) is unchanged;
the two check targets were corrected and the failure is recorded here per F-C
discipline (the failed assertion was this script's own auxiliary sign convention, not
a preregistered formula).

## 1. T1 — equivariance/covariance: the strata are SPLIT-RELATIVE

Basis validity and the cited perfectness cross-check: `[T1_so13_basis_valid,
T1_so13_perfect_crosscheck]`.

Computing `[lam, X]` for generic `lam` (6 gauge params) on the generic class member
and demanding each stratum condition be preserved identically in the 7 (or 8, chart
dropped) extension parameters gives an exact descending chain of stabilizers:

| condition preserved | exact stabilizer in so(1,3) | dim | check |
|---|---|---|---|
| upper-right block zero (base/angular split) | `span(B01, R23) = so(1,1)⊕so(2)` | 2 | `[T1_split_stabilizer_dim2]` |
| + fixed founded base block `H` | `span(R23) = so(2)` | 1 | `[T1_fixedH_stabilizer_dim1_so2]` |
| + triangular-K chart (`K[1,0]=0`) | `{0}` | 0 | `[T1_triangular_chart_stabilizer_zero]` |

So: (i) **no stratum condition is covariant under the full gauge algebra** — the four
mixing generators (B02, B03, R12, R13) destroy the block split itself, so
covariance-of-strata is not even well-posed pointwise without a supplied base/angular
split (this IS the T1 result, as anticipated by the prereg); (ii) even the base boost
moves the founded generator, `[so(1,1)-boost, H] = 2[[0,1],[-1,0]] ≠ 0`
`[T1_base_boost_moves_H]` — H is *equivariant, not invariant*, exactly the banked
07-26 correction; (iii) **the registered triangular chart is a pure gauge section**
(stabilizer `{0}`; obstruction entry `[R23,X]_[3,2] = d - a`
`[T1_triangularity_obstruction_is_d_minus_a]`).

The one exception: `tr[lam, X] = 0` identically for the FULL algebra
`[T1_trace_condition_fully_invariant]` — **the det-one condition `a+d = 0` (E03's
trace part) is the unique stratum condition covariant under all of so(1,3)**.

Per-stratum stabilizers given the split (all exact):
E04 (K=0): `so(2)` `[T1_E04_stabilizer_so2]`; E05 in chart-free full-K form: `so(2)`
`[T1_E05_fullK_stabilizer_so2]`, but its triangular presentation: `{0}`
`[T1_E05_triangular_stabilizer_zero]`; E06 spectator point: `so(2)`
`[T1_E06_stabilizer_so2]`.

**The so(2)-fixed-point set of the whole 7-parameter class is exactly the isotropic
line** `{b=0, C=0, a=d}` = `X_lambda = diag(-1,+1,λ,λ)`
`[T1_so2_fixed_set_is_isotropic_line]` — reproducing the banked SO(2)-screen row of
the joint no-go table. Centralizer-dimension cross-check 1/3/3/1 (generic/+1/−1/0)
agrees with the cited 07-28 values `[T1_centralizer_dims_1_3_3_1]`.

The diagonal (a,d) subfamily is itself NOT so(2)-stable off `a=d`
`[T1_diagonal_subfamily_not_so2_stable]`: it is a chart section. The residual-gauge
invariant content of the screen generator K is exactly `(tr K, det K, antisymmetric
part)` `[T1_so2_invariants_tr_det_antisym]`; a π/2 screen rotation maps
`diag(-k,+k) -> diag(+k,-k)` `[T1_e07_k_sign_is_chart]`, so **the sign of E07's k is
chart gauge; the invariant modulus is |k|** (equivalently the unordered eigenvalue
pair `{-k,+k}`).

SCOPE STAMP (T1): registered chart, pointwise one-parameter class, connected local
Lorentz algebra in the defining representation; adjoint action; nothing global.

## 2. T2 — composition closure: exact witnesses

The bracket of two class members is
`[X1,X2] = [[0,0],[(C1-C2)H + K1C2 - K2C1, [K1,K2]]]` `[T2_bracket_block_formula]` —
zero base block, i.e. it points OUT of the affine class (base coefficient 1) into its
linear part. `[K1,K2]` stays triangular `[T2_K_bracket_stays_triangular]` with
non-abelian witness `[K1,K2]_[0,1] = a·b2 + b·d2 - a2·b - b2·d`
`[T2_K_bracket_nonabelian_witness]`. The 8-dim envelope
`L8 = {[[s·H,0],[C,K_triang]]}` IS a Lie algebra (bracket has s-component 0)
`[T2_L8_is_lie_algebra]`: **class exponentials generate the 8-dimensional group
exp(L8), not the class itself.**

Finite non-closure witness (lives already in the abelian diagonal part of E05, hence
in every stratum with ≥ 2 members): `exp(-phi·X_{d=1})·exp(phi·X_{a=1})` has base
block = identity exactly but screen block `diag(e^{phi}, e^{-phi}) ≠ I` for
`phi ≠ 0`, while any class element with base = I forces `psi = 0` hence = I
`[T2_nonclosure_witness_base_identity, T2_nonclosure_witness_not_class_form]`.
**Exact statement: no stratum with at least two members is closed under composition
at total phi = 0.**

Off that locus, composition closes but the modulus composes non-trivially. The
diagonal subfamily is abelian `[T2_diagonal_subfamily_abelian]` (zero BCH
obstruction — E07 line and isotropic line included), and the product is class form
with the phi-weighted-mean modulus
`abar = (phi1·a1 + phi2·a2)/(phi1+phi2)`
`[T2_diagonal_composition_renormalized_modulus]`; `abar = a1` iff `a2 = a1`
`[T2_diagonal_modulus_shift_vanishes_iff_equal]`. **A constant-modulus assignment
survives composition only if every segment carries the same member** — a J07/J11-typed
requirement (transition/overlap data), stated as a requirement, not filled in.

SCOPE STAMP (T2): one-parameter segments with exact finite forms; group-level; no
global bundle claim.

## 3. T3 — the mixing cocycle

`g(phi,s)` (the E08 finite form) satisfies `dg/dphi = X_s·g`, `g(0)=I` — it IS
`exp(phi·X_s)` by linear-ODE uniqueness `[T3_E08_finite_form_is_exponential]`. With
`sigma = s(1-e^{-phi})`, concatenation (phi1 then phi2) obeys the EXACT law

```text
sigma_tot = sigma_1 + e^{-phi1} · sigma_2
```

`[T3_shift_cocycle_law]` — an affine 1-cocycle of the reciprocal channel valued in
the weight-`e^{-phi}` module (ax+b-type composition), associative with path-ordered
weights `sigma_123 = sigma_1 + e^{-phi1}·sigma_2 + e^{-phi1-phi2}·sigma_3`
`[T3_cocycle_associativity]`. Off total phi = 0 the product is again class form with

```text
sbar = [sigma_1 + e^{-phi1}·sigma_2] / (1 - e^{-(phi1+phi2)})
```

`[T3_class_form_recovered_off_zero_total]`, consistent on single-member segments
(`s1=s2=s ⇒ sbar=s`) `[T3_same_s_consistency]`, and **phi-history-dependent**:
sbar at (T/2, T/2) minus sbar at (T, 0) equals
`(s2-s1)·e^{-T/2}(1-e^{-T/2})/(1-e^{-T}) ≠ 0` unless `s1=s2`
`[T3_history_dependence_witness]`.

Full C block: `exp(phi·[[H,0],[C,0]]) = [[e^{phi H},0],[C·M(phi), I]]` with
`M(phi) = diag(1-e^{-phi}, e^{phi}-1)` `[T3_general_C_finite_form]`; composition
lower-left = `C2·M(phi2)·e^{phi1 H} + C1·M(phi1)` `[T3_general_C_cocycle]` — the same
path-ordered affine cocycle, channel-weighted `e^{-phi1}` (clock leg) and `e^{+phi1}`
(ruler leg). `det M(phi) = 0` iff `phi = 0` `[T3_M_invertible_iff_phi_nonzero]`, so
the composed mixing modulus `Cbar` exists uniquely off total phi = 0; at
`phi2 = -phi1` the residual is `(C1-C2)·M(phi1)` `[T3_zero_total_residual_C1_minus_C2]`.
First-order seed: `[X_C1, X_C2] = [[0,0],[(C1-C2)H, 0]]`
`[T3_first_order_C_bracket]`, nonzero iff `C1 ≠ C2`.

**J07 typing (stated, not filled):** a global assignment of mixing data cannot be a
constant matrix per chart; the overlap/transition datum a global extension would need
is exactly this weighted affine cocycle (path-ordered, history-dependent). Whether
UDT derives such data is OPEN — no global object is constructed here.

SCOPE STAMP (T3): exact finite one-parameter forms and their products; pointwise
class; no descent claim.

## 4. T4 — the (a,d)-plane atlas (diagonal subfamily b=0, C=0)

Finite form `exp(phi·diag(-1,1,a,d)) = diag(e^{-phi}, e^{phi}, e^{a phi}, e^{d phi})`
`[T4_diagonal_finite_form]`; physical metric (calibration c on the clock slot)
`diag(-c^2 e^{-2phi}, e^{2phi}, e^{2a phi}, e^{2d phi})` `[T4_metric_readout]` — a
generator entry m on a slot gives metric factor `e^{2m phi}`, sign convention CHECKED
against the banked E07 record `[T4_E07_sign_check]`.

Derived natively: `det g = -c^2 e^{2(a+d)phi}`, so the **4D chart volume exponent is
a+d** (the base pair contributes (−1)+(+1) = 0 exactly) `[T4_4d_volume_exponent_a_plus_d]`;
`det exp(phi X) = e^{(a+d)phi}` and `tr X = a+d` (the E03 ledger fact confirmed)
`[T4_det_one_line]`.

Seat coordinates: `(a,d) = (lambda - k, lambda + k)`, `lambda = (a+d)/2`,
`k = (d-a)/2` `[T4_lambda_k_coordinates]`. **The isotropic seat (joint-audit lambda)
and the E07 seat (k) are the two orthogonal axes of the plane, meeting only at the
spectator origin.** The MAP's seat-level equation "E07's k = the joint audit's
lambda" is resolved as a DECOMPOSITION, not an identity: the honest L2 modulus of the
diagonal subfamily is the PAIR `(lambda, k)` — invariantly `(lambda, |k|)`, since the
sign of k is screen-chart gauge (§1).

```text
                d
                ^
   E07 line    |         isotropic line a = d
 (a=-k, d=+k)  |            (lambda axis)
        \      |           /
         \     |          /   * (1,1)  SO(3)-forced      [CONDITIONAL, 07-27/28]
          \    |         /
           \   |        /
            \  |       /
             \ |      /
              \|     /
  -------------O--------------------> a
              /|\        O = (0,0) spectator; swap-forced [CONDITIONAL,
             / | \            diagonal subfamily only, 07-27]
            /  |  \
           /   |   \   * (-1/2,-1/2) orbit-volume-blind V_q, 1+2*lambda = 0
          /    |    \      [CONDITIONAL: stationary R x S3 branch, isotropic
         /     |     \      members only, 3D ORBIT volume — rank-closure 07-27]
        /      |      * (-1,-1)  SO+(1,2)-forced          [CONDITIONAL, 07-27/28]
       /       |
  anti-diagonal a+d = 0:  E07 line  =  det-one line  =  native 4D volume-blind
                          line (THREE names, ONE line) [T4_three_name_coincidence]
```

Pin table (every banked pin placed or declared not translatable):

| pin | locus | status/scope | source |
|---|---|---|---|
| spectator / swap-forced λ=0 | (0,0) | CONDITIONAL on supplied reciprocal swap; valid ONLY in this diagonal subfamily (full class keeps two mixing freedoms) | 07-27 audit, Result first |
| SO(3)-forced λ=+1 | (1,1) | CONDITIONAL on supplied timelike observer line | 07-27 + 07-28 reduced table |
| SO+(1,2)-forced λ=−1 | (−1,−1) | CONDITIONAL on supplied spacelike ruler line; different supplied global structure from +1 (splice forbidden) | 07-27 + 07-28 |
| det-one line | a+d=0 | fully so(1,3)-covariant trace condition (§1) | this package `[T4_det_one_line]` |
| E07 line | a+d=0 (k-axis) | = det-one line = 4D volume-blind line; invariant modulus |k| | this package `[T4_three_name_coincidence]` |
| 4D volume-blind locus | a+d=0 | derived natively here (exponent a+d) | `[T4_4d_volume_exponent_a_plus_d]` |
| orbit-volume-blind λ=−1/2 | (−1/2,−1/2) | CONDITIONAL pin, isotropic line ONLY; the cited V_q lives on the 3D S3 ORBIT of the stationary unique-K branch (2 screen legs at λ + 1 fibre leg at ruler weight +1 ⇒ exponent 1+2λ); NOT the 4D chart volume; NOT-TRANSLATED off a=d (no banked orbit-volume formula for a≠d exists; a naive extension is writable but its branch prerequisites are unbanked — N-6) | rank-closure 07-27; reconciliation `[T4_orbit_exponent_reconciliation]` |
| holonomy centralizer dims 1/3/3/1 | isotropic axis points | cross-checked exactly | 07-28; `[T1_centralizer_dims_1_3_3_1]` |

RECONCILIATION (the prereg's flagged mismatch, closed honestly): the banked V_q
exponent `1+2λ` and the native 4D chart exponent `a+d` (= `2λ` on the isotropic
line) are DIFFERENT functionals on DIFFERENT geometries — the 3D orbit space of the
stationary R×S3 branch (clock quotiented out, σ3 fibre carrying the ruler weight
e^{2φ}) versus the 4D block chart (clock and ruler cancelling). Their blind loci
(`λ = −1/2` vs `a+d = 0`) must not be conflated; both are recorded with their own
scopes. `[T4_isotropic_4d_exponent_2lambda, T4_orbit_exponent_reconciliation]`.

All three cited conditional pins lie on the isotropic axis k=0; **no banked gate pins
any point with k ≠ 0** `[T4_conditional_pins_on_isotropic_line]`. CR-1 (verifier):
the banked supplied-reduction gates are not silent on k — each of the three (supplied
SO(3), supplied SO+(1,2), supplied reciprocal swap) conditionally forces k = 0 under
its own supplied structure (07-27 full-class solves: K=diag(+1,+1), K=diag(−1,−1),
K=0). The precise statement: no banked gate pins k ≠ 0; k is unconstrained only
ABSENT supplied structure.

SCOPE STAMP (T4): diagonal subfamily of the registered chart; pin scopes as stamped
per row; the orbit-volume row additionally scoped to the stationary R×S3 branch.

## 5. T5 — conditional-gate table (assembly; citations only, no new gates)

| stratum \ supplied reduction | SO(3) observer line | SO+(1,2) ruler line | SO(2) screen (ordered pair) | reciprocal swap | none (full frame) |
|---|---|---|---|---|---|
| E02full (7) | forces the isotropic member λ=+1 IF also restricted to diagonal subfamily; does not touch b, C [07-27 Result first; 07-28 reduced table] | same, λ=−1 [ibid.] | fixes the isotropic line as invariant set; λ unselected [07-28 table; cross-checked `T1_so2_fixed_set_is_isotropic_line`] | λ=0 ONLY in diagonal subfamily; TWO mixing freedoms remain in full class [07-27, verbatim] | no selection; scalar-only centralizer [07-26]; zero active selector rank [07-26] |
| E03 (det-one) | forced member (1,1) has a+d=2: supplied SO(3) forces OUT of det-one | forced member (−1,−1) has a+d=−2: forces OUT of det-one | isotropic∩det-one = origin only | swap point (0,0) ∈ E03 | no selection [07-26] |
| E04 (K=0) | n/a to K; mixing untouched by cited gates | n/a | C not fixed by screen so(2) (equivariant only) | leaves two mixing freedoms [07-27] | no selection |
| E05 (C=0) | forces a=d=+1 member conditionally | forces a=d=−1 conditionally | isotropic sub-line invariant | λ=0 within its diagonal part | no selection |
| E06 (spectator) | incompatible (forces λ=+1≠0) | incompatible (λ=−1≠0) | consistent (fixed point) | FORCED as the diagonal-subfamily answer [07-27] | not selected; E07/E08 countermodels [E02 record] |
| diagonal subfamily | (1,1) pin | (−1,−1) pin | isotropic axis fixed | (0,0) pin — the gate's exact scope | no selection |
| E07 line | forces out (isotropic ≠ E07 except origin; conditionally forces k=0) | forces out (same; conditionally forces k=0) | line not invariant (chart section §1) | only its origin survives the swap gate (conditionally forces k=0) | no selection; no banked gate pins k≠0 (CR-1) |
| isotropic line | λ=+1 | λ=−1 | pointwise fixed (strongest covariance) | λ=0 | λ unselected [07-28 table]; V_q blind at λ=−1/2 [07-27 rank-closure, branch-scoped] |

Every cell is CONDITIONAL on its column's supplied structure; the +1 and −1 columns
belong to DIFFERENT supplied global structures and may not be spliced (07-27). None
of these gates is a current UDT consequence; supplying any of them is a premise.

F-D quantifier discipline for this table: "forces" always means "forces WITHIN the
named stratum, GIVEN the supplied structure, in the registered pointwise class" —
never unconditional, never cross-stratum.

## 6. Falsifier review (frozen list, adjudicated)

- **F-A (re-derivation masquerade):** no UNCONDITIONAL elimination is claimed
  anywhere in this package, so no elimination can rest on the rank-zero active set.
  The only unconditional NEW facts are C1 covariance types (split-relativity, chart
  artifacts) and C2 closure witnesses — typings, not eliminations. NOT FIRED.
- **F-B (bank contradiction):** no pointwise metric-only selection is claimed; E06
  uniqueness appears only as "unique closed subgroup" (closure property) and
  "swap-forced within the diagonal subfamily" (conditional, cited); E07/E08
  countermodels retained. NOT FIRED.
- **F-C (symbolic failure):** fired once in-run on this script's own auxiliary sign
  target (`a−d` vs `d−a`, §0 honesty note); corrected, rerun 47/47, exit 0. Recorded.
- **F-D (quantifier slip):** every forcing/uniqueness sentence above carries its
  quantifier scope explicitly; the ledger repeats them per row. Hunted; none found by
  the author (the blind verifier owns the final hunt).
- **F-E (imposition):** all statuses are typed by forcing identity or citation; no
  merit criterion appears; E07/E08 survive with UNCONSTRAINED/moduli statuses.

## 7. L1/L2 RE-TAG (T6) — strictly from Stage-1 evidence

- **L1 (which stratum): MODULUS-CARRIED, with derived TYPE structure.** No stratum is
  natively eliminated (outcome class O2/O3 mixture, both first-class per prereg §5).
  What Stage 1 DERIVED about L1: (i) stratum conditions are split-relative — not
  full-so(1,3)-covariant — so L1 is only well-posed after a base/angular split is
  supplied (itself part of the founded structure's presentation); (ii) the
  triangular-chart presentations of E02/E03/E05 are gauge sections (stabilizer {0}),
  so L1 must be posed on the chart-free full-K class or on so(2)-invariants;
  (iii) the det-one condition is the unique fully covariant condition AMONG this
  package's listed stratum/chart conditions (N-3: other fully covariant functions on
  the class exist, e.g. det X = −ad; uniqueness is quantified over the listed set);
  (iv) imposing E06 (or E04/E05 as premises) remains a typed J06-false-pass
  (VIOLATED_IF_IMPOSED), per the ledger. L1 elimination by C1/C2 alone: NONE —
  survival ledger is the deliverable.
- **L2 (transverse modulus): MODULUS-CARRIED as the PAIR (λ, |k|) on the diagonal
  subfamily — not one scalar; each pinned value CONDITIONAL(on cited supplied
  structure).** Stage 1 resolved the MAP's seat conflation: λ = (a+d)/2 (isotropic
  axis, so(2)-fixed, carrying ALL banked conditional pins +1/−1/0 and the
  branch-scoped −1/2 volume-blind point) and k = (d−a)/2 (E07 axis, sign chart-gauge,
  |k| invariant; no banked gate pins k ≠ 0, and each banked conditional gate forces
  k = 0 under its supplied structure — k is free only absent supplied structure, CR-1).
  λ values +1/−1/0 are
  CONDITIONAL(SO(3) / SO+(1,2) / swap, cited); absent a supplied reduction both λ and
  |k| are MODULUS-CARRIED. Additionally the b and C moduli of the full class remain
  carried (with the T3 cocycle as their composition type).

Maximum conclusion (within the prereg §5 ceiling, restated): stratum members are
eliminated or forced ONLY as scoped above (registered chart, pointwise one-parameter
class, conditional on cited supplied structure); L1/L2 re-tagged per this section. No
supplied reduction is adopted; no physics is selected; no response one-form or action
claim is made.
