# UDT founding-metric value-law problem

Date: 2026-08-25

Purpose: self-contained cold-solver brief for an external mathematical LLM
Status: problem statement, not canon and not a request to confirm UDT

## Executive statement

Universal Dimensionality Theory (UDT) has a short founded reciprocal construction and a much
larger, externally audited geometric evaluator around it. The present problem is narrower than
“choose one physical metric from every Lorentz metric.” In the bounded primary branch, the metric
already has the form

\[
g_\phi=-e^{-2\phi(r)}c_E^2dt^2+e^{2\phi(r)}dr^2+r^2d\Omega^2,
\]

and its observer-pair reciprocal kernel is derived algebraically after a physical pair pullback is
supplied. Angular, screen, and mixing contributions enter the pullback before the terminal pair
readout. There is no independent response profile to bolt onto the metric.

The unresolved object is the valued score itself: what fixes or propagates the function \(\phi\)
across physical separation and, eventually, across time? Existing identities reconstruct supplied
values and enforce consistency, but do not generate the values. The current bounded evidence does
not define an ODE, PDE, or GPU initial-value problem.

Your task is to determine whether a nonidentity value law follows from the stated founding
structure but has been overlooked. A valid answer may be:

1. a derivation of a native local or invariant metric condition;
2. a derivation of a genuinely global completed-relation law;
3. a proof that the stated premises underdetermine the values, together with the smallest exact
   additional premise type that would close them; or
4. identification of an inconsistency in the chain.

Do not assume that a conventional field equation must exist. An algebraic finite-family theorem,
a functional equation, an integrability condition, or a global relation constraint could be the
answer. Conversely, do not invent a law merely because prediction is desired.

## 1. Epistemic vocabulary

The status words below are part of the mathematical specification.

| Label | Meaning |
|---|---|
| `OBSERVED` | Empirical calibration input, not derived theory. |
| `DERIVED` | Follows from the declared premises in the stated scope. |
| `DERIVED_CONDITIONAL` | Follows after explicitly supplied metric, query, germ, or working premise. |
| `WORKING` | Provisional frame retained for investigation; not canon. |
| `WORKING_FOUNDATIONAL_CLARIFICATION` | Load-bearing provisional interpretation adopted by Charles Rotter, not derived from the bare metric. |
| `POSIT` | Additional declared assumption. |
| `CHOSE` | Convention, control family, or freely selected structure. |
| `OPEN` | Not presently owned by the theory. |

The strongest current statements are externally verified with caveats in bounded source and
geometric regimes. None has been canonized merely by appearing here.

## 2. Founding premises

### F1. Reciprocal \(c_E\) identity

`OBSERVED` calibration plus proposed foundational interpretation:

\[
L=c_ET,
\qquad
T=\frac{L}{c_E}.
\]

The two directions are coequal clock/ruler conversions. The constant \(c_E\) has dimensions of
length per time. It is not, by itself, a distance, an area, a history equation, or a proof about
local signal propagation.

### F2. Dual Reciprocity

Foundational UDT interpretation: a positional comparison acts contragrediently on the two sides of
the clock/ruler conversion pair. With

\[
q=\begin{pmatrix}c_Edt\\dr\end{pmatrix},
\qquad
P(\Delta)=\begin{pmatrix}u(\Delta)&0\\0&v(\Delta)\end{pmatrix},
\qquad
K=\begin{pmatrix}0&1\\1&0\end{pmatrix},
\]

Dual Reciprocity is

\[
P(\Delta)^T K P(\Delta)=K.
\]

Therefore

\[
u(\Delta)v(\Delta)=1.
\]

This conclusion uses Dual Reciprocity. Ordinary covariance of the conversion map would instead
give \(u=v\), so the inverse squeeze does not follow from the numerical existence of \(c_E\) alone.

### F3. Positional composition and reversal

`POSIT` / positional-relativity premise:

\[
P(\Delta_1+\Delta_2)=P(\Delta_1)P(\Delta_2),
\qquad
P(-\Delta)=P(\Delta)^{-1}.
\]

Continuity or measurability, positivity, and at least one nonidentity comparison give, after choosing
the sign and unit of the additive coordinate,

\[
D(\delta)=\operatorname{diag}(e^{-\delta},e^{+\delta}).
\]

The nontriviality input is separate: the trivial representation also obeys the group laws.

### F4. Local metric readout

`DECLARED READOUT` / local Lorentzian continuity: the transformed clock and ruler coframe is read
quadratically, and the static spherical chart uses an areal angular sector. This produces the
primary metric in Section 3.

### W1. Completed-pair Dual Reciprocity

`WORKING_FOUNDATIONAL_CLARIFICATION`, not canon: Dual Reciprocity applies to the completed physical
observer-pair pullback only after angular, screen, shift, and mixing contributions have entered.
Arbitrarily calibrated pair curves remain useful controls, but are not rival physical kernels.

