Stage A is complete. I have reconstructed the local compatibility conditions from the authorized accepted sources without opening the candidate. This is an independent mathematical reconstruction, not a verdict on the unseen candidate.

1. The precise local condition depends on what has been supplied.

Let \(g\) be smooth, time-oriented, four-dimensional, with signature \((-+++)\). Suppose a specified null family defines a smooth, nonzero, future-directed null line field on an open neighborhood. Choose a representative \(\ell\) and put \(\alpha=g(\ell,\cdot)\).

A smooth phase satisfying

\[
d\Theta=f\alpha,\qquad f>0
\]

exists locally exactly when

\[
\alpha\wedge d\alpha=0.
\]

Necessity follows by differentiating \(d\Theta=f\alpha\). Sufficiency is the local codimension-one Frobenius theorem: a nonvanishing integrable one-form has a local integrating factor. The sign can be chosen to give a future-raised gradient. Nullness then follows from nullness of \(\ell\).

This is a local statement after shrinking the neighborhood. It supplies neither a global real phase nor a globally consistent choice across caustics, intersecting branches, nontrivial periods, or a nontrivial foliation leaf space.

If the normalization itself is specified, so that the requirement is \(d\Theta=\alpha\), the condition is stronger: \(d\alpha=0\) locally. On larger domains, vanishing periods are additionally needed for a real global potential.

These statements concern a phase obeying the eikonal equation throughout an open neighborhood. A phase first jet supplied only along one ray does not establish those neighborhood hypotheses. G352 supplies its phase; its accepted derivation does not itself prove a general neighborhood extension theorem.

2. Null geodesicity is necessary but does not replace integrability.

For \(k=(d\Theta)^\sharp\) null throughout the neighborhood, symmetry of the Hessian gives

\[
k^b\nabla_b k_a
=k^b\nabla_a k_b
=\frac12\nabla_a(k^bk_b)=0.
\]

Thus the gradient normalization is affine, and

\[
k(\Theta)=g(k,k)=0.
\]

The phase is constant along its own null generators.

Conversely, a smooth affine null geodesic congruence need not admit an aligned phase. A direct counterexample in Minkowski coordinates \((t,x,y,z)\) is

\[
\ell=\partial_t+\cos z\,\partial_x+\sin z\,\partial_y .
\]

It is future null. Its coefficients depend only on \(z\), while \(\ell(z)=0\), so \(\nabla_\ell\ell=0\). But

\[
\alpha=-dt+\cos z\,dx+\sin z\,dy
\]

has, at \(z=0\),

\[
\alpha\wedge d\alpha
=dt\wedge dy\wedge dz-dx\wedge dy\wedge dz\ne0.
\]

No positive rescaling of this line field is a phase gradient on a neighborhood of that point. This is a geometric obstruction; it says nothing about physical population.

Normalization also requires care. If \(\nabla_\ell\ell=\kappa\ell\), any integrating factor producing an affine gradient must satisfy

\[
\ell(\log f)=-\kappa.
\]

That raywise equation is necessary, but does not enforce transverse integrability. For example, if \(d\Theta=dz-dt\), multiplying its raised gradient by a positive nonconstant function \(c(x)\) preserves affine null geodesicity, but \(c(x)(dz-dt)\) is not closed.

