# UDT native action and backreaction — disclosed non-cold derivation

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-14 |
| Mode | DERIVE + SELF-CAS; analytic and data-blind |
| MAP frozen first | `UDT_NATIVE_ACTION_NONCOLD_MAP.md`, SHA-256 `c82afb14ef299d6d7efa885cf857353d7a3d2452119f2ab59e61f7eee857d359` |
| Observing or targeting? | OBSERVING what positional dilation forces; no target action or mass identity |
| Driver status | **DISCLOSED NON-COLD** — historical EH/H3 and proposed-native-action records were visible |
| Symbolic verifier | `verify_udt_native_action_noncold.py` — 19/19 checks pass with SymPy 1.13.3 |
| GPU | Not used and not needed for this forcedness result |
| Independent verifier | **OPEN** — no fresh Arm A/B or blind Arm C pass in this result |
| Build-on grade | **PROVISIONAL CANDIDATE**, not banked and not canon |

**Owner clarification, 2026-07-15:** the \(S^2\) carrier is a historical working posit adopted
after derivation attempts failed, now explicitly **REOPENED**. It may emerge, remain postulated,
or be replaced. See UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md. The frozen MAP is retained
unchanged as an audit record of the premises visible at derivation time.

**\(X_{\max}\) clarification, 2026-07-15:** existence of one universal unattainable distance is a
WORKING POSIT; whether it is an independent constant or follows from whole-system closure involving
\(c\), native \(M_{\rm total}\), and possibly \(G\) is OPEN. See
UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md.

## 0. Result in one box

\[
\boxed{
\begin{gathered}
\text{Positional dilation is a FOUNDING UDT postulate and fixes kinematic metric structure.}\\
\text{It does not, by itself, select a unique geometric action, 4D carrier action,}\\
\text{boundary functional, or finite-cell mass charge.}
\end{gathered}}
\]

Accordingly:

- **Q1 — geometric action:** **UNDERDETERMINED / ALLOWED-FAMILY**, not uniquely forced.
- **Q2 — carrier completion and coupling:** **UNDERDETERMINED** by the static $L_2+L_4$ energy.
- **Q3 — native mass rule:** **OPEN** until an action and finite-cell boundary charge are selected.
- The H3 identity
  \[
  D^2N=\kappa_gN\rho_4,
  \qquad
  M_N=2\int N\rho_4 dV
  \]
  remains **DERIVED under the CONDITIONAL unrestricted-EH plus minimal physical-metric carrier
  premises**. It is not promoted to an unconditional consequence of positional dilation.

This does not weaken the founding postulate. It identifies the exact additional structure the
postulate presently does not supply.

## 1. What the postulate actually fixes

The operational positional-dilation inputs are R1 (differences), R2 (composition), and R3 (mutual
reciprocity). R1–R2 plus a named regularity premise give

\[
D(p,q)=G(\phi(q)-\phi(p)),
\qquad
G(x+y)=G(x)G(y)
\quad\Longrightarrow\quad
G(x)=e^{kx}.
\]

With the CHOSE convention $k=-1$,

\[
g_{tt}=-e^{-2\phi}c^2.
\]

R3 plus the named P8 slot identification gives, along the selected gradient direction,

\[
(-g_{tt}/c^2)g_{\parallel\parallel}=1.
\]

These are kinematic restrictions on admissible fields. They do not state an extremum principle.
Writing the restrictions schematically as

\[
C[g,\phi]=0,
\]

does not determine a functional $S[g,\phi]$ whose stationary points obey them. An action also needs
an off-shell field space, allowed invariants, coefficients, measure, derivative order, and boundary
functional. None follows merely from knowing the constraint surface $C=0$.

## 2. Q1 — the geometric action is not uniquely forced

### 2.1 A native, shift-legal counterfamily already exists

Even after adding the historical constrained-two-player and local-second-order premises, the most
general recorded kinetic/transverse candidate contains a family:

\[
S_{Z,\mu,W}=\int c\sqrt h\left[
\frac{Z}{2}(\partial_r\phi)^2
+\mu e^\phi K\,\partial_r\phi
+R^{(2)}[h]
+W(\phi)\mathcal K
\right]dt\,dr\,d^2x,
\]

