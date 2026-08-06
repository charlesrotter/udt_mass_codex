# Adversarial Review A — STEELMAN OP-DERIVED (try hard to FORCE P-opt from full Reciprocity)

Reviewer: independent adversarial pass, 2026-08-05. Zero derivation-code imported; all checks
recomputed from scratch in SymPy. Mandate: attack OP-INDEPENDENT as a lazy giveup by deriving
P-opt from the FULL Observer-Reciprocity structure (equivariance / naturality / groupoid cocycle
on NULL paths), not the weak "antisymmetry" version the driver used.

## 0. Setup recomputed independently
Reciprocal-lock metric `ds^2 = -A c^2 dt^2 + dr^2/A`, depth `phi = -1/2 log A` (so `A=e^{-2phi}`).
Radial null: `c dt = dr/A`, Fermat optical path `dl_opt = dr/A`. P-opt: `dl_opt = kappa dphi`.
Independent check: `dl_opt/dphi = -2/A'(r)`. **P-opt <=> A'(r) = const <=> A = 1 - r/X** (X=kappa/2).
Confirmed exactly. So "derive P-opt" == "force A' constant from reciprocity alone."

## 1. The weak version (what the driver used) — correctly insufficient
The cocycle `delta(p,q)=Phi(p)-Phi(q)` is antisymmetric AND satisfies the full composition law
`delta(p,q)+delta(q,s)=delta(p,s)` **for an ARBITRARY profile Phi** (SymPy: both reduce to 0
identically, no constraint on Phi). The H-type `A=sech(r/X)` gives `dl_opt/dphi =
2X cosh^2/sinh` (NOT const) yet is a perfectly valid antisymmetric, composing cocycle. So the
weak version cannot force P-opt. Driver correct here.

## 2. The STEELMAN: full equivariance / naturality on NULL paths — does it force P-opt?
I pushed every stronger lever the audit's groupoid-cocycle machinery offers. Each FAILS, and the
failure is structural, not lazy:

**(a) Groupoid single-valuedness / exactness.** Requiring `delta` be endpoint-only (all loop
periods vanish, `alpha=dPhi` locally) constrains phi to be a genuine *potential* — single-valued
in r. In the 1D radial sector this is automatic and says nothing about the r<->phi *profile*. No
constraint on A'. FAIL.

**(b) Uniqueness of a reciprocity-invariant parametrization — the crux.** The claim to force is
"the optical affine parameter and the depth coincide up to scale." I tested it as "depth
accumulates uniformly along the canonical parameter of the reciprocal radial flow." But the flow
admits SEVERAL equally natural canonical parameters, and each yields a DIFFERENT profile
(SymPy-verified):
  - uniform depth per **null-geodesic affine parameter** (I derived `dr/dlambda = E/c = const`,
    so *r itself is the affine parameter* of radial null rays): `dphi/dr=const` => **A = EXPONENTIAL**.
  - uniform depth per **optical/Fermat path** (= Killing coordinate-time x c): => **A = LINEAR = P-opt**.
  - uniform depth per **proper radial distance** `dr/sqrt(A)`: => **A = QUADRATIC**.
Reciprocity/naturality is AGNOSTIC among these. Decisively: the *geodesically canonical* choice
(the null affine parameter) gives EXPONENTIAL, **not** the L profile. So P-opt is not even the
naturality-preferred option — it is the specific selection "the Fermat optical length is the depth
meter," which reciprocity does not privilege. This is the opposite of a lazy giveup: the strongest
naturality argument actively points AWAY from L. FAIL (and then some).

**(c) Null strain object — light carries no reciprocity depth.** The signed depth extractor is
`delta_t = -1/2 log(lambda_timelike)`, defined on the UNIQUE TIMELIKE strain eigenline. A null
direction `(1,1)` under the reciprocal strain `diag(e^{-2delta},e^{2delta})` maps to
`(e^{-2delta},e^{2delta})` — NOT an eigenvector (timelike stretch != spacelike stretch). Light has
no single reciprocity strain-depth. The depth cocycle is intrinsically a CLOCK/timelike object; it
does not live on optical rays at all. So "light must meter depth under reciprocity" has no carrier
to begin with — there is nothing for reciprocity to make affine. FAIL at the root.

**(d) Round-trip / radar reciprocity.** A->B->A: both optical path and depth close to 0 for ANY
profile (SymPy: roundtrip depth = 0 identically). Radar distance is symmetric for every A. No
profile constraint. FAIL.

## 3. Verdict
Every strengthening of Observer Reciprocity — exact single-valued cocycle, full equivariance,
naturality of the flow parametrization, the null/strain object, round-trip radar — leaves the
radial profile A(r) FREE. Reciprocity fixes the reciprocal FORM `A=e^{-2phi}` and the cocycle
TYPE; it does not, and structurally CANNOT, fix A'(r). P-opt is a genuinely independent,
profile-selecting optical principle ("Fermat length meters depth"), equivalent to selecting the
orchestra's free law/`a`. OP-INDEPENDENT is CORRECT and NOT lazy.

Note for the record: the driver reached the right conclusion via the weak (antisymmetry-only)
argument; this review supplies the stronger justification he did not — and, importantly, shows the
best naturality argument gives EXPONENTIAL, further hardening OP-INDEPENDENT rather than merely
failing to overturn it.

**VERDICT: PASS** (OP-INDEPENDENT holds; P-opt not forced by full Reciprocity).
