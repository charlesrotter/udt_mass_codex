# Global bootstrap and the narrow matter-existence window — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Repository | `grok` at `64af120`; pre-existing dirty work preserved |
| Mode | Analytic DERIVE + self-CAS; DATA-BLIND |
| Owner principle record | `UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md` |
| MAP frozen first | `UDT_GLOBAL_BOOTSTRAP_ACTION_MAP.md`, SHA-256 `ba1c2fce78fc259644deb599299080b320a3ebbedf2a81540c0d28980cd9bbcf` |
| Symbolic verifier | `verify_udt_global_bootstrap.py` — **31/31 checks pass** |
| GPU | Not used and not yet warranted |
| Independent verification | **OPEN** |
| Build-on grade | **PROVISIONAL ANALYTIC RESULT**, not banked and not canon |

No observational density, particle count, lepton wall number, or window width was loaded. WR-L,
the corrected \(Q_H=1\) stability result, the reopened \(S^2\) status, and the conditional EH mass
identity retain their prior stamps.

## 0. Result

The owner-stated bootstrap principle supplies a genuine new **global selection equation**, provided
the eventual action derives both a total mass and a complete proper volume. It does not insert a new
local force or density coupling.

Let

\[
\nu=\frac{V[g]}{X^3}
\]

be the dimensionless proper-volume response of a complete solution and

\[
\mu=\frac{G M_{\rm pred}[g,\Psi]}{c^2X}
\]

its dimensionless predicted total mass. With

\[
\delta_U=\frac{G\bar\rho X^2}{c^2},
\qquad
\bar\rho=\frac{M_{\rm total}}{V[g]},
\]

global self-consistency requires

\[
\boxed{
\mu(\delta_U)=\nu(\delta_U)\,\delta_U.
}
\]

This is the bootstrap fixed-point equation in the one-parameter density reduction. In the full
theory, \(\mu\) and \(\nu\) may depend on additional dimensionless solution labels; those must be
solved, not frozen.

The new principle then requires the subset of roots that also carry stable matter to form a narrow,
nonempty set \(\mathcal W\):

\[
\boxed{
\mathcal W
=\left\{\delta_U:
\begin{array}{c}
\text{full nonlinear equations, finite-cell boundary, global closure,}\\
\text{and physical carrier-stability gates all pass}
\end{array}
\right\},
\qquad
\frac{\operatorname{width}(\mathcal W)}{\operatorname{center}(\mathcal W)}\ll1.
}
\]

The decisive status is:

- **DERIVED FROM THE NEW PRINCIPLE + DEFINITIONS:** bootstrap must be a simultaneous fixed-point
  problem; it cannot be a background density inserted into a local carrier equation.
- **DERIVED CONDITIONALLY:** in a WR-L static patch treated as the complete cell, the density window
  maps directly to a compactness/\(\alpha\) window.
- **SCOPED NEGATIVE:** the standalone flat \(S^2,L_2+L_4\) functional contains no universal-density
  variable and therefore cannot by itself generate the new window.
- **SCOPED EXCLUSION:** conditional EH+constant-\(\Lambda\) metric-only vacuum cannot produce WR-L.
- **OPEN:** whether a fully coupled metric/carrier/boundary action produces any bootstrap root, a
  narrow root set, or a unique root.
- **NOT UNIQUE YET:** the fixed-point/window requirement does not reconstruct a unique local action.

## 1. Exact global formulation

The complete unknown is not merely a carrier on a supplied background. It is

\[
\mathfrak U=(g_{\mu\nu},\Psi,\partial\mathcal M;M_{\rm total},X,c),
\]

where \(\Psi\) may be absent, the reopened \(S^2\) carrier, an emergent object, or another field.

A candidate variational completion has the schematic decomposition

\[
S[\mathfrak U]
=S_g[g]+S_\Psi[g,\Psi]+S_{\partial}[g,\Psi],
\]

