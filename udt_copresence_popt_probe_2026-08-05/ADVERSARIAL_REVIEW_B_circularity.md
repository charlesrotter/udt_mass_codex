# Adversarial Review B — circularity / loadedness / faithfulness

Reviewer: independent adversarial (blind-attack). Date: 2026-08-05. Target: the LEAD in
`DERIVATION_NOTES.md` + `PREREGISTRATION.md` — "copresence (C1 static + C2 distance-via-light
+ C3 uniform-depth-per-copresence-distance) + reciprocal-lock DERIVES P-opt (A=1−r/X),
upgrading the SNe fit to derived."

**VERDICT: REFUTE** (as a *derivation*). The "derivation" is CIRCULAR and C3 is LOADED;
x_max does NOT close the gap. Reciprocity IS used (so point 3 is not a refutation ground), but
reciprocity is not the selector — the tautological homogeneity choice is. The salvageable true
content is the weaker OP2-FAMILY null (narrows, kills two alternatives), NOT OP2-DERIVED.

All symbolic checks below independently reproduced (sympy).

---

## 1. CIRCULARITY — the core defect. C2+C3 RESTATE P-opt; they do not derive it.

Bank the identity the docs themselves cite: **P-opt ⇔ ℓ_opt affine in φ ⇔ A linear in r.**

Now read C2+C3 literally:
- C2: copresence-distance = ℓ_opt = ∫dr/A.
- C3: depth uniform per copresence-distance, i.e. **dφ/dℓ_opt = const.**

