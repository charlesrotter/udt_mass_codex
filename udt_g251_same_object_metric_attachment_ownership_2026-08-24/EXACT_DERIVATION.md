# G251 exact derivation — same-object metric-attachment ownership

Date: 2026-08-24

## 1. The attachment problem is a commutative-square problem

Work on the bounded G249 orbit

\[
g_\ell=\ell^2\bar g,\qquad \ell>0,
\]

after one complete dimensionless history and regular branch are supplied. Let \(q\) denote the
typed geometric object on which a metric evaluator acts: an interval, branch point, screen, orbit,
hypersurface region, spacetime region, or event. If the evaluator has constant weight \(w\),

\[
E_Q(g_\ell,q)=\ell^w E_Q(\bar g,q).
\]

An operational attachment needs more than this evaluator. It needs a physical record \(p\), an
identification \(\iota(p)=q\), and an independently calibrated datum \(A(p)\) such that

\[
\boxed{A(p)=E_Q(g_\ell,\iota(p)).}
\]

The four G251 ownership legs are therefore:

1. the metric evaluator is owned;
2. the physical record and model object are identified;
3. the absolute datum is calibrated independently of the unknown \(g_\ell\);
4. its claimed instance is nonzero and has \(w\ne0\).

G250 proves that all four legs would fix \(\ell\). It does not prove that any current source owns
all four.

## 2. Metric self-evaluation is circular

If the proposed “observation” is itself recomputed from the same unknown metric,

\[
A_\ell(p):=E_Q(g_\ell,q),
\]

then the attachment equation becomes

\[
E_Q(g_\ell,q)=E_Q(g_\ell,q),
\]

which is true for every positive \(\ell\). It contains no scale information. This is exactly the
G132 volume-form boundary: volume derived from the full metric is not an independent datum.

The same obstruction survives when several internal channels are compared. For weights
\(w_1,w_2\ne0\),

\[
\frac{Q_1(g_\ell)^{w_2}}{Q_2(g_\ell)^{w_1}}
=
\frac{\bar Q_1^{w_2}}{\bar Q_2^{w_1}},
\]

so the scale cancels. Such relations can test the dimensionless history, but cannot calibrate its
common homothety. Comparing different dimensional weights without this cancellation requires an
independently owned dimensionful bridge merely to make the equation well typed.

## 3. Direct metric classes

The current chain owns the following conditional evaluators:

| Class | Evaluator owner | Homothety weight | Current attachment boundary |
|---|---|---:|---|
| proper-time interval | G216 | \(+1\) | worldline/events and physical duration not selected |
| length/Jacobi amplitude | G244/G249 | \(+1\) | branch point and absolute length datum supplied |
| screen or orbit area | G132/G244 | \(+2\) | screen/orbit and calibrated physical area supplied |
| spatial three-volume | G210 | \(+3\) | hypersurface region and external volume supplied |
| spacetime four-volume | G132 | \(+4\) | spacetime region and external volume supplied |
| nonzero scalar curvature/tide | G227/G249 | \(-2\) | event/value supplied; value generation open |
| nonzero quadratic curvature | G227/G249 | \(-4\) | event/value supplied; value generation open |

G216 derives metric proper-time normalization and the pair-clock derivative only after a pair germ
is supplied. It does not select the physical event pair or provide an independently measured finite
duration. G244 derives Jacobi area and shape on a supplied regular sheet but explicitly leaves its
catalogue/source attachment open. G210 derives the volume mode without selecting its profile or
history. G227 reconstructs curvature from supplied compatible tidal data but leaves numerical value
generation open. G246 supplies local metric incidence after observer germs are supplied; it does
not select their physical population.

Thus all seven direct classes have a native metric evaluator, but no registered class currently
owns the physical same-object identification plus independent absolute datum. Their exact grade is

```text
DIRECT_OBSERVATIONAL_ATTACHMENT_MUST_BE_SUPPLIED
```

This is not a request for a new kernel term. It is the ordinary empirical step of declaring which
physical record is being compared with which metric object. That declaration must precede reading
its value and cannot be chosen because it gives a desired scale.

## 4. Dimensional composites are a different type

The three registered dimensional lengths

\[
\frac{G_{\rm obs}M}{c_E^2},\qquad
\frac{c_E}{\sqrt{G_{\rm obs}\rho}},\qquad
\frac{c_E^2}{\sqrt{G_{\rm obs}\epsilon}}
\]

are not metric evaluators on an identified pair object. Their coefficient, matter/density identity,
and placement in the metric network are unowned. They therefore require an additional matter or
instrument law before they can enter an attachment square. Their grade is

```text
MATTER_OR_INSTRUMENT_LAW_REQUIRED
```

This does not invalidate `G_obs`, mass, density, or energy density as observations. It prevents
dimensional compatibility from being promoted into a native metric equation.

## 5. Controls

- `c_E` converts an independently supplied clock interval into length units; it is not an interval.
- `G_obs` has no active native metric placement law.
- reciprocal redshift/clock ratios, causal cones, and normalized Jacobi shape are metric-owned
  evaluators or structures, but have weight zero and therefore cannot select the homothety scale.
- zero curvature remains zero throughout the orbit.
- G99 `X_eff` retains P1, external-`M_B`, and imported-transfer conditions and is not a native G249
  attachment.

None can satisfy the four-leg test in the current bounded source universe.

## 6. Source-exact landing

The complete 18-candidate ledger returns zero native attachment owners, seven direct classes that
need one supplied operational attachment, and three dimensional composites that need a matter or
instrument law. Every candidate carries explicit cited `E/I/C/W` fields. Exact rational tests
verify the self-evaluation family, scale-free internal cross-channel invariant, and independently
fixed-anchor control.

```text
CURRENT_METRIC_CHAIN_OWNS_EVALUATORS_AND_SUPPLIED_GEOMETRIC_OBJECT_TYPES
__NO_REGISTERED_CLASS_OWNS_AN_INDEPENDENT_SAME_OBJECT_ABSOLUTE_DATUM
__METRIC_SELF_EVALUATION_IS_CIRCULAR_AND_CANNOT_BREAK_THE_G249_HOMOTHETY
__DIRECT_CLOCK_JACOBI_AREA_VOLUME_AND_CURVATURE_ANCHORS_REQUIRE_ONE_SUPPLIED_OPERATIONAL_ATTACHMENT
__MASS_DENSITY_ENERGY_COMPOSITES_REQUIRE_AN_ADDITIONAL_MATTER_OR_INSTRUMENT_LAW
__NO_ANCHOR_VALUE_HISTORY_BRANCH_POPULATION_FIT_OR_OUTCOME_SELECTED
```

This is a source-bounded nonownership result, not a no-go theorem against empirical calibration. It
does not select an attachment type, value, history, branch population, prediction, or `X_max`.
