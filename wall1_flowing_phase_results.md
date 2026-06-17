# Wall 1 (pilot-wave): Does the UDT matter object carry a genuine FLOWING phase (a native de Broglie wave tied to MOMENTUM)? — Results

Date: 2026-06-17. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit, Self-Hardening discipline). Mode: **OBSERVE** (metric-led;
the cheapest/most-decisive Wall in `quantization_check1_guiding_MAP.md`, item
(i)). LOCAL branch `session-2026-06-17`. Conjecture-grade ponder support; NOT
canon, NOT yet blind-verified (attack-here block at end). **DATA-BLIND**: no
masses, ratios, hbar value, or wall numbers loaded, computed toward, or
compared.

THE QUESTION (metric-led, from the MAP): the native matter object is the static,
spherically-symmetric global-monopole TEXTURE — the real unit 3-vector hedgehog
n(x) (target S^2), degree-1 winding (N=3, q=1/3), plus an internal collective
ISO-ROTATION phase chi. When the object MOVES through the actual UDT metric
(g_tt = -e^{-2phi}, g_rr = +e^{2phi}, c_eff = e^{-2phi}), does its internal clock
manifest as a SPATIAL phase gradient — a native de Broglie wave tied to MOMENTUM
— or is the only phase a real STANDING oscillation / a SPIN-tied clock that
cannot play the de Broglie role?

DISCIPLINE: OBSERVE, not target. The de Broglie relation is NOT assumed; I feed
each candidate native clock through the EXACT metric machinery and report what
comes out, including absences. The single decision is WHICH native frequency (if
any) the internal clock has, because the metric machinery (Part B) is the same
regardless and turns out to close exactly.

Scripts (this push; exact symbolic / no fitting):
- `/tmp/wall1_phase.py` — sympy: proper time, 4-velocity normalization, the HJ /
  eikonal mass-shell test in the exact UDT metric.
- `/tmp/wall1_db.py` — sympy: local-frame (orthonormal) momentum/energy, the
  emergent dispersion, the depth-grading of the wavevector, the eikonal-of-the-
  medium-wave comparison.
- `/tmp/wall1_clocks.py` — enumeration of the native clocks and the rest-energy
  crux.
(These are scratch scripts in /tmp; the load-bearing content — every equation —
is reproduced verbatim below for the record.)

---

## PART A — THE NATIVE CLOCKS OF THE m=1 TEXTURE (enumerated)

