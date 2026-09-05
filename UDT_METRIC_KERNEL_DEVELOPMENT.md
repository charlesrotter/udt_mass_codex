# UDT: Development of the Metric and Reciprocal Kernel

*Accepted results, explicit premises, and open extensions*

## Edition record and authority

- **Edition date:** 2026-09-05
- **Scientific source snapshot:** `f23199e4a47aaf83acb9ea7d1ad382cd814159c2`
- **Manuscript state:** `FIDELITY_REVIEWED_FOUNDATIONS_AND_PILOT — PARTIAL_MANUSCRIPT`
- **Complete chapter coverage:** F1--F4 with G01/G02, and G350--G351
- **Supporting definitions used by the transfer pilot:** G348 and G349
- **Accepted successor acknowledged but not yet synthesized:** G352
- **Method revision used for drafting:** `657f5485d50fed4005455c33ebf1bf559b3ad516`

This manuscript is an explanatory synthesis. It is not canon, a scientific
source of record, or an upgrade to any source claim. `CANON.md` remains under
Charles's separate control. The exact registry and the cited evidence packages
remain authoritative for scientific grades; `LIVE.md` remains authoritative
for current operational status.

The declared foundations lineage is:

```text
F1 clock/ruler conversion interpretation
  + F2 Dual Reciprocity
  + F3 ordered composition and reversal
  + explicit positivity, continuity or measurability, and separate nontriviality inputs
  -> G01/G02 reciprocal character on supplied ordered depth
  + F4 declared quadratic/areal readout
  -> primary static-spherical metric form with supplied presentation phi(r)
```

The declared transfer-pilot lineage is:

```text
G348 metric null-screen and frequency geometry
  -> G349 finite labelled sheet-area geometry
  -> G350 two-ratio multiplicative transfer classification
  -> G351 owner-provisional conserved label measure
```

G352 is accepted at the selected snapshot and is named at the end of the pilot
so that this edition does not imply that G351 is the current endpoint. Its
argument is `NOT_YET_SYNTHESIZED` here. The completed pair kernel,
response-law development, and the rest of the causal development are also
`NOT_YET_SYNTHESIZED`; their headings below are a map for later work, not a
claim of coverage.

This edition excludes observational fitting, a selected spacetime history,
physical ray population, source physics, light or detector models, matter,
mass, actions, absolute scale, physical `X_max`, and canonization. It also
excludes protected local work and every unaccepted or unregistered branch.

### How status words are used

- **Provisional premise:** Charles has allowed the premise to be used in its
  stated scope. It is not derived and is not canon merely because consequences
  follow from it.
- **Conditional result:** the mathematics follows only when all stated inputs,
  domain conditions, and premises are supplied.
- **Externally accepted:** a bounded evidence package passed its recorded
  review. This does not make the result empirical fact or canon.
- **Open:** the cited sources do not select or establish the item.
- **Fidelity reviewed:** the explanation was checked against its sources; this
  label does not improve the grade of those sources.

## Reader orientation

This edition contains two completed, source-grounded parts of a larger account.
The first reconstructs the founding clock/ruler premises, the exact reciprocal
character they support on a supplied ordered depth, and the declared readout
that yields the primary static-spherical metric. It also records the crucial
boundary: the founding argument does not assign a depth to every physical
observer, event, separation, or history.

The second part is a later transfer pilot. Suppose a spacetime metric and a
labelled family of null paths have already been supplied. The metric then lets
us compare two things between two cuts of one retained path: frequency and
transverse sheet area. What rules can consistently transfer a scalar-valued
component using only those two ratios? And what additional restriction follows
if a finite amount assigned to the path labels is conserved?

The transfer answer comes in two logically separate steps.

1. G350 proves that every continuous, positive, local, multiplicative rule on
   its chosen full two-ratio domain is

   \[
   T(R,A)=R^pA^q,
   \]

   with two arbitrary real weights. Composition, reversal, and covariance do
   not choose either weight.

2. G351 adds a new owner-adopted provisional premise: a finite nonnegative
   measure on the supplied path labels is unchanged between source-free cuts.
   For the nonzero, absolutely continuous part on regular sheets, the same
   carried amount occupies metric area with density proportional to \(1/J\).
   Therefore its area weight is \(q=-1\). The observer/frequency weight \(p\)
   remains unselected.

In ordinary language, the metric tells us how a labelled sheet changes size,
but it does not say that anything is present on that sheet. The added
conservation premise says that the amount attached to the labels is retained.
Only then does spreading the same amount over a larger area force inverse-area
dilution. Neither step identifies the carried amount as light, energy,
probability, brightness, or detector response.

## 1. Definitions and conventions for the pilot

### 1.1 Supplied geometry and path family

The pilot begins downstream of several choices. It assumes:

- a smooth four-dimensional Lorentzian metric \(g\);
- a supplied labelled family of null paths and ordered cuts \(i,j,k\);
- a retained label \(\lambda\) referring to the same neighboring path at each
  cut;
- a future-directed null tangent \(k\) and supplied future-directed timelike
  endpoint observers \(u_i\);
- a common source-celestial presentation for the finite null sheet.

These are inputs to the result. G348 and G349 derive geometrical consequences
once they are supplied; they do not select the metric, the paths, their
population, or their physical interpretation.

### 1.2 Frequency and sheet-area state variables

At cut \(i\), the metric frequency read by observer \(u_i\) is

\[
\omega_i=-g(k,u_i)>0.
\]

Let \(X_i\) be the source-label-to-cut map. On the regular transverse stratum,
its metric sheet-area Jacobian is a finite positive number \(J_i>0\). In local
label coordinates \(\lambda\), the pulled-back metric area is

\[
d\alpha_i=J_i\,d\lambda.
\]

The finite sheet area counts sheets by preimage. It is not automatically the
area of the geometric image union when several labels reach the same image
point.

### 1.3 Ratio orientation and sewing

For transfer from cut \(i\) to cut \(j\), define

\[
R_{ji}=\frac{\omega_j}{\omega_i},
\qquad
A_{ji}=\frac{J_j}{J_i}.
\]

The first index is the destination and the second is the origin. With one
common path label and compatible cuts,

\[
R_{ki}=R_{kj}R_{ji},
\qquad
A_{ki}=A_{kj}A_{ji}.
\]

Reversal gives \(R_{ij}=R_{ji}^{-1}\) and
\(A_{ij}=A_{ji}^{-1}\). These identities are quotient algebra on supplied
endpoint state values. They do not choose a carried quantity or a transfer law.