### W2. Co-presence

`WORKING` semantics only: co-presence denotes event co-membership in a supplied whole solution. It
does not construct that solution or assign numerical depths. The endpoint-relative reversal theorem
does not use co-presence. Do not use it as a value law unless a new nonidentity mathematical
condition is explicitly derived from it.

### W3. UDT--GR quiet-limit reduction

`WORKING/POSIT`, provisionally authorized by Charles Rotter on 2026-08-25, not canon: UDT is a
metric-native extension of GR by a finite-separation reciprocal channel. In a quiet intermediate
regime, the complete UDT law must reduce continuously to the corresponding GR field structure,
constraint propagation, causal structure, and observer predictions. Departures at the extreme
regimes must arise from the same complete reciprocal metric machinery, not from a fitted regime
window or a correction applied after pair readout.

This is a reduction requirement, not a derivation of the Einstein equations from F1--F4 or W1. It
does not yet define the invariant quietness parameter, the full UDT parent operator, the source
sector, or the law governing departure from the GR branch. In the bounded first audit, GR vacuum
equations may be used only as an explicitly imported comparison condition on the static spherical
exterior.

### W3.1. Full-metric quiet non-discard theorem

`DERIVED_CONDITIONAL`, bounded to the primary static-spherical positive-
\(f=e^{-2\phi}\) W3 comparator: the quiet comparison must be evaluated with the complete
four-metric, including the areal sphere. Its two independent diagonal residuals are

\[
\mathcal E_0=r f'+f-1,
\qquad
\mathcal E_1=r f'+\frac{r^2}{2}f'',
\]

and the native G201 angular amplitudes obey the exact identity

\[
A_\parallel+A_\perp=\mathcal E_1-\mathcal E_0.
\]

On the imported quiet-vacuum comparison family \(f=1+C/r\), with \(C\ne0\),

\[
A_\parallel=\frac{3C}{2r},
\qquad
A_\perp=-\frac{3C}{2r}.
\]

Thus the angular instruments are active and cancel; they were not turned off to recover the GR
limit. The isolated two-dimensional clock-radius metric has identically zero Einstein tensor for
every \(f\), so it is a vacuous substitute. Flattening the areal sphere instead gives an exact unit
residual on \(f=1+C/r\). Either shortcut corrupts the bounded comparison.

This theorem does not select the UDT parent law. In particular, zero angular trace alone retains

\[
f=1+a r^2+\frac{b}{r},
\qquad
\mathcal E_0=\mathcal E_1=3a r^2,
\]

and the imported vacuum condition separately removes \(a\). G260 therefore closes the angular-
discard concern while leaving the parent/source value law, time-live extension, and loud-regime
departure `OPEN`.

### W4. Universal metric coupling

`WORKING/POSIT`, provisionally authorized by Charles Rotter on 2026-08-25, not canon: the completed
UDT metric is the single local geometry used by clocks, rulers, freely falling test systems, and
null propagation. At every regular event, a freely falling frame has local special-relativistic
form with the locally calibrated \(c_E\). Conditional pair \(c_{\rm eff}\) remains a finite-
separation observer-frame readout and is not a second local signal cone.

W4 forbids a force, clock law, or light cone bolted onto the pair readout independently of the
metric. It does not alter F1--F4's reciprocal algebra or the primary metric components. It also does
not, merely by being stated, select a field equation, source/history law, action, locality class,
differential order, or observer population. Those implications must be derived separately.

### Observational anchors

\(c_E\) and \(G_{\rm obs}\) are accepted `OBSERVED` anchors. Neither is presently an equation for
\(\phi\). Their presence does not license a fitted profile or an imported source law.

## 3. What the founding chain actually derives

The continuous one-dimensional reciprocal representation is

\[
S(\phi)=\operatorname{diag}(e^{-\phi},e^{+\phi}),
\qquad
S(\phi_1)S(\phi_2)=S(\phi_1+\phi_2).
\]

The local static-spherical metric readout is

\[
\boxed{
ds^2=-e^{-2\phi(r)}c_E^2dt^2+e^{2\phi(r)}dr^2+r^2d\Omega^2.
}
\]

Keep three types and three symbols distinct: \(\delta_{AB}\) is a supplied directed pair depth,
\(\phi(r)\) is the pointwise presentation potential of a supplied primary metric, and
\(\widehat\Phi_{\rm pair}\) is the terminal scalar read from one completed pair. When an exact
endpoint-potential description is available, denote that potential by \(V(A)\). These objects
coincide only in the matched calibrated primary radial reduction described below; the notation does
not establish a universal identity among them.

Writing \(f=e^{-2\phi}>0\), the same metric is

\[
ds^2=-f(r)c_E^2dt^2+f(r)^{-1}dr^2+r^2d\Omega^2.
\]