Once one optical phase exists, another gradient defining the same null line field must locally have the form \(d\widetilde\Theta=h(\Theta)d\Theta\), hence \(\widetilde\Theta=F(\Theta)\) with \(F'>0\). Arbitrary independent rescaling from generator to generator is generally unavailable.

3. A ray, a source-vertex sheet, and a neighborhood congruence supply different amounts of information.

An individual regular null geodesic has no transverse twist data to test. Locally around an interior point, one can construct an optical neighborhood containing it by choosing appropriate spacelike initial data for the eikonal equation. The other generators, wavefronts, and normalization are additional choices. This establishes local extendibility, not that the ray or the metric selects a unique extension.

For G349’s source-vertex family, the relevant three-dimensional map is

\[
(\lambda,n)\longmapsto\gamma_n(\lambda).
\]

On a screen-rank-two branch, after restriction to a locally embedded patch, its tangent space is spanned by the null generator and two orthogonal Jacobi variations. It is therefore a null hypersurface. A regular portion admits a local optical extension: intersect it with a spacelike hypersurface, prescribe compatible eikonal initial data there, and use local characteristic existence. The generator normalization can be prescribed compatibly on a transverse cut and carried affinely.

The one supplied source cone is only one phase level. It supplies neither neighboring phase levels nor a common transverse-label identification between them. A two-dimensional cut supplies still less.

The source vertex cannot be included as an ordinary point of a smooth nonzero gradient aligned with an open set of distinct outgoing directions: a single gradient at the vertex has only one direction. Caustics and intersecting branches likewise require branch restrictions; G348’s regular phase-space evolution does not make their spacetime projection one smooth congruence. None of these failures implies a singular metric.

For an already specified neighborhood congruence, neighboring rays cannot be replaced merely to manufacture a phase. Its own Frobenius condition must hold.

4. When the optical phase exists, local coordinates and a product realization can be supplied compatibly.

Choose two independent transverse labels \(y^A\) constant along \(k\), and choose an affine coordinate \(v\) with \(k(v)=1\). Locally,

\[
(\Theta,v,y^1,y^2),\qquad k=\partial_v
\]

are coordinates, with metric

\[
g=2\,d\Theta\,dv
+H\,d\Theta^2
+2B_A\,d\Theta\,dy^A
+q_{AB}\,dy^A dy^B,
\]

where \(q_{AB}\) is positive definite. This follows from \(k^\flat=d\Theta\): \(g_{vv}=g_{vA}=0\), \(g_{v\Theta}=1\). The coefficients are the supplied metric expressed in chosen coordinates, not a new field equation or selected metric.

At fixed phase, a regular cut \(v=v_i(\Theta,y)\) has induced transverse metric \(q_{AB}\) evaluated at that cut. Its cut-gradient contributes only the null generator direction. This matches the geometric reason behind G349’s variable-cut area result.

The local space of generators is represented by \((\Theta,y^1,y^2)\). Thus a G352 product can be chosen on \(I_\Theta\times\Lambda\):

\[
d\Xi=\frac{|d\Theta|}{\Delta\Theta}\otimes d\mu(y).
\]

Here \(d\Theta\) in the measure expression denotes positive phase-coordinate variation, not an asserted spacetime volume form. The product is three-dimensional data on phase and transverse labels; it does not automatically include an affine-parameter measure.

For the required realization, one supplies:

- a common transverse-label identification across the neighboring phase sheets;
- a finite nonnegative countably additive \(\mu\);
- the same support and weights on every phase slice;
- one common \(\Delta\Theta>0\);
- measurable, label-preserving comparison maps.

On a bounded phase interval this product is finite. On an unbounded interval it need not be finite, although the product remains a well-defined measure.

Local product coordinates do not derive phase-independent content. A phase-dependent relabeling generally presents the same measure using phase-dependent transverse measures. Consequently, the factorization is meaningful relative to the supplied identification of labels across phase slices. G351 conserves supplied measure between source-free cuts; it does not require different phase slices to have identical content.

Because \(k(\Theta)=0\), successive phase values are not successive positions along one generator. They label neighboring wavefronts. A timelike observer crosses those phase levels locally. A single ray or single cone cannot alone supply that entire product construction.

5. The accepted readout follows conditionally, with its original restrictions.

For a future unit timelike observer \(u_i\),

\[
\omega_i=-d\Theta(u_i)>0,
\qquad
\frac{d\Theta}{d\tau_i}=-\omega_i.
\]

On a regular label chart with

\[
d\mu_{\rm ac}=s(y)\,dy,\qquad dA_i=J_i(y)\,dy,\qquad J_i>0,
\]

the G351/G352 realization gives

\[
\Gamma_i=\frac{\omega_i}{\Delta\Theta}\frac{s}{J_i}.
\]

Therefore, on common nonzero absolutely continuous regular support,

\[
\frac{\Gamma_j}{\Gamma_i}
=\frac{\omega_j}{\omega_i}\frac{J_i}{J_j}
=R_{ji}A_{ji}^{-1}.
\]

Zero content obeys the homogeneous transfer relation but supplies no ratio or exponent witness. Singular content has no ordinary area-density exponent. At rank loss, the weighted pushforward remains finite only if \(\omega_i/\Delta\Theta\) is integrable against \(\mu\).

G352’s invariance under a common positive affine phase change requires scaling \(\Delta\Theta\) together with \(\Theta\). Although optical geometry permits monotone nonlinear \(F(\Theta)\), a nonlinear change does not preserve the declared common fixed-spacing readout by itself.

The weights \((1,-1)\) remain unique only for this readout in G350’s full independent positive character domain, as stated by the accepted G351/G352 sources. A single constructed geometry does not establish that full-domain uniqueness.

Literal atomic crossings remain different measures. No smooth instantaneous rate for them follows from the continuous product. Likewise, a local observer tangent supplies a local phase derivative, not a global observer worldline or guaranteed interception of every phase level.

6. What is determined, supplied, and open.

Geometry determines the integrability test for the specified family, the consequences of an existing eikonal phase, quotient-screen geometry, regular metric areas, and the local measured derivative of a supplied phase relative to a supplied observer.

The family itself, optical initial data or integrating factor, phase calibration, neighboring-phase extension, transverse identification, measure and populated support, fixed phase spacing, cuts, and observers remain supplied. The choice to use G352’s phase-independent product remains a chosen mathematical realization. G351 conservation and the G352 readout remain owner-adopted provisional premises.

There is no inherent mathematical incompatibility between an admissible optical congruence and choosing such a product. Minkowski space with

\[
\Theta=z-t,\quad v=(t+z)/2,\quad
g=2\,d\Theta\,dv+dx^2+dy^2
\]

and any finite transverse measure on a bounded \((x,y)\) patch supplies a simple mathematical witness. This does not establish physical instantiation or select this witness.

Physical carried content, sources, populated labels, cross-label physics, detector interpretation, light, energy, matter, history, scale, and \(X_{\max}\) remain open. Neither the obstruction example nor the compatible witness changes those grades.

7. Exposure, checks, and exact command record.

I received the Stage A dispatch in a separate context without the parent conversation. I have not opened or searched the candidate directory, work order, proof, code, outputs, or reviews. Incidental candidate exposure consisted of the supplied review question, pinned hash, and the commit subject printed by `git log`. Protected payload contents were not opened.

My exact underlying runtime model identifier is not exposed. I make no different-model claim. This is a separate-context argument and a separately written short arithmetic check, not a claim of proof independence from standard mathematical methods.

I personally verified branch `grok`, HEAD `3c841561ca0d1529ca41ef75fb1aece465ee0098`, and the visible untracked status. I did not repeat checkout, fetch, or pull because this dispatch is pinned and read-only. Parent synchronization and source-hash checks are parent-reported evidence, not checks I repeated. At the latest parent update, the live premise verifier was still running; I claim no completed pass. I did not query the wide registry.

The accepted-source audit grades control over pending historical headers in the G349 and G352 exact derivations. I read all ten authorized scientific documents, including the complete G348 derivation in two ranges. One combined tool result truncated part of the G352 audit/start of its derivation; I explicitly reread that material.

No scratch directory or script file was created. No repository file was written. No package scripts, infrastructure suites, GPU jobs, field-equation solves, or browsing were run. The short CPU check used Python 3.10.12 and exact `Fraction` arithmetic. It confirmed the displayed nonzero Frobenius three-form at \(z=0\), the flat optical-coordinate metric, and positive observer frequency \(1\). These are arithmetic checks accompanying the analytic argument, not a numerical completeness claim.

All commands used `/home/udt-admin/udt_mass_codex` as working directory. The exact shell commands were:

```bash
pwd && git status --short --branch && git rev-parse HEAD && git log -8 --oneline && sed -n '1,260p' AGENTS.md
awk '/STARTUP_CURRENT/{show=1} show{print} /END_STARTUP_CURRENT/{exit}' LIVE.md
awk '/STARTUP_CURRENT_BEGIN/{show=1} show{print} /STARTUP_CURRENT_END/{exit}' HANDOFF.md
sed -n '1,240p' CURRENT_RESEARCH_PROGRAM.md
sed -n '1,260p' CURRENT_SCIENTIFIC_PREMISES.md
rg -n '^#{1,4} |How we work|DRIVER TRIGGERS|discipline|verifier-before-record|completeness|no-shortcuts' CLAUDE.md
sed -n '9,83p' CLAUDE.md && sed -n '121,145p' CLAUDE.md
sed -n '1,260p' .claude/skills/no-shortcuts/SKILL.md
sed -n '1,260p' .claude/skills/completeness-map/SKILL.md
sed -n '1,280p' .claude/skills/verifier-before-record/SKILL.md
sed -n '1,220p' INDEX.md && sed -n '1,220p' MEMORY.md
wc -l udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/{AUDIT_REPORT.md,EXACT_DERIVATION.md} udt_g349_finite_null_wavefront_patch_area_2026-09-04/{AUDIT_REPORT.md,EXACT_DERIVATION.md} udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/{AUDIT_REPORT.md,EXACT_DERIVATION.md} udt_g352_clock_rate_carried_measure_readout_2026-09-05/{AUDIT_REPORT.md,EXACT_DERIVATION.md,ADOPTION_RECORD.md,EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md}
sed -n '1,280p' udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/AUDIT_REPORT.md && sed -n '1,340p' udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/EXACT_DERIVATION.md
sed -n '1,280p' udt_g349_finite_null_wavefront_patch_area_2026-09-04/AUDIT_REPORT.md && sed -n '1,360p' udt_g349_finite_null_wavefront_patch_area_2026-09-04/EXACT_DERIVATION.md
sed -n '341,430p' udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/EXACT_DERIVATION.md && sed -n '1,260p' udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/AUDIT_REPORT.md && sed -n '1,260p' udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/EXACT_DERIVATION.md
sed -n '1,240p' udt_g352_clock_rate_carried_measure_readout_2026-09-05/AUDIT_REPORT.md && sed -n '1,260p' udt_g352_clock_rate_carried_measure_readout_2026-09-05/EXACT_DERIVATION.md && sed -n '1,180p' udt_g352_clock_rate_carried_measure_readout_2026-09-05/ADOPTION_RECORD.md && sed -n '1,200p' udt_g352_clock_rate_carried_measure_readout_2026-09-05/EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md
sed -n '1,160p' udt_g352_clock_rate_carried_measure_readout_2026-09-05/AUDIT_REPORT.md && sed -n '1,105p' udt_g352_clock_rate_carried_measure_readout_2026-09-05/EXACT_DERIVATION.md
```

The exact arithmetic command was:

```bash
python3 -B -S - <<'PY'
from fractions import Fraction as F
from itertools import permutations
import sys
print('Python', sys.version.split()[0])
# At z=0 for ell=dt-vector+cos(z)dx-vector+sin(z)dy-vector:
# alpha=-dt+dx and d(alpha)=dz wedge dy, with coordinates t,x,y,z.
a={(0,):F(-1),(1,):F(1)}
da={(2,3):F(-1)}
def wedge(a,b):
    out={}
    for ia,va in a.items():
        for ib,vb in b.items():
            j=ia+ib
            if len(set(j)) != len(j): continue
            inv=sum(j[r]>j[s] for r in range(len(j)) for s in range(r+1,len(j)))
            k=tuple(sorted(j))
            out[k]=out.get(k,F(0))+va*vb*((-1)**inv)
    return {k:v for k,v in out.items() if v}
print('twisting_witness_alpha_wedge_dalpha_at_z0',wedge(a,da))
assert wedge(a,da)=={(0,2,3):F(1),(1,2,3):F(-1)}
eta=[F(-1),F(1),F(1),F(1)]
l=[F(1),F(1),F(0),F(0)]
assert sum(eta[i]*l[i]*l[i] for i in range(4))==0
# Flat compatible optical coordinates: Theta=z-t, v=(t+z)/2, x,y unchanged.
columns=[[F(-1,2),F(0),F(0),F(1,2)], [F(1),F(0),F(0),F(1)], [F(0),F(1),F(0),F(0)], [F(0),F(0),F(1),F(0)]]
g=[[sum(eta[m]*columns[i][m]*columns[j][m] for m in range(4)) for j in range(4)] for i in range(4)]
expected=[[0,1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]]
assert g==expected
print('flat_optical_metric',g)
k=[0,1,0,0]
assert [sum(g[i][j]*k[j] for j in range(4)) for i in range(4)]==[1,0,0,0]
u=[F(-1),F(1,2),F(0),F(0)]
assert sum(g[i][j]*u[i]*u[j] for i in range(4) for j in range(4))==-1
omega=-sum(g[i][j]*u[i]*k[j] for i in range(4) for j in range(4))
assert omega==1
print('flat_future_observer_omega',omega)
print('Exact arithmetic checks passed; analytic scope is stated separately.')
PY
```

It exited zero and printed:

```text
Python 3.10.12
twisting_witness_alpha_wedge_dalpha_at_z0 {(0, 2, 3): Fraction(1, 1), (1, 2, 3): Fraction(-1, 1)}
flat_optical_metric [[Fraction(0, 1), Fraction(1, 1), Fraction(0, 1), Fraction(0, 1)], [Fraction(1, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)], [Fraction(0, 1), Fraction(0, 1), Fraction(1, 1), Fraction(0, 1)], [Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(1, 1)]]
flat_future_observer_omega 1
Exact arithmetic checks passed; analytic scope is stated separately.
```

The three method protocols influenced this review by requiring explicit neighborhood versus ray hypotheses, separate ownership of the product measure, and factual exposure/check reporting. They supplied no scientific premise. I stop here awaiting Stage B.
