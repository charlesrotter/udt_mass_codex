# UDT — The Problem, for Fresh Eyes

A thin, self-contained statement of this program and its central open
problem, written so a capable model with NO prior context can engage the
big picture and suggest **where to look**. Kept deliberately minimal to
avoid importing this project's own (sometimes flawed) intermediate work.
Claims are labeled **[solid]** (derived/validated), **[observed]**
(matches data, mechanism not settled), or **[open]** (conjecture / not
derived).

## 0. What this is — and what it is not

UDT is an attempt at an **alternative physics from one geometric field**:
a single position-dependent *dilation* field, from which both cosmology
and matter are meant to **emerge**. It assumes **no ΛCDM** (no separate
dark matter, dark energy, or inflation ingredients) and **no Standard
Model** particle content. Standard-Model names (quark, gauge, color) are
treated as *labels only* — to be used if and when the geometry demands
them, never assumed. The only test is **matching observations**, not
reproducing SM/ΛCDM machinery. Please engage it on its own terms.

## 1. The postulate and the derivation of the metric

**The postulate (positional dilation):** time dilation varies with
*position* — a third equivalence alongside the special- and general-
relativistic ones. Clocks run at a position-dependent rate,
d(tau) = e^{-phi} dt, set by a single scalar field phi(x). (Physically:
the apparent finite speed of light is read as this position-dependent
time dilation.)

**The metric then follows (sympy-verified derivation, not an ansatz):**
1. Static spherical symmetry gives the two-function form
   ds^2 = -A(r) c^2 dt^2 + B(r) dr^2 + r^2 dOmega^2.
2. The positional-dilation postulate fixes the time part:
   g_tt = -e^{-2phi(r)} c^2, i.e. A = e^{-2phi}.
3. The vacuum / equilibrium field equation then forces
   B = 1/A = e^{+2phi} (equivalently the derived identity
   g_tt g_rr = -c^2). (In vacuum this is a theorem; whether it also holds
   *inside matter* was an open fork — now resolved, see §4.)

So the canonical UDT metric is

        ds^2 = -e^{-2phi} c^2 dt^2 + e^{+2phi} dr^2 + r^2 dOmega^2,

with phi the single primary object and the metric its expression. The
observational tie is the redshift law **1 + z = e^{phi}** — redshift is
dilation depth, not (only) recession. **[solid]**

## 2. It derivably reduces to GR at the appropriate scales

This is a **derivation, not an empirical match.** Writing the metric
function as v = e^{-2phi}, the **vacuum field equation** (G^theta_theta = 0)
reduces to the **flat-space Laplacian**

        v'' + (2/r) v' = 0,

whose unique asymptotically-flat solution is

        v = e^{-2phi} = 1 - r_s / r,

which is **exactly the Schwarzschild metric function.** So general
relativity — and with it the entire solar-system / laboratory regime — is
**recovered as a limit of UDT by construction**, not assumed. UDT departs
from GR only at cosmological depth and (the conjecture) deep inside
matter. **[solid]**

## 3. Mass, and the one cosmic anchor (Misner-Sharp)

Mass is read **geometrically**, not added: the Misner-Sharp mass of a
region is m(r) = (c^2 r / 2G)(1 - e^{-2 phi}). The universe is modeled as
a finite dilation cell whose outer boundary is the cosmic microwave
background, at dilation depth **phi ≈ 7.004 = ln(1 + z_CMB)** and radius
of order 9 Gpc; the total mass follows from the horizon relation
c^2 = 2GM/r. On this reading the standard distance measures
(luminosity d_L = r(1+z), comoving D_M = r) fit Pantheon+ supernovae and
DESI competitively with essentially **zero free parameters**. **[observed
— the absolute scale is fixed by one observation (the CMB), and the
temperature pipeline behind it is not yet fully clean; treat the anchor as
observational, not derived.]**

## 4. The angular sector: a real discreteness, and the source of matter