but this line does not supply any term. A complete bootstrap solution must satisfy, in its declared
variation domain,

\[
\frac{\delta S}{\delta g_{\mu\nu}}=0,
\qquad
\frac{\delta S}{\delta\Psi}=0,
\qquad
\mathcal B[g,\Psi]=0,
\]

along with a mass/charge definition

\[
M_{\rm pred}=\mathcal M[g,\Psi;S,S_{\partial}],
\]

and the identities

\[
V[g]=\int_\Sigma dV_g,
\qquad
\bar\rho=\frac{M_{\rm pred}}{V[g]}.
\]

The mass and volume must be evaluated on the same full solution. Computing a carrier mass in one
geometry and inserting it into a different global volume is not a bootstrap.

## 2. Why \(\delta_U\) is the correct dimensionless density

With \(G,c,X\) available, total density has the dimensionless combination

\[
\boxed{
\delta_U=\frac{G\bar\rho X^2}{c^2}.
}
\]

Write

\[
V[g]=\nu[g]X^3.
\]

Then the universal compactness is

\[
\chi_U=\frac{GM_{\rm total}}{c^2X},
\]

and exactly

\[
\boxed{
\delta_U=\frac{\chi_U}{\nu[g]}.
}
\]

This relation is kinematic/bookkeeping after \(M,V,X,c\) have native meanings. It is not a field
equation.

## 3. Conditional WR-L static-patch calculation

For the live macro metric

\[
ds^2=-A c^2dt^2+A^{-1}dr^2+r^2d\Omega^2,
\qquad
A=1-\frac rX,
\]

the constant-time spatial measure is

\[
dV=\frac{r^2\sin\theta}{\sqrt{1-r/X}}\,dr\,d\theta\,d\varphi.
\]

If—and only if—the static region \(0<r<X\) is taken as the complete volume entering the bootstrap,

\[
V_X
=4\pi\int_0^X\frac{r^2}{\sqrt{1-r/X}}\,dr
=\boxed{\frac{64\pi}{15}X^3}.
\]

The proper radial distance to \(r=X\) is finite:

\[
\ell_X=\int_0^X\frac{dr}{\sqrt{1-r/X}}=2X.
\]

This agrees with the live scope that \(r=X\) is a causal horizon at finite proper distance, not
automatically a hard end of all space. Therefore \(V_X\) is a **CONDITIONAL STATIC-PATCH VOLUME**, not
yet the derived total universal volume. If the completed universe includes another region, its
volume changes \(\nu\) and all numerical factors below.

For this conditional patch,

\[
\nu_{\rm WR-L}=\frac{64\pi}{15},
\qquad
\bar\rho=\frac{15M}{64\pi X^3},
\]

and

\[
\boxed{
\delta_U=\frac{15}{64\pi}\chi_U.
}
\]

## 4. What a narrow density window fixes

Let

\[
\delta_-<\delta_U<\delta_+.
\]

For constant \(\nu\), this maps to

\[
\nu\delta_-<\chi_U<\nu\delta_+.
\]

If one writes the still-unproved dimensional closure

\[
X=\alpha\frac{GM_{\rm total}}{c^2},
\qquad
\alpha=\frac1{\chi_U},
\]

then

\[
\boxed{
\frac1{\nu\delta_+}<\alpha<\frac1{\nu\delta_-}.
}
\]

Thus a narrow bootstrap window can sharply constrain the formerly free dimensionless coefficient
\(\alpha\). If the stable root is unique, it fixes \(\alpha\) rather than fitting it.

However, a finite window is an inequality, not one exact equation. The continuum

\[
\delta(s)=\delta_-+s(\delta_+-\delta_-),
\qquad 0<s<1,
\]

contains infinitely many possible densities whenever \(\delta_+>\delta_-\). “Extremely narrow” may
make the uncertainty small but does not convert the band into an exact unique value.

## 5. The actual bootstrap equation

Suppose a full dimensionless solve at trial \(\delta\) predicts

