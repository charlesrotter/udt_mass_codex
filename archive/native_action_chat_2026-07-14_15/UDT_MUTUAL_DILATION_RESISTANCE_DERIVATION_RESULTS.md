# UDT mutual-dilation resistance, finite reach, and carrier emergence — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Mode | Analytic DERIVE + self-CAS; DATA-BLIND |
| MAP frozen first | UDT_MUTUAL_DILATION_RESISTANCE_MAP.md, SHA-256 81993551051ad7dea41d42d13960e81202977fbfbefdc17069cc2b794ae80f9f |
| Observing or targeting? | OBSERVING whether the owner’s SR-like resistance intuition supplies UDT dynamics, whole-size stability, or a carrier |
| Symbolic verifier | verify_udt_mutual_dilation_resistance.py — **35/35 checks pass**, SymPy 1.13.3 |
| GPU | Not used and not needed; no uniquely determined nonlinear functional survived to a numerical solve |
| Independent verifier | **OPEN** — cold verification dispatch supplied separately |
| Build-on grade | **PROVISIONAL ANALYTIC RESULT**, not banked and not canon |

The macro lane remains WR-L and unchanged. The corrected round-\(S^2\), \(L_2+L_4\),
\(Q_H=1\) stability result remains valid within its stamps; this derivation neither reruns nor
promotes that conditional carrier model.

## 0. Result in one box

\[
\boxed{
\begin{gathered}
\text{Reciprocity + conditional hyperbolic reach give a natural divergent readout}\\
\mathcal R=\cosh(\Delta\phi)-1
=\frac1{\sqrt{1-(d/X)^2}}-1,\\[2mm]
\text{but they do not make it a unique action, mass law, or source.}\\[1mm]
\text{If used as a positive static pair energy, it favors contraction monotonically;}\\
\text{if its sign is reversed, it favors expansion monotonically.}\\
\text{There is no interior finite-size equilibrium and no forced }S^2\text{ carrier.}
\end{gathered}}
\]

The owner intuition contains a real structural piece and a failed dynamical inference:

- **SURVIVES:** reciprocal dilation has a natural \(\gamma\)-shaped quantity whose value and
  stiffness diverge as \(d\to X^-\).
- **FALSIFIED for MR-1 alone:** isotropic mutual attraction cannot both cancel at every point and
  stabilize the global scale. Positive MR-1 resists expansion toward \(X\), not collapse.
- **OPEN:** a future independently derived action or conservation law could place this invariant
  in a different role. No balancing term is licensed by the failure.

## 1. What reciprocity actually derives

For two positions,

\[
\Delta\phi_{AB}=\phi_B-\phi_A,\qquad
D_{AB}=e^{\Delta\phi_{AB}},\qquad D_{BA}=D_{AB}^{-1}.
\]

The simplest reciprocal-even algebraic invariant is

\[
\Gamma_{AB}
=\frac{D_{AB}+D_{BA}}2
=\cosh(\Delta\phi_{AB}).
\]

Under the **CONDITIONAL hyperbolic-composition branch**

\[
u_{AB}\equiv \frac{d_{AB}}X=\tanh|\Delta\phi_{AB}|,
\]

this becomes

\[
\Gamma(u)=\frac1{\sqrt{1-u^2}},
\qquad
\boxed{\mathcal R(u)=\Gamma(u)-1.}
\]

The exact derivatives are

\[
\mathcal R'(u)=\frac{u}{(1-u^2)^{3/2}}>0,
\qquad
\mathcal R''(u)=\frac{1+2u^2}{(1-u^2)^{5/2}}>0
\quad (0<u<1).
\]

Thus \(\mathcal R\) is positive, strictly increasing, strictly convex, and divergent at \(X\).
This is the mathematically sound part of the SR analogy.

### 1.1 Why the \(\gamma\) form is not uniquely forced

R1 and reciprocity require an even function of \(\Delta\phi\), but every

\[
\mathcal R_F=F(\cosh\Delta\phi),\qquad F(1)=0,
\]

obeys those symmetries. For example,

\[
\mathcal R_2=\cosh(2\Delta\phi)-1
\]

is also even, regular at zero, nonnegative, and divergent. Therefore:

\[
\boxed{\text{reciprocal invariant = DERIVED;\quad MR-1 functional choice = CHOSE candidate.}}
\]

Even the equality to \(1/\sqrt{1-u^2}\) is conditional on the recorded fractional-linear
distance-composition and chart join. It is not a consequence of the metric line element alone.

## 2. Putting MR-1 into an action is an additional premise

The same readout has three inequivalent interpretations:

1. **Static potential/energy:** it generates a force and can be tested for equilibrium.
2. **Kinetic inertia:** it may make changing dilation increasingly difficult, but contributes
   nothing to a static force unless a time-live covariant action supplies that coupling.
