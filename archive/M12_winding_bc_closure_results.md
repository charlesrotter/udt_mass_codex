# M12 CLOSURE RECORD — the imported Skyrme winding BC Theta(core)=m*pi: formally scoped, not closed-by-derivation

**Mode:** OBSERVE, forensic CLOSURE (committed-doc synthesis only; nothing recomputed,
nothing committed changed). **DATA-BLIND** — no particle mass, ratio, or wall number loaded,
computed, or compared. **Driver:** Claude Opus 4.8 (1M), agent for udt_mass_codex.
**Date:** 2026-06-21. **NEW file** (append-never-edit). **NOT canon.** Blind verifier:
PENDING (ATTACK HERE block at end).

**Purpose (per Charles's "finish everything"):** bring M12 (the imported Skyrme winding
boundary condition) to a CLEAN, honest state. Either find a NATIVE sector-distinctness
mechanism, or FORMALLY SCOPE the import — state precisely what the live program USES,
what it does NOT use, and what the open question is. This record does the latter (no native
mechanism exists yet, by audit), and is therefore a **"scoped, not closed-by-derivation"**
disposition — the honest one.

Sources synthesized (all committed, quoted by finding; none recomputed):
`theta_bc_provenance_results.md` (+verifier ae844999686082572),
`native_catalog_pi2_results.md` (+verifier a44ddf2a91729b467),
`NEGATIVES_REGISTRY.md` #61, `FOUNDATIONAL_ASSUMPTIONS_LEDGER.md` (M12 row),
`F0_SYSTEMATIC_AUDIT_results.md` (M12),
`native_dilation_weight_derivation_results.md` (the derived operator + angular obstruction),
`archive/pre_2026-07-01/static_soliton_rerun_derived_operator_results.md`, `archive/pre_2026-07-01/STEP2_timelive_matter_results.md`,
`P5e_proper_results.md` (the three derived-operator solves — all charge-1 only).

---

## 1. THE IMPORT, STATED PRECISELY

**What it is.** `Theta(core)=m*pi, Theta(seal)=0` is the **radial chiral-profile**
boundary condition that counts the number of times the chiral angle Theta sweeps 0->pi
across the cell. This is a **pi_3 / SU(2)-Skyrme baryon winding number** — the textbook
hedgehog convention, written verbatim as "the SU(2)/S^3 chiral Skyrme hedgehog"
(`matter_ansatz_derive.py:28,31-32`).

**What it does in the catalog.** It is the **sector index**: m=1,2,3 are distinguished
and topologically protected by this radial BC alone. The seed generator
(`spectral_radial_soliton.py`) is purely radial — its ONLY m-dependence is the boundary
row `FT[0]=Th[0]-m*PI` (line 141); the Theta-EL residual and stress carry no m, no psi.
The azimuthal `cos(m*psi)` winding rides along in the 3-D field but does NOT define the
protected sector. So the **entire classical m=1,2,3 "catalog of types" is indexed by this
one imported BC** (theta_bc_provenance, both verifiers).

**Provenance.** AUDITED and blind-verified TWICE: it is an **IMPORT**, not UDT-derived.
The three steelman routes to "derived" all FAILED:
- **Seal/junction/transgression** constrains only metric/dilation, never the matter twist
  angle (the `dpf_derive.py:118` "Theta" is the metric 2-form (ln f)*omega_H1 — a naming
  collision, not the matter angle).
- **Core regularity at strict r=0** forces only `sin(Theta(0))=0` — a NODE condition
  satisfied by 0, pi, 2pi, 3pi equally; it selects NEITHER the value NOR the m-ladder.
  So the import verdict for m>=2 is ROBUST even if the cell reaches r=0 (verifier
  SHARPENED this; the original audit was too generous to "derived").
- **Stated-as-convention** + self-tagged **CHOSE** in the project's own ledger in TWO
  places (`native_stabilizer_results.md:244-249`; `radial_Bfree_soliton_results.md:164`).

**Banked.** NEGATIVES_REGISTRY.md **#61** (STANDING, well-corroborated: two independent
audits + two verifiers). F0 audit: M12 = ADMITTED import, VERIFIER-SUPPORTED.

Self-tag: **CHOSE** (the m*pi endpoints). What is genuinely DERIVED and untouched: the
native pi_2 area-form CHARGE quantization (omega_H1, N=3, q=1/3, CANON C-2026-06-14-1) —
requires no radial Theta condition — and the EXISTENCE of a sized degree-1 soliton.

---

## 2. IS THERE A NATIVE REPLACEMENT? — NO native ladder mechanism exists (as of now)

