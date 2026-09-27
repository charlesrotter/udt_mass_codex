# Native outward return: local response and a finite-pair coefficient

Status: initial candidate, conditional source recovery plus one exact implementation
discriminator; **not a new field equation, scientific promotion, or canon**.
Baseline: `grok` at `6553f5e90e5e7a51030fb9f8205528f8420b0b0f`.

The positional interpretation is fixed by Charles's present work order: observed
`c` is wholly positional dilation, without an independent primitive transfer-speed
interpretation. `c_E` remains the observed clock/ruler calibration. This work does
not ask again why that interpretation holds or demand a numerical derivation of
`c_E`. The question is how it can enter an equation while preserving the owned
metric and response constraints.

## Result and novelty boundary

The already owned constraints genuinely restrict an implementation: complete
pair geometry must precede the reciprocal readout; one local metric supplies the
clock/ruler/null geometry; the specified DDR response must be pure trace on its
registered all-pair domain; and an unchanged relevant local metric jet cannot
produce different local responses merely because an additional reference/query
label changed. These constraints do not identify the physical response `E[g]`.

A concrete narrowed discriminator follows. On one supplied positive static
primary metric, two exactly matched static clock comparisons can have the same
terminal event and different finite-pair `c_eff/c_E`. Thus a proposed fixed local
response law cannot use that finite-pair number as a universal coefficient with
nontrivial surviving dependence on the reference query, if both queries are in
the implementation's admitted domain. It would cease to give a unique response
for that fixed local metric jet. Using it as a second proper-frame null speed
also conflicts directly with W4. Using it as a coordinate readout, with the
complete metric transformed consistently, is harmless and already owned.

This is an application of existing W4/Local Metric Sufficiency and calibrated
pair mathematics to one named replacement, not a new native exclusion of a
metric family. It does not prove that every diagnostic query is physically
populated, that all finite-pair dependence is forbidden, that UDT is generally
underdetermined, or that another postulate is necessary. The TC0/PJC1/FSR1
identity searches were not rerun. The open join remains the physical response
identification and native membership route, at exactly their current grades.

## Sources and epistemic ownership

Exact source-byte pins are in `SOURCE_PINS.tsv`. Current G312 authority overrides
the stronger historical quiet-GR wording wherever it occurs in older sources.

| Source / premise | Equation-relevant content used | Grade and surviving limit |
|---|---|---|
| `founding.md`, F1 | `L=c_E T` and inverse conversion | Observed calibration plus founding interpretation; not itself a value law or propagation proof |
| `founding.md`, F2 | Positive diagonal positional action satisfies `P^T K P=K`, hence `uv=1` | Foundational Dual Reciprocity; does not follow merely from numerical `c_E` |
| `founding.md`, F3 | Positive continuous/measurable nontrivial additive comparisons give `D(delta)=diag(exp(-delta),exp(delta))` | Positional composition/reversal posit with regularity, sign/unit and nontriviality disclosed; does not generate depth values |
| `founding.md`, F4 and section 3 | Quadratic Lorentzian readout gives `g=-f c_E^2 dt^2+f^-1 dr^2+r^2 dOmega^2`, `f>0`, on the static spherical areal branch | Declared readout and bounded branch; the reciprocal component relation is chart/branch specific, not a universal coordinate condition |
| `founding.md`, W1/section 6; G176/G178 audit reports | On a supplied regular completed pair, `m=T L_sigma=sqrt(-det h_sigma)`, `L_n=T^-1`, retained shift, `Phi=-log(T/T_star)` | Working foundational clarification, not bare-metric derived or canon; no pair population or global completion selected |
| `founding.md`, W4 | One local metric for clocks, rulers, free fall and null propagation; local calibrated `c_E` | Working/posit; finite-pair `c_eff` is not a second local cone; no field equation or response architecture selected |
| `founding.md`, W5 | Complete projective frame relation, including screen components and full carry needed for composition | Working foundational clarification; not proper/radar/areal distance, dimensional scale, path independence or history selection |
| `founding.md`, W6 | Co-presence is not propagation; observable controllable response stays inside completed metric causality | Working foundational clarification; no causal response functional, population, or evolution law supplied |
| G310 audit and later adoption; current G312 authority | For the specified symmetric response on the registered full all-pair domain, DDR gives `TF(E)=0`, hence `E=lambda(x)g` | Owner-adopted provisional postulate; population of all algebraic planes and physical response identification not inferred |
| `udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md` | Fixed relevant completed finite local metric jet fixes local response, without another hidden-history label | Local Metric Sufficiency affirmed owner-provisional; no jet order, tensor type/weight or principal nondegeneracy selected |
| Exact G301/G310/G312 registry rows and current G312 authority | In the entire extra G301 class `E=a Ric+b Rg`, `a!=0`, DDR gives trace-free Ricci zero; Bianchi gives regional constant curvature scalar | Conditional mathematics only; current GR is filter only and does not supply that class membership |