The settled carrier (native_stabilizer / monodromy_depth #49 / crux1) is the
charge-1 easy-axis baby-Skyrme hedgehog of a REAL unit 3-vector n (target S^2):
ONE radial profile Theta(r) (Theta(core)=pi -> Theta(seal)=0) plus a RIGID
internal SO(3) orientation R. There is NO second internal profile psi(r) (that
needs an S^3/SU(2) target — verifier-confirmed absent, monodromy_depth
2026-06-15). Every native internal periodicity is therefore one of the following:

### CLOCK 1 — the iso-rotor chi (the collective-coordinate clock) [DERIVED]
The collective-coordinate reduction (monodromy_depth #49, sympy-exact):
  L_eff(chi, chidot; D) = (1/2) Lambda_3(D) chidot^2 - E0(D),
  p_chi = Lambda_3(D) chidot = J (conserved, since chi is cyclic),
  chi(t) = omega_ang t + chi_0,   **omega_ang = J / Lambda_3(D).**
- It REQUIRES J != 0. A non-spinning texture (J=0) has omega_ang = 0 — NO chi
  clock at all.
- Its frequency is tied to SPIN J (a FREE classical initial datum — monodromy_depth
  Task 2/3), NOT to the rest mass/energy E0.
- Lambda_3(D) is depth-dependent (8.81 -> 134.11 as p: 0 -> 2), so omega_ang
  drifts with depth at fixed J, but J itself is unconstrained.

### CLOCK 2 — the breathing / fluctuation tower [DERIVED]
Small oscillations of Theta(r) about the ground soliton: a Sturm-Liouville
Hessian H u = omega^2 W u (lepton_soliton #44; whole_metric_full_solve §5.1).
  flat cell: omega = [0.445, 0.744, 1.019, 1.299, ...] (omega^2 = [0.198, 0.554,
  1.039, ...]); whole-metric lowest omega_1 ~ 0.310, and crucially **DEPTH-FLAT**
  (0.30995..0.31021 over a 5x change in the depth dial).
- These are REAL STANDING oscillations (radial nodes) — EXCITATION gaps above the
  ground state, requiring energy ABOVE E0 to be present. The ground soliton itself
  does NOT breathe (it is the static energy minimum). So these are gaps, not a
  carrier rest-frequency.

### CLOCK 0 (THE CRUX) — a REST-ENERGY / Compton clock omega_0 ~ E_rest/hbar? **ABSENT.**
The static charge-1 hedgehog is the EOM solution with d/dt(everything) = 0: the
profile Theta(r), the field n, and the metric are all static. The energy E0(D) is
the depth of the energy well (the soliton mass), a NUMBER — not the frequency of
any oscillating field component. There is no field that oscillates at E0/hbar.
This is the textbook fact that **a static real soliton classically does NOT
oscillate at its rest energy** — and it is independently confirmed by the
whole-metric solve: the ground state carries ZERO breathing excitation, and the
omega^2 > 0 are GAPS to excited states, not a self-oscillation of the carrier.

> **PART A read-out (the load-bearing observation):** UDT's static m=1 texture has
> NO native rest-energy (Compton) clock. Its only genuine internal clock is the
> iso-rotor chi at omega_ang = J/Lambda_3, set by SPIN J (free), not by mass. The
> breathing tower is a set of standing excitation gaps (depth-flat), not a carrier
> frequency. The de Broglie/pilot-wave construction needs a clock at E_rest/hbar
> (Compton); the metric does not provide one.

---

## PART B — THE PHASE UNDER MOTION (exact, in the actual UDT metric)

This part is METRIC-CLEAN and does NOT depend on which clock we use: the result
is the same functional form with whatever omega_clock the texture actually has.
Metric (Lorentzian, as given): g_tt = -e^{-2phi(r)}, g_rr = +e^{2phi(r)}; the
coordinate light speed dr/dt|_null = e^{-2phi} = f = c_eff (the refractive index).

### B1 — proper time along a moving worldline
For radial coordinate velocity v_r = dr/dt,
  **dtau/dt = sqrt( e^{-2phi} - e^{2phi} v_r^2 ).**
The internal-clock phase the object accumulates is S = omega_clock * tau.

### B2 — the phase field and the Hamilton-Jacobi / eikonal mass-shell — CLOSES EXACTLY
Take d_mu S = omega_clock * u_mu (the clock phase advances with proper time;
u_mu = the covariant 4-velocity). The exact 4-velocity (normalized
g_mu nu u^mu u^nu = -1, verified) has covariant components
  u_t = -e^{-2phi} / sqrt( (1 - v_r^2 e^{4phi}) e^{-2phi} ),
  u_r =  v_r e^{2phi} / sqrt( (1 - v_r^2 e^{4phi}) e^{-2phi} ).
Then the relativistic Hamilton-Jacobi / eikonal equation closes IDENTICALLY:
  **g^{mu nu} (d_mu S)(d_nu S) = -omega_clock^2     (sympy-exact).**
So S(t,x) = omega_clock * tau IS a bona fide eikonal/HJ phase field on the mass
shell, with omega_clock playing the role of the rest frequency. The phase field
exists and satisfies the right equation in the real UDT geometry.

### B3 — the de Broglie spatial gradient, and how c_eff = e^{-2phi} enters
- COORDINATE energy and wavevector:
  E_coord = -d_t S = omega_clock e^{-2phi} / sqrt((1 - v_r^2 e^{4phi}) e^{-2phi}),
  k_r = d_r S = omega_clock v_r e^{2phi} / sqrt((1 - v_r^2 e^{4phi}) e^{-2phi}).
- LOCALLY MEASURED (orthonormal-frame, what a static depth-D observer reads),
  p_hat = k_r / sqrt(g_rr) = k_r e^{-phi}, E_hat = (-d_t S)/sqrt(-g_tt) = E_coord e^{phi}:
  **p_hat = omega_clock v_r e^{2phi} / sqrt(1 - v_r^2 e^{4phi}),**
  **E_hat = omega_clock / sqrt(1 - v_r^2 e^{4phi}),**
  with the clean local dispersion
  **E_hat^2 - p_hat^2 = omega_clock^2     (sympy-exact),  i.e. E_hat^2 = p_hat^2 + omega_clock^2.**
  The local velocity is beta_local = p_hat / E_hat = v_r e^{2phi} = v_r / c_eff
  (the coordinate velocity expressed in units of the LOCAL light speed c_eff =
  e^{-2phi}) — exactly the gamma-factor argument 1 - v_r^2 e^{4phi} = 1 -
  beta_local^2. So locally it is a standard special-relativistic de Broglie
  relation with rest frequency omega_clock.
- THE GRADED-INDEX FACT (how c_eff enters): the COORDINATE wavevector is depth-
  graded, k_r = p_hat e^{phi} = p_hat / sqrt(c_eff). The coordinate de Broglie
  wavelength 2pi/k_r therefore STRETCHES/COMPRESSES with depth (the proper
  wavelength 2pi/p_hat refracts through the variable-index medium). So IF a flowing
  phase existed, it WOULD be a genuine graded-index de Broglie wave, refracted by
  c_eff exactly as the medium picture wants. The metric does this part for free.

### B4 — relation to the LATER-4 medium wave (-psi'' + V psi = omega^2 psi)
The medium wave (STATE_DERIVATION LATER-4): in the optical/tortoise coord
dr* = dr/f (f = e^{-2phi}), psi = u sqrt(P), the W2 c_eff wave reduces to Liouville
form -psi'' + V psi = omega^2 psi, V = -2 phi' f^2 / r. Its WKB/eikonal limit is
(dS_r/dr*)^2 = omega^2 - V(r*) at FIXED omega — i.e. the SPATIAL turning-point
structure of a STANDING radial mode (a confined ripple), NOT a translating
de Broglie phase. The HJ phase S = omega_clock tau of Part B is the FULL spacetime
eikonal whose t-component supplies the omega; the medium-wave eikonal is its
spatial restriction at fixed frequency. They are consistent (the HJ phase IS the
eikonal limit of the medium wave), but note the medium wave as written is 2nd-order
and supports STANDING ripples (this is exactly Wall 2's "real ripple, not a
1st-order flow"); a flowing phase has to come from the CLOCK part S = omega_clock
tau, i.e. from Part A's omega_clock being a real carrier frequency.

> **PART B read-out:** the metric machinery is FLAWLESS. Given ANY internal carrier
> frequency omega_clock, motion through the UDT metric produces an exact HJ/eikonal
> phase field obeying g^{mu nu} d_mu S d_nu S = -omega_clock^2, a local de Broglie
> relation E_hat^2 = p_hat^2 + omega_clock^2, p_hat = omega_clock beta_local /
> sqrt(1 - beta_local^2), and a depth-graded (c_eff-refracted) coordinate wavevector
> k_r = p_hat e^{phi}. The de Broglie structure is NATIVE TO THE GEOMETRY. The ONLY
> missing ingredient is a carrier omega_clock equal to E_rest/hbar — which Part A
> shows the texture does not have.

---

## PART C — HONEST VERDICT

The result is a clean SPLIT, and it is branch **(c) with a (a)-shaped near-miss** —
which is the most informative possible outcome and exactly what the MAP's BREAK A
anticipated:

**The de Broglie MACHINERY exists and is native (branch-a geometry).** Part B is
exact and unforced: the UDT metric turns ANY internal clock under motion into a
genuine spacetime eikonal phase whose spatial gradient is a momentum and whose
coordinate wavelength is refracted by c_eff (a graded-index de Broglie wave). The
relativistic HJ equation closes to -omega_clock^2 identically; the local dispersion
is the textbook E^2 = p^2 + omega_clock^2. There is NO obstruction in the geometry.

**BUT the carrier clock is SPIN-tied, not MASS-tied — Wall 1 FAILS as stated
(branch c).** The only genuine native internal clock is the iso-rotor chi at
omega_ang = J/Lambda_3(D), set by the SPIN J (a free classical datum), and there
is NO rest-energy/Compton clock omega_0 ~ E_rest/hbar (Part A). Feeding the only
available clock into the (exact) Part-B machinery gives a "de Broglie wave" whose
wavelength is set by SPIN, not by mass/momentum-via-mass — a FALSIFIABLE MISMATCH:
- a SPINLESS texture (J=0) would have omega_clock = 0 and hence NO phase / NO
  de Broglie wave, even while carrying mass and momentum — but real spin-0 objects
  DO have de Broglie waves;
- two equal-mass, equal-momentum objects of different spin J would carry DIFFERENT
  de Broglie wavelengths — but the de Broglie wavelength depends on momentum only.
So the texture as it stands does NOT carry the momentum-tied flowing phase the
pilot-wave reading needs. The chi-clock is a flowing phase (chi = omega_ang t + chi0
flows in one direction, cyclic, no nodes — unlike the standing breathing modes), so
"flowing vs standing" is NOT the failure point; the failure is that the flow rate is
governed by SPIN, not by REST ENERGY. The breathing tower IS the standing-oscillation
alternative, and it is depth-flat and gapped — also not a carrier.

WHAT WOULD CHANGE THE VERDICT (scoped, for the registry): the verdict is branch-c
ONLY because the classical static soliton has no rest-energy oscillation and the
only collective clock is J-tied. It would FLIP to branch-a if EITHER (1) a native
relation pins omega_clock = E0/hbar (a "the carrier frequency IS the rest energy"
identity — this is precisely the hbar/Compton-clock question PARKED as INPUT in the
MAP premise ledger item 6; if hbar enters and E_rest/hbar becomes the carrier
frequency, Part B delivers the full native de Broglie wave immediately), OR (2) the
quantum completion supplies a phase e^{-i E t/hbar} on the soliton (the standard QM
carrier), in which case the metric's exact Part-B machinery again does the rest.
Both are QUANTUM-layer inputs, not classical metric outputs — so CLASSICALLY,
metric-led, the flowing momentum-phase is ABSENT, and that absence is the result.

> ONE-LINE VERDICT: The UDT metric provides the COMPLETE de Broglie geometry for
> free (exact eikonal, momentum-gradient, c_eff-refraction), but the static texture
> provides NO mass/rest-energy carrier clock to ride it — its only clock is
> spin-tied (omega_ang = J/Lambda_3). So Wall 1 FAILS classically: there is a
> flowing phase, but it flows at the SPIN rate, not the de Broglie (rest-energy)
> rate. The flowing momentum-phase appears only if a native or quantum relation
> pins the carrier frequency to E_rest (the parked hbar/Compton question).

---

## PREMISE LEDGER (every value / BC / sign / choice tagged)

| # | Premise | chose / derived | note |
|---|---------|-----------------|------|
| D1 | Metric g_tt=-e^{-2phi}, g_rr=+e^{2phi}; c_eff=e^{-2phi} | DERIVED (given UDT metric; CANON R-areal) | the input geometry |
| D2 | Carrier = real unit 3-vector n, target S^2; ONE radial profile Theta(r) + rigid SO(3) orientation; no internal psi(r) | DERIVED | native_stabilizer / crux1 / monodromy_depth (verifier-confirmed S^3 twist absent) |
| D3 | Iso-rotor clock: L_eff=(1/2)Lambda_3 chidot^2 - E0; omega_ang=J/Lambda_3; chi cyclic, J conserved | DERIVED | monodromy_depth #49, sympy-exact |
| D4 | J (spin) is a FREE classical datum; omega_ang therefore unconstrained | DERIVED | monodromy_depth Task 2/3 |
| D5 | Breathing tower omega_n (standing, gapped, depth-flat omega_1~0.31) | DERIVED | lepton_soliton #44, whole_metric §5.1 |
| D6 | Static soliton has NO rest-energy field oscillation (E0 is a well depth, not a frequency) | DERIVED | EOM is static; whole_metric ground state has zero breathing excitation |
| D7 | dtau/dt = sqrt(e^{-2phi}-e^{2phi}v_r^2); u_mu normalized to -1 | DERIVED | sympy-exact, this push |
| D8 | g^{mu nu} d_mu S d_nu S = -omega_clock^2 for S=omega_clock tau, d_mu S=omega_clock u_mu | DERIVED | sympy-exact, this push (eikonal closes) |
| D9 | Local dispersion E_hat^2 = p_hat^2 + omega_clock^2; beta_local = v_r e^{2phi} = v_r/c_eff | DERIVED | sympy-exact, orthonormal frame |
| D10 | Coordinate wavevector k_r = p_hat e^{phi} (depth-graded de Broglie wavelength) | DERIVED | sympy-exact; c_eff refraction |
| D11 | Medium-wave -psi''+V psi=omega^2 psi, V=-2 phi' f^2/r; its WKB eikonal = spatial restriction of S at fixed omega | DERIVED | STATE_DERIVATION LATER-4 (already verifier-cleared); consistency shown here |
| C1 | Radial worldline (motion along r) as the representative translation | CHOSE | the depth direction is the only inhomogeneous direction; angular motion would add frame-drag terms (not examined; flagged) |
| C2 | "Internal-clock phase advances with proper time," S = omega_clock tau, d_mu S = omega_clock u_mu | CHOSE (the natural pilot-wave ansatz being TESTED) | this is the de Broglie hypothesis itself; Part B tests whether it closes (it does) — the test is which omega_clock exists |
| C3 | Identify omega_clock with a NATIVE clock (chi or breathing), NOT with E0/hbar | DERIVED-by-absence | there is no native E0/hbar clock (D6); this IS the verdict |
| C4 | hbar and a Compton relation omega_0=E_rest/hbar | NOT INVOKED (parked as INPUT, MAP ledger item 6) | the single thing whose presence would flip c->a |
| C5 | Depth family / Lambda_3(D) numbers (8.81->134.11) | DERIVED (monodromy_depth) on the chosen log cell phi=-p ln(r_int/r) | scaffolding; not load-bearing for the verdict |

---

## THE SINGLE MOST LOAD-BEARING PREMISE (flag for the blind verifier)

**D6 / C3 — that the static UDT texture has NO native rest-energy (Compton) clock,
so the only carrier frequency available is the SPIN-tied omega_ang = J/Lambda_3.**
The entire verdict (branch c, not a) rests on this. If a verifier finds ANY native,
classical, hbar-free field oscillation of the m=1 ground texture at a frequency tied
to E0 (the rest mass) — not to spin J, and not merely a gapped breathing excitation
that must be externally populated — then omega_clock = E0/hbar-type carrier exists,
Part B's exact machinery delivers a true mass-tied de Broglie wave, and Wall 1 FLIPS
to branch (a). I claim no such clock exists for a static real soliton, but this is
the rung to attack hardest. (Secondary attack: C2 — confirm that S = omega_clock tau
with d_mu S = omega_clock u_mu is the only natural phase ansatz and that the exact
eikonal closure g^{mu nu}d_mu S d_nu S = -omega_clock^2 is not an artifact of the
radial-worldline choice C1; check an angular/boosted worldline.)

---

## CONFIDENCE

- PART B machinery (eikonal closes; local de Broglie dispersion; c_eff grading):
  HIGH (~0.95). Exact sympy, frame-checked, and it is just GR HJ theory transcribed
  to the UDT metric — robust.
- PART A enumeration (the only native clocks are chi (spin) and breathing
  (gapped/standing); no rest-energy clock): HIGH (~0.9), resting on the
  already-verifier-cleared monodromy_depth and whole_metric results.
- PART C verdict (Wall 1 fails classically because the carrier is spin-tied, not
  mass-tied; flips only with the parked hbar/Compton input): MEDIUM-HIGH (~0.8).
  The structural claim is solid; the residual uncertainty is exactly D6/C3 (could a
  rest-energy clock hide in the quantum completion or in a clock I have not
  enumerated?), which is why it is flagged for the verifier.

---

## DATA-BLIND CONFIRMATION

No lepton/hadron masses, ratios, Koide, sqrt(2), hbar value, or wall numbers were
loaded, recalled, computed toward, or compared. The push was METRIC-LED (move the
m=1 texture through the actual UDT metric and OBSERVE whether its internal clock
yields a momentum-tied spatial phase), tested the de Broglie ansatz rather than
assuming it, and reports the absence (no rest-energy carrier clock) as a
first-class result. hbar and the Compton relation were deliberately NOT invoked
(parked as INPUT per the MAP), and their absence is precisely what makes the
classical verdict branch-c.

---

## BLIND VERIFIER — PENDING. ATTACK HERE:
1. **D6/C3 (load-bearing): is there genuinely NO native rest-energy clock?** Hunt
   for any classical, hbar-free field oscillation of the m=1 ground texture tied to
   E0 (mass), not to spin J. The breathing modes are gapped standing excitations
   (must be populated) — confirm they cannot serve as a carrier. If a mass-tied
   self-oscillation exists, Wall 1 flips to branch (a).
2. **C2/C1 (eikonal robustness): re-derive g^{mu nu} d_mu S d_nu S = -omega_clock^2**
   for S=omega_clock tau independently, and check it on a NON-radial / boosted
   worldline (angular motion, off-axis) — confirm the closure is not special to the
   radial choice and that no frame-drag term spoils d_mu S = omega_clock u_mu.
3. **The local dispersion E_hat^2 = p_hat^2 + omega_clock^2 and beta_local = v_r/c_eff.**
   Re-derive in the orthonormal frame independently; confirm the coordinate
   wavevector grading k_r = p_hat e^{phi} (the graded-index de Broglie wavelength).
4. **Whole-before-slice.** This tested the FLOWING-PHASE existence specifically.
   Confirm the negative is scoped to "no mass-tied carrier classically" and does NOT
   over-claim against the pilot-wave program once hbar/the Compton relation is
   admitted (the parked INPUT) — at which point Part B's exact machinery would
   deliver the de Broglie wave. The verdict is conditional on C4 staying parked.

---

## BLIND VERIFIER VERDICT — 2026-06-17 (agent: blind-adversarial-verifier, Opus 4.8 1M)

Independent re-derivation (own sympy 1.14.0, `/tmp/verify_partB*.py`,
`verify_tautology.py`) + adversarial recon across monodromy_depth,
lepton_soliton_spectrum, whole_metric_full_solve, STATE_DERIVATION LATER-4/5.
NOT confirmation-seeking; I tried to FIND a rest-energy clock and to break the
eikonal closure. Per-task verdicts:

**(A) Part B re-derivation — SURVIVES (exact).** Reproduced independently:
dtau/dt = sqrt(e^{-2phi} - e^{2phi} v_r^2); u_mu normalized to g_mn u^m u^n = -1
(sympy `-1`); `g^{mu nu} d_mu S d_nu S = -omega_clock^2` closes IDENTICALLY;
E_hat^2 - p_hat^2 = omega_clock^2; beta_local = v_r e^{2phi} = v_r/c_eff;
k_r/p_hat = e^{phi}. All four "value identities" reproduce exactly (the two raw
`False` prints were only sympy failing to fold sqrt(e^{2phi})->e^{phi}; forced
powsimp confirms equality). Algebra is RIGHT.

**(B) Substantive-or-tautological — PARTIAL (mostly near-trivial).** I re-ran the
closure on (i) a FULLY general worldline (radial + both angular velocities) in the
metric with general areal R(r) — closes to -omega^2; and (ii) a GENERIC metric with
ARBITRARY g_tt=-A(r), g_rr=B(r) — also closes to -omega^2. So `g^{mu nu} d_mu S
d_nu S = -omega^2` is mathematically EQUIVALENT to u.u=-1 and is METRIC-INDEPENDENT:
it is "any relativistic point clock has a proper-time HJ phase," true for every
spacetime, NOT special to UDT. This also disposes of the secondary attack (C1/C2):
no frame-drag term spoils it, closure is not a radial-choice artifact. The ONLY
genuinely UDT-native content in Part B is the specific graded-index factor
c_eff=e^{-2phi}: the e^{phi} in k_r=p_hat e^{phi} and beta_local=v_r/c_eff. The doc
is honest about this ("it is just GR HJ theory transcribed," confidence note), so
no overclaim — but a reader should not mistake the "exact closure" for UDT-specific
physics. Substantive part = the c_eff refraction only; the rest is generic.

**(C) Crux premise "no native rest-energy clock" — SURVIVES.** Refute-first hunt
failed to find one. (i) LATER-4 medium wave -psi''+Vpsi=omega^2 psi, V=-2 phi' f^2/r:
well is real but DOES NOT TRAP under the regular core BC — lowest mode is pure
BOX-CONTROL (omega_0^2 ~ pi^2/R_wall^2 at every depth, even phi0=-5; LATER-5 verifier
deepened the well 17 orders of magnitude, E0.R^2 stuck at pi^2). Box-set, not
mass-set; no bound rest mode. (ii) No full non-static solution carries an intrinsic
rest oscillation; the round static soliton is the unique static charge-1 solution;
off-diagonal sector linearly decouples. (iii) Breathing ground carries ZERO
excitation — every breathing spectrum has strictly positive lowest omega^2 (0.198
flat / 0.096 whole-metric), i.e. NO zero-mode and no self-oscillation; the omega_n
are gaps that must be populated, and omega_1~0.31 is depth-FLAT so not mass-tied.
(iv) A moving/excited texture only acquires the Part-B phase from whatever omega_clock
it already has — motion manufactures no new rest frequency. (v) Seal is a Z2 t->-t
reflection (interval, not a time-circle): no classical periodicity is forced, so no
classical rest beat. After honest effort I find NO native, classical, hbar-free
rest-energy clock. The absence STANDS.

**(D) Spin-mass mismatch — SURVIVES.** J is a FREE classical datum (monodromy_depth
L116/134; Delta chi=2pi n imposes no condition on omega; quantizing J needs hbar and
even then fixes SPIN not mass). E0(D)/mass is continuous and independent of J. So the
chi-clock omega_ang=J/Lambda_3 is genuinely decoupled from mass: J=0 => zero phase on
a massive object, and equal-mass/equal-momentum/different-J objects => different
wavelengths. No native relation ties J to E0 for the ground state. The mismatch is a
real falsifiable wrong prediction, exactly as claimed.

**(E) Premise audit — SURVIVES (honest, nothing smuggled).** "Fails classically,
flips to pass the instant omega_clock=E_rest/hbar is pinned" is accurate: the flip
literally requires injecting hbar (a Compton relation E_rest=hbar omega_0) or a QM
carrier e^{-iEt/hbar} — both QUANTUM-layer inputs absent from the classical metric.
C4 (hbar) is correctly tagged NOT-INVOKED/parked. No hidden assumption inflates the
classical result; the negative is properly scoped to "no mass-tied carrier
classically" and does not over-claim against the pilot-wave program once hbar is
admitted (Part B then delivers the wave).

OVERALL: Part-C verdict (Wall 1 fails classically; spin-tied not mass-tied carrier;
flips only with the parked hbar/Compton input) is CORRECT. Confidence the verdict is
right: **0.88.**

SINGLE BIGGEST WEAKNESS: not an error but a framing risk — Part B's "exact eikonal
closure" is metric-independent kinematics (I proved it for an arbitrary metric), so
its rhetorical weight ("the de Broglie machinery is NATIVE and exact") overstates;
the only native ingredient is the c_eff=e^{-2phi} graded index. This does not change
the verdict but should temper any claim that UDT "provides the de Broglie geometry"
beyond the refraction factor. Residual on (C): the hunt is bounded by the enumerated/
already-solved sectors; a rest clock hiding in an un-enumerated nonstationary weld or
the quantum completion cannot be excluded by classical search (the doc flags this).

FLIP CHECK: NO task flips the conclusion. (A) confirms the algebra, (C)/(D)/(E)
confirm the crux. The result's verdict stands as written.