The reciprocal radial block has determinant \(-c_E^2\), so

\[
\sqrt{-g}=c_Er^2\sin\theta.
\]

The group current is the matrix-valued one-form

\[
\mathcal J=S^{-1}dS=\operatorname{diag}(-d\phi,d\phi).
\]

Its correctly typed representation quadratic form is

\[
\boxed{
\frac12\operatorname{Tr}(\mathcal J\otimes\mathcal J)
=d\phi\otimes d\phi,
}
\]

or, after evaluation on a tangent vector \(X\),

\[
\frac12\operatorname{Tr}(\mathcal J(X)^2)=(X\phi)^2.
\]

A scalar such as \(g^{ab}\partial_a\phi\partial_b\phi\) additionally uses the spacetime metric.
Literal exterior multiplication instead gives \(\mathcal J\wedge\mathcal J=0\) because this
reciprocal Lie algebra is abelian. Thus the founding structure supplies a representation quadratic
form up to normalization. It does **not** prove that a physical action or energy equals that form,
nor does it determine the function \(\phi(r)\).

The logical input/output boundary is crucial:

\[
\boxed{\text{supplied ordered depth }\delta\ \longmapsto\ D(\delta)}
\]

is derived. The map

\[
\boxed{(\text{events, observers, separation, history})\ \longmapsto\ \delta}
\]

is not derived merely by writing the representation.

## 4. Correct type order: the kernel is downstream of the metric

The bounded construction is

\[
\begin{gathered}
\text{primary UDT metric}
+\text{ supplied calibrated ordered observer/event pair germ}\\
\longrightarrow \text{complete pair pullback }h=F^*g\\
\longrightarrow \text{completed reciprocal calibration}\\
\longrightarrow \text{terminal pair scalar and the other typed outputs}.
\end{gathered}
\]

It is not a fixed path or pre-existing physical distance followed by a separately attached dilation
formula. A bare pair of observer names still does not identify events, calibrations, or a pair
germ. Once a physical query supplies that typed relation, however, no universal preferred path is
needed for the scalar readout.

## 5. Full metric pullback before scalar readout

Let a supplied Lorentz metric be represented locally by an invertible coframe

\[
g=E^T\eta_4E,
\qquad
\eta_4=\operatorname{diag}(-1,1,1,1),
\]

and let \(J\) be the rank-two tangent matrix of a supplied pair germ. Then

\[
\boxed{h=J^TE^T\eta_4EJ.}
\]

In the conditional complete \(2+2\) chart,

\[
E=\begin{pmatrix}B&0\\QS&Q\end{pmatrix},
\qquad
J=\begin{pmatrix}Y\\Z\end{pmatrix},
\]

so

\[
\boxed{
h=Y^TB^T\eta_2BY+(SY+Z)^TQ^TQ(SY+Z).
}
\]

Here \(B\) is the clock/radial block, \(Q\) the positive screen scale and shape, \(S\) all four
base-to-screen mixing components, and \(Y,Z\) the supplied pair-tangent blocks. This is a complete
conditional local configuration/evaluation chart. It is not a law selecting arbitrary histories
for these fields.

In the primary static-spherical metric,

\[
B=\operatorname{diag}(c_Ee^{-\phi},e^{\phi}),
\qquad
Q=\operatorname{diag}(r,r\sin\theta),
\qquad
S=0,
\]

and for pair tangent components \((t_i,r_i,\theta_i,\varphi_i)\),

\[
h_{ij}=-c_E^2e^{-2\phi}t_it_j+e^{2\phi}r_ir_j
+r^2\theta_i\theta_j+r^2\sin^2\theta\,\varphi_i\varphi_j.
\]

The angular terms are a metric-fixed Gram contribution. They enter \(h\) before any scalar is
read. Even a diagonal ambient metric can give a shifted, nondiagonal pair metric for nonradial
germs. Angular participation does not universally change \(\widehat\Phi_{\rm pair}\): it changes
that readout only when it changes the completed clock entry \(h_{00}\). With the same calibrated
clock germ it may instead change the tape density, shift, pair plane, and Jacobi response while
\(\widehat\Phi_{\rm pair}\) remains fixed.

## 6. Pair decomposition and the completed reciprocal kernel

On the regular Lorentzian pair stratum

\[
h_{00}<0,
\qquad
\det h<0,
\]

there is a unique positive shifted decomposition

\[
h_\sigma=-T^2(dy^0+\beta\,d\sigma)^2+L_\sigma^2d\sigma^2,
\]

with

\[
T^2=-h_{00},
\qquad
\beta=\frac{h_{01}}{h_{00}},
\qquad
L_\sigma^2=h_{11}-\frac{h_{01}^2}{h_{00}},
\qquad
T^2L_\sigma^2=-\det h.
\]

Before W1, an arbitrary auxiliary ruler calibration admits the useful control scalar