`c_E`, `G_obs` remain observational anchors. No new use of `G_obs`, source law,
matter, action, carrier, absolute scale, `X_max`, local CSN, or physical population
is made. The user-fixed interpretation is authority for this work order, not a
claim that the old algebra newly proves the interpretation.

## Scope before computation

Metric-led finite diagnostic, exact rather than approximate. Domain: one smooth
four-dimensional Lorentzian static spherical primary geometry, `r>0`, `f>0`,
and two supplied matched static-clock references with one terminal event `B`.
The same metric and all its local jets at `B` are held fixed. This is a bounded
control domain, not an assertion that this geometry or both pairs are realized
physical UDT histories. No source, boundary, global completion, physical light
carrier, observation model or general time-live response is supplied.

Choices: the primary branch and complete readout are pinned-by-THEORY only at
their source-stated conditional grades. Static reference locations and
`f(r)=1+(r/ell)^2`, `ell>0`, are free-and-explored controls. `ell` is an arbitrary
length used to report radii, not a selected scale. The equatorial evaluation is
a regular spherical chart choice, with both angular terms retained. Common
Killing time and reciprocal carried ruler normalization specify the matched
comparison; generic pair/frequency transfer is not presumed. No pinned-by-HABIT
physical term is introduced.

CPU only; dependency-free exact rational arithmetic; no grid/GPU/long solve.
The script is capped at 120 seconds. The outcome was algebraically explored
before this candidate/check was frozen; this is not outcome-blind observation.
The maximum claim is the scoped evaluator/control and replacement discriminator
above. Stop at that result and the response-identification join.

## Matched comparisons: what varies and what stays fixed

Write `x0=c_E t` and retain the complete metric

`g=-f(r)(dx0)^2+f(r)^-1 dr^2+r^2 dOmega^2`.

Static W4 clocks satisfy `d tau_r=sqrt(f(r)) dt`. Choose a static reference
`P`, let `a=f(P)>0`, and compare all clocks using this same static time flow.
The matched clock factor at `B` is

`T_PB=d tau_B/d tau_P=sqrt(f(B)/f(P))`.

Its completed reciprocal ruler factor is `L_PB=1/T_PB`. Thus

`delta_PB=-log T_PB=(log f(P)-log f(B))/2`,

`q_PB=c_eff^(PB)/c_E=T_PB/L_PB=f(B)/f(P)`.

These are the exact matched primary radial relations from `founding.md`
sections 3, 6 and 7. They obey the matched composition and inverse rules.
They are not asserted for arbitrary moving observers, radiation records, or
general terminal readouts. No angular spatial reversal is used to infer pair
reversal. The clock reference fixes `T_star`; setting it to one is made only in
that carried reference calibration.

The same construction can be displayed with the pair coordinates
`y0=sqrt(a) x0`, `y1=r/sqrt(a)` and unchanged angular coordinates. Then

`g=-(f/a)(dy0)^2+(a/f)(dy1)^2+r(y1)^2 dOmega^2`.

The areal radius remains `r`, not `y1`; in particular the angular sector is not
silently changed to `y1^2 dOmega^2`. This is a carried chart/coframe description
of the same geometry. The pair determinant is `-1`; in this static radial
example the shift is zero. The generic shifted source remains
`h_sigma=-T^2(dy0+beta d sigma)^2+L_sigma^2 d sigma^2`, with density
`m=sqrt(-det h_sigma)` and `beta_n=beta/m`. Its density is not assumed to define
an integrable coordinate differential in general. No general screen, shift or
density is discarded by choosing this finite control.

Now hold `B` at `r=2 ell` and take references `A` at `ell` and `C` at `3 ell`.
For the declared control profile,

