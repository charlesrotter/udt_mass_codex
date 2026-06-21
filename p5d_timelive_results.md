# P5d — The Time-Live Observation (the payoff of the everything-on solver build)

**Mode:** OBSERVE (let structure emerge, report WHAT IS THERE). NOT a target hunt.
**Agent:** claude-opus-4-8[1m]. **Date:** 2026-06-20. **Status:** NOT canon. Append-only.
**Branch:** `p5d-timelive`. **DATA-BLIND** (units L=1; only residuals, omega-scalings,
code-unit M_MS — nothing M_MS/spectrum/ratio is BANKED).
**Script (NEW, committed with this doc):** `p5d_timelive.py`.
**Discipline:** OPEN time only (no closed-time import). a(phi)=-1 GR baseline (P3 ruler
weight k=0 -> W==1). Native S^2 carrier (P2). B=1/A FREE. Observe-not-target (NO tower/
catalog hunt; #65 retired, NOT re-litigated).

---

## 0. WHAT P5d IS (and is not)

P5d is the OBSERVATION the everything-on solver build (P1 general Einstein hybrid + P2
native S^2 matter + P3 a(phi) ruler + P4 live time row) was built to enable: **with time
LIVE on the round ground-state object, what does the full clean metric DO?**

It is NOT a tower/catalog hunt. #65 already SETTLED that one classical carrier does not
tower (reduced-proxy, box-controlled). P5d does not re-litigate that. The genuinely new
question vs #65: #65 was a REDUCED PROXY (modeled radial profile, single-mode SL eigen-
problem, full coupled solve not built). P5d uses the FULL CLEAN stack (general 4x4
Einstein pole-stable hybrid + native S^2 EL coupled to the full metric + a(phi) ruler +
the P4-validated live time row) and asks whether the full coupling shows the SAME structure
the proxy did, or something the proxy MISSED.

**HONEST EXPECTATION stated up front (anti-false-convergence):** the classical time-live
solve most likely gives a CONTINUUM (no discrete oscillator), per postulate A (discreteness
is a SEPARATE downstream quantization step). A continuum is a REAL OBSERVATION, not a
failure. P5d reports what is there.

---

## 1. WHAT I BUILT / RAN

**The observation, made native and in-budget.** The P4 live residual's TIME rows (the cos^1
harmonic-balance rows — the linearized Einstein G^t_t / G^r_r / matter-EL operator acting on
the live amplitudes x=(a1,b1,F1), PLUS the G^t_r momentum row the live time sources) are,
for a FROZEN static background, EXACTLY a quadratic-in-omega operator:

```
   R_time(x; omega) = [ K  +  omega C  -  omega^2 M ] x
     K = the omega^0 (static spatial restoring / curvature) operator
     C = the omega^1 content  (the G^t_r momentum / open-time d_t channel)
     M = the omega^2 content  (the d_t^2 -> -omega^2 INERTIA)
```

This is the harmonic-balance content of P4's `einstein_live` + `field_dn_s2_live`, with the
P4 CONTAINMENT PINS on the live amplitudes RELEASED (P4 pinned a1=b1=F1=0 to make
containment a bitwise check; P5d releases them to see the DYNAMICS) and the regular
charge-1 fluctuation BCs kept (a1(seal)=0, b1(core)=0, F1(core)=F1(seal)=0).

`p5d_timelive.py`:
- `static_background_cell(NR,cell)` — solves the round S^2 ground state at an arbitrary
  cell (the round-channel representative of the saved p5c round ground state; 3*Nr radial
  unknowns, ~5 s).
- `time_rows(x; bg, omega)` — the live-amplitude (cos^1) residual rows, NO containment pins.
- `assemble_KCM(...)` — builds K, C, M by exact central-FD of `time_rows` in each amplitude
  direction at omega in {0, +w1, -w1}, separating the omega-powers exactly
  (K=J(0); C=(J(+)-J(-))/(2w1); M=-(J(+)+J(-)-2J(0))/(2w1^2)).
- `qep_scan(...)` — scans real omega; sigma_min of (K + omega C - omega^2 M); minima/zeros
  are the live eigenfrequencies.
- `run_boxscan` — sigma_min global-min omega vs cell R (the box-control gate).

**How far it floored:** EVERYTHING ran cleanly IN BUDGET. Static background floors to
Phi ~ 1e-20 in ~5 s. K,C,M assembly ~9 s. Each `qep NR cell` invocation ~14-18 s (well
under the 6-min cap). NO hang, NO background poll, SINGLE clean sequential process per call.
Runs: containment (Nr=12); QEP at (Nr=12, cell=10,14,18) and (Nr=16, cell=14); box-scan.