\[
\phi_{\rm control}=\frac14\log\!\left(\frac{-\det h}{h_{00}^2}\right).
\]

W1 instead applies Dual Reciprocity after completion. Positivity defines the spatial coframe
normalization

\[
\boxed{
m=TL_\sigma=\sqrt{-\det h_\sigma},
\qquad
\vartheta^1=m\,d\sigma.
}
\]

In the coframe \((dy^0,\vartheta^1)\), rather than necessarily in a new coordinate chart,

\[
\det h_{\rm n}=-1,
\qquad
L_{\rm n}=T^{-1},
\qquad
\beta_{\rm n}=\frac{\beta}{m}.
\]

Writing \(T_\star\) for the declared clock-unit reference, the dimensionless terminal readout is

\[
\boxed{
\widehat\Phi_{\rm pair}
=-\log\!\left(\frac{T}{T_\star}\right)
=-\frac12\log\!\left(\frac{-h_{00}}{T_\star^2}\right).
}
\]

The common shorthand \(T_\star=1\) is valid only in the corresponding calibrated units. A literal
coordinate differential \(ds=m\,d\sigma\) with \(y^0\) fixed additionally requires
\(d(m\,d\sigma)=0\); otherwise \(\vartheta^1\) is an anholonomic coframe element and its derivatives
must be retained in regional connection and curvature calculations.

The pair shift is retained. No additional scalar \(\mu\), angular coefficient, regime function,
path score, or post-readout response profile appears. W1 is nevertheless provisional, so every
conclusion using \(m\) and \(\widehat\Phi_{\rm pair}\) remains conditional on that working
clarification.

For the founded radial pair block,

\[
h_{AB}=\operatorname{diag}(-e^{-2\delta_{AB}},e^{+2\delta_{AB}}),
\]

one has

\[
T_{AB}=e^{-\delta_{AB}},
\qquad
L_{AB}=e^{+\delta_{AB}},
\qquad
\widehat\Phi_{AB}=\delta_{AB}
\]

in the matched unit calibration \(T_\star=1\).

The equivalent dimensionless readouts are

\[
q_{AB}=\frac{T_{AB}}{L_{AB}}=e^{-2\delta_{AB}},
\qquad
\chi_{AB}=\frac{L_{AB}-T_{AB}}{L_{AB}+T_{AB}}=\tanh\delta_{AB}.
\]

The conditional quantity \(c_{\rm eff}^{(AB)}/c_E=q_{AB}\) is an inter-observer frame readout. It
is not automatically a local material signal speed.

## 7. Endpoint-relative depth, reversal, and composition

A terminal pair readout is not itself an endpoint potential or a directed arrow. The formulas in
this section apply to the pair groupoid of one exact reciprocal calibration class. Equivalently,
if a more general comparison groupoid is intended, additive depth must vanish on every isotropy
loop so that the cocycle has trivial additive holonomy. Under that exactness qualification, fix a
reference endpoint and define a potential \(V(A)\). Then

\[
\boxed{\delta_{AB}=V(B)-V(A).}
\]

On a general path or comparison groupoid, composition and reversal produce a one-cocycle but do
not alone imply this endpoint-difference form. Nonzero loop depth would add freedom rather than
close the values.

Therefore

\[
\delta_{BA}=-\delta_{AB},
\qquad
q_{BA}=q_{AB}^{-1},
\qquad
\chi_{BA}=-\chi_{AB}.
\]

For matched carried endpoint states,

\[
\delta_{AC}=\delta_{AB}+\delta_{BC},
\qquad
q_{AC}=q_{AB}q_{BC},
\]

and

\[
\chi_{AC}=\frac{\chi_{AB}+\chi_{BC}}{1+\chi_{AB}\chi_{BC}}.
\]

These are exact consistency laws. They do not generate the endpoint potentials or establish
cross-query calibration carry between independently constructed experiments.

For a supplied conserved-frequency source-observer query in the matched exact primary calibration,
the current conditional radiative attachment is

\[
\log(1+z)=V({\rm source})-V({\rm observer}).
\]

F1--F4 and W1 alone do not connect a generic terminal pair readout to photon frequency, moving
observers, or a time-live transfer problem. Within the stated attachment, no angular correction,
P1 radial profile, luminosity law, or fitted transfer term is inserted after the kernel. This is
not, by itself, a theory of light, flux, or source populations.

## 8. Native angular interlock

For the primary static-spherical metric define

\[
p=r\phi'(r),
\qquad
\zeta=r^2\phi''(r).
\]

The two local nonradial angular amplitudes are

\[
A_{\parallel}=e^{-2\phi}(2p^2+p-\zeta),
\qquad
A_{\perp}=1-e^{-2\phi}(1+p).
\]

At every finite real \(\phi\),

\[
\det\frac{\partial(A_{\parallel},A_{\perp})}{\partial(p,\zeta)}=-e^{-4\phi}\ne0,
\]

