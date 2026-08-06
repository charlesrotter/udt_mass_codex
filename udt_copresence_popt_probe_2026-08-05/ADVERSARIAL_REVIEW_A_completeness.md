# Adversarial Review A — completeness & C2-forcing of P-opt

Date: 2026-08-05. Reviewer: adversarial (Opus, zero-context recompute). Target: `DERIVATION_NOTES.md`
step-2 claim that the **x_max kernel forces the light-distance reading (C2) -> A=1-r/X (L) = P-opt**.
Method: independent sympy from scratch (`scratchpad/rev.py`, `rev2.py`, `dl.py`); no project code imported.

## VERDICT: NARROW (the C2-forcing claim does NOT hold under a licensed reading of x_max)

x_max does not force light-distance. The forcing is an artifact of an **unlicensed "finite PROPER
separation" reading of x_max** that G14 explicitly leaves OPEN and forbids as a radial edge. Under the
coordinate/areal reading — arguably MORE natural — the proper-distance choice (quadratic) also survives,
so P-opt is not forced. I did not find a clean NAMED finite-*proper* non-L copresence distance (that would
be a hard REFUTE), so the verdict is NARROW, but the narrowing kills the central mechanism.

## 3. Independent verification of the three integrals (CONFIRMED)
Reciprocal-lock metric ds² = -A dt² + (1/A)dr² + r²dΩ² (rho=r areal, canon C-2026-06-10-1); phi=-½lnA.
"Uniform depth per X" (dphi/dX=k) with weight w=dX/dr gives generically **A(r)=exp(-2k·X_copres(r))**.
- X=coord (=null-affine; radial null geodesic has dr/dλ=E const, so affine≡coord): A=e^{-2kr}. proper=∞, optical=∞.
- X=optical (w=1/A): A=1-2kr (=L). proper=**2X (finite)**, optical=∞.
- X=proper (w=1/√A): A=(1-kr)² (quadratic). proper=∞, optical=∞.
All three profiles and the three proper integrals reproduce the notes exactly.

## 2. The x_max reading is the load-bearing, UNLICENSED premise (decisive)
G14 / STATUS_AND_WORKFLOW.md define x_max as the **relational positional-dilation asymptote**: the
separation limit where dilation exp(|delta|)->∞ (i.e. A->0). It writes s(p,q) as "the **still-open**
nonnegative observer-pair **separation type**" and forbids reading it as "a material wall, preferred
center, radial edge." The DERIVATION_NOTES silently substitutes **s = PROPER distance** — the choice that
does ALL the forcing. Enumerated survivor table ("A->0 wall at finite distance-in-measure-m"):

| x_max measured in | exp | L (optical) | quadratic (proper) | survivors |
|---|---|---|---|---|
| PROPER (notes' reading) | ∞ excl | 2X finite | ∞ excl | **{L}** (the claim) |
| COORDINATE / areal (=rho, canon) | ∞ excl | X finite | L0 finite | **{L, quadratic}** -> NOT forced |
| OPTICAL (= the copresence measure C2 itself) | ∞ | ∞ | ∞ | **{}** — even L excluded |

Coordinate = areal radius = canonical rho is a genuine geometric "separation between observers," at least
as natural as proper distance for a *max separation* that G14 calls relational and "not a radial edge."
Under it, the proper-distance copresence choice (quadratic, = OP2-DIFFERENT) is NOT excluded. x_max fails
to force L.

**Structural circularity.** Because A=exp(-2k·X_copres), the dilation wall (A->0) sits at
X_copres = +∞ for EVERY copresence choice. So x_max can *never* be finite in the copresence measure
itself; a finite x_max requires a SECOND, different measure. The derivation measures copresence in
OPTICAL distance (C2) but x_max in PROPER distance — two inconsistent measures. Under ONE consistent
measure, no profile survives (optical row above). The pick of the second measure — not x_max — is what
selects L. "x_max forces light-distance" is therefore circular: it needs C2 (n=1, optical) already chosen.

## 1. Candidate-set completeness
- **Areal radius** = coordinate r (canon rho=r theorem) -> exp profile -> excluded; not a new competitor.
- **Luminosity distance** d_L=(1+z)²r=r/A: its uniform-depth ODE A'=2kA/(2kr-A) is singular (denominator
  sign-flip at 2kr=A, A≈0.35); A reaches a minimum and never hits 0 — NO clean A->0 dilation wall.
  Pathological, not a clean competitor (`dl.py`).
- **Dilation-parameter itself** (X=phi): dphi/dphi=1 trivially; selects no profile. Degenerate.
- **The power-law FAMILY** A=(1-r/X)^{1/n} from copresence-distance X=∫dr/A^n (n=1 optical=L, n=½ proper=
  quadratic): proper-to-wall = **finite for ALL n>½** (verified: n=¾->3X, n=1->2X, n=2->4X/3, n=3->6X/5).
  So "finite proper distance" per se selects an **infinite family, not uniquely L**. L is pinned only by
  the extra choice n=1 (=optical=C2). Whether ∫dr/A^{n≠1} is a "plausible" *named* copresence distance is
  arguable — these are legitimate monotone radial functionals but not standard-named — so this is not a
  clean REFUTE, but it shows the finite-proper criterion is far from unique to L.

## Bottom line
Step-2's "x_max forces the light-distance reading -> P-opt" is **not derived**. It rests on (i) reading
x_max as finite PROPER separation, which G14 leaves OPEN and forbids as a radial edge; and (ii) implicitly
using a different measure for x_max than for copresence — the second-measure pick, not x_max, chooses L.
Under the coordinate/areal reading quadratic co-survives; under the copresence(optical) measure nothing
survives. P-opt remains conditioned on C2 (an operational choice), exactly as the notes' honest-status
section warns — but the "x_max SUPPORTS C2 by killing the alternatives (VERIFIED)" line overclaims and
should be downgraded: x_max kills the alternatives ONLY under the unlicensed proper reading.
