# Dilation equivalence, conserved mass, and the UDT action sieve — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Repository | `grok` at `64af120`; unrelated dirty files preserved |
| Mode | Analytic DERIVE + self-CAS; DATA-BLIND |
| MAP frozen first | `UDT_DILATION_SUBSTRATE_ACTION_MAP.md`, SHA-256 `16040edfdca72f92c9e4e3d5cd00945082bdd913fa678558a1f7f33809200a95` |
| Symbolic verifier | `verify_udt_dilation_substrate_action.py` — **28/28 checks pass** |
| GPU | Not used and not needed |
| Independent verification | **OPEN** |
| Build-on grade | **PROVISIONAL ANALYTIC RESULT**, not banked and not canon |

WR-L is unchanged. The corrected \(Q_H=1\) stability result is unchanged within its stamped
conditional model. The \(S^2\) carrier remains reopened. Observer-dependent gravitational-mass
amplification remains excluded.

## 0. Result

The new owner guidance materially narrows the problem, but it does not yet select one unconditional
UDT action.

\[
\boxed{
\begin{gathered}
\text{Frame-removable dilation cannot by itself carry invariant geometric cost.}\\
\text{The minimal invariant geometric discriminator is curvature/non-integrability.}\\
\text{Exact total-mass conservation can be total-energy conservation; it does not force}\\
\text{an independent substrate-number current.}\\
\text{Neither frame neutrality nor conservation alone selects a unique carrier action.}
\end{gathered}}
\]

There are two surviving levels:

1. **Weak recycling principle:** the total UDT energy/mass is constant and localized matter is one
   form of it. This requires a time generator, a total energy definition, and a sealed flux law. It
   does **not** require an additional internal current.
2. **Strong substrate principle:** there is also an independently conserved substrate amount
   \(\nabla_\mu\mathcal J^\mu=0\). This requires an additional continuous symmetry. Even then, its
   charge is not automatically energy or gravitational mass.

The strongest unique branch available is still conditional:

\[
\boxed{
\begin{aligned}
&\text{metric only + unrestricted 4D variation + locality + full covariance}\\
&\quad+\text{second-order metric equations + no extra fields + flat-frame neutrality}\\
&\Longrightarrow \text{EH-form geometry up to normalization, boundary, and topology,}
\end{aligned}}
\]

using the Lovelock classification as a mathematical theorem. Those premises are not all derived from
positional dilation, and this branch does not itself produce a matter carrier or a local recycling
current.

## 1. What “the same cost as SR/GR dilation” can mean exactly

For SR,

\[
\frac{d\tau}{dt}=\sqrt{1-\frac{v^2}{c^2}},
\qquad
\gamma_v=\frac{1}{\sqrt{1-v^2/c^2}}.
\]

For the live WR-L metric,

\[
\frac{d\tau}{dt}=\sqrt{A(r)}=\sqrt{1-\frac rX},
\qquad
\gamma_X=\frac{1}{\sqrt{1-r/X}}.
\]

Therefore the exact kinematic dictionary is

\[
\boxed{\frac{v^2}{c^2}\longleftrightarrow\frac rX},
\qquad
\gamma_v\longleftrightarrow\gamma_X.
\]

It directly gives

\[
r\to X^-\quad\Longrightarrow\quad
\frac{d\tau}{dt}\to0,
\qquad
\gamma_X\to\infty.
\]

This is **DERIVED KINEMATICS**. It determines a frame-comparison factor. It does not by itself
determine energy stored in the geometry.

The owner phrase “same cost” has at least two non-equivalent completions:

- **W1-K:** the same kinematic dilation factor. This is already supplied by the metric.
- **W1-D:** frame-removable dilation has no intrinsic dynamical cost; only invariant failure of the
  geometry to be flattened has cost. This is the working interpretation tested below.

No numerical equality between an SR particle's kinetic energy and a UDT field-action density is
derived or assumed.

## 2. Flat accelerated-frame test

Consider the flat accelerated chart, with \(c=1\) temporarily,

\[
ds^2=-(1+a x)^2dt^2+dx^2+dy^2+dz^2.
\]

Writing its lapse as \(N=e^{-\phi}=1+ax\) gives