\[
K_{AB}=\frac{1}{2}e^{-\phi}\partial_r h_{AB},
\qquad
\mathcal K=K_{AB}K^{AB}-K^2.
\]

Under the global depth shift,

\[
\phi\mapsto\phi+\lambda,
\qquad
K_{AB}\mapsto e^{-\lambda}K_{AB},
\]

both $(\partial_r\phi)^2$ and $e^\phi K\partial_r\phi$ have weight zero. In the strict-shift branch,
$W=e^{2\phi}$ also makes $W\mathcal K$ weight zero. Therefore positional-shift bookkeeping fixes
neither $Z$ nor $\mu$. On a round transverse metric $h_{AB}=\rho(r)^2\Omega_{AB}$, the $\phi$ equation
contains

\[
\partial_r\!\left(Z\rho^2\phi'+2\mu\rho\rho'\right).
\]

Changing $\mu$ changes the equation for a general transverse profile while preserving the same
shift rule. The CAS check `C1–C2` verifies this exactly. Thus two distinct members, for example
$\mu=0$ and $\mu\ne0$, satisfy the same stated forcing rule. That is already a countermodel to
uniqueness.

This family is itself **CONDITIONAL** on a radial/transverse split, a local term inventory, a
flat-mismatch criterion, and the treatment of $\phi$ as a longitudinal field. It proves
nonuniqueness inside that chosen class; it does not elevate the class to native law.

### 2.2 EH is a conditional branch, not a positional-dilation theorem

If one separately CHOOSES all of the following:

- an unrestricted four-dimensional metric as the only geometric field;
- local diffeomorphism covariance;
- metric equations of at most second differential order;
- the Lovelock-style minimality premises;

then the classified bulk action is, up to normalization, cosmological term, topology, and boundary
terms,

\[
S_g^{\rm cond}
=\frac{1}{2\kappa_g}\int\sqrt{-g}\,(R-2\Lambda)\,d^4x+B_{\partial\mathcal C}.
\]

This is a valid **CONDITIONAL** route. Positional dilation does not derive the unrestricted variation
space, the derivative-order bound, $\Lambda=0$, $\kappa_g$, or the finite-cell boundary functional.
In particular, native finite-cell canon supplies no spatial infinity from which $\Lambda=0$ or an
asymptotic charge normalization follows. The H3 local-room calculation adds $\Lambda=0$ and $N\to1$
as a scoped comparison choice.

### 2.3 Restrict-then-vary is not vary-then-restrict

For the reciprocal static spherical metric

\[
ds^2=-A(r)c^2dt^2+A(r)^{-1}dr^2+r^2d\Omega^2,
\]

the exact Ricci scalar is