---

## 2. THE OBSERVATION (the time-live dynamics found)

### (a) CONTAINMENT — PASS (sanity, inherited from P4)
```
Nr=12 cell=14:  ||time-rows(x=0, omega=0)|| = 3.16e-10   (-> 0)
```
The static round ground state IS the omega=0 fixed point of the live residual: at omega=0
the live amplitudes carry no force and the static soliton is recovered. (Re-confirms P4b in
the released-amplitude form.)

### (b) THE OPERATOR STRUCTURE — the headline observation
Assembled K, C, M on the round ground state (Nr=12, cell=14):
```
   ||K|| = 4.48e+00     (the static restoring / curvature operator)
   ||C|| = 6.13e-01     (the omega^1 G^t_r momentum channel;  ||C||/||K|| = 0.137)
   ||M|| = 2.24e-09     (the omega^2 INERTIA;  ||M||/||K|| = 5.0e-10  ==  MACHINE FLOOR)
```

**THE INERTIA OPERATOR IS ZERO.** The omega^2 / d_t^2 content cancels identically for the
round diagonal metric. With no inertia (no mass term), the system is NOT an oscillator:
`R_time = K x + omega C x` is LINEAR in omega, dominated by the first-order G^t_r momentum
channel. There is **no eigenfrequency, no resonance, no restoring oscillation, no tower**.

This is verified to be a genuine PHYSICS cancellation, not a dropped term:
```
max|dtt_g|(omega=1) = 1.08e-01   (NONZERO: the d_t^2 inertia content IS computed and wired)
max|dt_g| (omega=1) = 1.22e-01
```
The d_t^2 content is genuinely present in the metric partials and reaches the kernel's
dGamma[T] -> Riemann (P4 measured the live-Christoffel shift 0.062). It then CANCELS in the
diagonal G^t_t for the round metric — exactly Birkhoff.

### (c) DIAGONAL G^t_t vs OFF-DIAGONAL G^t_r (the channel decomposition)
On a round background with a live diagonal amplitude, varying omega:
```
 omega   max|dG^t_t| (diagonal inertia)   max|G^t_r| (momentum)
 0.00    0.0000e+00                        0.0000e+00
 0.10    1.78e-15  (machine floor)         1.05e-03   (linear in omega)
 0.30    2.66e-15  (machine floor)         3.15e-03
 1.00    1.78e-15  (machine floor)         1.05e-02
```
The diagonal time-kinetic shift is FLAT at machine floor for all omega (no inertia); the
live channel is purely the G^t_r momentum constraint, LINEAR in omega — the Birkhoff-escape
channel, the only thing the live time does on the round object. (Reproduces P4c(b,c) in the
full released-amplitude stack.)

### (d) K has zero modes (flat directions)
```
K singular values (Nr=12): [3.41 2.29 1.27 0.72 ... 0.06 | 0.0 x6]
```
The static restoring operator is rank-deficient: there are amplitude combinations with NO
restoring force (flat directions). Combined with M=0, the global minimum of sigma_min(omega)
sits at **omega=0** (the flat direction) at every cell. There is no nonzero frequency.

---

## 3. BOX-CONTROL GATE (the binding gate for any intrinsic-omega claim)

There is NO intrinsic nonzero omega to box-control — but the gate's real content here is:
does the no-inertia result survive cell-size and resolution change? YES, decisively.
```
=== BOX-CONTROL SCAN  Nr=12 ===
  cell R |    M_MS  | sig0(w=0) | w_globalmin | sigmin |  w*R
  10.000 |  2.98596 |  0.0e+00  |   0.00000   | 0.0e+0 | 0.000
  14.000 |  4.31663 |  0.0e+00  |   0.00000   | 0.0e+0 | 0.000
  18.000 |  5.63792 |  0.0e+00  |   0.00000   | 0.0e+0 | 0.000

  ||M|| across cells (10/14/18):  2.85e-9 / 2.24e-9 / 2.08e-9   (machine floor, R-independent)
  ||K|| across cells (10/14/18):  8.90    / 4.48    / 2.70      (scales ~ curvature, ~1/R^2)
  Nr=16 cell=14:  ||M|| = 2.93e-9  (machine floor; NOT a low-resolution artifact)
```
**VERDICT:** the inertia stays at machine floor at every cell AND at higher resolution
(Nr=16). The global-min frequency is omega=0 at every cell. There is no oscillator to
box-control. The static restoring ||K|| scales with the box (~1/R^2, a curvature operator),
which is the box-controlled CONTINUUM behavior #65 reported — confirmed here in the full
clean stack.