\[
\phi=-\log(1+ax),
\qquad
\partial_x\phi=-\frac{a}{1+ax}\ne0.
\]

Yet direct computation gives

\[
R^\rho{}_{\sigma\mu\nu}=0,
\qquad
R_{\mu\nu}=0,
\qquad
R=0.
\]

Thus a bare first-gradient density \(F(\nabla\phi\cdot\nabla\phi)\), when \(\phi\) is merely extracted
from a lapse, can assign nonzero cost to a flat accelerated chart. It cannot be a generally
frame-neutral metric action without further structure.

The scope is important:

- **DERIVED:** lapse gradient alone is not an invariant measure of gravitational geometry.
- **NOT derived:** every physical scalar-gradient action is forbidden. If \(\phi\) is an independent
  physical substrate, or if UDT has a physically preferred foliation, its gradient may carry real
  cost—but that is an additional branch/premise.
- The accelerated metric above is a GR comparison chart, not automatically a member of the
  reciprocal UDT configuration space. Its role is to falsify lapse-gradient-as-universal-invariant,
  not to replace the UDT metric.

This sharpens the prior counterfamily result. The family

\[
S_F=\int d\mu\,X^{-2}F(X^2\nabla\phi\cdot\nabla\phi)
\]

remains a valid proof of action underdetermination, but under W1-D it can survive as fundamental
physics only if \(\phi\) has independent physical status or a preferred UDT structure is declared.

## 3. Frame neutrality does not erase WR-L

For

\[
ds^2=-A(r)c^2dt^2+A(r)^{-1}dr^2+r^2d\Omega^2,
\]

the exact Ricci scalar is