3. **Kinematic readout:** it reports reciprocal dilation and supplies no dynamics at all.

Positional dilation and reciprocity do not select among these. The static branch is nevertheless
the strongest direct realization of the proposed gravity-balance intuition, so test

\[
E_\phi
=\sigma\sum_{a<b}w_{ab}
\left[\cosh(\phi_a-\phi_b)-1\right],
\qquad \sigma>0,\quad w_{ab}>0.
\]

The coefficient, graph/pair set, weights, and continuum measure are all **FREE**. They are retained
only to prove a result that is independent of their positive values.

### 2.1 Full variation and Hessian

\[
\frac{\partial E_\phi}{\partial\phi_a}
=\sigma\sum_b w_{ab}\sinh(\phi_a-\phi_b),
\]

and for any variation \(v_a\),

\[
\boxed{
\delta^2E_\phi[v,v]
=\sigma\sum_{a<b}w_{ab}\cosh(\phi_a-\phi_b)(v_a-v_b)^2\ge0.}
\]

The common shift \(v_a=\mathrm{const}\) is the exact R1 zero mode. On a connected positive-weight
graph it is the only zero direction.

There is also a direct stationarity proof:

\[
\sum_a\phi_a\frac{\partial E_\phi}{\partial\phi_a}
=\sigma\sum_{a<b}w_{ab}
(\phi_a-\phi_b)\sinh(\phi_a-\phi_b)\ge0.
\]

Every term vanishes only when \(\phi_a=\phi_b\). Hence the only stationary state is

\[
\boxed{\phi_a=\text{constant}\quad\text{modulo the R1 common-depth shift}.}
\]

So the positive MR-1 graph energy smooths away nontrivial positional dilation. It does not derive a
WR-L profile or a nonconstant self-supported universe.

## 3. Decisive whole-scale test

Now test the proposed finite-universe balance in the physical distance variable. Fix relational
constituents and weights and uniformly rescale all separations,

\[
d_{ab}\mapsto\lambda d_{ab},\qquad
u_{ab}=d_{ab}/X,\qquad 0<\lambda u_{\max}<1.
\]

For

\[
E_+(\lambda)=\sigma\sum_{a<b}w_{ab}\mathcal R(\lambda u_{ab}),
\]

the exact scale derivatives are

\[
\boxed{
\frac{dE_+}{d\lambda}
=\sigma\sum_{a<b}w_{ab}
\frac{\lambda u_{ab}^2}
{\left[1-(\lambda u_{ab})^2\right]^{3/2}}>0,}
\]

\[
\frac{d^2E_+}{d\lambda^2}
=\sigma\sum_{a<b}w_{ab}
\frac{u_{ab}^2\left[1+2(\lambda u_{ab})^2\right]}
{\left[1-(\lambda u_{ab})^2\right]^{5/2}}>0.
\]

There is no interior stationary scale. The energy decreases whenever the configuration contracts.
For one pair,

\[
\boxed{
F_d=-\frac{d}{dd}\left[\sigma\mathcal R(d/X)\right]
=-\sigma\frac{d/X^2}{\left(1-d^2/X^2\right)^{3/2}}.}
\]

The force is inward and diverges near \(X\). It strongly prevents further **expansion**, while making
no barrier at all against contraction. Reversing the energy sign reverses every force and every
scale derivative: expansion is then favored all the way toward \(X\), again with no interior
equilibrium.

\[
\boxed{
\begin{array}{c|c|c}
\text{sign} & \text{force} & \text{scale tendency}\\ \hline
+\mathcal R & \text{attractive} & \lambda\downarrow\ \text{(contraction)}\\
-\mathcal R & \text{repulsive} & \lambda\uparrow\ \text{(expansion toward \(X\))}
\end{array}}
\]

### 3.1 Why local vector cancellation is not enough

For a finite configuration with positions \(\mathbf r_a\),

\[
\lambda\frac{dE}{d\lambda}
=\sum_a\mathbf r_a\cdot\nabla_{\mathbf r_a}E
=-\sum_a\mathbf r_a\cdot\mathbf F_a.
\]

If the net force vanished at **every** point, the right side would vanish. The positive MR-1 scale
derivative is strictly nonzero, so all forces cannot cancel in a finite configuration admitting
the scale variation. Symmetric neighbors can cancel at one selected point; that is not global
stationarity.

Taking “infinite gravity from all directions” does not evade the test. An undefined
\(\infty-\infty\) cancellation is not a variational solution. Every finite pre-limit has the
strict scale sign above, and a proposed continuum limit must first define a finite action and
measure.

## 4. MR-1 does not replace the live WR-L macro profile

The live macro lane is

\[
A_{\rm WR}=1-y,\qquad y\equiv r/X.
\]

The conditional hyperbolic distance chart is