\[
R=-A''-\frac{4A'}r+\frac{2(1-A)}{r^2},
\]

and $\sqrt{-g}/(c\sin\theta)=r^2$. Hence

\[
r^2R
=\frac{d}{dr}\left[-r^2A'-2rA+2r\right].
\]

Therefore the EH action restricted to the one-function reciprocal family has

\[
\frac{\delta S_{EH}^{\rm reduced}}{\delta A}=0
\]

in the bulk. This is the **V1 tangent-variation result**.

If instead an unrestricted metric is varied first and reciprocity is imposed on the resulting
equations, the mixed components are

\[
G^t{}_t=G^r{}_r=\frac{rA'+A-1}{r^2},
\qquad
G^\theta{}_\theta=\frac{1}{2}A''+\frac{A'}{r}.
\]

The unrestricted vacuum equation gives

\[
A+rA'=1.
\]

This is the stronger **V2 equation**. It uses virtual variations normal to the reciprocal
configuration surface and is not the Euler equation of the reduced UDT field space.

There is a further correction to the historical multiplier discussion. With free warps $\nu,\lambda$
and constraint $\nu+\lambda=0$, a multiplier gives

\[
E_\nu+\eta=0,
\qquad
E_\lambda+\eta=0,
\qquad
\nu+\lambda=0.
\]

Eliminating $\eta$ gives only

\[
E_\nu-E_\lambda=0.
\]

But on the reciprocal surface the exact EH expressions obey $E_\nu=E_\lambda$ identically. Thus the
multiplier equation is empty there, just like tangent variation. It does **not** imply
$E_\nu=E_\lambda=0$. Setting their common value to zero restores the discarded unrestricted normal
equation by hand. CAS checks `B1–B3` verify this.

Consequently:

- “EH reduced on the reciprocal family is empty” is **DERIVED**.
- “EH is therefore excluded or wrong” is **not derived**.
- “A multiplier makes reduced EH equivalent to unrestricted Einstein equations” is **false**.
- “Unrestricted EH, followed by a reciprocal solution restriction” is a distinct, CONDITIONAL
  completion.

## 3. Q2 — the static carrier energy does not determine a 4D source

The supplied flat-static functional is

\[
E[\mathbf n]=\int d^3x\left(\rho_2+\rho_4\right),
\]

\[
\rho_2=\frac{\xi}{2}\,\partial_i\mathbf n\cdot\partial_i\mathbf n,
\qquad
\rho_4=\frac{\kappa_4}{4}F_{ij}F_{ij},
\qquad
F_{ij}=\mathbf n\cdot(\partial_i\mathbf n\times\partial_j\mathbf n).
\]

It fixes an energy on one reference slice. It does not state how time derivatives enter, which metric
contracts them, how the lapse or shift enters, or what is held fixed during metric variation.

### 3.1 Conditional minimal physical-metric completion

The H3 branch CHOOSES

\[
S_m^{\rm min}=-\int\sqrt{-g}\left[
\frac{\xi}{2}\,\partial_\mu\mathbf n\cdot\partial^\mu\mathbf n
+\frac{\kappa_4}{4}\Omega_{\mu\nu}\Omega^{\mu\nu}
\right]d^4x.
\]

On a static slice, direct metric variation gives

\[
\rho=\frac{\xi}{2}X+\frac{\kappa_4}{4}Y,
\]

\[
S_{ij}=\xi\left(D_i\mathbf n\cdot D_j\mathbf n-\frac{1}{2}\gamma_{ij}X\right)
+\kappa_4\left(F_i{}^kF_{jk}-\frac{1}{4}\gamma_{ij}Y\right),
\]

\[
S=\gamma^{ij}S_{ij}=-\frac{\xi}{2}X+\frac{\kappa_4}{4}Y,
\qquad
\rho+S=\frac{\kappa_4}{2}Y=2\rho_4.
\]

The cancellation is exact (`E1`). Its provenance is **DERIVED given the CHOSE four-dimensional
minimal completion**, not from the three-dimensional energy alone.

### 3.2 Explicit same-energy/different-source countermodel

In an adapted static clock foliation, consider only as a countermodel

\[
S_m^{(a_2,a_4)}
=-\int dt\,d^3x\,N\sqrt\gamma
\left(N^{a_2}\rho_2+N^{a_4}\rho_4\right).
\]

For every $(a_2,a_4)$, the reference $N=1$ static density is exactly $-(\rho_2+\rho_4)$. But lapse
variation gives

\[
-\frac{1}{\sqrt\gamma}\frac{\delta S_m^{(a_2,a_4)}}{\delta N}
=(1+a_2)N^{a_2}\rho_2+(1+a_4)N^{a_4}\rho_4.
\]

At $N=1$ the source depends on two arbitrary exponents even though the supplied static energy is
identical. CAS checks `D1–D2` verify the statement.

This family is **not proposed as UDT physics**. It is an adapted-foliation countermodel showing that
the static functional cannot logically determine lapse coupling. Full covariance would exclude or
repackage members only after full covariance and the clock-field content are adopted as extra
premises.

The same nonuniqueness persists inside a fully covariant enlarged class: a term such as

\[
\Delta S_m=\alpha\int\sqrt{-g}\,R
\left(\partial_\mu\mathbf n\cdot\partial^\mu\mathbf n\right)d^4x
\]

vanishes in the flat reference energy because $R=0$, yet its metric variation changes curved
backreaction. The coefficient and higher-derivative/nonminimal premise are unforced. Again this is a
**countermodel only**, not an invented UDT coupling. Excluding it requires the explicit minimality and
derivative-order premises used by the H3 branch.

Therefore the physical-metric carrier action is a clean WORKING choice, but it is not uniquely derived
from positional dilation plus the flat-static energy.

## 4. Q3 — what survives for mass

### 4.1 No action-independent finite-cell mass follows

A gravitational charge is the boundary generator associated with a chosen action and its allowed
variations. The founding metric relation does not supply that generator. Moreover, adding a total
divergence can leave bulk equations unchanged while changing the finite-cell boundary functional and
charge. With no spatial infinity, there is no native ADM normalization to fill the gap automatically.

The canonized static seal condition $\phi(r_s)=0$ supplies one boundary value; it does not determine
the complete metric/carrier boundary action, reference subtraction, or charge normalization.

Thus no unconditional equation of the form “mass equals this carrier integral” is presently derived
from positional dilation alone.

### 4.2 Conditional EH/minimal-coupling identity

Under the named unrestricted-EH and minimal physical-metric matter premises, the exact static lapse
equation is

\[
D^2N=\frac{\kappa_gN}{2}(\rho+S).
\]

Using the conditional matter identity above gives

\[
\boxed{D^2N=\kappa_gN\rho_4.}
\]

For any smooth finite volume $V$, the divergence theorem then gives

\[
\boxed{
\frac{2}{\kappa_g}\oint_{\partial V}D_iN\,dS^i
=2\int_VN\rho_4\,dV.}
\]

This finite-volume equality does not require spatial infinity. What remains conditional is calling
the left side the physical UDT mass and fixing its normalization from the EH boundary generator.

Only after the exact equation is fixed may the controlled weak-field expansion be made. For

\[
N=1+O(\kappa_g)
\]

about a fixed leading carrier,

\[
M_N=2E_4^{(0)}+O(\kappa_g).
\]

For a stationary flat $L_2+L_4$ carrier when the dilation variation is admissible (decaying field or
no boundary contribution), the exact scaling family

\[
E(\lambda)=\lambda E_2+\lambda^{-1}E_4
\]

gives

\[
E'(1)=0\quad\Longrightarrow\quad E_2=E_4,
\]

so

\[
\boxed{M_N=E_2+E_4+O(\kappa_g)}
\]

in that conditional weak-backreaction branch. Checks `E1–E5` verify the stress cancellation and
virial algebra.

## 5. Adjudication of the historical action claims

| Historical statement | Result of this derivation |
|---|---|
| Positional dilation is merely a hypothesis to be re-derived | **REJECTED framing:** it is FOUNDING |
| The reciprocal metric form fixes the action | **Not established:** kinematics does not choose off-shell dynamics |
| Reduced EH is empty on the simple reciprocal family | **CONFIRMED exactly** |
| Therefore EH is the wrong/excluded UDT action | **Overstated:** emptiness is V1-scoped; unrestricted EH is a separate conditional branch |
| EH plus a reciprocity multiplier reproduces unrestricted Einstein equations | **RETRACT:** the multiplier leaves only the identically satisfied tangent equation |
| The transverse mismatch action is uniquely native | **Overstated:** its form and $(Z,\mu,W)$ coefficients/branches retain CHOSE/OPEN premises |
| Flat-static $L_2+L_4$ uniquely fixes stress/backreaction | **False:** a 4D completion and metric variation are required |
| H3 $D^2N=\kappa_gN\rho_4$ and $M_N=2\int N\rho_4$ | **CONDITIONAL DERIVED:** exact under unrestricted EH + minimal physical-metric carrier coupling |

## 6. Fork closure requirements

To move beyond UNDERDETERMINED, UDT needs an additional founding or derived rule that selects:

1. the off-shell fields and whether reciprocity is a hard configuration constraint, an on-shell
   solution condition, or a relation that may relax inside matter;
2. covariance/foliation structure, locality, and derivative order;
3. the allowed geometric invariants and their relative normalizations;
4. the unique four-dimensional completion and metric coupling of the $S^2$ carrier;
5. the finite-cell boundary functional, allowed variations, reference configuration, and charge
   normalization.

Only after those are fixed is there a determined nonlinear boundary-value problem. GPU numerics would
then test solutions of that selected theory; numerics cannot choose among the action forks.

## 7. Adversarial self-attack

1. **Could “the metric is the theory” silently mean unrestricted metric-only Lovelock premises?**
   Not from the supplied foundation. If Charles adds that as a founding rule, the EH branch becomes
   selected within its theorem class, but $\Lambda$, normalization, boundary action, and matter
   completion still require resolution.
2. **Could R3 be only an on-shell selector rather than an off-shell constraint?** Yes; that is V2.
   The present record does not decide. This is why the result is underdetermination, not an exclusion
   of V2.
3. **Could a more elaborate multiplier recover the unrestricted equation?** Only by adding derivative,
   boundary, or normalization structure for the multiplier. The algebraic multiplier enforcing
   $\nu+\lambda=0$ does not. Any enlargement is a new action premise and must be derived separately.
4. **Are the countermodels being smuggled in as candidate physics?** No. The $(Z,\mu)$ family is used
   to break uniqueness inside the historical native-action class. The lapse-weight and curvature
   terms are logical witnesses only. They are not recommended, fitted, or entered into a solver.
5. **Could full covariance plus minimal coupling remove the matter countermodels?** Yes, by assumption.
   That returns precisely the H3 conditional branch and its exact stress identity. The static energy
   alone still did not supply those assumptions.
6. **Could the finite-cell fold uniquely fix mass despite action ambiguity?** Not from the recorded
   parity condition. A derived boundary symplectic/Hamiltonian analysis could close this and is the
   correct next analytic object if Charles supplies or selects the bulk action.
7. **Could the weak-field identity fail in the numerical box?** The algebraic stress cancellation
   cannot, but $E_2=E_4$ requires an admissible scale variation. A fixed finite box can add a boundary
   virial term; therefore the equality is stated only under its explicit virial premise.

None of these attacks restores a unique action from the current foundation. They identify exactly
which added premise would change each branch.

## 8. Self-audit

- **UDT purity:** no Standard Model, quantum, fluid, Q-ball, boson-star, or textbook mechanism is used.
- **GR status:** EH/Lovelock are comparison and CONDITIONAL branches only, never adopted as native by
  familiarity.
- **No target engineering:** no fitting, physical cutoff, effective correction, or new coupling is
  proposed. Counterterms appear only as nonuniqueness witnesses and are not UDT candidates.
- **Full nonlinear operators:** all curvature, stress, and lapse identities used above are exact. The
  weak-field statement is made only after the exact conditional equation and carries $O(\kappa_g)$.
- **Variation provenance:** V1, V2, V3, and the H3 V4 branch remain distinct.
- **Boundary honesty:** the native finite-cell mass generator remains OPEN.
- **Whole-before-slice:** the exact EH reduction is stamped static/spherical/diagonal/areal/reciprocal;
  it is not stated as the verdict of the full metric.
- **Carrier status:** $S^2$ was a historical WORKING POSIT and is now **REOPENED**; round target is
  CHOSE; $L_2+L_4$ is DERIVED only given those inputs and adopted for the existing lane. The
  carrier itself may emerge or be replaced; its 4D completion remains disputed.
- **Verification:** CAS is self-verification only. A fresh independent derivation and adversarial pass
  remain required before banking.

## 9. Reproduction

Run:

```bash
python3 verify_udt_native_action_noncold.py
```

The script independently constructs the reciprocal and free-warp static spherical metrics, computes
Christoffels/Ricci/Einstein tensors, evaluates second-order Euler operators, checks the multiplier
elimination, verifies the $(Z,\mu)$ kinetic family, checks the lapse-weight countermodel, and reproduces
the conditional stress/virial identities. A passing script verifies those encoded algebraic statements
only; it cannot establish native premises or uniqueness.