The metric has an **angular sector** with a genuine **topological
(cohomological)** structure that is **independent of scale / of phi**.
Solved natively, it forces a small set of exact rational invariants — in
particular **N = 3** and a charge **q = 1/3** (with related numbers such
as 1/18). These are *derived, not fitted*, and they are the **one place a
discrete structure appears on its own** in the theory. **[solid]**

This sector turns out to be **the source of matter.** The one-function
metric (g_tt g_rr = -c^2) forces the equation of state p_r = -rho, which a
plain scalar cannot supply but the angular winding field **does**: the
unit-vector field whose winding is the N=3 / q=1/3 invariant sources
exactly p_r = -rho, so **B = 1/A is derived to hold inside matter** (not
only vacuum), with phi the *response*. Its native action is fixed and
entirely internal — a two-derivative term **plus the square of the winding
current** (this second term is the textbook Skyrme term, but here it is
*derived as our own object*, the metric-norm of the N=3 winding form, not
imported) — and it builds a **localized soliton of definite size** set by a
single scale: a particle with an intrinsic length, emergent, nothing added.
The realized particle carries the clean B=1/A metric in its **exterior** and
an EOS-softened **interior** (the same structure as a star). **[solid —
blind-verified this session]**

**A caution on lepton masses (correcting an earlier hope).** The most
natural single-cell version of the spectrum **fails a clean pre-registered,
data-blind test.** One cell holds **exactly one** such soliton (not a
tower); its only internal family is O(1)-spaced *breathing* modes, which
cannot produce the large lepton mass ratios (~207, ~3477) at any cell depth
(checked deep), and which give Koide Q ≈ 1/3, not 2/3. So the lepton family
is **not** the internal modes of a single cell. We flag this so fresh eyes
are **not** sent down it. **[the single-cell spectrum is falsified; the
cross-cell question (§6) is open]**

## 5. Driven negative, the metric makes cavities by itself

When phi is driven **negative** (the matter regime, where e^{-2phi} > 1),
the metric **spontaneously forms localized wells / "cavities"** — with
nothing added by hand. These are the natural candidates for matter: the
working picture is **a particle = one stable cell** of the metric, and this
session found that such a cell holds **exactly one** soliton (one cell = one
particle, not a tower). **[solid that cavities form and hold one soliton;
[open] the full identification with physical particles.]**

## 6. The central open problem (what we want fresh eyes on)

Real particles come in a **discrete spectrum** — specific masses with
specific ratios. **Where does that discreteness come from?**

This session **sharpened** the question by ruling out the obvious answer.
It is **not** inside a single cell: one cell = one particle, and its
internal modes are O(1) — far too small for the lepton hierarchy, whose
ratios are *exponential* (hundreds to thousands). So the discrete family
must live **across cells** — distinct stable cells, one per particle. Two
things are then open:

(i) **What discretizes the family of cells?** A single cell's depth is a
*continuum* (we cannot pin it from one cell), so the discreteness must come
from the **topological / winding sectors** (where N=3, q=1/3 live), or from
an **ensemble selection** (cells interacting in a shared back-reacted
medium), or from a **dynamic, time-dependent** phi–angular interaction —
we do not know which.

(ii) **Where does the exponential hierarchy come from?** Plausibly a
dilation-depth exponential, m ~ M_Planck · e^{-Gamma}, with Gamma set by
the angular/topological data and the cell's depth — but this is not derived.

**The ask:** given §0–5, and given that the single-cell route is now
**falsified**, where would you look for the **cross-cell discreteness** and
the **exponential hierarchy**? What would you compute first? Which of our
assumptions would you challenge? We want genuinely fresh thinking — **do not
feel bound by how we have approached it.**

## Ground rules for suggestions

- **Derive from the metric/action.** Do not add couplings, potentials, or
  mechanisms "because they would help." If a structure is needed, it must
  come out of the geometry.
- **No SM/ΛCDM import**, and no fitting masses by adding free parameters.
  We want the spectrum to *emerge*.
- **Match observations.** A proposal's value is whether the geometry,
  followed honestly, reproduces what is measured.
