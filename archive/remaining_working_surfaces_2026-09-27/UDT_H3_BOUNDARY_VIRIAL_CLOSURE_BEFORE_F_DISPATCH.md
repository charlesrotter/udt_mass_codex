# WORKSTATION DISPATCH — H3 boundary-virial closure before F

**Date:** 2026-07-16  
**Branch:** `grok`  
**Order:** audit G → derive/test boundary virial → bounded box scout → **STOP**; F remains locked  
**Data discipline:** DATA-BLIND. No particle labels, observed masses, fitted couplings, or chosen physical cutoff.  
**Record discipline:** preserve unrelated dirty files; do not edit `LIVE.md` or `CANON.md`.

## 0. Audited input and the question

Commit `493d104` passes the dispatched G gates:

- the eight-orientation densities reproduce the corrected `noNull` energy;
- \(\rho+S=2\rho_4\) holds pointwise;
- the seven-point DST-I Poisson solve and discrete bond flux close to roundoff;
- the independent verifier passes 90/90.

The weak-field lapse result therefore stands with its existing premise stamp:

\[
M_N^{(0)}=2E_4
\qquad
\text{CONDITIONAL on the EH lapse identity.}
\]

At fixed \(L=6\), however, the continuum-at-fixed-box audit gives

\[
E_{\rm carrier}=E_2+E_4\simeq275.9,
\qquad
M_N^{(0)}=2E_4\simeq283.3\text{--}283.5,
\]

with

\[
\delta_{\rm vir}=\frac{E_2-E_4}{E_2+E_4}\simeq-2.7\%.
\]

Do **not** call this a choice between two equally valid particle masses.  Algebraically,

\[
M_N^{(0)}-E_{\rm carrier}=E_4-E_2=\int_\Omega S\,dV .
\]

The open question is whether this integrated stress is the support supplied by the pinned finite box and tends
to zero as the boundary recedes.  This dispatch derives and tests that proposition before finite-amplitude F.

## 1. Premise ledger

- \(S^2\) carrier and \(L_2+L_4\) functional: **POSIT / CHOSE**.
- Eight-orientation no-null discretization: **DERIVED numerically** as the same continuum functional.
- G lapse identity and \(M_N^{(0)}=2E_4\): **CONDITIONAL** on the EH metric-only action.
- Finite-grid static stability at \(L=6\), `HBW=2`: **OBSERVED / NUMERICALLY CERTIFIED**.
- “The virial gap is a box effect”: **WORKING / OPEN** until this dispatch.
- Infinite-volume stability or mass: **OPEN** regardless of the scout outcome.

No GR field equation is used to derive the carrier or its virial relation.  The stress identity below follows
directly from the stated carrier functional; the conditional EH premise enters only when reading \(2E_4\) as a
lapse mass.

## 2. Preflight

Run and show:

```bash
git checkout grok
git fetch origin
git pull --ff-only origin grok
git status --short --branch
git log -8 --oneline
```

Read in order:

1. `LIVE.md` CURRENT STATE;
2. `HANDOFF.md`;
3. `stability_branch_follow_256_DECISION.md`;
4. `UDT_H3_CORRECTED_G_THEN_F_SEQUENCING_DISPATCH.md`;
5. `noNull_phaseG_mass.py`, `noNull_phaseG_mass_ALL.json`, and the G verifier output;
6. `noNull_energy.py`, `noNull_resolve.py`, and the three critical-field manifests.

Hash every input.  Preserve the existing NPZs.  The new larger-box fields must have new, explicit filenames.

### 2.1 Complete the missing G raw-log evidence first

The G commit references `phaseG_production.log` and `phaseG_verify.log` in
`phaseG_evidence_2026-07-16/environment.txt`, but those two raw logs are not tracked in commit `493d104`.
This is an evidence-completeness miss, not a numerical contradiction.

Before V1:

1. record SHA-256 hashes of the committed production and verifier JSON;
2. rerun the exact committed G production and verifier commands while capturing complete stdout/stderr into
   `phaseG_evidence_2026-07-16/phaseG_production.log` and
   `phaseG_evidence_2026-07-16/phaseG_verify.log`;
3. compare the regenerated JSON and all gate scalars with the committed record;
4. if any load-bearing value changes beyond printed roundoff or the verifier is not 90/90, stop before V1;
5. include the recovered logs and pre/post hashes in the boundary-virial evidence commit.

Do not silently replace the existing JSON.  A deterministic identical rerun closes the evidence gap; a
difference is a new result requiring adjudication.