---

## 4. COMPARISON TO #65 (the reduced proxy)

**The full clean solver REPRODUCES #65's structure — it does not reveal a hidden tower.**

- #65 (reduced proxy: modeled radial profile + single-mode SL eigenproblem): intrinsic
  centrifugal/charge floor + box-continuum, NO new bound tower, ~1/R box-controlled.
- P5d (FULL clean stack: general 4x4 Einstein pole-stable hybrid + native S^2 EL coupled to
  the full metric + a(phi) ruler + live time row, amplitudes RELEASED): the round time-live
  channel has **NO inertia operator** (M = machine floor, R- and resolution-independent),
  hence NO oscillator, NO eigenfrequency, NO tower. The static restoring K is box-controlled
  (~1/R^2). The only live channel is the LINEAR G^t_r momentum constraint (the Birkhoff
  escape). This is the SAME {continuum + box-controlled} structure the proxy found.

**Did the full coupling reveal anything the proxy MISSED?** YES — one sharper, native fact
the proxy could not see: the absence of a tower on the round object is not a centrifugal-
barrier accident, it is a **Birkhoff cancellation of the diagonal d_t^2 inertia**. The d_t^2
content IS computed and wired (dtt_g~0.11, reaches dGamma[T]->Riemann), but it cancels
IDENTICALLY in the diagonal G^t_t for the round metric. The live time on the round object is
a pure first-order momentum flux (G^t_r, odd in omega per P4c(a)) with ZERO restoring
inertia — there is literally no oscillator to quantize on the round channel. This is a
cleaner, more structural statement than the proxy's "box-controlled barrier".

**Where a diagonal d_t^2 inertia WOULD survive:** the non-round l>=2 wave channel (phase0
B2 / P4c(c)), where d_t^2 h survives the angular projection. That is the off-round time-live
solve — NOT run here (see deferred, below). The ROUND ground state, observed in full, carries
no oscillator.

---

## 5. AUDIT — every compromise / freeze, flagged