\[
R=-A''-\frac{4A'}r-\frac{2(A-1)}{r^2}.
\]

With the live WR-L relation

\[
A=1-\frac rX,
\]

this gives

\[
\boxed{R_{\rm WR-L}=\frac{6}{Xr}}.
\]

Therefore WR-L is not removed by the flat-frame gate. It contains invariant curvature away from the
flat limit and is eligible to carry geometric dynamics. This calculation does not identify its
action or source.

## 4. What the flat-frame gate does and does not select

A local covariant metric-only action can contain, schematically,

\[
S_g=\int d^4x\sqrt{-g}\left[
c_0+c_1R+c_2R^2+c_3R_{\mu\nu}R^{\mu\nu}+\cdots
\right].
\]

All curvature terms vanish on flat geometry, so W1-D eliminates chart-dependent lapse-gradient cost
but does not distinguish \(R\) from \(R^2\), \(R_{\mu\nu}R^{\mu\nu}\), or higher curvature invariants.

If “flat geometry has zero intrinsic gravitational action and is an admissible vacuum” is imposed in
the strong sense, the non-derivative \(c_0\) / \(\Lambda\) term is also excluded. This is
**CONDITIONAL on that strong reading**, not promoted here; a universal finite-cell term could change
the global interpretation.

The Lovelock-style uniqueness route requires the additional premises:

1. four spacetime dimensions;
2. unrestricted physical metric as the only geometric field;
3. local, fully spacetime-covariant action;
4. no preferred foliation or independent dilation scalar;
5. metric equations no higher than second differential order;
6. no additional local curvature scale/coupling branch;
7. variation of the full metric before reciprocal/static reduction.

Under those premises, the metric action is restricted to

\[
S_g^{\rm L}=
\frac{1}{2\kappa_g}\int d^4x\sqrt{-g}(R-2\Lambda)
+S_{\rm boundary}+S_{\rm topological}.
\]

W1-D in its strong flat-vacuum form sets \(\Lambda=0\), and an observed \(G\) can normalize
\(\kappa_g\). This is a **UNIQUE-CONDITIONAL** branch. It is not an unconditional native derivation,
because items 2–7 are not all consequences of positional dilation.

## 5. The variation-order obstruction remains decisive

For the reciprocal one-function spherical family, the EH radial density is

\[
r^2R=-r^2A''-4rA'-2(A-1).
\]

Exactly,

\[
\boxed{
r^2R=\frac{d}{dr}\left[-r^2A'-2r(A-1)\right].
}
\]

Consequently,

\[
\frac{\delta}{\delta A}\int dr\,r^2R\equiv0.
\]

Thus:

\[
\boxed{
\text{vary full metric then impose reciprocity}
\ne
\text{impose reciprocal one-function metric then vary}.
}
\]

The EH-form branch obtains nonempty equations only through unrestricted metric variation. The UDT
foundation has not yet selected that variation domain.

The prior carrier-source audit gives the same warning from the matter side:

\[
\text{unrestricted lapse source}:\quad \rho+S=2\rho_4,
\]

whereas reciprocal-constrained variation gives

\[
\text{reciprocal tangent source}:\quad
\rho+p_\parallel=2(\rho_{2\parallel}+\rho_{4\parallel}).
\]

These are generically different. The new conservation principle does not make them equal.

## 6. Three different meanings of conservation

### 6.1 Diffeomorphism identity

For a covariant metric action with Euler tensor \(E^{\mu\nu}\), invariance under
\(\delta g_{\mu\nu}=2\nabla_{(\mu}\xi_{\nu)}\) yields

\[
\boxed{\nabla_\mu E^{\mu\nu}\equiv0.}
\]

This is a gauge/variational identity. It does not by itself supply a positive local substrate amount.
Its associated gravitational charges require a generator and boundary prescription.

### 6.2 Total energy current

Given a symmetric total stress tensor on a stationary background with time generator \(\tau^\mu\),

\[
j_E^\mu=-T^\mu{}_{\nu}\tau^\nu.
\]

If

\[
\nabla_\mu T^{\mu\nu}=0,
\qquad
\nabla_{(\mu}\tau_{\nu)}=0,
\]

then

\[
\nabla_\mu j_E^\mu
=-T^{\mu\nu}\nabla_{(\mu}\tau_{\nu)}=0.
\]

With a sealed zero-flux boundary, the integrated total energy is constant. If UDT identifies total
mass by \(M_{\rm total}=E_{\rm total}/c^2\), this is enough for the **weak recycling principle**:
localized matter may appear while another sector loses exactly the same energy.

For dynamical gravity, the total conserved quantity is generally a Hamiltonian/boundary charge rather
than the integral of a unique local gravitational energy density. A UDT finite-cell time generator,
boundary term, and time-live seal law are therefore still required.

### 6.3 Independent substrate current

The stronger statement

\[
\nabla_\mu\mathcal J^\mu=0
\]

requires an independent continuous physical symmetry. It is not forced by total-energy conservation.

To prove nonuniqueness, take two real substrate components \(\psi_1,\psi_2\),

\[
s=\psi_1^2+\psi_2^2,
\]

and the family

\[
\mathcal L_{f,V}
=\frac12 f(s)\nabla_\mu\psi_a\nabla^\mu\psi_a-V(s).
\]

Every choice of \(f\) and \(V\) has the same continuous internal rotation symmetry and current

\[
\mathcal J^\mu
=f(s)(\psi_1\nabla^\mu\psi_2-\psi_2\nabla^\mu\psi_1),
\qquad
\nabla_\mu\mathcal J^\mu=0
\]

on its equations of motion. Distinct actions therefore possess the same conservation type.

Moreover, a static configuration can have \(\mathcal J^0=0\) and nonzero potential/gradient energy.
Thus

\[
\boxed{Q_{\rm substrate}\ne M\quad\text{without an additional derived identity}.}
\]

The family is a countermodel to uniqueness, not a proposed UDT carrier.

## 7. Exact recycling ledger and black-hole accounting

Let \(M_L\), \(M_H\), and \(M_R\) denote localized, horizon/black-hole, and diffuse/geometric
reservoir contributions to one total ledger. Pure transfer can be written

\[
\dot M_L=\Gamma_E-\Gamma_H,
\]

\[
\dot M_H=\Gamma_H-\Gamma_R,
\]

\[
\dot M_R=\Gamma_R-\Gamma_E.
\]

Then identically

\[
\boxed{\dot M_{\rm total}=\dot M_L+\dot M_H+\dot M_R=0.}
\]

This is a bookkeeping identity, not a derived mechanism. The rates must be outputs of the eventual
local field equations.

It exposes a hard falsification gate: if matter crosses a horizon and the black-hole contribution
increases by the same amount, total mass is already conserved. Creating replacement matter without
depleting either \(M_H\) or \(M_R\) gives

\[
\dot M_{\rm total}=\Gamma_E>0,
\]

which double-counts mass. Therefore “recycling” must mean conversion through the ledger, never
unpaired compensatory creation.

No local, causal route \(H\to R\to L\) has yet been derived. A horizon is an internal surface for the
whole-universe ledger; exterior-only loss is not total destruction.

## 8. Audit of the metric-plus-carrier branch

The new principles do not force a carrier, but they clarify what a carrier would need to do.

### 8.1 Reopened \(S^2\) carrier

The existing carrier

\[
\mathbf n:\mathbb R^3\to S^2
\]

with static \(L_2+L_4\) energy remains a valid falsifiable survivor. Its corrected \(Q_H=1\) critical
configuration has a positive, numerically certified scoped spectrum.

But:

- \(Q_H\) is a topological sector label, not a derived gravitational-mass current;
- configurations with the same \(Q_H\) can have different energy;
- the flat-static energy does not fix the time-live action;
- previous forcedness work found additional allowed \(X_2^2\)-type and \(L_6\) invariants;
- total-energy conservation holds for every time-invariant member and therefore does not remove those
  alternatives.

Consequently,

\[
\boxed{
\text{conserved total mass does not derive }S^2\text{ or uniquely select }L_2+L_4.
}
\]

The possibility that \(S^2\) is an emergent order parameter of a deeper substrate remains OPEN.

### 8.2 Historical native geometric action

The prior constrained/foliated angular-curvature-mismatch action passes a scoped flat off-round
cancellation test in its transverse sector. It remains mathematically meaningful within that class.

However, its \(\phi'^2\) sector and preferred radial/transverse split are not yet shown to be the
full time-live, frame-neutral UDT action. Under W1-D it has two honest readings:

1. \(\phi\) is only a metric/frame variable: the first-gradient cost requires a new invariant
   justification and may fail the flat-frame test.
2. \(\phi\) is an independent physical substrate/preferred-structure variable: the cost may be real,
   but the extra physical status is a premise.

Thus W1-D does not erase that prior action, but it prevents its scoped flatness result from being
promoted to a unique full spacetime action.

## 9. Existing conditional mass identity

Under the existing premises

- unrestricted metric variation;
- EH-form metric-only geometric action;
- minimal physical-metric carrier coupling;
- static carrier;

one has

\[
D^2N=\kappa_gN\rho_4,
\qquad
M_N=2\int N\rho_4\,dV.
\]

For weak backreaction and a stationary \(L_2+L_4\) carrier,

\[
E_2=E_4,
\qquad
M_N=2E_4=E_2+E_4.
\]

The recycling posit adds a new compatibility demand:

\[
M_N\stackrel{?}{=}M_{\rm conserved\ boundary/Hamiltonian}
\]

for the same full action and finite cell. This equality is **OPEN**; it must be derived, not declared.
The reciprocal-constrained source generally modifies the first equation and therefore does not
silently inherit the identity.

## 10. What the electron mass would fix

For a static two-term carrier at physical size \(R_s\), write

\[
E(R_s)=C_2\xi R_s+\frac{C_4\kappa_4}{R_s}.
\]

Stationarity gives

\[
R_s^2=\frac{C_4\kappa_4}{C_2\xi},
\qquad
E_*=2\sqrt{C_2C_4\xi\kappa_4}.
\]

If the electron is CHOSEN to be this lowest carrier,

\[
E_*=m_ec^2
\]

fixes

\[
\boxed{
\xi\kappa_4=\frac{m_e^2c^4}{4C_2C_4}.
}
\]

The ratio \(\kappa_4/\xi\), hence the physical size, remains free. The observed mass fixes one
normalization/product; it does not select the action family, carrier target, or time sector.

## 11. Total mass and universal \(X\)

If a future native closure gives

\[
X=\alpha\frac{GM_{\rm total}}{c^2},
\]

then

\[
\dot M_{\rm total}=0\quad\Longrightarrow\quad\dot X=0
\]

for constant \(G,c,\alpha\). This makes conservation consistent with a universal constant \(X\).
It does not determine \(\alpha\), prove the closure, or supply the second independent equation needed
if both \(c\) and \(X\) are global outputs.

## 12. Surviving action space

| Branch | What the new principles accomplish | What remains open | Grade |
|---|---|---|---|
| Full metric, Lovelock-minimal | Frame neutrality + named minimality leave EH form; strong flat-vacuum reading removes \(\Lambda\) | UDT derivation of unrestricted variation/minimality; matter emergence | **UNIQUE-CONDITIONAL** |
| Full metric, higher curvature | Frame neutral and locally covariant | Infinitely many coefficients/operators; higher-order dynamics | **ALLOWED FAMILY** |
| Reciprocal metric reduced before variation | Keeps positional relation explicit | EH bulk EL is empty; carrier source differs | **INSUFFICIENT as EH-derived dynamics** |
| Metric + physical substrate | Can support localized/diffuse conversion and internal current | Field/target/symmetry/action not selected | **ALLOWED FAMILY / OPEN** |
| Reopened \(S^2,L_2+L_4\) | Known stable scoped static survivor; conditional mass identity available | Fundamental provenance, extra invariants, time sector, recycling | **WORKING CONDITIONAL SURVIVOR** |
| Finite-cell boundary charge | Natural place for total gravitational mass | Boundary generator, normalization, time-live zero-flux law | **OPEN** |
| Hand-fixed \(M_{\rm total}\) constraint | Enforces desired answer | Nonlocal imposed mechanism; no action provenance | **REJECTED** |

## 13. What has genuinely been narrowed

The new guidance supplies two useful sieves:

1. **Geometry sieve:** a lapse/dilation gradient is not sufficient evidence of physical cost. Any
   geometric action must be invariant under frame rewriting; curvature is the minimal known
   discriminator.
2. **Ledger sieve:** matter emergence must be an equal-and-opposite redistribution in a single total
   charge. Horizon absorption is not destruction in that ledger, and replacement matter cannot be
   added without depletion.

It also corrects an overstrong inference from the prior PONDER:

\[
\boxed{
\text{constant total mass does not itself require an independently conserved substrate amount.}
}
\]

An internal substrate current is one stronger possible completion, not yet a UDT consequence.

## 14. The remaining decisive physical fork

The next question is no longer “which formula looks like GR?” It is:

\[
\boxed{
\text{Is positional dilation entirely metric geometry, or is there an independent physical
substrate degree of freedom?}
}
\]

- If **entirely metric**, the Lovelock-minimal route becomes the strongest conditional completion;
  matter must then emerge as localized geometry or from a separately justified matter sector.
- If **independent substrate**, its configuration space and continuous symmetry must be specified or
  derived. Conservation then constrains the action but does not uniquely select it.

The present owner guidance does not decide this fork, and this derivation does not manufacture the
answer.

## 15. Falsification gates for the next stage

A candidate action fails if it:

1. assigns intrinsic geometric cost to a flat frame representation without declaring a physical
   preferred structure;
2. obtains equations only by varying a larger field space while claiming the reciprocal reduced
   action produced them;
3. counts horizon-retained mass and replacement matter simultaneously;
4. inserts a global creation rate or mass constraint rather than deriving local transfer;
5. calls a topological/internal charge “mass” without proving the equality;
6. cannot define a finite-cell total energy and its boundary flux;
7. silently replaces the raw UDT carrier source with \(\rho+S=2\rho_4\);
8. uses the electron mass to fit more than one independent freedom;
9. assumes \(S^2\) fundamental because its conditional soliton is stable;
10. treats \(\dot M=0\) as a derivation of the \(X(M,c,G)\) closure coefficient.

## 16. Verification scope

The standalone symbolic verifier checks:

- flat accelerated-chart curvature and nonzero lapse gradient;
- reciprocal determinant and SR/UDT gamma map;
- full spherical Ricci scalar and \(R_{\rm WR-L}=6/(Xr)\);
- reduced EH total-derivative identity and empty Euler operator;
- a distinct curvature-squared bulk operator;
- stationary energy-current contraction;
- a generic internal-Noether counterfamily;
- recycling and double-counting ledgers;
- \(L_2+L_4\) virial/mass calibration algebra;
- source inequivalence and global-\(X\) bookkeeping.

It does not prove the Lovelock theorem, establish the physical interpretation W1-D, prove a carrier
exists, derive a recycling transfer process, or certify a finite-cell Hamiltonian charge.
