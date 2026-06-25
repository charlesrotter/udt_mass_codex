# UDT_REBUILD.md — UDT Canonical Geometry (rebuilt)

> **STATUS: the clean canonical statement of UDT's geometry as rebuilt from the ground up (sessions 6–8).** It
> REPLACES `udt_canonical_geometry.md` (the old corpus, suspect labels). Organized BY TOPIC, not by session.
> **Not yet Charles-canonized** (Self-Hardening Protocol: only Charles canonizes). Full audit trail / provenance /
> closed attempts / changelog = **`UDT_REBUILD_History.md`**. Current working frame + next steps = **`HANDOFF_SESSION.md`**
> (THE FRAME). **The audit doc** (grades/audits claims; the 7 audits + Self-Hardening Protocol) =
> `mass_emergence_canonical_geometry.md`.
> **Discipline:** every claim states what the METRIC does, import-free; scaffolding (the fitted floor) is OUT;
> calibrated, not dramatized; "[DERIVED]/[VERIFIED]" claims carry the verifier id in History.

> **WORKING ADDENDUM 2026-06-09 - negative-phi mass rebuild:** the Form-T/Dirac import is being treated as
> legacy for the mass-emergence side. Current exploratory work lives in `negative_phi_native_geometry.md`.
> The active noncanonical frame is: finite-action negative-phi matter cells; electron mass as the single
> dimensionful anchor; and no Standard Model mechanism import. Current frontier: the metric now supplies
> exact candidates for `eta=1/18` and `eta/2=1/36` through C1 boundary momentum/action plus H1/S2 projection
> on the self-similar `q=1/3` branch; H1 trace/product powers are exact if the labels are internal and
> independent; and the metric action produces radial and angular Hessian blocks. Remaining open gates:
> derive or bank `q=1/3`, choose intrinsic-boundary versus warped-DtN transfer action, prove typed-slot
> independence, and compute the boundary reduction / Schur complement for coefficients. Status:
> noncanonical working probe, narrowed but not canonized.

---

## 1. The metric & axioms (postulate P0)

UDT is **positional dilation**: time dilation grows with distance, completing Einstein's velocity/acceleration
equivalences. The metric is
$$ds^2 = -e^{-2\varphi(r)}\,dt^2 + e^{+2\varphi(r)}\,dr^2 + r^2 d\Omega^2, \qquad g_{tt}\,g_{rr}=-1\ (\text{"}B=1/A\text{"}).$$

- **The metric IS φ — DEFINITIONAL, not Einstein-matter-sourced.** `B=1/A` forces `G^t_t = G^r_r` identically, so
  the metric's Einstein "source" is the tautological `G/8πG`; matter does not source the metric in the usual way.
  Matter instead sources φ **as a scalar field** (§4). *(Part I, verified.)*
- **Vacuum field equation** (from the C1 action `S_φ = −(c/2)∫ e^{−2φ}(∂φ)²√−g`):
  `φ″ + 2φ′/r − 2φ′² = 0`, exact solution `φ(r) = ½ln(r/(2+Cr)) + A`. Reduces to GR (→ Schwarzschild;
  Mercury, bending, β=γ=1 pass via the C1 action). Macro: redshift `1+z = e^φ`.
- **φ→−φ is an EXACT symmetry — the inside-out mirror.** φ>0 = gravity/cosmo side; φ<0 = matter side; φ→−∞ =
  a curvature-singular core (the φ→−φ image of a black-hole horizon). *(Part J.)*
- **Cosmology is Charles's domain** (same positional dilation; repo `/home/udt-admin/UDT` needs major work, off-limits).

## 2. The postulates (the honest input list)

| | postulate | status |
|---|---|---|
| **P0** | the positional-dilation metric | foundation |
| **A** | spin-½ matter (the fermion) | **BANKED** — conventional low-cost input; not derivable from geometry |
| **B** | channel closure `(j,ℓ,|κmax|)=(½,1,3)` — contains "the 3" | **BANKED** — bespoke; ALL derive routes CLOSED |
| **F** | the mₑ anchor | the ONE allowed dimensionful input (the single scale) |

- **Derive-A / derive-B are CLOSED — do not reopen as "free derivations."** Algebraic routes (ℓ-reach, spin-2
  ceiling, the Diophantine form, the κmax lemma) all died on the boson↔fermion / single-↔multi-body **category gap**.
  The **topological spin-from-isospin** route (the last hope) *relocates* the ½ into a flux/isospin input — it does
  not produce it. *(History Parts G/H/L.)* What the metric DOES derive: the **floor |κ|≥1** (core normalizability +
  Dirac `j≥½`); the cap at 3 is not in the metric (its own cap is ≈31, scale-set).