and the inverse is

\[
p=e^{2\phi}(1-A_{\perp})-1,
\qquad
\zeta=2p^2+p-e^{2\phi}A_{\parallel}.
\]

This proves that the reciprocal and angular sectors are native parts of the same metric state. The
angular response is not an independently fitted orchestra. But when \(A_{\parallel}\) and
\(A_{\perp}\) are outputs of the same supplied metric, the inverse is tomography: it reconstructs
the supplied first two profile jets \((p,\zeta)\). It does not impose a residual that propagates
\(\phi\).

The reciprocal magnitude is minimal near \(\phi=0\) and grows toward either signed extreme. The
angular modes need not follow one lockstep loudness envelope because they also depend on
\(p,\zeta\).
At any \(\phi\), lawful jets can cancel both angular modes. Therefore “loud–quiet–loud” is native
for reciprocal contrast, but a universal angular version is not presently derived.

## 9. What a complete relation network does

A sufficiently rich, compatible, numerically valued network of full pair pullbacks can reconstruct
all ten local components of the ambient Lorentz metric. With W1, the completed tuple consisting of
the normalized pair metric and positive density \(m\) retains the full pullback information.

Thus a fully valued rank-complete relation network can be the metric state. No second “history
selector” is needed after all values are known. The problem is that the current laws do not create
those values.

For a connected graph of \(N\) event vertices with incidence matrix \(B\),

\[
\delta=BV,
\qquad
\delta_{ij}=V_j-V_i,
\]

and

\[
\ker B=\operatorname{span}\{(1,\ldots,1)\},
\qquad
\operatorname{rank}B=N-1.
\]

After one reference calibration, \(N-1\) independent values remain. Reversal, triangles, and all
cycle identities hold automatically for every assignment of the vertex potentials. They certify
composition but do not propagate the potentials.

This is the current meaning of “physical history”: a complete, mutually compatible valuation of
the primary metric/relation state across its spatial and time-live domain—not a choice among every
imaginable Lorentz metric.

## 10. Exact present obstruction

At any finite set of distinct positive radii \(r_i\), arbitrary finite data

\[
\phi(r_i)=\phi_i,
\qquad
\phi'(r_i)=\frac{p_i}{r_i},
\qquad
\phi''(r_i)=\frac{\zeta_i}{r_i^2}
\]

have a unique polynomial realization of degree below \(3N\). Adding a nonzero multiple of

\[
\prod_{i=1}^N(r-r_i)^3
\]

preserves every registered value, first derivative, and second derivative while changing higher
germs. The same statement holds for finite time-live event data.

Consequences:

- finite scalar and angular samples do not select an unrestricted global profile;
- observations cannot honestly calibrate an unrestricted function and call it a derivation;
- an ODE/PDE solver requires a residual not currently present;
- a GPU would only accelerate an evaluator or an imported equation at this stage.

This is a bounded underdetermination theorem, not a proof that UDT can never own a value law.

## 11. Real constraints already known

The open profile is not devoid of structure.

### Smooth areal center

With at least \(C^2\) regularity, bounded center curvature requires

\[
\phi(r)=O(r^2),
\qquad
\phi'(r)=O(r),
\qquad
\phi''(r)=O(1)
\qquad (r\to0).
\]

A clean sufficient condition for a smooth Cartesian center is

\[
\phi(r)=\psi(r^2),
\qquad
\psi\ \text{smooth},
\qquad
\psi(0)=0.
\]

The sign of \(\phi\) does not by itself force a radial turn. Any monotonicity statement must declare
the radial orientation and the relevant interval separately.

### Exact quiet overlap

With \(s=\log(r/r_0)\), simultaneous zero reciprocal depth and zero local angular second-jet
response require

\[
\boxed{\phi=0,\qquad \phi_s=0,\qquad \phi_{ss}=0.}
\]

For a nontrivial analytic sign crossing, the first active order is odd and at least cubic. This
leaves infinitely many profiles; the cubic is a control, not a selected history.

### Regularity and completion controls

Smooth-center, analytic, geodesically complete, globally hyperbolic primary control families exist
with an inner trough, quiet crossing, and outer reciprocal asymptote. These requirements restrict
the arena but have not selected a unique family or its constants.

### Absolute scale

The complete dimensionless metric and a regular branch fix normalized Jacobi response with no
angular amplitude coefficient. A positive homothety preserves dimensionless reciprocal history,
conditional redshift ratios, causal cones, and normalized shapes while changing absolute area. One
independent dimensionful attachment can fix that remaining scale after a dimensionless history is
known. Neither \(c_E\) nor \(G_{\rm obs}\) alone creates a length.

### \(X_{\max}\)

\(X_{\max}\) is a `WORKING` frame-shared positional-dilation asymptote. Its value, profile, and
global realization remain `OPEN`. It must be a consequence of a completed relation/history, not an
input used to manufacture that history.