The ratio \(A_{ji}\) is meaningful only when numerator and denominator refer to
the same intrinsic neighboring-ray family, common source presentation, and
retained label. It must not be assembled from unrelated skies, directions, or
path assignments.

### 1.4 Regularity and object identity

The pointwise density arguments below require the common screen-rank-two
stratum, where the relevant \(J_i\) are finite and strictly positive. This is a
transverse metric-rank condition, not merely ordinary coordinate rank.

The following objects remain distinct throughout this manuscript:

- metric frequency \(\omega_i\) and its ratio \(R_{ji}\);
- metric sheet-area Jacobian \(J_i\) and its ratio \(A_{ji}\);
- a measure \(\mu\) carried on label space;
- an ordinary density of only the absolutely continuous part of that measure;
- a scalar-valued component assigned an observer weight;
- any later physical interpretation such as light or energy.

Sharing a symbol or numerical value would not make two of these the same
physical object.

## 2. Foundations

### 2.1 Premise and convention ledger

The founding construction has several inputs with different epistemic roles.
They must not be collapsed into a single claim that "the metric was derived
from reciprocity alone."

| Item | Status in this account | Exact role |
|---|---|---|
| \(c_E\) | `OBSERVED` calibration plus proposed foundational interpretation | Converts the clock and ruler units in the paired description. |
| F1 | proposed foundational interpretation of the observed calibration | Treats \(L=c_ET\) and \(T=L/c_E\) as coequal clock/ruler conversions. |
| F2 | foundational Dual Reciprocity interpretation | Requires positional comparison to act contragrediently on the two conversion channels. |
| F3 | `POSIT` | Supplies additive composition and reversal of ordered comparison depth. |
| positivity and continuity or measurability | explicit mathematical assumptions | Exclude irregular characters and permit the exponential classification. |
| one nonidentity comparison | separate nontriviality input | Excludes the trivial representation, which also obeys composition. |
| sign and unit of \(\delta\) | `CHOSE` | Fix the convention for the additive logarithmic coordinate. |
| F4 | `DECLARED READOUT` / local Lorentzian continuity | Reads the transformed clock/ruler coframe quadratically and supplies the areal angular sector in the primary chart. |
| G01/G02 | `DERIVED` in their bounded scope | Give the reciprocal character and its matrix action once ordered depth is supplied. |

The later W1, W5, W6, quiet-GR, and response-law premises are not inputs to the
proof in this chapter. They refine the complete physical interpretation or
dynamics downstream. Their later adoption cannot be used retroactively to make
F1--F4 say more than their own argument establishes.

### 2.2 F1: the reciprocal \(c_E\) identity

The observed dimensional calibration is written

\[
L=c_ET,
\qquad
T=\frac{L}{c_E}.
\]

F1 interprets these as coequal conversions between clock and ruler channels.
The constant \(c_E\) has units of length per time. This identity aligns the
units, but by itself it does not imply a reciprocal squeeze, select a distance,
define a signal speed, determine a metric history, or give an equation for
\(\phi\).

### 2.3 F2: Dual Reciprocity supplies the inverse pairing

Write the clock/ruler column and a positive diagonal comparison as

\[
q=\begin{pmatrix}c_Edt\\dr\end{pmatrix},
\qquad
P(\Delta)=\begin{pmatrix}u(\Delta)&0\\0&v(\Delta)\end{pmatrix}.
\]

Dual Reciprocity preserves the off-diagonal evaluation pairing

\[
K=\begin{pmatrix}0&1\\1&0\end{pmatrix},
\qquad
P(\Delta)^T K P(\Delta)=K.
\]

Direct multiplication gives

\[
P^TKP
=\begin{pmatrix}0&u(\Delta)v(\Delta)\\
u(\Delta)v(\Delta)&0\end{pmatrix},
\]

and therefore

\[
\boxed{u(\Delta)v(\Delta)=1.}
\]

This is the step that makes the two channels inverse rather than equal. If one
asked only for ordinary covariance of the conversion map, the corresponding
condition would give \(u=v\), not \(uv=1\). The reciprocal character therefore
uses F2; it does not follow from the numerical existence of \(c_E\).

### 2.4 F3: composition turns the inverse pair into an exponential

F3 supplies the ordered comparison law

\[
P(\Delta_1+\Delta_2)=P(\Delta_1)P(\Delta_2),
\qquad
P(-\Delta)=P(\Delta)^{-1}.
\]

Because \(u>0\), \(\log u\) is additive. Under the stated continuity or
measurability condition, an additive real character is linear. After choosing
the sign and unit of its additive coordinate and using \(v=u^{-1}\), the
nontrivial branch is

\[
\boxed{
D(\delta)=\operatorname{diag}(e^{-\delta},e^{+\delta})
}
\]

with

\[
D(\delta_2)D(\delta_1)=D(\delta_1+\delta_2),
\qquad
D(-\delta)=D(\delta)^{-1}.
\]

The result is a one-dimensional reciprocal representation. Nontriviality is
not a consequence of the group laws: \(D=I\) would satisfy them too.

### 2.5 F4: from reciprocal coframe to the primary metric

F4 is the declared geometrical readout. It says to read the transformed clock
and ruler coframe quadratically with Lorentzian sign, and, in the bounded
static-spherical chart, to use \(r\) as areal radius. When the local
presentation potential is denoted by \(\phi(r)\), this gives

\[
\boxed{
ds^2=-e^{-2\phi(r)}c_E^2dt^2
     +e^{+2\phi(r)}dr^2
     +r^2d\Omega^2.
}
\]

Thus the metric form follows from F1--F3 only after F4's readout and chart
choice are supplied. The formula fixes how a supplied \(\phi\) enters the
clock and radial ruler coefficients. It does not, at this stage, determine
which function \(\phi(r)\) a physical spacetime realizes.

### 2.6 Maximum conclusion of the founding premise chain

The bounded founded implication is

\[
\boxed{
\text{supplied ordered depth }\delta
\longmapsto
D(\delta)=\operatorname{diag}(e^{-\delta},e^{+\delta}).
}
\]

Together with F4, a supplied primary presentation \(\phi(r)\) is read as the
metric above. The reverse physical assignment

\[
\boxed{
(\text{events, observers, separation, history})
\longmapsto \delta
}
\]

is not contained in this proof. Neither is a field equation, source, action,
matter model, path population, absolute scale, \(X_{\max}\), or observational
prediction.

## 3. Reciprocal construction

### 3.1 What the reciprocal character fixes