- The angular sector's ℓ=1 **representation theory is genuinely [DERIVED]** (§3) — but the *physical* quark
  identification rests on A + a rank-2 ansatz + free SM labels (charges, masses = fits). *(Guiding doc §1–§2.)*
- **The fitted floor `{μ²=π/3, φ₀=−cos(π/5), r*}` + the hard wall = SCAFFOLDING — stripped, NOT canonical.** Every
  mass in the old corpus (`6π⁵`, `84π`, …) is a dense `(rational)·πᵏ` fit, not a prediction. *(Guiding doc §0–§4.)*

## 3. The three sectors (the structure / "the instruments")

- **Radial (positional dilation) = the SCALE axis.** Proven **scale-free / covariant**: the bare matter spectrum
  depends only on the dimensionless `m·r*` (self-similar), and the metric sets **no absolute scale on its own**. A
  feature — a scale-covariant carrier of a mass ladder. *(Parts O/P.)*
- **Angular (round S²) = the QUANTUM-NUMBER axis, φ-blind** (`g_θθ=r²`, identical at every scale). **The ℓ=1
  operator algebra IS su(3)** (`8 = 3⊕5`; the totally-antisymmetric singlet exists *only* for N=3; given spin-½ the
  closure Diophantine is uniquely `(½,1,3)`). Color, the quark triplet, N=3, and the charges-as-multiplicity-ratios
  (`2/3 = (2j+1)/(2ℓ+1)`) are the group theory of the metric's own two-sphere. *(Guiding doc §1.)*
- **The φ-blind FORCE sectors — PINNED (Part T), kinematics vs dynamics:**
  - **QED (abelian Coulomb) = REAL metric-given DYNAMICS, φ-blind.** Verified symbolically (`da_register_pin.py`):
    `g^tt g^rr=−1` ⟹ `√−g g^rr g^tt = −r²` (φ cancels) ⟹ the static Maxwell equation gives **exact flat-space
    Coulomb `A_t = c₀ + Q/r`** at *every* scale (not just the flat limit). This is a genuine, usable interaction.
  - **su(3) KINEMATICS = REAL metric-given** (the ℓ=1 operator algebra `8=3⊕5` *only* at ℓ=1; the ε_abc singlet,
    unique iff N=3; the multiplicity labels `2/3=(2j+1)/(2ℓ+1)`). Usable as the **color-singlet projection +
    channel/charge bookkeeping — a SELECTION RULE, not a force.**
  - **su(3) DYNAMICS (a color FORCE / gauge connection / confinement / running α_s) = NOT metric-given.** The spin
    connection on `ds²` generates **SO(3,1), not SU(3)** (CR-195); `g_μν` carries no non-abelian internal bundle.
    Corpus concedes this (CG §18.6: "QCD partially proved — kinematics exact, **dynamics open**"). Any "QCD
    confinement DERIVED" labels (VR §29.5 / CG §19.10) are a tautological `I₂` integral + a boundary-condition
    "confinement" + dimensional matching of `b₀` — **not a dynamical force** (adversarially verified, Part T).
  - **RESOLUTION of the FRAME-vs-Part-N contradiction:** a kinematics/dynamics conflation. Part N denied the
    dynamical gauge bundle (right); §1/FRAME asserted the kinematic algebra (right). The FRAME **OVERCLAIMED**
    "QCD … to be USED" as a binding instrument — **there is NO metric-given color force.**
- **The strong coupling's STRUCTURE is geometric [DERIVED + verified, Part U].** With the *full* Dirac 4-spinor
  (upper-ℓ + lower-ℓ̃), the angular matrix elements `⟨Ω_κ|Y_{2,q}|Ω_κ'⟩` reproduce CR-190's rank-2 coupling matrix
  **EXACTLY** (Block A first row `[1,7/2,6]/(5π)`; the two parity blocks `{−1,+2,−3}/{+1,−2,+3}` DECOUPLE). The
  blocks **SURVIVE the full stress-energy back-reaction**: the Dirac bound states are **parity eigenstates**
  (`Pψ=(−1)^{ℓ_up}ψ`, verified full-spinor), the parity-even `T^{μν}` sources only the **polar** ℓ=2 channel, and
  the axial M2 self-source is **parity-forbidden** — so the `g_ij` tensor pieces refine matrix *values*, not the
  two-block selection rule (adversarial verifier SURVIVED). The ℓ=2 source is **color-SELECTIVE** (the color-singlet
  sources zero quadrupole, exact; a colored state sources nonzero). ⚠ **CAVEAT:** that this structure *is* the
  metric's ℓ=2 **back-reaction** is a HYPOTHESIS — the angular form `⟨Ω|Y₂|Ω⟩` is shared by *any* ℓ=2 coupling
  (mechanism-independent; loop not closed). So the rank-2 structure is reproduced + parity-protected **[solid]**; its
  back-reaction *origin* and its *magnitude* are **not** derived. *(`da_derive_G_vertex.py`, `da_derive_G_parity.py`.)*