## 12. What has already been ruled out as an automatic closure

These results prevent repeated false solutions:

1. **The reciprocal representation alone.** It maps supplied depth to a reciprocal squeeze; it
   does not assign depth values.
2. **The obvious quadratic group action.** The invariant norm exists, but reciprocal symmetry also
   permits arbitrary suitable \(F(Y)\). No unique physical action follows. The simplest quadratic
   radial action does not produce the historical WR-L control profile.
3. **A familiar Einstein-Hilbert equation.** No current UDT premise selects it. GR may be used as a
   comparison or limit, not imported as the missing UDT law.
4. **Cartan, Bianchi, metricity, and curvature identities.** They organize or integrate compatible
   supplied metric data; they do not generate curvature values.
5. **Null geodesic and Jacobi equations.** They propagate a supplied ray or screen through supplied
   curvature; they do not create the ambient metric history.
6. **Rank-complete matched networks.** They faithfully reconstruct a supplied metric and compose
   depths, while accepting invariantly distinct profiles.
7. **Co-presence as solution membership.** It is semantic membership, not a nonidentity value
   condition.
8. **All-germ isotropy.** It would force constant sectional curvature and
   \(e^{-2\phi}=1-Kr^2\), but that stronger premise is not presently owned by UDT.
9. **Finite-order local autonomous closure over the unrestricted profile family.** At every finite
   jet order, analytic profiles can share the registered state and differ at the next invariant
   derivative. This does not rule out a smaller derived family, a nonlocal law, or infinite-state
   closure.
10. **Finite observational anchors.** They can calibrate constants inside an independently derived
    finite family; they cannot derive an unrestricted smooth function.
11. **Post-readout orchestra, scalar \(\mu\), fitted regime weights, P1, or \(X_{\max}\).** None is
    an active native kernel input.

## 13. The exact open mathematical problem

### Stage A: bounded primary branch

Starting only from F1–F4 and, where explicitly accepted, W1, determine whether the primary metric

\[
g_\phi=-e^{-2\phi(r)}c_E^2dt^2+e^{2\phi(r)}dr^2+r^2d\Omega^2
\]

and the totality of its completed physical observer-pair relations imply a nonidentity law for
\(\phi\).

Two broad mathematical types remain live:

\[
\boxed{\mathcal C[g]=0}
\]

for an independently derived diffeomorphism-natural invariant condition that reduces the primary
profile to a proper smaller family, or

\[
\boxed{\mathcal G[g,\mathscr R]=0}
\]

for a genuinely global law on the completed relation network \(\mathscr R\) that constrains values
rather than merely reconstructing, comparing, or composing them.

A third acceptable landing is a proof that no such nonidentity law follows from F1–F4 and W1. Such
a proof must identify the exact model freedom and state the smallest additional premise type; it
must not silently choose a preferred profile.

### Stage B: extension test

If Stage A yields a law or finite family, determine its mathematical route to a complete
nonspherical and time-live metric. Merely activating the complete coframe fields \(B,Q,S,Y,Z\)
enlarges the configuration arena and is not itself closure. State clearly whether the proposed law
is:

- intrinsically four-dimensional and covariant;
- a symmetry-reduced theorem needing a separate extension principle; or
- incompatible with the full pullback/orchestra architecture.

Do not claim a complete universe from a Stage-A-only theorem.

## 14. Candidate-law acceptance contract

A proposed law counts as a native solution only if all of the following are satisfied.

1. **Ownership:** every premise used is F1–F4 or W1, or is visibly labelled as a new premise.
2. **Naturality:** the law is invariant under spacetime diffeomorphism, lawful pair-domain
   reparameterization, local Lorentz/screen gauge, and observer relabelling appropriate to its type.
3. **Nonidentity:** it rejects at least one regular valuation currently admitted by the evaluators.
4. **Noncircularity:** it is stated without inserting a desired profile, \(X_{\max}\), observed
   feature, SNe/BAO/CMB outcome, or fitted coefficient.
5. **Value content:** it constrains or propagates \(\phi\) values, not only their readout,
   decomposition, derivatives after supply, consistency, or reconstruction.
6. **Existence:** at least one nontrivial regular member survives; characterize the whole surviving
   family rather than displaying only a desired member.
7. **Well-posedness/type:** specify whether the result is algebraic, differential, integral,
   functional, groupoid-valued, or global; state its data and gauge freedoms.
8. **Primary reduction:** recover the founded determinant-one radial pair block and endpoint
   reciprocity exactly.
9. **Orchestra compatibility:** angular/screen/mixing data remain upstream of terminal readout; no
   post-kernel correction is introduced.
10. **Scope:** state all omitted singular, caustic, topological, time-live, nonspherical, source,
    matter, and transfer sectors.