\[
M_{\rm pred}(\delta)=\frac{c^2X}{G}\,\mu(\delta)
\]

and

\[
V(\delta)=X^3\nu(\delta).
\]

Self-consistency requires the density reconstructed from those outputs to equal the trial density:

\[
\delta
=\frac{G M_{\rm pred}X^2}{c^2V}
=\frac{\mu(\delta)}{\nu(\delta)}.
\]

Therefore

\[
\boxed{
F_{\rm boot}(\delta)
=\mu(\delta)-\nu(\delta)\delta=0.
}
\]

The matter-bearing window consists only of roots/branches that also pass existence, boundary,
regularity, charge, and stability gates.

This distinguishes two questions:

1. **Does a self-consistent universe exist?** Solve \(F_{\rm boot}=0\).
2. **Can stable matter exist in it?** Test the carrier/full-system critical point and physical
   Hessian on those roots.

Neither answer may be imposed while constructing \(\mu\) or \(\nu\).

## 6. Why the bootstrap root does not reconstruct the action

Even an exact root \(\delta_*\) does not determine the full response. For example,

\[
\mu_1(\delta)=\nu\delta_*+a(\delta-\delta_*)^2,
\]

and

\[
\mu_2(\delta)=\nu\delta_*+b(\delta-\delta_*)^4
\]

both satisfy

\[
\mu_i(\delta_*)=\nu\delta_*,
\]

but differ away from the root. These are response-function counterexamples, not candidate UDT
actions. They establish an inverse-problem fact:

\[
\boxed{
\text{one bootstrap root, or one narrow window, does not uniquely reconstruct local dynamics.}
}
\]

The principle is nevertheless highly selective when applied prospectively: complete candidate
actions must derive \(\mu\), \(\nu\), and \(\mathcal W\) without window engineering.

## 7. Conservation does not dynamically tune total density at fixed volume

For the conditional \(V=\nu X^3\) with constant \(\nu\),

\[
\bar\rho=\frac{M}{\nu X^3}
\]

gives

\[
\boxed{
\frac{\dot{\bar\rho}}{\bar\rho}
=\frac{\dot M}{M}-3\frac{\dot X}{X}.
}
\]

Likewise,

\[
\delta_U=\frac{GM}{\nu c^2X}
\]

gives, for constant \(G,\nu\),

\[
\boxed{
\frac{\dot\delta_U}{\delta_U}
=\frac{\dot M}{M}-\frac{\dot X}{X}-2\frac{\dot c}{c}.
}
\]

Thus, if \(M,X,c\) are constant, recycling among localized, horizon, and reservoir sectors leaves
total density unchanged. It preserves the ledger; it does not steer the universe toward the window.

If \(M\) and \(c\) are constant but \(X\) changes,

\[
\frac{\dot\delta_U}{\delta_U}=-\frac{\dot X}{X}.
\]

Then maintaining matter viability would require the full geometry/constant closure to keep the root
inside \(\mathcal W\); a compensatory matter-creation rule cannot change total density when total mass
is conserved.

This makes the bootstrap principle primarily an **existence/realization selector**, not an automatic
late-time feedback mechanism.

## 8. One compactness root is still only one global relation

Suppose the bootstrap fixes \(\chi_U=\chi_*\). Then

\[
\chi_* = \frac{GM}{c^2X}
\]

fixes the product \(c^2X=GM/\chi_*\), not \(c\) and \(X\) separately. Indeed,

\[
c\mapsto\lambda c,
\qquad
X\mapsto\frac{X}{\lambda^2}
\]

leaves \(\chi_U\) unchanged.

Therefore the narrow density principle may supply the previously missing **dimensionless
compactness selector**, but a second independent dimensional closure remains necessary if both
\(c\) and \(X\) are to emerge rather than be observed inputs.

The electron mass can normalize one local energy combination. It does not by itself supply a total
particle count, universal volume, or second global equation.