The matrix \(D(\delta)\) has determinant one. One channel acquires
\(e^{-\delta}\), the other \(e^{+\delta}\), and their product remains one.
Composition adds depths and reversal negates the ordered depth. These are exact
algebraic properties for every supplied \(\delta\).

In the primary static-spherical presentation, it is useful to write

\[
f=e^{-2\phi}>0,
\]

so that

\[
ds^2=-f(r)c_E^2dt^2+f(r)^{-1}dr^2+r^2d\Omega^2.
\]

The reciprocal clock-radius block has determinant \(-c_E^2\). Consequently
the full coordinate volume density is

\[
\sqrt{-g}=c_Er^2\sin\theta.
\]

This cancellation is an algebraic consequence of the reciprocal radial block.
It is not a field equation and does not select \(f\) or \(\phi\).

### 3.2 The representation current, correctly typed

For

\[
S(\phi)=\operatorname{diag}(e^{-\phi},e^{+\phi}),
\]

the matrix-valued one-form is

\[
\mathcal J=S^{-1}dS=\operatorname{diag}(-d\phi,d\phi).
\]

Its representation quadratic form is the symmetric tensor statement

\[
\boxed{
\frac12\operatorname{Tr}(\mathcal J\otimes\mathcal J)
=d\phi\otimes d\phi.
}
\]

After evaluation on a tangent vector \(X\),

\[
\frac12\operatorname{Tr}(\mathcal J(X)^2)=(X\phi)^2.
\]

A scalar contraction such as
\(g^{ab}\partial_a\phi\partial_b\phi\) additionally uses the spacetime metric.
Exterior multiplication instead gives \(\mathcal J\wedge\mathcal J=0\) because
the reciprocal Lie algebra is abelian. None of these identities promotes the
quadratic form into a physical action, energy, or equation of motion.

### 3.3 Four related quantities that must remain distinct

The current source hierarchy distinguishes:

- \(\delta_{AB}\): a supplied signed depth on an ordered pair;
- \(\phi(r)\): a pointwise presentation potential for a supplied primary
  metric;
- \(\widehat\Phi_{\rm pair}\): the terminal scalar read from a supplied,
  regular, calibrated completed pair metric;
- \(V(A)\): an endpoint potential only on branches where the pair-depth law is
  endpoint exact.

They can coincide in a matched calibrated primary radial reduction. Their
notation and occasional numerical agreement do not establish a universal
identity.

In particular, pair reversal is

\[
(g_\phi,A,B,\delta_{AB})
\longmapsto
(g_\phi,B,A,-\delta_{AB}).
\]

It leaves the supplied metric profile \(\phi(r)\) unchanged. Replacing the
whole metric profile by its conjugate, \(g_\phi\mapsto g_{-\phi}\), is a
different operation and generally changes the geometry. The sign of an
ordered arrow is therefore not, by itself, a label for a micro- or
cosmological regime; physical regime language needs an owned scale-to-profile
assignment.

### 3.4 Why a pointwise factorization does not own physical depth

The current registered G01/G02 audit tests whether the complete factorized coframe can
universally recover one preferred pointwise \(\phi\). Let \(z=e^\phi>0\), use
the multiplicative notation

\[
D_\times(z)=\operatorname{diag}(z^{-1},z),
\]

and write a supplied complete coframe as

\[
\vartheta=D_\times(z)\,\bar\vartheta.
\]

For any positive local function \(h\), the simultaneous replacement

\[
z'=zh,
\qquad
\bar\vartheta'=D_\times(h)^{-1}\bar\vartheta
\]

leaves the complete coframe unchanged:

\[
D_\times(z')\bar\vartheta'=D_\times(z)\bar\vartheta=\vartheta.
\]

Thus the same completed geometry can admit different reciprocal
factorizations unless an additional reference or physical depth owner is
supplied. This does not erase \(\phi\) as the logarithmic coordinate of the
representation. It says that a chosen pointwise factor is not automatically a
universal observable extracted from arbitrary complete geometry.

### 3.5 A real but branch-local metric owner

On a stationary branch possessing an intrinsic timelike Killing line \(K\),
define its lapse norm

\[
N(x)=\sqrt{-g(K,K)}\big|_x.
\]

For ordered points \(p,q\), the metric then supplies

\[
q_K(p,q)=\frac{N(q)}{N(p)},
\qquad
\delta_K(p,q)=-\log q_K(p,q)
=\log\!\frac{N(p)}{N(q)}.
\]

This ratio composes, reverses, and is unchanged by a constant rescaling of
\(K\). It is therefore a genuine metric-native depth owner on that stationary
stratum. It is not a universal construction for nonstationary geometries or
arbitrary observer pairs, where the required intrinsic Killing line may not
exist.

### 3.6 What calibration and transport do not add

Three tempting identifications fail at the type boundary.

First, \(c_E\) matches clock and ruler units but does not normalize the
dimensionless depth. The family

\[
D_a(\Delta)=\operatorname{diag}(e^{-a\Delta},e^{+a\Delta})
\]

obeys pairing preservation, composition, and reversal for every constant
\(a\). A physical separation-to-depth attachment must supply what the abstract
character does not.

Second, signed ordered depth and nonnegative symmetric separation cannot be
the same scalar for a nonzero pair: reversal requires
\(\delta_{BA}=-\delta_{AB}\), whereas separation magnitude satisfies
\(\rho(B,A)=\rho(A,B)>0\). A physical construction may need both a magnitude
and an oriented lift.

Third, Levi-Civita transport preserves the Lorentz metric, whereas nonzero
reciprocal dilation does not act as a Lorentz isometry of the unbalanced
clock/ruler interval. The off-diagonal \(K\) above is the dual evaluation
pairing, not the local spacetime interval. Ordinary metric transport cannot be
renamed the missing depth law.

### 3.7 Boundary to the completed kernel

W1 later places Dual Reciprocity after the full angular, screen, shift, and
mixing pullback. W5 later gives a working physical interpretation to the
complete projective pair state, and W6 distinguishes non-signalling
co-presence from causal response. Those working clarifications do not change
F1--F4, \(D(\delta)\), or the primary metric, and they do not supply a general
event/observer/path-to-depth assignment.

Their detailed proofs and complete pair formulas belong to Section 4 and are
`NOT_YET_SYNTHESIZED` in this edition. The safe join is therefore only this:
the founding character is the algebraic reciprocal core later used by a
supplied completed-pair construction; it is not yet being identified with a
null-path frequency ratio, physical distance, or signal speed.

## 4. Completed metric and pair kernel

`NOT_YET_SYNTHESIZED`

This part will place angular, screen, shift, and mixing contributions before
the terminal reciprocal readout and preserve the conditional status of the
completed-pair evaluator.

## 5. Response-law development

`NOT_YET_SYNTHESIZED`

This part will state adopted premises at their point of entry, reconstruct the
bounded curvature response, and keep selected initial data, global history,
topology, occupancy, and scale open unless their cited sources say otherwise.

## 6. Causal and area geometry

`PARTIAL — SUPPORTING DEFINITIONS ONLY`

G348 works with an arbitrary supplied smooth four-dimensional Lorentzian metric
and a regular affine null segment. It develops the quotient screen, Jacobi
transport, endpoint frequency, rank loss, and caustic behavior. G349 passes
from infinitesimal screen geometry to a supplied finite compact labelled null
map and defines the positive metric sheet-area Jacobian used here.

These results are metric-derived, but they are general Lorentzian geometry, not
features shown to distinguish UDT from every other spacetime theory. They do
not supply a finite beam population, transported physical content, brightness,
luminosity, distance law, selected history, or scale.

A caustic here is loss of transverse quotient-screen rank. It need not be a
spacetime singularity, and it is not the same as ordinary endpoint-map rank:
the ordinary map can retain rank two while its restored tangent plane is
null-degenerate and has zero metric two-area. The underlying labelled map and a
measure pushed through it can remain meaningful even when a regular
two-dimensional density fails.

**Contribution to the pilot:** G348 and G349 supply \(\omega_i\), \(J_i\), the
regular stratum, and the sheet-versus-image distinction. They do not supply the
transfer multiplier classified by G350 or the conserved measure posited by
G351.

**Unresolved join:** the physical population of paths and the physical meaning
of any content carried on them remain open.

## 7. Conservation and carried readouts

### 7.1 G350: classify rather than guess the transfer rule

#### Question and inputs

G350 chooses a deliberately bounded candidate class. A transfer multiplier

\[
T:\mathbb R_{+}\times\mathbb R_{+}\longrightarrow\mathbb R_{+}
\]

may depend only on the two local ratios \((R,A)\). It is required to be
continuous, positive, normalized at identity, and exactly multiplicative under
sewing:

\[
T(R_2R_1,A_2A_1)=T(R_2,A_2)T(R_1,A_1).
\]

The quantifier is over the chosen full abstract domain
\(\mathbb R_+^2\), where \(R\) and \(A\) are independent positive
coordinates. This is a classification domain. G350 does **not** prove that one
particular metric history physically realizes every pair in that domain. If a
rule were required only on a smaller realized subset, the same reasoning would
classify at most the subgroup it generates unless an additional density or
attainability result were supplied.

#### Character theorem

Set

\[
f(x,y)=\log T(e^x,e^y).
\]

Positivity makes the logarithm defined, and multiplicative sewing becomes the
additive equation

\[
f(z+w)=f(z)+f(w), \qquad z,w\in\mathbb R^2.
\]

Continuity rules out discontinuous Cauchy solutions. If
\(p=f(1,0)\) and \(q=f(0,1)\), additivity first fixes rational multiples,
continuity extends them to real multiples, and coordinate decomposition gives

\[
f(x,y)=px+qy.
\]

Therefore

\[
\boxed{T(R,A)=R^pA^q}, \qquad p,q\in\mathbb R.
\]

Conversely, every real pair \((p,q)\) gives a continuous positive normalized
multiplicative rule, so the family is complete within the chosen class.

Identity and reversal add no selector. Multiplicativity and positivity already
give \(T(1,1)=1\), while

\[
T(R^{-1},A^{-1})=T(R,A)^{-1}
\]

holds for every character. Endpoint-observer covariance likewise types a
choice rather than making it. If an endpoint observer change rescales
\(\omega_i\) by \(D_i>0\), then a component declared to have weight \(p\)
must transform as \(C_i' = D_i^pC_i\). This works for every real \(p\).

#### Meaning and boundary

G350 replaces an assumed transfer formula with an exhaustive answer inside one
explicit class, but it proves nonuniqueness rather than a physical light law.
Rules such as \(1\), \(R\), \(A\), \(A^{-1}\), \(RA^{-1}\), and
\(R^2A^{-1}\) all satisfy the structural requirements.

The result is not exhaustive over endpoint coboundaries, nonlocal rules,
additive or interacting content, phase-dependent laws, or field-valued
transport. It supplies no nonzero source content and no rule for combining
different labels.

### 7.2 The new premise introduced by G351

G351 does not obtain conservation from the metric, the reciprocal kernel, or
G350. It uses the following **owner-adopted provisional premise** in a bounded
source-free setting:

> A supplied populated labelled null family carries a finite, nonnegative,
> countably additive measure \(\mu\) on label space, and the same measure is
> retained at every cut when no sources or sinks are present.

This premise does not create \(\mu\), choose its magnitude or support, decide
which labels Nature populates, or state what the measure physically represents.
It says only that a supplied measure is cut-independent in the declared
source-free regime.

For each cut map \(X_i\), the pushforward

\[
(X_i)_*\mu(B)=\mu(X_i^{-1}(B))
\]

is consequently well defined for measurable image sets. Pushforward retains
label multiplicity because it counts preimages.

### 7.3 How inverse area follows on the regular absolutely continuous part

Work in a two-dimensional regular label chart with coordinate measure
\(d\lambda\). Decompose the finite measure into its absolutely continuous and
singular parts:

\[
\mu=\mu_{\mathrm{ac}}+\mu_{\mathrm{s}},
\qquad
d\mu_{\mathrm{ac}}=s(\lambda)\,d\lambda,
\qquad
\mu_{\mathrm{s}}\perp d\lambda.
\]

At a regular cut,

\[
d\alpha_i=J_i\,d\lambda, \qquad J_i>0.
\]

Only the absolutely continuous component necessarily has an ordinary density
with respect to this area measure. Its Radon–Nikodym density is

\[
n_i=\frac{d\mu_{\mathrm{ac}}}{d\alpha_i}
    =\frac{s}{J_i}
\quad\text{almost everywhere}.
\]

Because the conserved label-space density \(s\) is the same at both cuts,

\[
\boxed{n_j=\frac{J_i}{J_j}n_i=A_{ji}^{-1}n_i}
\quad\text{almost everywhere}.
\]

This equality is the safe general statement: it never divides by \(n_i\).
Only on support where \(n_i\ne0\) may it be rewritten as

\[
\frac{n_j}{n_i}=A_{ji}^{-1}.
\]

Thus the area exponent is \(q=-1\) for a nonzero absolutely continuous regular
density, conditional on the new conservation premise.

To compare this with G350, introduce a positive reference frequency
\(\omega_*\) and define a component of **declared** observer weight \(p\):

\[
C_i=\left(\frac{\omega_i}{\omega_*}\right)^p n_i.
\]

The reference makes real powers dimensionless and cancels from the transfer
ratio; it is not a selected physical scale. Then

\[
\frac{C_j}{C_i}=R_{ji}^{p}A_{ji}^{-1}
\]

where the ratio is taken on nonzero support. In G350's full independent
positive domain, requiring the observer-weight-stripped sheet measure to be
conserved forces the residual

\[
R^{a-p}A^{q+1}
\]

to equal one for all independent positive \(R,A\). Varying \(R\) with \(A=1\)
forces \(a=p\); varying \(A\) with \(R=1\) forces \(q=-1\). Conservation fixes
the area weight inside this class. It still does not choose \(p\).

### 7.4 Zero, singular components, multiplicity, and caustics

These qualifications are part of the theorem, not optional footnotes.

**Zero content.** If \(\mu=0\), every regular density is zero and the
division-free equality remains true. Zero supplies no exponent witness: many
transfer laws map zero to zero.

**Singular content.** A finite measure need not possess an ordinary area
density. For example, a unit atom at one label gives positive mass to a
singleton that has zero regular sheet area. No ordinary density integrated
against that area can represent the atom. The singular component therefore has
no ordinary density exponent \(q\).

**Many-to-one maps.** If two labels of masses \(m_1,m_2\) reach the same image
point, the pushforward assigns their sum there. A geometric image-union area,
which counts the location only once, loses this multiplicity. This is
measure-theoretic preimage accounting, not a detector law or a rule for phase,
interference, or incoherent addition.

**Caustics.** When transverse rank is lost, \(J\) can approach zero. A regular
density \(s/J\) can diverge or turn into a singular measure even though the
finite label measure and its pushforward remain defined. G351 does not extend
an everywhere-finite pointwise inverse-area density through every caustic, nor
does it classify simultaneous zero-area limits.

### 7.5 What G351 changes, and what remains open

G351 changes exactly one part of G350's nonuniqueness: conditional on the new
conserved-label-measure premise, the ordinary regular density has inverse-area
weight. It does not alter the metric, reciprocal kernel, angular sector, or
bounded response equation.

It does **not** select:

- the observer/frequency weight \(p\);
- a physical identity for \(\mu\) or \(C\);
- a source magnitude, source distribution, or populated label set;
- emission, absorption, phase, interference, cross-label aggregation, or a
  detector response;
- light, photon energy, brightness, flux, luminosity, probability, or distance;
- a ray route, observer germ, metric history, topology, occupancy, matter,
  mass, action, stability, observation, absolute scale, physical `X_max`, or
  canon.

The executable checks in the source packages are regression and corroborating
evidence. The analytic character theorem and measure-theoretic argument carry
the mathematical conclusion. External acceptance is evidence of bounded
review, not experimental confirmation.

### 7.6 Transition to the accepted but unsynthesized readout step

At the selected snapshot, G352 is externally accepted in a bounded conditional
scope. Its two additional inputs must remain separate. First, Charles
provisionally adopted the clock-rate carried-measure readout premise: a supplied
conserved sequence of causal phase/event crossings is read as crossings per
observer proper time per metric sheet area. Second, G352 chose a bounded
mathematical realization using continuous total phase variation, fixed common
phase spacing, and a phase-independent nonnegative product with the same G351
label measure on each phase slice. The metric and G351 do not derive that
realization. Conditional on both inputs, and within G350's full independent
positive character domain, G352 fixes \(p=1\) and retains \(q=-1\). Literal
atomic crossings and other readouts remain distinct. G352 does not identify the
content as light, energy, a detector signal, or an observational distance.

`NOT_YET_SYNTHESIZED`: this edition has not reconstructed G352's definitions,
proof, degeneracy conditions, or evidence. The strongest safe transition is
therefore: G351 leaves \(p\) open; an accepted later result reports that one
separately chosen clock-rate readout fixes it conditionally. That later choice is
not retroactive evidence that G350 or G351 selected \(p\).

## 8. Open physical connections

The pilot reaches a mathematically controlled transfer family and one
premise-conditional inverse-area density law. A physical prediction chain still
requires documented answers to at least the following joins:

1. What physical entity, if any, does the carried label measure represent?
2. What produces nonzero content and determines its support?
3. Which labels and paths are physically populated?
4. Which observer-weighted readout corresponds to an actual measurement?
5. How do distinct labels combine, including phase or interference if those
   concepts are eventually present?
6. What happens at emission, absorption, caustics, and detector registration?
7. Which admissible metric history and scale are used?

Until these joins are supplied or derived in their own accepted scopes,
inverse-area dilution is not by itself a native law of luminosity or a
supernova-distance prediction.

## Appendix A. Pilot coverage and source map

All paths below are relative to the repository root and refer to scientific
snapshot `f23199e4a47aaf83acb9ea7d1ad382cd814159c2`.

### G01 — `MAIN_ARGUMENT`, `FIDELITY_REVIEWED`

- **Manuscript use:** Sections 2.6 and 3.3--3.7, especially the exact
  input/output boundary, pointwise presentation freedom, and stationary
  Killing branch.
- **Source:**
  [founding ownership audit](udt_founding_phi_ownership_morphism_audit_2026-08-05/AUDIT_REPORT.md),
  with the current premise language and corrected current typing in
  [founding.md](founding.md).
- **Dependencies actually used:** supplied ordered depth; positive reciprocal
  character; supplied factorized complete coframe; and, only for the positive
  branch-local result, a stationary metric with an intrinsic timelike Killing
  line.
- **Exact source grade:**

```text
DERIVED_RECIPROCAL_CHARACTER_ON_SUPPLIED_ORDERED_DEPTH
```

- **Open scope retained from the exact registry row:** general
  observer/event/path-to-depth law; signed-orientation/nonnegative-magnitude
  join; endpoint-exact potential branches; and physical normalization/profile.

### G02 — `MAIN_ARGUMENT`, `FIDELITY_REVIEWED`

- **Manuscript use:** Sections 2.3--2.6 and 3.1--3.2, the exact matrix
  character and its algebraic consequences on supplied depth.
- **Source:**
  [G02 exact derivation](udt_founding_phi_ownership_morphism_audit_2026-08-05/EXACT_DERIVATION.md),
  with the direct F1--F4 assumption ledger in
  [the founding-postulate derivation](UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md)
  read through the current corrections in [founding.md](founding.md).
- **Dependencies actually used:** F1 conversion interpretation, F2
  contragredient pairing, F3 composition and reversal, positivity, continuity
  or measurability, a nonidentity input, and chosen sign/unit convention; F4
  enters only for the primary metric readout.
- **Exact source grade:**

```text
DERIVED_DELTA_MAPS_TO_DIAG_EXP_MINUS_DELTA_EXP_PLUS_DELTA
```

- **Open scope retained from the exact registry row:** physical map to
  \(\delta\); physical complete-pair cocycle selection; degeneracy/global-loop
  continuation; and complete realization.
- **Historical-source correction:** the older founding-postulate document is
  used for its bounded assumption ledger and direct matrix derivation, not for
  its obsolete review-state header or its untyped shorthand
  \(\tfrac12\operatorname{Tr}(\mathcal J^2)=d\phi^2\). Section 3.2 follows the
  current symmetric-tensor typing in `founding.md`.

### G348 — `SUPPORTING_LEMMA`, `PARTIAL`

- **Manuscript use:** Section 1 and Section 6 definitions of metric frequency,
  quotient screen, regular rank, and caustic boundary.
- **Source:**
  [G348 exact derivation](udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/EXACT_DERIVATION.md),
  especially Sections 1, 3, 5, and 6; bounded status in the
  [G348 audit report](udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/AUDIT_REPORT.md).
- **Dependencies actually used:** supplied smooth four-dimensional Lorentzian
  metric, regular affine null segment, null tangent, endpoint observers, and
  quotient-screen construction.
- **Exact source grade:**

```text
EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED__PREREGISTERED_AT_17C35CC6__CROSSING_ALTERNATIVES_REFINED_OUTCOME_UNSEEN_AT_23E50369__FRESH_GPT56SOL_AUTHENTICATED_33_PAYLOADS_AND_ACCEPTED_WITH_NO_MATHEMATICAL_DEFECT_OR_REQUIRED_REPAIR__39542_PRODUCTION_CHECKS__9759_IMPLEMENTATION_DISTINCT_SMOOTH_TIDE_RK4_AND_RAPIDITY_CHECKS__21_OF_21_HOSTILE_MUTATIONS_REPORTED_CAUGHT__EXTERNAL_SCRATCH_RECONSTRUCTION_PASS__19_POSTREVIEW_AGGREGATE_NO_WRITE_AND_RETURN_AUTHENTICATION_GATES__ARBITRARY_SMOOTH_4D_LORENTZIAN_METRIC_AND_REGULAR_AFFINE_NULL_SEGMENT__LEVI_CIVITA_QUOTIENT_CONNECTION__SELF_ADJOINT_TIDE__SYMPLECTIC_PHASE_FLOW_COMPOSITION_AND_REVERSAL__SOURCE_FREQUENCY_SQUARED_DIRECTIONAL_AREAS__ARBITRARY_FINITE_TIMELIKE_ENDPOINT_OBSERVER_COVARIANCE__WRONSKIAN_FORCES_DETERMINANT_ZERO_ORDER_EQUAL_TO_KERNEL_DIMENSION__RANK_ONE_SIMPLE_SIGN_FLIP__RANK_ZERO_DOUBLE_NO_SIGN_FLIP__TYPE_I_GENERATOR_INVERSE_SCALAR_AND_STATIONARY_SEWING_ONLY_CHARTWISE__GENERAL_LORENTZIAN_GEOMETRY_NOT_UNIQUELY_UDT__IMPLEMENTATION_DISTINCT_NOT_PREMISE_INDEPENDENT__UNSIGNED_CHECKSUM_GIT_CHRONOLOGY_AND_TAUTOLOGICAL_HOSTILE_CONTROLS_RETAINED_AS_NONBLOCKING_EVIDENCE_CAVEATS__NO_FINITE_BEAM_LIGHT_TRANSFER_DISTANCE_POPULATION_HISTORY_SCALE_XMAX_OR_CANON__METRIC_KERNEL_ANGULAR_EQUATION_UNCHANGED
```

### G349 — `SUPPORTING_LEMMA`, `PARTIAL`

- **Manuscript use:** Sections 1 and 6 definition of finite metric sheet-area
  Jacobian, common label presentation, multiplicity, and image-union boundary.
- **Source:**
  [G349 exact derivation](udt_g349_finite_null_wavefront_patch_area_2026-09-04/EXACT_DERIVATION.md),
  especially Sections 1–5, 7, and 8; bounded status in the
  [G349 audit report](udt_g349_finite_null_wavefront_patch_area_2026-09-04/AUDIT_REPORT.md).
- **Dependencies actually used:** supplied finite compact celestial patch,
  source observer, labelled null family, affine cut, and metric screen area.
- **Exact source grade:**

```text
EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED_AFTER_PREREGISTERED_R1_R4_REPAIRS__PREREGISTERED_AT_84CB5264__FIRST_HOSTILE_20_OF_21_AND_BEHAVIORAL_CUSP_REPAIR_AT_134ECD4A_RETAINED__FRESH_GPT56SOL_INITIAL_REVIEW_ACCEPTED_WITH_CAVEATS_AND_MIXED_RANK_DEFECT__R1_R4_PREREGISTERED_AT_C2967132__REPAIR_FOLLOWUP_AUTHENTICATED_37_PAYLOADS_AND_ACCEPTED_WITH_NO_REMAINING_DEFECT__44321_PRODUCTION_ASSERTIONS__14321_IMPLEMENTATION_DISTINCT_ASSERTIONS__22_OF_22_HOSTILE_MUTATIONS_CAUGHT__21_OF_21_AGGREGATE_NO_WRITE_GATES__FINITE_COMPACT_SUPPLIED_NULL_EXPONENTIAL_MAP__CUT_GRADIENT_CANCELS_FROM_METRIC_GRAM_FORM__TRANSVERSE_SCREEN_RANK_DISTINCT_FROM_ORDINARY_MAP_RANK__SPACELIKE_MULTIPLICITY_WEIGHTED_SHEET_AREA__GEOMETRIC_UNION_AREA_REQUIRES_GLOBAL_PREIMAGE_IDENTIFICATION__ORDINARY_RANK_TWO_NULL_SHEETS_HAVE_ZERO_METRIC_AREA__CAUSTICS_FOLDS_CUSPS_ORIENTATION_OBSERVER_AND_PATH_LABEL_BRANCHES_RETAINED__GENERAL_LORENTZIAN_GEOMETRY_NOT_UNIQUELY_UDT__NO_LIGHT_TRANSFER_DISTANCE_POPULATION_HISTORY_SCALE_XMAX_OR_CANON__METRIC_KERNEL_ANGULAR_EQUATION_UNCHANGED
```

### G350 — `MAIN_ARGUMENT`, `FIDELITY_REVIEWED`

- **Manuscript use:** Section 7.1 two-ratio character classification and
  nonselection of weights.
- **Source:**
  [G350 exact derivation](udt_g350_frequency_area_carried_content_ownership_2026-09-05/EXACT_DERIVATION.md),
  especially Sections 1–12; bounded status and review caveats in the
  [G350 audit report](udt_g350_frequency_area_carried_content_ownership_2026-09-05/AUDIT_REPORT.md)
  [G350 initial external review](udt_g350_frequency_area_carried_content_ownership_2026-09-05/EXTERNAL_REVIEW_RESPONSE.md),
  and [G350 accepted repair follow-up](udt_g350_frequency_area_carried_content_ownership_2026-09-05/EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md).
- **Dependencies actually used:** accepted G348/G349 metric frequency and
  labelled sheet-area state values; chosen full abstract positive two-ratio
  domain; positivity, continuity, locality, and exact multiplicative sewing.
- **Exact source grade:**

```text
EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED_AFTER_PREREGISTERED_R1_R4_REPAIRS__PREREGISTERED_AT_2B050A38__FRESH_GPT56SOL_AUTHENTICATED_37_PAYLOADS_AND_ACCEPTED_WITH_TWELVE_PRECISION_AND_EVIDENCE_CAVEATS__R1_R4_REPAIRS_PREREGISTERED_BEFORE_EXECUTION__REPAIR_FOLLOWUP_AUTHENTICATED_48_PAYLOADS_AND_ACCEPTED_WITH_NO_REMAINING_DEFECT_OR_SCIENTIFIC_REGRESSION__120010_FROZEN_PRODUCTION_CHECKS__35295_IMPLEMENTATION_DISTINCT_EXACT_FORMULA_CHECKS__HISTORICAL_25_OF_25_ROUTE_LIMITED_TO_HARD_CODED_CONTRACT_ENUMERATION__14_OF_14_SEMANTIC_MUTANTS__4000_OF_4000_REPAIR_NUMERICS_WITH_2000_WIDE_LOG_CASES__33_OF_33_FINAL_AGGREGATE_NO_WRITE_GATES__CONTINUOUS_POSITIVE_LOCAL_TWO_RATIO_MULTIPLICATIVE_CLASS_ON_FULL_ABSTRACT_RPLUS_SQUARED_DOMAIN__T_EQUALS_R_TO_P_A_TO_Q_FOR_ARBITRARY_REAL_P_Q__IDENTITY_REVERSAL_SEWING_AND_OBSERVER_COVARIANCE_SELECT_NO_WEIGHT__INVERSE_AREA_REQUIRES_NEW_UNADOPTED_CONSERVATION_PREMISE__NONZERO_SOURCE_CAUSTIC_CONTINUATION_AND_CROSS_LABEL_AGGREGATION_REMAIN_SUPPLIED_OR_OPEN__NO_CARRIED_FIELD_LIGHT_FLUX_LUMINOSITY_DISTANCE_HISTORY_SCALE_XMAX_OR_CANON__METRIC_KERNEL_ANGULAR_EQUATION_UNCHANGED
```

### G351 — `MAIN_ARGUMENT`, `FIDELITY_REVIEWED`

- **Manuscript use:** Sections 7.2–7.5 owner-provisional conservation premise,
  inverse-area density, and degeneracy limits.
- **Source:**
  [G351 exact derivation](udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/EXACT_DERIVATION.md),
  especially Sections 1–9; bounded status and review caveats in the
  [G351 audit report](udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/AUDIT_REPORT.md)
  and [G351 external review](udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/EXTERNAL_REVIEW_RESPONSE.md).
- **Dependencies actually used:** G350 character family; finite nonnegative
  countably additive label measure supplied under the owner-provisional
  source-free conservation premise; regular positive sheet Jacobian; Lebesgue
  decomposition and Radon–Nikodym differentiation.
- **Exact source grade:**

```text
EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED_ON_OWNER_ADOPTED_PROVISIONAL_PREMISE__PREREGISTERED_AT_42E48241__R1_R5_REPAIRS_PREREGISTERED_BEFORE_EXECUTION__FRESH_GPT56SOL_AUTHENTICATED_42_PAYLOADS_IN_EXACT_44_FILE_INTAKE__INDEPENDENT_ANALYTIC_RECONSTRUCTION_AND_45_OF_45_REPLAY__60325_OF_60325_PRODUCTION__11290_OF_11290_IMPLEMENTATION_DISTINCT__12_OF_12_HOSTILE__STANDARD_FINITE_NONNEGATIVE_COUNTABLY_ADDITIVE_LABEL_MEASURE__NONZERO_ABSOLUTELY_CONTINUOUS_REGULAR_DENSITY_N_EQUALS_S_OVER_J__AREA_TRANSFER_A_INVERSE__WITHIN_G350_FULL_INDEPENDENT_POSITIVE_CHARACTER_DOMAIN_T_P_EQUALS_R_TO_P_A_INVERSE_AND_Q_EQUALS_MINUS_ONE__P_REMAINS_ARBITRARY_DECLARED_OBSERVER_WEIGHT__FINITE_MEASURE_AND_PUSHFORWARD_SURVIVE_CAUSTIC_RANK_LOSS__SINGULAR_PART_HAS_NO_ORDINARY_DENSITY_EXPONENT__EXECUTABLE_COUNTS_ARE_REGRESSION_EVIDENCE_NOT_ANALYTIC_PROOF__DOCUMENTARY_CHRONOLOGY_NOT_TRUSTED_TIMESTAMP__NO_SOURCE_POPULATION_CROSS_LABEL_PHYSICS_LIGHT_DISTANCE_HISTORY_SCALE_XMAX_MATTER_OR_CANON__METRIC_KERNEL_ANGULAR_EQUATION_UNCHANGED
```

### G352 — `BOUNDARY_RESULT`, `NOT_YET_SYNTHESIZED`

- **Manuscript use:** Section 7.6 current-successor notice only.
- **Source:**
  [G352 exact derivation](udt_g352_clock_rate_carried_measure_readout_2026-09-05/EXACT_DERIVATION.md),
  [G352 audit report](udt_g352_clock_rate_carried_measure_readout_2026-09-05/AUDIT_REPORT.md),
  [G352 initial external review](udt_g352_clock_rate_carried_measure_readout_2026-09-05/EXTERNAL_REVIEW_RESPONSE.md),
  and [G352 accepted repair follow-up](udt_g352_clock_rate_carried_measure_readout_2026-09-05/EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md).
- **Dependencies actually asserted here:** only the exact accepted registry
  status; this manuscript has not reconstructed the source argument.
- **Exact source grade:**

```text
EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED_ON_OWNER_ADOPTED_PROVISIONAL_PREMISE__PREREGISTERED_AT_F5EE3393__R1_SIGN_REPAIR_PREREGISTERED_AT_14AFC199__R2_REPAIRS_PREREGISTERED_AT_B0BC9F24__FRESH_REVIEW_REPAIR_RETURNED__SEALED_R2_GPT56SOL_AUTHENTICATED_42_PAYLOADS_IN_EXACT_44_FILE_INTAKE__R2_REPAIR_COMPLETION_ACCEPTED__103648_OF_103648_PRODUCTION_OVER_2400_DISTINCT_STATES__73889_OF_73889_IMPLEMENTATION_DISTINCT_OVER_2700_DISTINCT_STATES__18_OF_18_HOSTILE__49_OF_49_FINAL_AGGREGATE__OWNER_PROVISIONAL_CLOCK_RATE_READOUT__CHOSE_CONTINUOUS_TOTAL_PHASE_VARIATION_AND_PHASE_INDEPENDENT_NONNEGATIVE_PRODUCT_MEASURE__NONZERO_ABSOLUTELY_CONTINUOUS_REGULAR_DENSITY_GAMMA_EQUALS_OMEGA_OVER_DELTATHETA_TIMES_S_OVER_J__T_CLOCK_EQUALS_R_A_INVERSE__P_EQUALS_ONE_AND_Q_EQUALS_MINUS_ONE_UNIQUE_ONLY_FOR_THIS_READOUT_IN_G350_FULL_INDEPENDENT_POSITIVE_CHARACTER_DOMAIN__ATOMIC_CROSSINGS_P_ZERO_AND_OTHER_READOUTS_REMAIN_DISTINCT__MEASURE_VALUED_CAUSTIC_FORM_FINITE_ONLY_UNDER_FREQUENCY_INTEGRABILITY__EXECUTABLE_COUNTS_REGRESSION_NOT_ANALYTIC_PROOF__UNSIGNED_COSEALED_MANIFEST_NOT_TRUSTED_ORIGIN_OR_TIMESTAMP__NO_LIGHT_ENERGY_DETECTOR_DISTANCE_SOURCE_POPULATION_HISTORY_MATTER_MASS_SCALE_XMAX_OR_CANON__METRIC_KERNEL_ANGULAR_EQUATION_UNCHANGED
```

## Appendix B. Unresolved joins

| Join | Strongest statement in this edition | Missing authority |
|---|---|---|
| Physical situation to founding depth | The reciprocal character is exact after ordered depth is supplied; a stationary Killing branch has a metric-native owner. | A general observer/event/path-to-depth law, including the signed-arrow/nonnegative-magnitude join. |
| Founding depth to null-path state | Both are now typed in this manuscript, but no universal identity is asserted between \(\delta\), presentation \(\phi\), terminal pair readout, or metric frequency ratio. | The completed-pair construction and a supplied physical query; Section 4 is not yet synthesized. |
| Metric geometry to carried content | Geometry supplies \(R\) and \(A\), not nonzero content. | A physical source/content premise or derivation. |
| G350 to G351 | Exact after adding the owner-provisional conserved label measure. | Conservation is not metric-derived. |
| G351 to G352 | Registry records an accepted conditional clock-rate readout. | Full source reconstruction is not yet in this manuscript. |
| Label measure to light or energy | No identification is made. | Physical identity, units, source, and measurement law. |
| Labelwise transfer to detector output | Multiplicity is retained mathematically. | Cross-label aggregation, phase/interference, and detector rule. |
| Admissible geometry to our universe | The pilot accepts a supplied metric. | History/initial data, occupancy, topology, and scale selection as applicable. |
| Geometry/readout to observations | No native observational prediction is claimed. | Complete frozen prediction chain and observational protocol. |

## Appendix C. Evidence and review limits

- The F1--F4 reconstruction separates interpretation, posit, convention,
  declared readout, and derived consequence. Its equations do not derive the
  physical map to depth or the function \(\phi(r)\).
- G01/G02's exact reciprocal character is relational and applies on supplied
  ordered depth. The factorization witness and branch-local Killing result are
  boundaries on universal ownership, not competing metric laws.
- G350's classification is an analytic theorem for its declared class. Large
  executable counts are regression evidence, not thousands of independent
  proofs.
- G351's inverse-area result is a measure-theoretic consequence of a separately
  adopted premise. The singular counterexample and caustic distinctions are
  load-bearing.
- The external reviews independently reconstructed the bounded central
  arguments, but their co-sealed manifests do not provide trusted external
  timestamps or signatures for historical chronology.
- This pilot did not replay the complete G348–G352 evidence suites. Its fidelity
  review is editorial/source-level unless a specific discrepancy makes a small
  computation load-bearing.
- General Lorentzian geometry used as mathematical method is not thereby a
  uniquely UDT prediction.

## Appendix D. Edition change record

- **2026-09-05, reviewed foundations expansion:** reconstructed F1--F4 and
  G01/G02; separated every premise, mathematical assumption, convention, and
  declared readout from the derived reciprocal character; added the primary
  metric readout, correctly typed representation current, factorization
  freedom, stationary branch-local owner, and exact unresolved physical-depth
  boundary. Fresh source-first fidelity review found one minor dependency-spine
  omission: the short lineage omitted F3 reversal and the separate positivity
  input although the body included both. The lineage was repaired, and final
  review returned `ACCEPT` with no change to the scientific conclusion.
- **2026-09-05, candidate pilot:** created the full manuscript skeleton; wrote
  the continuous G350–G351 pilot; added supporting G348/G349 definitions;
  acknowledged G352 without synthesizing it; recorded source grades,
  unresolved joins, and review limits. Fresh source-first fidelity review found
  two wording defects: ordinary map rank had been conflated with transverse
  quotient-screen rank, and the G352 notice had not separated its adopted
  readout premise from its chosen continuous product realization. Both were
  repaired and the repair-only follow-up returned `ACCEPT`. No scientific
  premise, source package, registry grade, current status surface, or canon was
  changed.