"dφ/dℓ_opt = const" is, word for word, "ℓ_opt is affine in φ" — which IS P-opt. With the
reciprocal metric (g_xx=1/A, so dℓ_opt/dr = 1/A and dφ/dr = −A'/2A), dφ/dℓ_opt = −A'/2, so
"= const" ⟺ **A' = const ⟺ A linear**. C2+C3 ⇒ P-opt is therefore an **identity dressed as a
result**. The driver concedes this ("Likely yes by construction", Q1; "the entire result rests
on the two premises"). Step 1 contributes **zero** derivational content — it assumes the
conclusion under a different name.

So the WHOLE non-trivial claim must live in step 2: does **x_max alone** force the optical
reading (hence P-opt) without leaning on the tautological C3-optical? It does not — see §2.

## 2. x_max does NOT force L. A finite-proper, non-linear profile survives.

The step-2 table ({null-affine→exp, optical→L, proper→quadratic}) is internally correct
(verified): exp and quadratic both have **infinite** proper distance → x_max-excluded; L has
proper distance 2X → x_max-OK. But x_max's *actual* content is only "**finite proper size**",
and that admits an **infinite family**, not just L. Concretely, Review-B's own
**H = (X−r)/(X+r)**:

| profile | proper distance ∫dr/√A | x_max | dφ/dℓ_opt | linear? |
|---|---|---|---|---|
| A=e^{−r/X} (exp) | ∞ | EXCLUDED | non-const | no |
| A=(1−r/X)² (quad) | ∞ | EXCLUDED | non-const | no |
| **A=1−r/X (L)** | **2X** | OK | **1/2X const** | **yes** |
| **A=(X−r)/(X+r) (H)** | **X(2+π)/2 ≈ 2.571X** | **OK** | X/(X+r)² non-const | **no** |

(All four rows sympy-verified.) **H is x_max-admitted and NOT linear.** The ONLY thing that
kills H is C3 in its optical form (dφ/dℓ_opt const) — i.e. the P-opt tautology of §1. Therefore
x_max, stripped of the circular C3-optical, selects a **family** (every finite-proper A(r)),
not L. The uniqueness of L is imported by the assumption, not forced by x_max.

The driver flags "candidate set may be INCOMPLETE" as "the crack the reviews must widen." It is
not hypothetical: H is a **demonstrated** survivor already in hand. The "x_max forces the
light-distance reading" sentence is true only relative to a **hand-picked triple**; the moment a
fourth finite-proper profile is admitted, x_max stops being a selector.

Note H's identity: **φ_H = arctanh(r/X)** (verified) — the *rapidity/velocity-composition*
profile. Under a copresence-homogeneity read as "depth adds like relativistic rapidity through
c" (which is arguably CLOSER to Charles's reciprocity-through-c language than the Fermat path),
the homogeneous profile is **H, not L**. So a reasonable alternative homogeneity gives a
non-L, finite-proper, x_max-OK answer. This is the answer to attack-point 2 below.

## 3. IS C3 LOADED? Yes — the distance in C3 is chosen to be the one that yields linear.

"No preferred depth" does not pick a distance. C3 attaches homogeneity to the **optical**
distance specifically. Enumerate the natural homogeneity readings and their profiles (verified):
- uniform depth per **coordinate r** (dφ/dr const) → **exponential** (φ=r/2X).
- uniform depth per **proper distance** (dφ/ds const) → **quadratic** (φ=s/L0).
- uniform depth per **optical distance** → **linear = L** (the driver's C3).
- uniform depth per **rapidity** (dφ/darctanh(r/X) const) → **H**.

Two of these are x_max-excluded (exp, quad), but **two survive** (L, H). Picking "optical" out
of the surviving pair is the loaded step: it is the choice that yields the pre-desired A=1−r/X.
"Homogeneity = uniform depth per LIGHT-distance" is therefore **not** a neutral formalization of
"no preferred depth"; it is one of several, selected post hoc because it lands on P-opt. **C3 is
loaded.**

## 4. DOES THE ARGUMENT USE RECIPROCITY? Yes — but reciprocity is substrate, not selector.

Fair finding for the driver: reciprocity (g_xx=1/A) **is** used. It gives dℓ_opt/dr = 1/A, and
that is exactly what turns "dφ/dℓ_opt const" into "A' const ⟹ A LINEAR". Without g_xx=1/A the
same homogeneity would NOT yield a linear A (dℓ_opt/dr = √(g_xx/A) breaks the −A'/2 collapse).
So the derivation is faithful to *invoking* reciprocity; point 3 of the charge sheet is **not**
a refutation ground.

BUT: reciprocity only narrows the metric to the one-function family A(r); it is agnostic among
L, H, quadratic, exponential (all have g_xx=1/A). The step that *selects* L is the tautological
C3-optical, not reciprocity. Charles's claim is that reciprocity-through-c "leads **directly**"
to P-opt. The honest reading: reciprocity supplies the stage; the P-opt selection is a separate,
assumed (§1) and loaded (§3) homogeneity axiom. So even where reciprocity is used, it is not
what "leads to P-opt" — the assumption is.

## 5. FAITHFULNESS of C1–C3 against the banked kernel (static, x_max, finite mass-energy, time flows).

- **C1 static**: faithful (Killing time, time flows). No objection.
- **C2 distance-via-light**: **unfaithful-leaning / convenient.** Copresence = "all share one
  now" = simultaneity. The natural separation between two *simultaneous* (co-present) observers
  is the **proper distance on the t=const slice**. The light/Fermat path connects events at
  **different coordinate times** — i.e. events that are NOT co-present. So a faithful copresence
  arguably demands **proper** distance ⇒ quadratic ⇒ x_max-EXCLUDED (∞ proper) ⇒ the honest
  outcome is **tension** (copresence-homogeneity is incompatible with x_max), not L. C2 swaps
  the simultaneity distance for the light distance precisely to dodge that exclusion and land on
  L. This is reverse-engineering from the wanted finite-proper answer.
- **C3**: loaded (§3).

So C1–C3 is a *convenient* formalization: C2 dodges the x_max exclusion of the natural
(proper/simultaneity) distance, and C3 pins the surviving freedom to the optical distance that
restates P-opt. The construction reaches P-opt because it was built to.

## 6. What is actually true (the honest residue)

- reciprocal-lock ⇒ family A(r), g_xx=1/A. [banked, real]
- x_max ⇒ finite proper size ⇒ **kills exponential and quadratic** homogeneities. [real, useful]
- Uniqueness of L over the remaining finite-proper family (incl. H=arctanh profile) is **NOT**
  established — it rests on choosing optical homogeneity, which restates P-opt. [the gap]

That is the driver's own **NULL / OP2-FAMILY** branch ("copresence tightens but does not
uniquely force P-opt; a family survives"), NOT OP2-DERIVED. The "candidate set complete"
condition in the conditional verdict is **false** (H is a concrete survivor), so the conditional
collapses. The SNe fit does **not** upgrade to "derived."

---

## VERDICT: REFUTE (circular + loaded; x_max does not close it).

Strongest single point: **H=(X−r)/(X+r) has finite proper distance X(2+π)/2, survives x_max,
and is non-linear — so x_max does not force L; the only thing that excludes H is C3-optical,
which is P-opt restated. The derivation assumes its conclusion.** Reciprocity is genuinely used
but is not the selector. Faithfulness of C2 is additionally suspect (copresence=simultaneity
argues for proper distance, which is x_max-excluded — the driver switches to light-distance to
escape). The honest banked statement is OP2-FAMILY (narrows, kills exp+quad), not OP2-DERIVED.
