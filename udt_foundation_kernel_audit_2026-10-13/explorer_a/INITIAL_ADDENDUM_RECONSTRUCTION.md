# Explorer A — initial reconstruction after recovered owner excerpt

Status: initial analytic candidate, still before old proof or sibling exposure.
This is an exposure supplement, not an overwrite of the preceding edition.
`INITIAL_APPROACH.md` and `INITIAL_RECONSTRUCTION.md` were written immediately
before the parent's addendum notice arrived. They are preserved byte for byte:

- Approach SHA-256: `0ed810a09b8438668449c3256a28017ff78de5c8dff84bacae34370820ab12f7`.
- Reconstruction SHA-256: `96726ec137ab43500fa958939c6b67bee45205249407a663a9cdeede3f4da5b9`.

New exposure: only `../OWNER_SOURCE_ADDENDUM.md` and
`../ADDENDUM_SOURCE_PINS.json`. The former has SHA-256
`859303072648d7f8011e0753acfc5274ac28dfd6a34cbc8143e99227a0a87fcb`.
It supplies the recorded June 18 owner quotation, including explicit
difference-dependence, consistent composition, and mutual slow-clock symmetry.
The quotation is attributed by its source; a complete raw conversation has not
been inspected. The assertion that these requirements uniquely derive a metric
is a claim under examination. The full source proof remains unexposed.

This changes the earlier finding that the starting owner words supply no
mathematical composition requirement: such a requirement is now explicitly
present in a later dated quotation. It does not yet specify the operational
objects, composition domain or a structural metric equation. The following
results replace neither the original record nor the source's wording.

## A. Strong favorable formalization: positive signed-difference composition

Test the following explicitly declared mathematical interpretation, rather than
assuming that ordinary English already supplies all its quantifiers. Let a
positive scalar comparison `D(b-a)` depend only on signed differences of a
real position/depth coordinate `φ`. Suppose comparisons compose as products
for every admitted intermediate position:

`D(c-a) = D(c-b) D(b-a)`.

Assume `D` is continuous on an interval around zero with the relation valid
whenever the differences and sums are in its domain. This regularity is natural
for a smooth metric realization but is an explicit hypothesis of this lemma.
Since `D>0`, composition at zero gives `D(0)=1`. Choosing opposite differences
then gives `D(-x)=1/D(x)`. Setting `L(x)=log D(x)` turns composition into
`L(x+y)=L(x)+L(y)`. Subdivision and rational multiples determine
`L(qx)=qL(x)`; continuity extends to real multiples on the connected domain.
Hence

`D(x)=exp(k x)`

for a real constant `k`. Equivalently, if differentiability is assumed one can
differentiate the composition law at zero to obtain `D'=kD`, `D(0)=1`.
The exponential is therefore a sound conditional consequence of this precise
scalar composition requirement. The overall scale and sign of `φ` have not
been fixed: rescaling `φ` rescales `k`. This is stronger than merely observing
that every positive number can be written as an exponential.

If `D(φ_B-φ_A)` is identified with the stationary received tick ratio
`R_AB=a_A/a_B`, fixing one reference value yields

`a(φ)=C exp(-kφ)`, and `A(φ)=C² exp(-2kφ)`.

Here `C>0` is time/calibration normalization. Composition constrains the lapse
under this identification. It does not fix the radial coefficient. Every
metric in the family

`ds²=-C² exp(-2kφ(r)) c_E²dt² + B(r)dr² + r²dΩ²`, `B(r)>0`,

has the same stationary tick ratios. Thus these scalar clock data, by
themselves, do not distinguish `B=C^-2 exp(2kφ)` from another positive smooth
`B`. These are countercontrols to uniqueness from the stated scalar data, not
models claimed to satisfy all owner intentions, including mutual redshift.

## B. Exact incompatibility if that same scalar is both future tick ratios

The strong signed-difference model has `D(x)D(-x)=1`. It cannot also satisfy
strict `D(x)<1` and `D(-x)<1` for a nonzero separation. If exchange symmetry
means `D(x)=D(-x)`, positivity forces `D(x)=1`. Therefore:

**A positive, position-only, signed-difference scalar comparison with full
intermediate-position product composition cannot itself represent strict
mutual received slowing in both directions.**

This is a proof for the declared formalization, not a claim that the owner's
words mandate it or that every geometric realization of the founding program
fails. It also does not establish a structural relation between `g_tt` and
`g_rr`; the contradiction is present in the scalar operational identification
before the radial metric coefficient enters.

One can still use `D` as a change-of-frame or common-time conversion with an
inverse. Then the exponential composition lemma survives, but the two actual
future signal experiments need separate derivation. The absence of a privileged
position does not, by itself, equate an inverse transformation with a new future
signal. The moving-clock control in the initial reconstruction illustrates the
distinction with explicit causal events and equal proper-clock conventions.

## C. Two narrower meanings preserve mutual slowing without this contradiction

First, composition may concern ordered nonnegative path lengths rather than all
signed differences. For `s>=0`, `Q(s)=exp(-κs)`, `κ>0`, satisfies
`Q(s+t)=Q(s)Q(t)` and is below one at positive lengths. Giving both directions
the same length yields two slowings. Equivalently,
`exp(-κ|φ_B-φ_A|)` composes when intermediate points lie between the endpoints
on a monotone line, but not for arbitrary intermediate points or return paths.
For a return, positive path length adds; it does not vanish with endpoint
coordinate difference. This is a consistent scalar semigroup alternative,
explicitly unadopted. It supplies no metric or native positional signal law.
It locates a real missing quantifier: what intermediate positions and what
notion of composition does the owner's statement require?

Second, physical emission/reception maps compose along causal event chains.
If a pulse is relayed from A to B to C, derivatives multiply by the ordinary
chain rule, provided those actual events and signal branches are specified.
A return to A ends at a later event. It is not the identity map just because
the spatial observer label is again A. In dynamic/moving preparations a return
map may have nonunit slope without logical contradiction. Erasing event times
and replacing the causal chain by the identity of position labels imports an
assumption not justified by ordinary proper clocks or causality.

These alternatives are worth preserving because they show that the contradiction
in B is sensitive to the operational domain. They are not a rescue by changing
the founding interpretation: they are candidate readings to compare against
the dated words and old derivation. Neither is being adopted as UDT.

## D. What this adds to the kernel reconstruction

The supplied reciprocal metric still yields `a=exp(-φ)`, `b=exp(φ)` and the
chosen normalized contrast `(b-a)/(b+a)=tanh φ`. The recovered composition
wording provides a possible independent reason for an exponential comparison,
given the exact positive scalar, regularity and signed-domain interpretation.
It does not yet supply:

1. The operational realization of that scalar as a lapse ratio, frame map,
   causal tick-transfer ratio or path quantity.
2. A deduction of the radial metric coefficient from the clock comparison.
3. A selection of the normalized contrast as a physical kernel/readout.
4. A consistent identification of inverse comparison with both future signal
   slowings, rather than separate operational maps.

These are distinct joins. The old proof may support some of them, so the next
step remains substantive source comparison. The strongest favorable initial
survivor is exponential scalar composition and the metric's reciprocal algebra;
the strongest adverse result is the exact conflict between full signed scalar
composition and strict mutual received slowing on the same position-only object.

No numerical run was used or needed for these exact implications. No extra
source, protected work, old proof, sibling argument or maintained summary was
opened. This supplement and the two preserved initial files constitute the
initial freeze to be compared and reviewed; they are not three maintained
scientific summaries.