## 3. V1 — derive the finite-domain carrier virial identity

For

\[
\mathcal E=\mathcal E_2+\mathcal E_4,
\quad
\mathcal E_2=\frac{\xi}{2}\partial_i\mathbf n\cdot\partial_i\mathbf n,
\quad
\mathcal E_4=\frac{\kappa}{4}F_{ij}F_{ij},
\]

derive from the functional—not from a textbook assertion—the spatial stress

\[
\mathcal T_{ij}
=\xi\left(\partial_i\mathbf n\cdot\partial_j\mathbf n-\frac12\delta_{ij}X\right)
+\kappa\left(F_{ik}F_{jk}-\frac14\delta_{ij}Y\right),
\]

where \(X=\partial_k\mathbf n\cdot\partial_k\mathbf n\) and \(Y=F_{kl}F_{kl}\).

Verify symbolically:

\[
\mathcal T_{ii}=-\mathcal E_2+\mathcal E_4=S.
\]

For an exact stationary solution, derive the translation identity

\[
\partial_i\mathcal T_{ij}=0
\]

including the \(|\mathbf n|=1\) constraint explicitly; show why the Lagrange-multiplier term drops after
contraction with \(\partial_j\mathbf n\).  Then derive

\[
\boxed{
E_4-E_2
=\int_\Omega \mathcal T_{ii}\,dV
=\oint_{\partial\Omega}x_j\mathcal T_{ij}\nu_i\,dS
\equiv B_{\partial\Omega}
}
\]

for a finite domain.  State the residual-corrected identity under one explicit Euler-residual sign convention
and verify that sign symbolically.  The numerical test must include the residual-work term rather than assuming
the saved fields are exactly critical.

Required consequence:

\[
\boxed{
M_N^{(0)}=E_{\rm carrier}+B_{\partial\Omega}
}
\]

under the conditional lapse premise.  Only if \(B_{\partial\Omega}\to0\) in a controlled isolated limit may one
recover \(M_N^{(0)}=E_{\rm carrier}\).

Create a short derivation record plus a CAS/algebra verifier.  Label the continuum identity **DERIVED** and the
application to the numerical box **to be tested**.

## 4. V2 — exact discrete scale response on the existing three fields

Create `noNull_boundary_virial.py`.  Reuse only the corrected eight-orientation functional.

At fixed field samples and fixed \(N\), change the common physical lattice scale

\[
h\mapsto\lambda h,
\qquad L\mapsto\lambda L,
\]

without changing \(\xi,\kappa\) or the array values.  The existing functional must give exactly

\[
E(\lambda)=\lambda E_2+\lambda^{-1}E_4,
\]

so

\[
\left.\frac{dE}{d\ln\lambda}\right|_{\lambda=1}=E_2-E_4.
\]

Verify this by direct recomputation at

\[
\lambda=1\pm\epsilon,
\qquad
\epsilon\in\{2\times10^{-4},10^{-4},5\times10^{-5}\},
\]

and by the analytic split.  Required relative agreement: \(<10^{-9}\).  This is an exact discrete conjugate
response of the fixed-box family; it is not yet evidence that the response vanishes at large \(L\).

At each of \(128^3,192^3,256^3\), also report:

- \(\int S\,dV=E_4-E_2\);
- \(2E_4-(E_2+E_4)\);
- the equality of those two expressions to roundoff;
- the residual work of the dilation generator, using the full corrected raw gradient and an explicitly stated
  tangent/free projection;
- a Cauchy bound on that residual work.

Do not let a preconditioned norm replace the raw energy derivative.

## 5. V3 — localization and surface-stress audit

The G record localized \(E_4\) but not \(E_2\).  On the three existing \(L=6\) carriers, report nested cube and
sphere fractions for **both** \(E_2\) and \(E_4\), using the same site-density convention and radii as G.

Build the eight-orientation-averaged \(\mathcal T_{ij}\) from the same one-sided derivatives.  On nested cubic
surfaces evaluate

\[
B(a)=\oint_{\partial C_a}x_j\mathcal T_{ij}\nu_i\,dS
\]

with all face placement and quadrature choices explicit.  Compare it with the enclosed trace

\[
V(a)=\int_{C_a}(\rho_4-\rho_2)\,dV
\]

and the residual-work correction from §3.  Because a site-based one-sided discretization need not possess an
exact local Noether theorem, this is a convergence test, not an assumed exact lattice identity.

Required reporting:

- raw \(B(a),V(a)\), residual correction, and closure error at every surface/grid;
- face-placement sensitivity of one half-cell in/out;
- whether the closure improves from 128→192→256 at matched physical \(a\);
- no hand-tuned surface selection.

If the local surface construction fails to converge, label it `UNRESOLVED`; the exact global scale response from
V2 still stands but must not be relabeled a proven boundary theorem.

## 6. V4 — bounded fixed-spacing box scout

The decisive discrimination requires moving the numerical boundary while holding the local resolution and mask
thickness fixed.  Do a bounded scout before any large production extension.

### V4a — coarse fixed-\(h\) scout

Use

\[
h_\mathrm{c}=12/127\simeq0.0944882,
\]

with grid sizes

\[
N\in\{128,160,192\},
\qquad
L_N=\frac{(N-1)h_\mathrm c}{2}
\simeq\{6.000,7.512,9.024\}.
\]

Construct the larger-box starts by centering the \(N=128,L=6\) carrier in the larger arrays and filling every
new site with the same asymptotic constant \(\mathbf n_\infty\).  Do not rescale or interpolate the carrier core.
Keep `HBW=2`, which now has the same physical thickness throughout this fixed-\(h\) scout.

Independently re-relax the \(N=160\) and \(N=192\) fields with the repaired moving-tangent trust-region
Newton–Krylov code, the corrected energy, fixed boundary, exact \(U(1)\) handling, and no Derrick rescaling.
Require

\[
\|g_f\|_{M^{-1}}<0.05
\]

using the same definition as the certified fields.  Report failures honestly; do not loosen the gate.

For every converged box report \(E_2,E_4,E,E_4-E_2,\delta_{\rm vir}\), both no-null charges, criticality, maximum
neighbor angle, and \(E_2/E_4\) localization.  The primary scout question is simply whether
\(|\delta_{\rm vir}|\) decreases as \(L\) increases at fixed \(h\).

### V4b — one finer confirmation, conditional on the scout

Run this only if V4a is monotone and technically clean.  At

\[
h_\mathrm f=12/191\simeq0.0628272,
\]

compare the existing \(N=192,L=6\) carrier with a padded, independently re-relaxed
\(N=240,L\simeq7.51\) carrier.  Use the same gates and observables.  Do not run a Hessian.

If V4a is non-monotone, fails criticality, changes topology, or reveals a second branch, stop before V4b and
return `UNRESOLVED` with the raw trajectories.

## 7. Decision table

| Outcome | Allowed conclusion |
|---|---|
| V2 exact; V3 closes with grid convergence; \(|\delta_{\rm vir}|\) decreases cleanly with \(L\) in V4 | **STRONG BOX-STRESS LEAD**: the fixed-box gap is carried by boundary dilation stress; infinite-volume closure still OPEN |
| V2 exact but V3 does not converge; V4 gap decreases | **BOX-EFFECT NUMERICAL LEAD**, local boundary theorem OPEN |
| V2 exact; V4 gap persists at larger \(L\) | finite-box explanation not supported in the probed range; carrier/action interpretation OPEN |
| Any larger box fails criticality or topology | new branch/boundary problem; stop, no mass identification |

No bounded scout may establish the \(L\to\infty\) limit.  Do not extrapolate an infinite-volume mass from three
box sizes unless a later dispatch preregisters and verifies that limit.

## 8. Independent verification and deliverables

Create an independent verifier that does not import production density, stress, surface, or scale-response
functions.  It must recompute:

- the eight-orientation \(E_2,E_4,S\) integrals;
- the exact \(h\)-scale derivative;
- at least three surface-stress entries per existing grid;
- every larger-box energy, charge, and criticality scalar from saved fields;
- all decision-table predicates.

Retain raw relaxation trajectories.  Hash and manifest every new field.  Run syntax checks and the existing
evidence checker.  Commit one evidence-only commit containing code, compact JSON, derivation/CAS record,
verifier, raw logs, and manifests.  Do not edit `LIVE.md` or `CANON.md`.

## 9. Stop

Stop after this boundary-virial return.  **Do not run F.**

The current honest status while this dispatch is pending is:

\[
\boxed{
\begin{gathered}
\text{fixed-box carrier static stability: numerically settled within stamps},\\
M_N^{(0)}=2E_4:\ \text{conditional Gauss/lapse identity},\\
M_N^{(0)}=E_{\rm carrier}:\ \text{OPEN because }\int S\,dV\neq0,\\
\text{boundary-stress explanation: WORKING / to be tested.}
\end{gathered}
}
\]