## 4. Matter binding & the spectrum

- **Binding criterion [DERIVED + verified].** A massive, no-wall Dirac fermion binds (a gap bound state, 0<E<m)
  **iff the operator sees `e^{2Φ}>1`** (i.e. Φ>0). On the bare φ≤0 inside-out profile the WKB momentum
  `k² = E²e^{4Φ} − m²e^{2Φ} − κ²/r² < 0` everywhere ⟹ no binding; binding requires the operator to couple to −φ.
- **The angular sector regularizes the singular core** (centrifugal `−κ²/r²` turns the core from limit-circle to
  limit-point) ⟹ a **DETERMINED discrete standing-wave spectrum** — *the metric creates a particle-like spectrum on
  its own, with no imposed pocket or wall.* *(Part M.)*
- **What IS a particle? [RESOLVED, ontology test].** A particle is the **normalizable Dirac BOUND MODE** (finite
  `∫(G²+F²)dr`, discrete spectrum, spin-½) — it lives in the φ<0 matter sheet but sits **SHALLOW** (localizes at
  φ≈0, bound by the φ-tail; `⟨e^{|φ|}⟩≈1`). It is **NOT** the deep φ→−∞ pocket: that pocket is the metric `f=1+2/r`
  = Schwarzschild `f=1−2M/r` with **M=−1 (NEGATIVE mass)**, a genuine **curvature singularity** (Kretschmann
  `K=48/r⁶→∞`), and φ is monotone with no localized lump (Part K) — i.e. a **negative-mass NAKED SINGULARITY** (the
  inside-out mirror of a black-hole core), not a normalizable particle. ⟹ *the particle = the shallow bound mode;
  the deep pocket = singular background.* *(`da_particle_ontology`.)*
- **But the spectrum is scale-free / COMPRESSED** (Rydberg-like, depends only on `m·r*`; channel ratios O(1);
  Koide `Q≈1/3`, never 2/3). **The mass HIERARCHY is NOT in the bare metric's spectrum** — shown target-blind, over
  the metric's full natural channel range, without imposing B's cap or Koide, and not rescued by the exact angular
  operator, a monopole flux, nested cores, or a scale-invariant geometric tower (the time-dilation factor `e^{4Φ}`
  E-locks the conformal core attraction). *(Parts N/O/P.)*
- **Back-reaction (the matter→φ source), from the action [DERIVED + verified]:**
  `φ″ + 2φ′/r − 2φ′² = (1/C) e^{4φ} (T^r_r − T^t_t)`, with
  `T^r_r − T^t_t = −2σ[ κ(F²−G²)/r + Φ′(F²+G²) + m e^{Φ} G F ]` (σ=−1 binding). Classical mean-field back-reaction
  is **real but smooth and SCALE-COVARIANT** — it deepens binding and mildly reshapes ratios but selects **no
  absolute scale**. ⟹ the scale must come from QUANTUM/running effects, not classical mean-field. *(Part R.)*

## 5. The boson (dilaton) sector

The fluctuations of φ obey `−(r²e^{−4φ}u′)′ = ω²r²u`. **The clean dilaton is MASSLESS** (`μ²=0`; the scaffolded
`μ²=π/3` was a spurious mass) ⟹ its spectrum is a **gapless continuum** (no discrete modes). So the same metric makes
**discrete, massive, fermionic MATTER** + a **massless, continuous, bosonic FORCE-CARRIER** (dilaton/graviton-like)
— a clean **matter ↔ force-carrier asymmetry**. *(Part S.)*

## 6. Mass emergence — the honest status ("the orchestra")

- **VINDICATED:** the metric, with no external mechanism, **creates a real discrete spinor spectrum on its own**
  (binding + the angular regularization). The "geometry makes a particle spectrum" half of the thesis holds.
- **OPEN:** the **mass hierarchy** (and Koide 2/3, the sharp ratios) is **not** in the bare/classical metric — every
  classical sector probed in isolation rings **smooth/compressed**.
- **No hierarchy *found* in the single-particle metric via the levers tried so far [OPEN NEGATIVE — not a closure].**
  The coordinate spectra examined are compressed (~2×, §4), and the depth amplification of the real states examined
  is shallow (`⟨e^{|φ|}⟩≤1.75`, GPU, 3-cutoff stable). A *suggestive* (not conclusive) structural reason: the angular
  barrier that regularizes the core (makes states real) also keeps them shallow (real ⊥ deep). **⚠ This is "not seen
  in these attempts," NOT a proof that the single-particle metric lacks the hierarchy** — and given this session's
  high error rate, treat it as a lead to keep probing (other channels/configurations, finer methods), NOT a theorem.
  The **multi-body ENSEMBLE** is the natural untried lever; a **2nd anchor** is the fallback.