## 9. Action-branch audit

### 9.1 Conditional EH metric-only vacuum

For WR-L,

\[
R=\frac{6}{Xr},
\]

and the mixed Einstein-tensor readout is

\[
G^t{}_t=G^r{}_r=-\frac{2}{Xr},
\qquad
G^\theta{}_\theta=G^\varphi{}_\varphi=-\frac{1}{Xr}.
\]

An EH+constant-\(\Lambda\) vacuum would require \(R=4\Lambda\), constant, and
\(G^\mu{}_\nu=-\Lambda\delta^\mu{}_\nu\). WR-L satisfies neither condition.

\[
\boxed{
\text{WR-L is not a vacuum solution of the conditional EH+constant-}\Lambda\text{ metric-only branch.}
}
\]

This is a **SCOPED CONDITIONAL EXCLUSION**, not a native UDT field equation. The EH branch must add a
derived matter/carrier stress, abandon source-free WR-L, or cease to be the geometric action.

Metric-only “matter as geometry” remains OPEN because no native localized metric solution and no
bootstrap mass response \(\mu\) have been derived.

### 9.2 Higher-curvature metric-only actions

They pass the flat-frame curvature gate and may admit non-EH vacuum geometries. But the bootstrap
principle does not select their invariant basis or coefficients. Reverse-engineering a term so that
WR-L or a narrow window appears would violate the no-target/no-mechanism rule.

Grade: **ALLOWED FAMILY, untested**.

### 9.3 Prior constrained/native geometric action

The prior angular-curvature-mismatch action possesses scoped flat off-round cancellation, but its
full time-live completion, total Hamiltonian charge, universal proper volume, and unrestricted versus
constrained variation provenance remain open. Therefore neither \(\mu(\delta)\) nor
\(\nu(\delta)\) is presently defined for it.

Grade: **CONDITIONAL REDUCED BRANCH; bootstrap not yet formable**.

### 9.4 Standalone reopened \(S^2,L_2+L_4\) carrier

Its flat static scale energy is

\[
E(R_s)=C_2\xi R_s+\frac{C_4\kappa_4}{R_s}.
\]

It has

\[
R_*^2=\frac{C_4\kappa_4}{C_2\xi},
\qquad
\left.\frac{d^2E}{dR_s^2}\right|_{R_*}>0
\]

for positive coefficients, but neither \(E\) nor \(R_*\) contains \(\delta_U\). Thus its standalone
scale mode has no density window:

\[
\boxed{
\frac{\partial E}{\partial\delta_U}=0,
\qquad
\frac{\partial R_*}{\partial\delta_U}=0.
}
\]

This does not erase the corrected numerical stability result. It establishes that the flat carrier
functional alone cannot implement the new global-bootstrap principle.

- Under the **strong local-window reading**, the standalone flat model fails the principle.
- Under the primary **global-window reading**, the carrier remains a conditional survivor only after
  full physical-metric coupling, backreaction, boundary closure, and total-mass self-consistency are
  solved.

The current numerical box \(L=6\) is a solver choice and must not be identified with the cosmic
\(X\).

### 9.5 Conditional EH plus carrier

This branch can in principle define both a geometric mass response and carrier viability, but the
existing work has only a weak/static conditional source identity and has not solved the global
backreacted universe. It also retains the unrestricted-versus-reciprocal source fork.

Grade: **FORMABLE IN PRINCIPLE, NOT YET SOLVED**.

### 9.6 Boundary/global-charge branch

The bootstrap requires a charge defined on the finite cell and a time-live zero-flux law. Static
\(\phi=0\) at the seal does not by itself provide the Hamiltonian generator, charge normalization, or
total volume beyond a causal horizon.

Grade: **REQUIRED STRUCTURE, OPEN**.

### 9.7 Explicit average-density coupling

An action term such as

\[
\mathcal L_{\rm local}(x;\bar\rho)
\]