| Item | tag | note |
|---|---|---|
| Observe-not-target | HELD | NO tower/catalog/spectrum hunt; #65 not re-litigated. The QEP was posed to OBSERVE what omega(s) the live metric admits, and it admitted none (M=0) — reported as the continuum it is, not chased. |
| Containment (omega->0 == static) | PASS | ||time-rows(x=0,omega=0)|| = 3e-10; static soliton is the omega=0 fixed point. |
| Data-blind, nothing banked | HELD | only residuals, omega-scalings, operator norms, code-unit M_MS. No M_MS/ratio/spectrum banked. (M_MS shown only as a code-unit background label; it differs from p5c's full-3D value because the round CHANNEL uses radial profiles + a different interior excision — both valid round ground states, data-blind.) |
| Anti-hang | HELD | single clean sequential process per call; every call 5-18 s (<<6 min cap); NO background poll; Nr<=16. FIVE+ prior agents hung; this did not. |
| Round channel (c=d=0 diagonal) | CHOSE (tractable, per #65/P4) | the round time-live channel is the in-budget one; the OFF-ROUND l>=2 inertia channel is P5e-deferred (named, not hidden). |
| Released the P4 amplitude pins | CHOSE (the whole point) | P4 pinned a1=b1=F1=0 for a bitwise containment check; P5d releases them to OBSERVE dynamics, keeping only the regular charge-1 fluctuation BCs. The released system has the static soliton as its omega=0 fixed point (containment, sec 2a). |
| Frozen background for the QEP | CHOSE (category-A) | K,C,M are assembled on the FROZEN static round ground state — the standard fluctuation-operator read (small-amplitude linear response about the floored solution). NOT a physics linearization of the solution itself (the background is the exact nonlinear floor). The "do the live amplitudes back-react" question is the fully-coupled time-live Newton = P5e/#65-class, throughput-deferred. |
| FD Jacobian (eps=1e-6, central) | CHOSE (numeric) | central-difference; the omega-power separation is exact for the quadratic HB form. Spot-checked: M is at machine floor regardless of eps order (the cancellation is structural). |
| POLE-STABLE HYBRID (inherited P4) | inherited (category-A) | the load-bearing P4 conditioning fix (Weyl backbone + kernel time-DELTA); omega=0 -> Weyl exactly. |
| a(phi)=-1 (k=0, W==1) | BASELINE | GR baseline; a(phi)!=-1 is P3 exploration, not P5d. |
| Core cutoff rc=0.05 | inherited | the #61 scar; inherited, scoped. |

**Is time GENUINELY live?** YES — dt_g~0.12, dtt_g~0.11 are nonzero and wired; the live row
produces a nonzero G^t_r linear in omega (sec 2c). Nothing stayed static except where
Birkhoff FORCES it (the round diagonal G^t_t inertia — correctly, and OBSERVED as the M=0
cancellation). Open-time only.

---

## 6. SCOPED STATUS + what quantization (postulate A) inherits

**P5d = DONE for its scope: the time-live OBSERVATION on the round ground state, in the full
clean stack, in budget.**

- **OBSERVED:** the round time-live channel is a CLASSICAL CONTINUUM with NO oscillator. The
  d_t^2 inertia cancels identically (Birkhoff) -> M = machine floor (R- and resolution-
  independent); the only live channel is the first-order G^t_r momentum flux (odd in omega).
  The static restoring K is box-controlled (~1/R^2). This is EXACTLY the expected pre-
  quantization classical result (postulate A: discreteness comes from quantizing a continuum,
  a SEPARATE downstream step) — a REAL observation, reported as such, NOT a failure.
- **CONFIRMS #65** in the full clean stack (general Einstein + native S^2 + a(phi) + live
  time, amplitudes released): no tower on the round carrier. SHARPENS it: the absence is a
  Birkhoff cancellation of the diagonal inertia, not a barrier accident.
- **NO box-control verdict on an intrinsic omega** — because there is no nonzero intrinsic
  omega (M=0). The box-control gate instead confirmed the no-inertia result is R- and
  resolution-independent.

**What quantization (postulate A on this continuum) INHERITS:**
- The classical time-live object on the round ground state is a continuum with NO classical
  oscillator on the diagonal channel — so DISCRETENESS cannot come from a classical round
  resonance (consistent with the catalog reframe: discreteness is NOT one carrier's spectrum).
- The live structure that DOES survive classically is the first-order G^t_r momentum channel
  (odd in omega) and the rank-deficient restoring K (flat directions). A quantization
  postulate would act on THIS structure — the momentum/phase channel and the flat directions
  — not on a (nonexistent) classical frequency ladder.
- The validated, in-budget K/C/M assembly is the handoff artifact: any quantization step has
  the exact classical operator content (restoring K with its zero modes, momentum C, zero
  inertia M) on the round ground state to act on.

**P5e-DEFERRED (named, not a verdict):** the OFF-ROUND l>=2 time-live channel, where the
diagonal d_t^2 inertia survives the angular projection (phase0 B2), is where a non-zero M
COULD appear — the fully-coupled off-round time-live Newton with omega free (the #60/#65-class
throughput wall). Not run here. P5d's round-channel result stands on its own: the round ground
state carries no classical oscillator.

---

## 7. ATTACK HERE (for a blind verifier)

- **The M=0 claim (the headline).** Re-assemble K,C,M (`assemble_KCM`) and confirm
  ||M||/||K|| ~ 1e-10 at machine floor. Verify it is a CANCELLATION not a dropped term:
  `build_metric_live(omega=1)` gives dtt_g~0.11 NONZERO (the inertia IS computed); the
  cancellation is in the diagonal G^t_t (sec 2c table: dG^t_t ~1e-15 across omega). If you can
  exhibit ANY round-channel amplitude direction with a nonzero omega^2 restoring (||M|| above
  ~1e-6), the no-oscillator claim is wrong — find it.
- **Containment.** `p5d_timelive.py contain 12 14` must give ||time-rows(x=0,omega=0)|| ~ 0.
- **Box/resolution independence of M=0.** Re-run `qep` at other cells / Nr=16 and confirm
  ||M|| stays at machine floor (it is NOT a single-grid artifact).
- **Released-amplitude vs P4 pins.** Confirm `amplitude_bc_mask` pins ONLY the 4 regular
  fluctuation-BC nodes (a1(seal), b1(core), F1(core), F1(seal)) and frees the rest — i.e. the
  P4 containment pins on the interior amplitudes ARE released (the dynamics is genuinely open).
- **Did I smuggle a target?** Grep the script: no m*PI ladder added, no banked M_MS/ratio, no
  desired-frequency search. The QEP was posed to find whatever omega the live metric admits;
  it found none (M=0), reported as the continuum.
- **The honest two-edged read:** a skeptic could say "M=0 means the round channel is the WRONG
  place to look for dynamics" — agreed; that is exactly the P5e-deferred off-round l>=2 channel,
  and the catalog reframe (#65/postulate A): the round carrier does not tower, by construction.