If the result reduces the profile to a finite family with \(k\) constants, say exactly how many
independent dimensional or dimensionless anchors are required. Only then may observations calibrate
those constants and independent data test the law.

## 15. Registered discriminators and countermodels

Use these to test whether a proposed law is genuinely nonidentity.

### Static finite-order twins

Near a regular quiet orbit let \(s=\log(r/r_0)\) and

\[
\phi_b(s)=s^3+c s^4+b s^5.
\]

The \(b=0\) and \(b=7\) metrics have identical metric four-jets at \(s=0\), hence identical
\((R,\nabla R,\nabla^2R)\) there, but differ in the next invariant radial derivative. A law that only
renames finite-jet Cartan data will not separate them.

### Time-live diagnostic twins

\[
g_b=-dt^2+e^{2bt^2}(dx^2+dy^2+dz^2).
\]

For the supplied \((\partial_t,\partial_x)\) pair germ, every member completes to the same terminal
pair readout \(\widehat\Phi_{\rm pair}=0\), while

\[
\mathcal R_b(t)=12b(1+4bt^2),
\qquad
\mathcal R_b(0)=12b.
\]

Thus pair normalization is not ambient evolution.

### Network-valued counterfamily

Every smooth vertex potential produces exact reversal, triangle, and cycle closure. A proposed
network law must do more than demand those identities.

### Finite-anchor counterfamily

The cubed-node deformation in Section 10 preserves arbitrary finite scalar and angular second-jet
data while changing the profile elsewhere. A claimed finite-anchor derivation must defeat this
counterfamily by first deriving a finite-dimensional family.

The purpose of these controls is not to demand one favored outcome. A candidate may reject both
members of a displayed pair, provided it independently derives and exhibits a nonempty surviving
solution space.

## 16. Anti-scaffolding rules for the external solver

### Forbidden as UDT derivations

- importing Einstein equations, a cosmological constant, fluids, Standard Model fields, QED,
  textbook optical transfer, or another familiar dynamical equation;
- choosing an action because it is minimal, standard, renormalizable, elegant, or successful in GR;
- treating \(r\) as a pre-existing operational proper distance to which the kernel is appended;
- adding an angular correction after \(\widehat\Phi_{\rm pair}\) or the conditional redshift
  attachment has been computed;
- fitting an unrestricted \(\phi(r,t)\), a spline, polynomial, neural network, regime score, or
  branch weight to observations;
- using \(X_{\max}\), a wall, seam, center, horizon, or boundary value to generate the local law;
- promoting W1 or co-presence to canon without identifying the added premise;
- calling metricity, Bianchi identities, Cartan realization, Jacobi propagation, or network
  consistency a value equation unless a nonidentity restriction is demonstrated;
- selecting a profile for resemblance to reality before classifying the solution space.

### Allowed mathematical tools

Standard differential geometry, Lie theory, invariant theory, functional equations, groupoids,
Cartan methods, global analysis, variational inverse problems, topology, and numerical algebra are
allowed as methods. GR may be used as a reference or limiting comparison. A mathematical technique
does not become imported physics unless its equation or boundary condition is adopted as a UDT law.

External mathematical sources may be consulted and cited. Any physical premise not present in this
brief must be labelled `NEW PREMISE`, not presented as a derivation.

## 17. Questions worth examining without presupposing their answers

1. Does the totality of completed ordered comparisons define a stronger functional equation than
   pairwise additive depth once all lawful overlaps and calibrations are included?
2. Can “separation” be defined intrinsically by the reciprocal relation so that naturality and
   composition jointly constrain \(\phi\), without circularly assuming \(r(\phi)\) or \(X_{\max}\)?
3. Does requiring one smooth rank-complete network for **all physically populated** pair germs add a
   nonidentity condition, or only restate a supplied metric? Be precise about the population premise.
4. Is there a four-dimensional invariant of the complete pullback family that is not merely
   reconstructive and that follows from Dual Reciprocity itself?
5. Can reciprocal group geometry plus locality, additivity, or extensivity uniquely determine an
   action? If an extra additivity premise is needed, state it and test whether it is genuinely
   independent.
6. Could one observational anchor close only a genuine normalization freedom, or would it select a
   function? Prove the parameter count before invoking data.
7. If the premises are insufficient in principle, can two inequivalent complete valued models be
   constructed that satisfy every premise and every typed relation in this brief? That would be the
   strongest underdetermination theorem.

These are lenses, not requested conclusions.

## 18. Required external response

Return all of the following.

1. **Primary landing:** one of
   `NATIVE_VALUE_LAW_DERIVED`, `GLOBAL_RELATION_LAW_DERIVED`,
   `CURRENT_PREMISES_UNDERDETERMINE_VALUES`, `FOUNDING_CHAIN_INCONSISTENT`, or a more precise token.