with \(\bar\rho\) inserted to turn matter on only inside a desired band is nonlocal and unforced. A
hard density cutoff is likewise forbidden.

Grade: **REJECTED unless independently derived from a legitimate global variational variable and
boundary condition**.

## 10. Matter-window boundary mechanisms are outputs, not premises

For a continuous solution branch, a boundary of \(\mathcal W\) could occur through:

1. disappearance of the nontrivial critical solution;
2. a physical Hessian eigenvalue reaching zero;
3. loss of finite mass/charge;
4. loss of global regularity or boundary closure;
5. failure of the bootstrap equation itself.

If stability is lost smoothly, one expects the boundary condition

\[
\lambda_{\min}^{\rm phys}(\delta_\pm)=0.
\]

But a branch may terminate singularly or fail the boundary before a Hessian zero occurs. Therefore
zero-mode boundaries are a test branch, not a postulate.

## 11. What would be required to compute \(\mathcal W\)

No GPU scan is warranted yet because no surviving branch has a complete native action, global mass,
and time-live boundary definition. Once one does, the proper computation is:

1. nondimensionalize with trial \(\delta_U\) and keep all action coefficients fixed by theory or one
   declared observational normalization;
2. solve the full nonlinear metric, carrier, and boundary equations simultaneously;
3. compute \(M_{\rm pred}\), \(V\), and
   \(F_{\rm boot}=\mu-\nu\delta\) from the solved fields;
4. continue all solution branches in \(\delta\), without targeting a narrow interval;
5. at every bootstrap root, independently verify criticality, topology/charge, raw Hessian residuals,
   boundary flux, and convergence;
6. locate all existence/stability endpoints and test grid, domain, and discretization convergence;
7. obtain a fresh independent implementation before calling \(\mathcal W\) narrow or unique.

This is a nonlinear eigenvalue/continuation problem. GPU numerics become relevant only after the
continuum functional and global boundary problem are no longer open.

## 12. What the new principle has accomplished

The bootstrap principle does not yet produce the unique action, but it supplies the strongest native
global discriminator obtained in this sequence:

\[
\boxed{
\begin{gathered}
\text{The action must generate its own mass, volume, background geometry, and matter viability.}\\
\text{Those outputs must close }\mu(\delta)=\nu(\delta)\delta.\\
\text{Stable matter-bearing roots must occupy only a narrow, derived window.}
\end{gathered}
}
\]

It can potentially fix \(\chi_U\) and the dimensionless \(X\)-mass coefficient \(\alpha\). It cannot
by itself:

- determine the absolute pair \((c,X)\);
- choose metric-only versus independent substrate;
- derive \(S^2\);
- make the standalone \(L_2+L_4\) carrier density-sensitive;
- define total mass or the finite-cell boundary charge;
- reconstruct a unique local action from one root/window.

## 13. Updated frontier

\[
\boxed{
\begin{gathered}
\text{Global Bootstrap / Narrow Matter Window = OWNER-STATED WORKING PRINCIPLE.}\\
\text{Bootstrap fixed-point architecture = DERIVED.}\\
\text{WR-L patch density-to-compactness map = CONDITIONAL-DERIVED.}\\
\text{Pure EH+}\Lambda\text{ vacuum realization of WR-L = EXCLUDED within that conditional branch.}\\
\text{Standalone flat }S^2,L_2+L_4\text{ density window = ABSENT in that scoped functional.}\\
\text{Fully coupled action, global charge, window existence/width, and carrier = OPEN.}
\end{gathered}
}
\]

## 14. Verification scope

The standalone CAS checks the reciprocal spherical curvature, WR-L Einstein readout, conditional
proper volume, density/compactness/\(\alpha\) maps, fixed-point algebra, inverse-response
counterexample, conservation identities, compactness scaling degeneracy, standalone carrier scale
mode, and one-mass calibration. It does not prove the owner principle, Lovelock premises, window
existence, action completeness, total-volume identification, or physical carrier stability.