The native-catalog question (#61's "option a" reopener) was directly tested in
`native_catalog_pi2_results.md`: with the imported Skyrme BC REMOVED and the charge fixed
ONLY by UDT's native pi_2 area-form degree k (n: cell -> S^2), does the native L2+L4 action
produce a CATALOG of distinct stable types at k=1,2,3, or just ONE family?

**What banked solidly (verifier-confirmed, independently re-derived):**
- The pi_2 area-form degree = exactly k (own integral); the Hopf pi_3 charge = 0 (the
  hedgehog is a suspension, not a linked texture).
- On a contractible 3-cell, a smooth n: B^3 -> S^2 is null-homotopic, so the degree is a
  **SEAL/BOUNDARY charge (global-monopole-like), NOT bulk topological protection**. A
  degree-k texture can be continuously, singularity-free retracted to vacuum. "Stability"
  of a degree-k type is therefore an ENERGETICS question, not a topological guarantee.

**What did NOT cleanly bank (the honest nuance):** the headline "E_k > k*E_1 => degree-k
unbinds => ONE family" was downgraded by its blind verifier (a44ddf2a91729b467) to
**STANDS-CONDITIONALLY — the clean one-family null is NOT established**, for two reasons:
(1) an **L4 transcription bug** in the torch solvers (a missing 1/sin^2 factor and an
e^{4phi} vs e^{2phi}) — the verdict DIRECTION survives correction in the HELD frame
(deep-cell E2/E1~2.26, E3/E1~3.89), but the magnitudes were wrong; (2) the verdict is
**boundary-condition-frame-dependent**: the HELD frame (degree pinned at both radial ends)
UNBINDS, but the more-honest FREE frame (radial Neumann) deep-cell partially BINDS
(E/E1 < k) — and the doc had selectively reported the HELD result.

**Net, stated precisely:** there is **NO native sector-distinctness mechanism**. What the
native pi_2 analysis DOES establish is the harder, cleaner fact: on a regular contractible
cell the area-form degree is a **boundary charge with no bulk protection**, so nothing
NATIVE holds a degree-k (k>=2) object together as a distinct protected type. The
energetic "one family" headline is not banked (BC-frame + L4-bug confounded), but the
direction it points is unambiguous and is the load-bearing one for M12:

> **As of now, NO native k-ladder / sector-distinctness mechanism exists. The m=1,2,3
> catalog rides the import; remove the import and the multiplicity goes with it
> (whether by unbinding or by leaking through the free boundary — either way, no
> protected ladder).**

Definitive answer to the brief's question: **NO native ladder mechanism exists.** The
m-catalog rides the import.

---

## 3. FORMAL SCOPING OF M12 (the clean disposition)

### (a) WHAT THE LIVE PROGRAM USES = CHARGE-1 NATIVE ONLY.

The imported m>=2 ladder is **NOT used in any derived-operator result.** Confirmed by
direct read of all three live-program solves on the newly-derived two-player operator:

- `archive/pre_2026-07-01/static_soliton_rerun_derived_operator_results.md` — premise P3: "**Charge-1 hedgehog:
  Theta(0)=pi, Theta(seal)=0** ... Did NOT build the m>=2 ladder. The core value pi is a
  **NODE selecting degree-1, not the forbidden m*pi twist ladder**."
- `archive/pre_2026-07-01/STEP2_timelive_matter_results.md` — premise Pr-charge: "Charge-1 hedgehog ... **No m>=2
  winding ladder built.**" GATE A: Theta core->seal 3.142 -> 0.000 (clean charge-1).
- `P5e_proper_results.md` — premise Pr-charge: "Charge-1 hedgehog ... **No m>=2 ladder.**"

The single value Theta(0)=pi used in the live program is a **degree-1 NODE** (two opposite
poles, the minimal sector), NOT the imported m*pi twist-COUNT ladder. The catalog index
m (the suspect quantity) never enters the live build. **The live program's matter charge
is the native degree-1 object only.** (Note: even the degree-1 node value is not yet
derived from strict-r=0 regularity on the committed finite-r_core cell — that remains
the open r=0 physical question of #61 — but it is a single NODE, not the m-ladder import,
and nothing multi-type is built on it.)

### (b) WHAT IS PARKED = the distinct-objects catalog.

The "row of distinct stable particle types" (the multi-type catalog) is **PARKED**. It
needs a NATIVE distinctness mechanism that **does not yet exist** (Sec 2). The native
pi_2 result points the discreteness of particle families AWAY from "a stack of static
lumps of different winding" and toward the DYNAMICAL / closed-time / quantization sector
(the standing direction). This is consistent with the whole post-postulate arc: the
classical metric gives a CONTINUUM (no classical discreteness — STEP2, P5e_proper both
box-control on the derived operator); **discreteness requires quantization**, and
distinct-object multiplicity is a quantum-sector question, parked at the classical level.

### (c) THE IMPORT IS QUARANTINED — no blocking authority, not used, NOT replaced.

M12 is **quarantined**: it has **no blocking authority** (it indexes nothing in the live
program; #61 is a SCOPED negative, not a verdict on the metric), it is **not used** in any
derived-operator result, and it is **NOT replaced** (no native mechanism was derived to
take its place). This is the clean, honest disposition: **"scoped, not closed-by-
derivation."** The ledger M12 row already reflects this exactly:

> M12 ... IMPORT (the m-catalog) ... **OPEN (quarantined, NOT replaced)** — used charge-1
> native only, parked the ladder; native sector-distinctness mechanism never built.

Charles's F0 risk read confirms M12 is **additive, won't change results** (it is parked,
not load-bearing).

---

## 4. DOES THE DERIVED OPERATOR / OFF-ROUND CHANGE THE PROSPECTS? (flag, not claim)

The native pi_2 catalog test (Sec 2) was run on the **OLD operator** (static L2+L4 on the
fixed-background metric, before the two-player derived operator). The live program has
since moved to the **DERIVED two-player operator** (`native_dilation_weight_derivation`),
where the central finding is an **angular-curvature OBSTRUCTION**: R1-on-the-action cannot
homogenize the transverse/angular 2/r^2 curvature with the same single conformal weight —
the angular block is phi-free, so it is **exactly the term the global-shift symmetry
cannot wash out**, and it is "structurally aligned with Charles's standing hunch that
discreteness / scale comes from the phi-ANGULAR interaction" (that doc, Branch P). The
independent re-derivation found the SAME anisotropy ALSO obstructs the **time-live**
kinetic sector (g^{tt} ~ e^{+2phi} vs g^{rr} ~ e^{-2phi}, opposite shift-weight).

**FLAG (observe-not-target):** the derived-operator **off-round / angular sector** — the
consolidated B1'-type build, where distinct angular/topological sectors live and where the
phi-angular hunch is located — is the **natural place a NATIVE sector-distinctness
mechanism could later appear.** The angular curvature is precisely the term that refuses
the uniform weight and legitimately admits a depth scale; if a native distinctness
mechanism exists, this anisotropic angular/time sector is where to look for it.

This is a FLAG, **not a claim**: nothing here shows the off-round build DOES produce
distinct sectors. The derived-operator solves run so far (static_soliton_rerun, STEP2,
P5e_proper) are all **charge-1 only** and all **box-control to a continuum** — they have
NOT been run with the degree FREE across a native pi_2 multiplicity test, and the native
pi_2 catalog has NOT been re-run on the derived operator with the angular sector live.
So: **the prospects on the derived operator are UNEXAMINED, not improved.** The honest
statement is "this is where to look next, IF the parked catalog is ever taken up," not
"the derived operator fixes M12."

---

## 5. PREMISE LEDGER (chose / derived)

| # | Premise / value | Status |
|---|---|---|
| L1 | Theta(core)=m*pi, Theta(seal)=0 is a pi_3/SU(2)-Skyrme baryon winding BC | DERIVED-by-audit (theta_bc_provenance + 2 verifiers); self-tagged CHOSE in source ledger |
| L2 | The m=1,2,3 catalog is indexed/protected by this radial BC ALONE | DERIVED-by-audit (spectral_radial_soliton.py:141; both verifiers) |
| L3 | NO native sector-distinctness / k-ladder mechanism exists | DERIVED-by-audit (native_catalog_pi2: pi_2 degree is a boundary charge, no bulk protection; energetic "one family" direction holds but exact null NOT cleanly banked — L4 bug + HELD/FREE frame, verifier-flagged) |
| L4 | Live program (static_soliton_rerun, STEP2, P5e_proper) uses CHARGE-1 NATIVE only; no m>=2 ladder | DERIVED-by-read (P3/Pr-charge in all three docs) |
| L5 | The catalog (multi-type multiplicity) is PARKED | disposition (no native mechanism; quantum/dynamical sector) |
| L6 | M12 is QUARANTINED — no blocking authority, not used, NOT replaced | disposition (matches ledger M12 row exactly) |
| L7 | Native pi_2 CHARGE quantization (omega_H1, N=3, q=1/3) is untouched/derived | DERIVED upstream (CANON C-2026-06-14-1); NOT contaminated by M12 |
| C1 | Native pi_2 test was on the OLD operator; derived-op angular sector is where a native mechanism COULD be sought | FLAG (observe-not-target); derived-op multiplicity UNEXAMINED |
| C2 | The degree-1 node value Theta(0)=pi is not yet r=0-derived on the finite-r_core cell | OPEN (the #61 r=0 question); a single node, not the m-ladder import |

**REGIME STAMP:** static-and-time-live derived-operator program; finite mirrored cell;
charge-1 native degree-1 used live; the imported m-ladder parked + quarantined; native
pi_2 catalog test on the OLD operator only. DATA-BLIND held throughout.

---

## 6. SINGLE CLEANEST STATEMENT

`Theta(core)=m*pi, Theta(seal)=0` is an imported pi_3/SU(2)-Skyrme baryon winding BC that
indexes the classical m=1,2,3 catalog; it is self-tagged CHOSE and banked as NEGATIVE #61
(twice blind-verified). **No native sector-distinctness mechanism exists**: the native
pi_2 area-form degree is, on a regular contractible cell, a boundary charge with no bulk
protection — nothing native holds a degree-k (k>=2) object together as a distinct type
(the energetic "one family" direction holds; the exact null is NOT cleanly banked, L4-bug
+ HELD/FREE-frame, verifier-flagged). M12 is therefore **formally SCOPED, not closed-by-
derivation**: the live program **USES charge-1 native only** (confirmed in
static_soliton_rerun / STEP2 / P5e_proper — "no m>=2 ladder"), the **distinct-objects
catalog is PARKED** (awaits a native distinctness mechanism that does not yet exist), and
the **import is QUARANTINED — no blocking authority, not used, NOT replaced.** The
derived-operator **off-round / angular sector (the phi-angular-hunch home, where the
angular-curvature obstruction lives) is FLAGGED as the natural place a native distinctness
mechanism could LATER be sought** — observe-not-target; the prospects there are
UNEXAMINED, not improved.

---

## 7. ATTACK HERE (for the blind verifier — required before banking)

1. **The "no native mechanism" claim (L3, load-bearing).** Confirm from
   native_catalog_pi2_results.md + its verifier that (a) the pi_2 degree is a
   BOUNDARY charge with no bulk protection (the contractible-cell argument + the
   singularity-free retraction), and (b) the energetic "one family" headline was
   DOWNGRADED to STANDS-CONDITIONALLY (L4 transcription bug + HELD/FREE frame
   dependence). Do NOT let this record overclaim a clean energetic null — it must rest
   on the boundary-charge/no-bulk-protection fact, which IS solid, plus the unambiguous
   DIRECTION, not on a banked E_k>k*E_1 null.
2. **The charge-1-only USE claim (L4, the scoping core).** Independently confirm
   static_soliton_rerun (P3), STEP2 (Pr-charge), P5e_proper (Pr-charge) each state
   charge-1 / "no m>=2 ladder" and that Theta(0)=pi is used as a degree-1 NODE, not the
   m*pi twist ladder. If ANY live derived-operator result uses m>=2, the "quarantined,
   not used" scoping is wrong.
3. **The quarantine claim (L6).** Confirm #61 carries no blocking authority over the live
   program and that the ledger M12 row says "quarantined, NOT replaced." Confirm the
   native pi_2 CHARGE quantization (N=3, q=1/3) is genuinely untouched by M12.
4. **The off-round FLAG (C1) — targeting check.** Confirm this record FLAGS the
   derived-operator angular sector as where a native mechanism COULD be sought WITHOUT
   claiming it does (observe-not-target). Confirm the native pi_2 catalog was on the OLD
   operator and has NOT been re-run on the derived operator — i.e. the prospects are
   honestly "unexamined," not "improved."
5. **r=0 / degree-1 node (C2).** Confirm this record does NOT claim the degree-1 node
   value is derived (it is the open #61 r=0 question); confirm it correctly distinguishes
   "a single node" from "the m-ladder import."
6. **Disposition honesty.** Confirm this is presented as "scoped, not closed-by-
   derivation" — NOT as a derivation closing M12, and NOT as a soft pretend-closure.

---

## VERIFICATION (2026-06-21) — blind pass, agent a3edae128be9c0dc4
STANDS — honestly scoped, neither over-closed nor under-stated. USE=charge-1 native only confirmed (all three
derived-operator solves use degree-1 Theta(0)=pi, "no m>=2 ladder built"). The "NO native ladder" claim correctly
rests on the SOLID part (native pi_2 = a boundary/seal charge on a contractible cell, NO bulk topological
protection) and does NOT over-rely on the downgraded E_k>k*E_1 headline (which native_catalog_pi2 itself marks
STANDS-CONDITIONALLY due to an L4 transcription bug + HELD/FREE frame dependence) -- the honest nuance is
preserved. Off-round flag correctly observe-not-target ("where to look later, NOT improved by the derived
operator"). M12 = formally SCOPED (charge-1 native USED / catalog PARKED / import QUARANTINED-not-replaced).