\[
u\equiv x/X=\tanh\phi=\frac{1-A}{1+A}.
\]

They coexist only if \(x\) and areal \(r\) are kept distinct:

\[
\boxed{u=\frac{y}{2-y},\qquad
A=\frac{1-u}{1+u}=1-y.}
\]

Setting \(x=r\) would instead equate two different profiles and is not licensed. The reciprocal
invariant can be written directly on WR-L without making that identification:

\[
\Gamma_{\rm WR}(y)
=\frac12\left(\sqrt A+\frac1{\sqrt A}\right)
=\frac{2-y}{2\sqrt{1-y}}
\longrightarrow\infty
\quad (y\to1^-).
\]

Thus the divergent reciprocal readout is compatible with the WR-L wall, while the
\(1/\sqrt{1-u^2}\) expression uses the separate hyperbolic distance chart. None of this supplies
an action.

## 5. Locality and continuum-action audit

The direct continuum version of the pair candidate would be

\[
E_{\rm pair}
=\frac{\sigma}{2}\int d\mu(p)\,d\mu(q)\,
W(p,q)\left[\cosh(\phi(p)-\phi(q))-1\right].
\]

This is exact and R1-clean, but it introduces an unforced measure \(d\mu\), kernel \(W\), pair domain,
and normalization. It is bilocal: separated regions have cross terms, and an all-pair action
generically scales with the number of pairs rather than additively with volume.

For a smooth field and a small separation \(\mathbf y\),

\[
\Delta\phi
=y^i\nabla_i\phi+O(|y|^2),
\]

and on an affine patch the exact series is

\[
\mathcal R
=\frac12(y^i\nabla_i\phi)^2
+\frac1{24}(y^i\nabla_i\phi)^4
+O(|y|^6).
\]

For a general smooth field, Hessian and higher-derivative terms also enter at third and higher
orders. Odd contributions cancel only after **CHOOSING an even kernel**. For a standard one-scale
normalized kernel \(W_\ell(\mathbf y)=\ell^{-3}W(\mathbf y/\ell)\), the integrated quadratic
moment scales as \(\ell^2\), while the surviving fourth-order moments scale as \(\ell^4\).
Therefore:

- normalizing by \(\ell^{-2}\) to retain a finite local \(L_2\) term makes the quartic and all
  barrier information vanish as \(O(\ell^2)\);
- normalizing by \(\ell^{-4}\) to retain the quartic term makes the quadratic term diverge as
  \(\ell^{-2}\);
- retaining both requires a finite interaction range, two independent scalings, or a subtraction.
  None is supplied by the founding premises.

So the exact \(X\)-barrier and a local continuum action do not arrive together:

\[
\boxed{
\begin{array}{c}
\text{exact finite-separation barrier}\Rightarrow\text{bilocal/nonlocal rule},\\
\text{controlled zero-range local limit}\Rightarrow\text{quadratic scalar gradient; barrier lost}.
\end{array}}
\]

This does not forbid nonlocal UDT dynamics. It says that locality, the kernel, the measure, and the
four-dimensional time-live completion remain **OPEN**, not derived. A local ansatz
\(F(X^2g^{\mu\nu}\nabla_\mu\phi\nabla_\nu\phi)\) would be another choice: a distance bound is not a
gradient bound, the invariant changes sign between temporal and spatial gradients, and R1 does not
select \(F\).

## 6. Carrier-emergence census

### 6.1 Positional scalar alone

\(\phi\) has target \(\mathbb R\); the bounded variable \(u=\tanh\phi\) has target the open interval
\((-1,1)\). Both are contractible:

\[
\pi_3(\mathbb R)=\pi_3((-1,1))=0.
\]

Thus positional dilation alone does not contain Hopf-like topological sectors.

### 6.2 Normalized dilation gradient

Where \(\nabla\phi\ne0\), one can construct

\[
\mathbf n=\frac{\nabla\phi}{|\nabla\phi|}\in S^2.
\]

This explains why an \(S^2\) **candidate** is geometrically tempting in three spatial dimensions,
but it does not derive the existing carrier:

1. on a compact boundaryless whole domain, a smooth real scalar has extrema where
   \(\nabla\phi=0\) and \(\mathbf n\) is undefined; on a cell with boundary, avoiding such zeros
   requires boundary/flow-through structure that is not supplied;
2. writing \(\mathbf n=f\nabla\phi\) gives the exact Frobenius restriction
   \[
   n^\flat\wedge dn^\flat=0
   \qquad
   \left(\mathbf n\cdot(\nabla\times\mathbf n)=0
   \text{ in a local oriented 3-chart}\right),
   \]
   so it is a special hypersurface-orthogonal direction field, not a generic \(S^2\) map;
3. no independent round-target action or nontrivial topological sector follows from the
   construction.

### 6.3 Pair directions

