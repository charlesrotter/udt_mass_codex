# SGE1 direct mathematical review

Reviewer `/root/sge_math`, 2026-09-29. Candidate initial SHA256:
`7fe9dd385437f927504d90ebe27e70b8751e889efe9140c240a3ee1913aa0484`.
Source-first seal and its explicit metadata correction precede exposure.

**Verdict: VERIFIED-WITH-CAVEATS for the analytic restrictions, subject to the
one domain clarification M1 before integration.** This verdict does not accept
native geometry selection, an empirical prediction, a new premise or canon.
No load-bearing algebraic defect was found in equations(1)--(7). The sole
required repair concerns a globally stated auxiliary-field construction, not
the finite frequency law. The repaired overlay must be re-reviewed.

## M1 — existence of a single matching observer extension is a hypothesis

Defective implication: section2 starts by extending the endpoint clocks to a
smooth future unit field U on a tube of the ray. If interpreted as automatic
under section1's smooth time-oriented metric and regular-null-branch conditions,
that existence does not follow. Those conditions alone neither require an
embedded ray neighborhood nor exclude coincident endpoint events with distinct
clock tangents. No global chronology was assumed for equation(1).

Concrete diagnostic: put the flat metric -dt²+dx²+dy²+dz² on a domain where
t and x have equal positive periods P. It is time orientable. The null geodesic
k=∂t+∂x closes after P, without conjugate points. Select the one-winding branch
using the flat universal cover; it has a smooth regular local incidence map.
Take clocks through the same projected endpoint event with lifted tangent
u_e=(1,0,0,0) and u_o=(5/4,3/4,0,0). Both are future unit. In the cover,
emission is (s,0) and reception near the selected lift is
(P+5b/4,P+3b/4), so null incidence gives b=2s. Thus Z=2 is a regular comparison.
A single-valued spacetime field at the repeated event cannot equal both u_e
and u_o. The countercontrol is supplied geometry; it does not claim physical
UDT admission or refute the ordinary chronological experimental sector.

Strongest survivor: equations(2),(3), their bounds, and equation(7) hold whenever
the stated smooth U exists on the relevant neighborhood. The general frequency
ratio(1) remains valid on the broader regular branch and does not need a global
congruence. Along a parameterized ray, local extensions can also be used with
the necessary compatibility/patch bookkeeping; no such global theorem is needed.

Smallest source-preserving repair: explicitly declare that the congruence-based
part of the calculation is restricted to a ray neighborhood admitting a smooth
future unit field matching its endpoint clocks. Note that an embedded compact
segment with distinct endpoint events admits such an extension. Do not infer
its existence from time orientation alone. Keep equation(1) at its source scope.
This narrows the auxiliary representation domain, not the physical theory.

## Analytic checks and conclusions

1. **Frequency and physical-comparison typing.** Endpoint variation gives(1)
   exactly at the inherited regular null interface. No independent multiplier
   can be appended at fixed complete (g,Q) while keeping that observable. The
   diagnostic D_pos is honestly declared to require physical operational
   matching and native attribution; it is not claimed to be an invariant split
   selected by definition. Free-fall initial data must evolve under each metric.

2. **Directional generator.** Contracting ∇U twice with k gives
   K=H+σ(n,n)+a·n. The normalized measure ωdλ is invariant under common constant
   affine rescaling. Vorticity cancels only in this contraction. G402/G403 and
   CRD1/FSL1 source ownership is explicit. Direction independence for all n
   forces a=σ=0, for the one chosen U. No observer population or isotropy of
   the actual universe is inferred.

3. **Auxiliary-field change.** From ω_tilde=bω one has
   -d log ω_tilde=-d log ω-d log b and dℓ_tilde=b dℓ. This proves(3), including
   its sign and measure factor. Equal endpoint clocks give b_e=b_o=1 and exact
   cancellation. This is change of the intermediate observer field, not a
   coordinate transformation or a change to specified physical observers.
   The identity therefore prevents K alone being called an observer-independent
   positional density. It does not forbid meaningful fields tied to an explicitly
   admitted physical congruence, nor a relational/full-comparison law.