| Quantity | Query `A -> B` | Query `C -> B` |
|---|---:|---:|
| `f(reference)` | `2` | `10` |
| `f(B)` | `5` | `5` |
| `q=c_eff/c_E` | `5/2` | `1/2` |
| Metric at `B` in fixed base chart | Identical | Identical |
| All metric jets at `B` in fixed base chart | Identical | Identical |
| Proper local null ratio `(d ell_local/d tau_local)/c_E` | `1` | `1` |

The two different `q` values are not a scalar invariant of the local metric at
`B`. Nor are they rival outputs for one identical calibrated query: the reference
query changed. This distinction is essential to the result.

For radial null directions in either carried chart,

`dy1/d(t_P)=+/- c_E q_PB`, where `t_P=y0/c_E`.

But the proper local distance and clock factors give

`d ell_local/d tau_local=+/- c_E`.

Returning both carried coordinate null directions to the common base chart
gives `dr/dx0=+/- f(B)` for each. This preserves the one metric cone. Calling
the differing coordinate quotients a second proper-frame propagation law would
confuse a readout with the geometry that produced it; no independent primitive
transfer-speed interpretation is needed for this mathematical observation.

## Exact discriminator and its exceptions

Let `J` denote the completed relevant finite local metric jet, and let a proposed
replacement produce response `H(J,q_PB)`. Local Metric Sufficiency requires

`H(J,q_AB)=H(J,q_CB)`

whenever the fixed-`J` comparisons both belong to that implementation's admitted
query domain and no query datum is itself part of the response being asked for.
This is a consistency requirement, not a new response law. The displayed
control gives `q_AB != q_CB`. Hence direct nontrivial substitution into a
universal local coefficient fails this requirement whenever it actually changes
`H`. An independent reference-label dependence cannot be hidden by calling the
coefficient positional.

For the sharper special case of replacing the proper-frame metric null speed
`c_E` by `c_E q`, the original proper metric null residual, divided by the common
time factor, is `q^2-1`. It is `21/4` and `-3/4` for these controls, respectively,
instead of zero. This calculation concerns precisely the forbidden second-cone
implementation; it does not identify the real finite-pair ratio with a signal
speed.

Several cases do **not** fall to this discriminator:

- A full coordinate/unit transformation carries every metric and derivative
  factor consistently; no physical response then changes.
- Query factors can cancel in a composite invariant response. The argument
  tests surviving dependence, not appearances of a symbol.
- Multiplying an equation `E=0` by a nowhere-zero `q` leaves its solution set
  unchanged. It still changes a separately specified off-shell response unless
  the response equivalence is explicitly defined; it creates no new dynamics
  merely by relabelling the equation.
- A finite-query observable may legitimately depend on its reference or path.
  It is not being asserted to be the universal local metric response at `B`.
- A supplied or later justified rule might select a specific reference/query
  from the relevant local geometry, or allow only one comparison. This control
  does not disprove such a rule, supply it, or prove both test queries physical.

Consequently the accepted positional interpretation does not demand replacing
every occurrence of `c_E` by an arbitrary finite-pair `c_eff`. Keeping the
observed conversion `x0=c_E t` is consistent with that interpretation and W4;
deriving a physical response beyond the owned constraints remains open here.

## Evidence, provenance, and omissions

`check_matched_queries.py` uses exact rational arithmetic to recompute the
full diagonal metric pullbacks at a regular equatorial point, pair regularity
and determinants, composition/reversal, the common base null directions,
proper-frame ratios and the named bad-substitution residuals. Original stdout
is `EXACT_CHECK.json`, stderr is retained, and `EXECUTION.md` records the command
and version. These finite checks support the explicit control; they do not
prove physical population, all-query coverage, or an unknown field law.

The worker is a separate Codex context from the parent, same inherited model
(no different-model independence claimed). Parent top-level startup, successful
sync and preceding full 406-row verifier PASS are attributed evidence. This
worker independently checked local branch/hash/status, read AGENTS and the
triggered CLAUDE/no-shortcuts/completeness protocols, and reconstructed the
native argument from the pinned sources before seeing the parent's extension
candidate or proof. Its own check script is a construction check, not an
independent review. Source grades are preserved, not re-certified in full.

Protected/unrelated payloads were neither read nor changed. No existing solver
operator was changed, so old P1/P2 solver harnesses were not replayed. No full
curvature or GR-extension claim is made by this native packet. The parent's
separate review cycle and final premise audit remain the checkpoint gates.