The direction from \(A\) to \(B\) is a point of \(S^2\), but it is **bilocal** and there are many such
directions at each location. Selecting or averaging one direction requires a neighbor rule, kernel,
or new order field. That is additional structure.

### 6.4 Hyperbolic-angular completion

The most economical route that visibly contains \(S^2\) is the candidate state

\[
U=(\cosh\phi,\ \sinh\phi\,\mathbf n),
\]

with pair invariant

\[
\Gamma_{AB}
=\cosh\phi_A\cosh\phi_B
-\sinh\phi_A\sinh\phi_B\,\mathbf n_A\cdot\mathbf n_B.
\]

Aligned directions give \(\Gamma_{AB}=\cosh(\phi_A-\phi_B)\), and the local target metric is

\[
d\ell_{\rm state}^2=d\phi^2+\sinh^2\phi\,d\Omega_2^2.
\]

This is a useful **candidate census result**, not a derivation of the round-\(S^2\) carrier:

- for angular mismatch, the energy depends on absolute depth; at equal depth
  \[
  \Gamma=1+(1-\mathbf n_A\cdot\mathbf n_B)\sinh^2\phi,
  \]
  so the common shift \(\phi\mapsto\phi+C\) is not R1-invariant;
- the angular fiber collapses at \(\phi=0\), allowing angular structure to unwind through the
  origin;
- the full hyperbolic target is contractible, so it does not itself provide the existing Hopf
  protection;
- an action and spacetime transformation law remain unspecified.

### 6.5 Carrier verdict

\[
\boxed{
\begin{gathered}
S^2\text{ is not forced by the present derivation. It remains a reopened,}\\
\text{conditional survivor candidate.}
\end{gathered}}
\]

The derivation did expose two honest routes worth remembering—gradient directions and
hyperbolic angular fibers—but both fail at least one preregistered carrier gate. An independent
unit vector would restore a smooth round \(S^2\), but positing that vector is exactly the historical
carrier posit one level upstream.

## 7. No \(c,X,M_{\rm total}\) closure follows

Calling \(\Gamma\) an “effective mass multiplier” would import the dynamical interpretation the
derivation is testing. The pair coefficient \(\sigma\), measure, and pair count are all free, so
MR-1 does not define a native \(M_{\rm total}\).

Dimensional analysis still gives only

\[
\chi_U=\frac{GM_{\rm total}}{c^2X}.
\]

The two expressions

\[
X=\beta\frac{GM_{\rm total}}{c^2},
\qquad
c^2=\beta\frac{GM_{\rm total}}X
\]

are algebraic rearrangements of the same equation. If both \(c\) and \(X\) are global solution
outputs, a second independent native equation remains necessary.

## 8. Status ledger after the derivation

| Claim | Status |
|---|---|
| \(\Gamma=(D+D^{-1})/2=\cosh\Delta\phi\) | **DERIVED** from reciprocal dilation |
| \(\Gamma=1/\sqrt{1-(d/X)^2}\) | **DERIVED conditionally** on hyperbolic distance composition/chart join |
| MR-1 is the unique resistance/action/mass law | **FALSIFIED / UNDERDETERMINED** |
| Positive MR-1 pair energy has no finite nonzero scale equilibrium | **DERIVED under candidate P**, independent of positive weights |
| Isotropic force cancellation prevents collapse | **FALSIFIED for candidate P** by the scale variation |
| MR-1 as kinetic inertia | **OPEN** pending a full covariant time-live action |
| Exact MR-1 barrier as a local continuum action | **NOT DERIVED**; local limit loses the barrier |
| \(S^2\) carrier emerges from the present inputs | **NOT DERIVED** |
| Existing round-\(S^2\), \(L_2+L_4\) carrier | **HISTORICAL WORKING POSIT, REOPENED; conditional survivor** |
| WR-L macro form | **UNCHANGED** |
| \(X\) origin/value and \(c,X,M_{\rm total}\) closure | **OPEN** |

## 9. What is actually needed next

The missing object is still a native off-shell dynamical principle. It must independently specify:

1. whether reciprocal resistance is potential, inertia, source, or readout;
2. the full time-live field space and covariant variation domain;
3. the measure/locality rule and finite-cell boundary primitive;
4. any second contribution or constraint that creates an interior scale extremum—if UDT truly has
   one—without adding it merely to cancel the MR-1 scale sign;
5. the carrier configuration space, if matter is not carried by \(\phi\) alone;
6. a native mass functional and a second whole-system closure if \(c\) and \(X\) are joint outputs.

Until such an ingredient is independently motivated, the honest stopping point is:

\[
\boxed{
\text{divergent reciprocal resistance: strong kinematic lead;}
\quad
\text{static anti-collapse mechanism: falsified for MR-1 alone;}
\quad
\text{native action and carrier: OPEN.}}
\]