- **The MAGNITUDE (hierarchy + strong-force strength) is genuinely OPEN — and the dilaton stiffness `C` is
  UNDETERMINED.** `c²=2GM/r*` is a *boundary* closure, not a constraint on the kinetic `C`; the solar-system match
  pins the *gravity* coupling, not necessarily the *matter* back-reaction. ⚠ *Session-8 caution: several magnitude
  verdicts attempted this session ("gravitational `~M_Pl²`", a "modest 80× gap", "needs QFT/dimensional
  transmutation") were normalization errors and are **RETRACTED** — see History. The honest residue is: structure
  geometric [solid], magnitude OPEN [not settled either way].*
- **THE FRAME (Charles):** mass emergence is a **full composition (a jazz/big band), not a solo.** The sectors of §3
  are the *instruments*; the pattern lives in the **ENSEMBLE playing together**, and is invisible if any instrument
  is missing (the permutation problem). The smooth solo tones + the one clear chord (the §5 matter/force asymmetry)
  are likely the **first glimpses** of the pattern, not dead ends. The sharp/quantized structure (the "ruler") most
  likely lives in the metric's **OWN quantum sector — its QED/QCD** (§3), i.e. quantum/running effects, not classical
  mean-field (consistent with Part R).

## 7. Open work / next

1. **★ ASSEMBLE THE ENSEMBLE (the next build) — WITH THE REGISTER PINNED (Part T).** The honest "quantum register"
   is **NOT "QED + QCD as two forces"**: only **(a) the φ-blind abelian Coulomb interaction** (real DYNAMICS,
   verified) and **(b) su(3) KINEMATICS** (the ε_abc color-singlet projection + channel/charge labels — a SELECTION
   RULE) are metric-given. **There is NO metric-given color FORCE** to confine the quarks (Part T). So the build is:
   multiple radial fermions (`da_binding_criterion.py`) in their **shared, self-consistently back-reacted metric**
   (Part-R source) + the **abelian Coulomb** interaction + the **su(3) color-singlet projection as a selection rule**.
   ⚠ This is the *honest maximal* ensemble — but note it has **no confining instrument**, so it may still ring smooth;
   if it does, that is evidence the missing "ruler" is **either** the conceded-open QCD dynamics (would have to come
   from quantum/running effects in the radial sector — Part R's open frontier) **or** genuinely outside the bare
   metric. Do **not** smuggle in a color force to force a result. ⚠ A PARTIAL assembly (fermion + Coulomb only) will
   likely ring SMOOTH (the permutation problem) — assemble what the register actually contains, all at once.
2. **§5 RPA pion** (the collective q̄q mode; bridges single-particle ↔ collective).

**The φ→±φ mirror — TESTED, NOT a spectral instrument [symbolic].** φ→−φ is an exact symmetry of the metric but
**not of the binding Dirac**: it sends `e^{2Φ}→e^{−2Φ}` (binding sheet → non-binding sheet, 0 bound states), and no
companion transform (E,m,κ signs, G/F swap) restores it (a symbolic search found NONE; the `e^{±2Φ}` obstruction is
constant-redefinition-proof). ⟹ it gives **no spectral pairing, no E↔−E antiparticle relation, no new quantum number**
in the mass spectrum, so it does NOT belong to "the band." Its real role is structural — the **matter↔gravity
(micro↔macro) SCALE bridge** (φ<0 spectrum ↔ φ>0 anchor c²=2GM/r*) — i.e. part of the *scale/quantum* question, not
the spectral ensemble. (Consistent: the band's missing instruments are the quantum/QED-QCD ones, not the mirror.)

## Method & discipline

- **Calculate what the METRIC does; strip every non-UDT import & assumption.** Be wary even of imported *mechanisms*
  — including the **Form-T Dirac solver** (it bakes in a spinor ⟹ postulate A; the circularity flag). The cleanest
  import-free probe is **watch what φ does when driven negative.** No CR-labeled constructs, no scaffolding, no
  SM/QFT yardsticks.
- **Verifier-before-record** on every closure/derivation/negative (blind adversarial agent). **Calibrate, don't
  dramatize.** **Only Charles canonizes.**
- Tools: `da_binding_criterion.py` (the binding), `da_backreact_source.py`/`da_backreact_scf.py` (the source),
  `da_boson_breathe.py` (the dilaton), `da_phi_driven_negative.py` (φ driven negative). GPU = Tesla V100 via torch.cuda.
