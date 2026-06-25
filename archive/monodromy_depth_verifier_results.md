# BLIND ADVERSARIAL VERIFIER — Depth-Monodromy of the Collective-Coordinate Soliton

Verifier: Claude (Opus 4.8, 1M context), agent run 2026-06-15. Blind, independent
re-derivation. The constructor scripts (`monodromy_depth_probe.py`,
`monodromy_collective_reduction.py`) were NOT run. Own sympy CPU symbolic work +
scipy/numpy float64 numerics. Target: `monodromy_depth_results.md` (NO-MONODROMY).

Mandate: TRY HARD to REVIVE a depth-dependent angular phase; the negative must
survive an ACTIVE S^3 / psi(r) rescue. DATA-BLIND (no lepton/hadron wall numbers,
no Koide, no sqrt(2), no 45-deg loaded, computed, or compared).

Scripts (this run, committed):
- `verif_monodromy_twist.py` — generalized ansatz with internal-longitude twist
  Psi(r); L2+L4 radial functional (sympy, exact angular reduction).
- `verif_L4_check.py` — L4/L2 angular-integral machinery + carrier identification.
- `verif_psi_eom.py` — the DECISIVE test: Psi enters the action only as (Psi')^2
  (S^2 carrier).
- `verif_psi_s3.py` — the S^3/SU(2) Skyrme escape hatch: symmetric iso-twist also
  enters only as (Psi')^2.
- `verif_berry_seal.py` — Berry phase = 0, seal Dirichlet-mismatch test, chi
  cyclic => no D_n, Bohr-Sommerfeld = SPIN.
- `verif_numeric.py` — degree=1/dTheta=pi depth-fixed, forced-twist gamma(D)
  smooth (no isolated roots), Lambda_3(D) smooth/monotone.

---

## DECISIVE RESULT OF THE ESCAPE-HATCH ATTACK (Claim 3, the hardest)

I built the MOST GENERAL axially-symmetric charge-1 ansatz that ADMITS a second
internal profile — an internal-longitude twist Psi(r):

    n = ( sinTheta(r) cos(phi+Psi(r)), sinTheta(r) sin(phi+Psi(r)), cosTheta(r) )

(Psi=const => pure meridian/hedgehog; Psi(r) varying => an S^3-like internal
helix sweeping nonzero solid angle.) I formed the EXACT L2+L4 proper-energy
radial functional on the back-reacted UDT cell (sympy, angular integration in
closed form), then read its Psi-dependence:

    E_r[Theta,Psi,phi]  contains Psi ONLY through  (Psi')^2,
    coefficient  W(r) = pi xi r^2 e^{-phi} sin^2(Theta) >= 0,
    coefficient of the LINEAR term Psi'^1  ==  0 (exactly),
    bare-Psi (non-derivative) dependence  ==  none.

Consequences (decisive):
- Psi = const is ALWAYS a solution of the Psi-EOM `d/dr[W(r) Psi'] = 0`, and it is
  the strict ENERGY MINIMUM (any Psi'!=0 raises E because W >= 0).
- There is NO SOURCE for Psi'. Neither the back-reaction phi(r) (it only reweights
  W, staying positive) nor anything else appears linearly in Psi' or as a bare
  Psi. A depth-dependent monodromy needs a depth-SOURCED Psi'(r); the action
  provides no source term, so back-reaction CANNOT induce one.
- With free/natural (Neumann) seal endpoints, the natural BC gives W Psi'|ends = 0
  => Psi' == 0 everywhere => pure meridian => zero swept solid angle at EVERY depth.

THE ESCAPE HATCH IS CLOSED. The back-reaction does not revive a twist.

### The S^3 escape hatch ALSO fails (refines Claim 4)

I went further and put a genuine S^3/SU(2) Skyrme hedgehog on the cell
(U=exp[i F(r) (R_z(Psi) hat{r}).tau], the unit 4-vector pion field) and applied
an internal isospin twist Psi(r) about the iso-3 axis. Result:

    E_r[F,Psi,phi]  again contains Psi ONLY through (Psi')^2,
    coefficient  pi xi r^2 e^{-phi} sin^2(F) sin^2(theta) >= 0,
    LINEAR coefficient == 0,  bare-Psi == none.

So even S^3 does NOT source a depth-phase from a *sigma-model* iso-twist. This
SHARPENS the structural reason (below): the obstruction is not merely "S^2 has one
profile"; it is that an axisymmetric internal twist about the easy/iso axis is a
CYCLIC (U(1)-symmetric) coordinate, entering purely as its squared gradient, for
BOTH targets. A genuinely depth-quantizing S^3 phase would require the Hopf/linking
(pi_3) WZW/theta term — a topological term, NOT a sigma-model twist — which is
absent from L2+L4. (This is consistent with, and independent of, the project's
standing read that a WZW/spinor ingredient lives in a different sector.)

---

## CLAIM-BY-CLAIM VERDICTS

**Claim 1 — winding depth-fixed, Berry phase = 0.** CONFIRMED.
- Degree B = 1 and Delta Theta = Theta(core)-Theta(seal) = pi at EVERY depth: this
  is fixed by the charge-1 BCs (Theta(core)=pi -> Theta(seal)=0), depth-independent
  by construction (`verif_numeric.py`, p=0..2 all give dTheta=pi).
- Berry/geometric phase gamma = INT (1-cosTheta) Psi'(r) dr. For the meridian
  (Psi'=0) gamma = 0 identically, for ANY Theta(r) and ANY depth. Since the action
  FORCES Psi'=0 (above), gamma=0 is forced, depth-independently. CONFIRMED.

**Claim 2 — chi cyclic => no D condition.** CONFIRMED.
- L_eff = (1/2)Lambda_3(D) chidot^2 - E0(D); p_chi = Lambda_3(D) chidot is
  conserved (chi cyclic, no explicit chi). omega = J/Lambda_3(D); over one period
  T=2pi/omega, Delta chi = 2pi for EVERY D. Single-valuedness imposes NO condition
  on D. No D_n selected classically.

**Claim 3 — back-reaction / seal revive a depth phase (S^3/psi(r))?** REFUTED-the-revival /
the negative STANDS. The decisive result above: Psi enters only as (Psi')^2 with
zero source on BOTH S^2 and S^3; back-reaction reweights but never sources a twist.
- Seal stress test (`verif_berry_seal.py`, `verif_numeric.py`): even if one FORCES
  a Dirichlet twist Psi(seal)-Psi(core)=Delta at the seal, the EOM gives
  W(r)Psi'=C with W = r^2 e^{-phi} sin^2(Theta), so Psi'=C/W and the swept phase
  gamma(D) is SMOOTH in D and PROPORTIONAL to the forced Delta — it has NO isolated
  2pi-n roots in D, so it does not quantize D. And W->0 at the seal (sin^2Theta->0)
  while the Berry connection (1-cosTheta)->0 there, so the seal carries no twist
  weight. The mirror-fold IDENTIFIES the cell with its image (a parity action on
  the azimuth); it does not SOURCE a gradient — the minimal-energy single-valued
  representative is Psi=const, zero swept solid angle. NO REVIVAL.

**Claim 4 — S^2 carrier structurally cannot carry a depth phase; needs S^3.**
CONFIRMED, with a sharpened reason. An S^2 baby-Skyrme charge-1 hedgehog has one
radial polar profile Theta(r) + a rigid SO(3) orientation, with an exact SO(2)
(U(1)) about the easy axis. Any internal-azimuth twist is that cyclic U(1)
coordinate, entering the action purely as (Psi')^2 with no source — hence pinned to
const, hence zero depth-phase. SHARPENING: this same U(1)-cyclic obstruction kills a
*sigma-model* iso-twist on S^3 too; reviving a genuine depth-monodromy needs the
S^3 *topological* (Hopf/pi_3 WZW) term, not merely the larger target. So "needs
S^3" is correct but specifically means "needs the S^3 WZW/Hopf term," not an S^3
sigma profile. The structural reason is SOUND (and stronger than stated).

**Claim 5 — Bohr-Sommerfeld quantizes SPIN, not DEPTH.** CONFIRMED. J=hbar(n+nu)
fixes the iso-rotor angular momentum; E_n(D)=E0(D)+hbar^2(n+nu)^2/(2 Lambda_3(D))
is a rotational SPIN tower on a cell of ARBITRARY depth D. It rides hbar (flagged
in the doc) and selects spin, not depth. To get a depth ladder one must IMPORT a
J<->D link — a non-native patch, correctly identified by the doc as forbidden.

Auxiliary: Lambda_3(D) is smooth/monotone in depth (`verif_numeric.py`), no
isolated structure that could hide an accidental depth selection. It is a
stiffness/inertia, not an accumulated phase, so its single-valuedness cannot bite.
(My absolute Lambda_3 values differ from the doc's because I used a stand-in
monotone profile, not the settled BVP — irrelevant: the verdict rides only on
smoothness + the Psi-structure, both robust.)

---

## NON-BLOCKING NOTES (honest)

- The literal ansatz formula printed in the source docs
  (`n=(sinTheta sin th cos ph, ...)`) is not unit-norm as written; it is shorthand.
  The settled object is the easy-axis unit-3-vector hedgehog (n3=cosTheta(r) the
  easy axis, exact SO(2) about target-3) — the relevant invariants
  (one polar profile + rigid orientation + cyclic azimuth) are unchanged, and the
  verdict does not depend on the coefficient conventions I could not reproduce
  exactly. The L4 angular integral here carries the known global-monopole
  azimuthal tail (the Lambda_perp cell-divergence of n3_direction); it does not
  affect the Psi-structure, which is what decides the monodromy.
- I did not re-solve the settled BVP; I used the BC-fixed structural facts
  (degree=1, dTheta=pi) and the symbolic action structure, which is where the
  load-bearing kill lives.

---

## OVERALL VERDICT: **STANDS (NO-MONODROMY).**

Berry phase zero & winding depth-fixed? **YES** (both BC/topology-fixed; gamma=0 on
the forced meridian). chi cyclic => no D condition? **YES** (Delta chi=2pi closes
for every D). Does back-reaction/seal revive a depth-phase via S^3/psi(r)?
**NO** — the decisive symbolic result is that the internal twist Psi enters the
action ONLY as (Psi')^2 with ZERO source, on BOTH S^2 and S^3, so neither the
sourced phi nor the mirror seal can induce a depth-dependent swept solid angle; the
active rescue FAILS. Is the S^2-needs-S^3 reason sound? **YES, and sharper** — the
obstruction is the U(1)-cyclic nature of the iso-twist (kills sigma-twists on both
targets); a genuine revival needs the S^3 *Hopf/WZW topological* term, not a sigma
profile.

The NO-MONODROMY negative SURVIVES the active S^3/psi(r) + seal rescue. The
single-cell L2+L4 angular collective coordinate does NOT discretize the cell depth;
the depth continuum (#39/#43) is NOT lifted, and #48 (no evenly-spaced geometric
ladder) is corroborated (no ladder selected at all). Result: **CONFIRMED — STANDS.**

SCOPE / premise set (for NEGATIVES_REGISTRY): single-cell; settled L2+L4 S^2
baby-Skyrme charge-1 easy-axis hedgehog (+ the S^3/SU(2) sigma escape hatch tested
and closed); depth family phi=-p ln(r_int/r); static back-reacted cell with
same-minus mirror seal; classical (hbar-free) single-valuedness primary,
Bohr-Sommerfeld flagged. CONDITIONS-CHANGED trigger: if a native S^3 *Hopf/WZW
topological* term (pi_3) is introduced, or an inter-cell phase links chi across
cells, the existence question REOPENS.

---

## DATA-BLIND CONFIRMATION

No lepton/hadron wall numbers, no Koide ratio, no sqrt(2), no 45-degree condition,
no lepton number was loaded, matched, or consulted in any verifier script or in
this document. The verification was METRIC-LED (does the settled collective-
coordinate reduction + an actively-tried internal twist produce a depth-dependent
monodromy?), tested the rescue hardest, and reports the negative as it survived.