4. **Stationary restriction.** Killing conservation gives -g(k,ξ)=C on each
   ray and ω=C/N. N is constant on stationary clock orbits. Both actual future
   slopes are therefore reciprocal, independently of the photons' distinct C.
   The proof requires the common Killing field on the compared region and
   clocks on its orbits; it applies with stationary shift. Moving clocks in a
   stationary metric lie outside it. The conclusion is about both NET shifts,
   so it cannot exclude a separately postulated positional component masked
   by other contributions. Return availability and chronology remain separate.

5. **Controlled local bound.** With ℓ increasing from0 toL and |K'|≤B,
   |∫(K-K_e)dℓ|≤∫Bℓdℓ=BL²/2. Thus(5) is exact under the derivative bound.
   It selects neither B nor a physical crossover scale. K_e=0 gives only this
   local quadratic estimate; one normal frame or ordinary clocks is not a
   proof of finite-region GR accuracy.

6. **Matched comparison bound and asymptote.** Equation(6) follows from the
   triangle inequality on the complete mapped generators. The matching includes
   clock/ray data and uses a positive reporting orientation for each ray.
   The absolute-integral bound is sufficient, not necessary, because signed
   contributions can cancel. Divergent Z requires divergent log-integral;
   common finite |K| and L bounds preclude this. Escaping a bound need not be a
   curvature singularity. Source FSL1's direction condition and typed scalar
   clock sign are retained. No observed distance or X_max is identified.

7. **Curvature relation.** The product rule and Ricci commutator yield the
   stated Raychaudhuri sign convention. The extra geodesic/shear-free/twist-free
   reduction has its hypotheses stated. It prescribes no Ricci value and does
   not identify DDR E. Geometric identity is correctly distinguished from
   geometry selection. No full-premise underdetermination theorem is claimed.

## Independent checks and evidence limits

Source-first reviewer-owned exact checks:16 PASS, captured in source_first_01.
The initial exposure metadata erroneously said17; immutable
SOURCE_FIRST_METADATA_CORRECTION.json immediately corrects that count to16.
This is metadata history, not an additional scientific repair.

Direct reviewer-owned exact checks:22 PASS,0.576187647s,46828KiB maximum RSS,
Python3.10.12/SymPy1.13.1,60s/512MiB cap, one-thread environment, no GPU.
The code and plan were written before outcomes. The distinct metric
g=(1+t+x)²eta and rapidity log(1+2x-t-t²) activate nontrivial observer and
geometry dependence. The direct implementation recomputes metric contraction,
connection, null geodesic equation, observer covariant derivative and Ricci;
it does not import author code or define Ricci from the tested identity.
The wrong sign and omitted length Jacobian fail with exact residuals16/19
and1/4. The source-first stationary incidence and direct closed-branch
countercontrol use independently written coordinate arguments.

After direct checks finished, the reviewer read author check_geometry.py,
geometry_repair.stdout/json and original geometry.stderr. The24 named author
controls include5 explicit wrong-rule sensitivities and active shear/twist/
acceleration. The original structural equality of equivalent positive logarithms
failed as reported; the repair checks the normalized difference. That is an
implementation repair, not a changed theorem. Author code was not rerun: the
distinct reviewer derivation/checks already recompute the load-bearing quantities;
a same-code replay would only add regression evidence. No count is a proof.

Same inherited model; exact runtime identifier unavailable. Fresh-context,
source-first reconstruction and distinct implementation axes are available.
Different-model, different-library, formal-proof and human review UNTESTED.
The reviewer had prior source proofs and verdicts, so this is not blind reproof
of established G402/G403/ICN1/FSL1. No empirical fit, physical admission, full
historical-suite replay, scale selection or source law was tested. Parent owns
the full406-row audit and startup/remote synchronization. No protected payload
was read, hashed, modified or cited.

Await M1 overlay and exact integration bindings for bounded re-review.