2. **Premise/type ledger:** list every used premise and classify it as founded, working, supplied,
   mathematical method, observational anchor, or newly proposed.
3. **Strongest derivation:** show every load-bearing step. Do not jump from symmetry to dynamics.
4. **Strongest countermodel:** actively try to refute your own landing using Section 15.
5. **Exact law, if positive:** give a coordinate-free form, then its primary static-spherical
   reduction and full solution-family classification.
6. **Nonidentity demonstration:** exhibit at least two regular valuations treated differently by the
   law for a reason independent of the desired answer.
7. **Extension status:** explain whether and how the result extends to nonspherical/time-live
   complete coframes.
8. **Parameter and anchor count:** identify all remaining constants/functions and what observations
   could legitimately calibrate only after derivation.
9. **Runnable checks:** supply symbolic or numerical code for every finite-dimensional or
   symmetry-reduced load-bearing identity. Code is evidence, not a substitute for the proof.
10. **Failure landing, if applicable:** identify the smallest missing premise by exact mathematical
    type and explain why it is independent of F1–F4/W1.
11. **Lay explanation:** explain what was found without ontology-first language or unexplained jargon.

Do not answer with another survey of prior work. The purpose is to attempt the derivation from the
stated foundation, or to prove cleanly why the foundation does not contain it.

## 19. Honest current ceiling

The present UDT corpus owns a coherent metric-native evaluator and reconstruction architecture:

\[
\text{supplied depth}
\to \text{reciprocal character}
\to \text{primary metric/pullback}
\to \text{completed pair kernel}
\to \text{redshift and typed angular/transport outputs}.
\]

It does not yet own

\[
\text{separation/time}
\longmapsto
\text{the complete numerical primary-state valuation}.
\]

The open bridge is real, but it is narrow. A successful external derivation would convert the
current evaluator into a finite predictive history family or a global relational evolution law. A
rigorous underdetermination theorem would be equally valuable because it would identify, without
scaffolding, the smallest premise that UDT still needs. G260 removes one possible false explanation
for this ceiling: the gap is not caused by deleting the angular sector in the quiet comparison.

## 20. Controlling source spine

These repository paths record the exact bounded evidence behind this brief. They are references,
not extra premises required to understand the problem.

- `UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md`
- `udt_uncompressed_pair_kernel_reconstruction_2026-08-14/`
- `udt_g166_primary_metric_ordered_pair_kernel_descent_2026-08-18/`
- `udt_g167_primary_metric_full_pair_pullback_orchestra_2026-08-18/`
- `udt_g170_endpoint_relative_bidirectional_pair_response_2026-08-19/`
- `udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/`
- `udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/`
- `udt_g201_primary_metric_phi_jet_regime_amplitude_2026-08-21/`
- `udt_g202_quiet_overlap_profile_anchor_classification_2026-08-21/`
- `udt_g204_primary_metric_global_regularity_asymptotic_profile_2026-08-21/`
- `udt_g212_observer_equivalence_history_bridge_whiteboard_2026-08-22/`
- `udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/`
- `udt_g215_completed_scalar_shared_clock_incidence_descent_2026-08-22/`
- `udt_g217_founded_depth_event_pair_first_jet_ownership_2026-08-22/`
- `udt_g231_cartan_regional_realization_bridge_2026-08-23/`
- `udt_g233_primary_profile_cartan_closure_discriminator_2026-08-23/`
- `udt_g234_post_g233_native_closure_route_map_2026-08-23/`
- `udt_g235_rank_complete_matched_network_nonselection_2026-08-23/`
- `udt_g249_reciprocal_angular_absolute_scale_ownership_2026-08-24/`
- `udt_g252_local_proper_clock_same_object_attachment_contract_2026-08-24/`
- `udt_g253_native_kernel_minimal_dependency_compression_audit_2026-08-24/`
- `udt_g254_complete_timelive_solver_closure_audit_2026-08-24/`
- `udt_g255_g165_g254_lost_closure_recovery_audit_2026-08-24/`
- `udt_g256_primary_state_value_closure_rank_2026-08-25/`
- `udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/`
- `udt_g258_redshift_area_inverse_metric_reconstruction_2026-08-25/`
- `udt_g259_metric_only_parent_operator_fork_classification_2026-08-25/`
- `udt_g260_gr_quiet_angular_nondiscard_audit_2026-08-25/`

## Lay summary

UDT has derived the design of the instrument: when two calibrated observers are compared, clocks
and rulers change reciprocally, and the angular machinery is already part of the same metric. The
instrument can read any supplied situation consistently and a rich enough network of readings can
reconstruct the whole metric.

What is missing is the score telling the instrument what values to play from place to place and
moment to moment. Current composition rules say that all musicians are reading the same score; they
do not write the score. The external task is to find whether the founding design secretly forces
that score, or to prove that one additional musical principle is genuinely required.
