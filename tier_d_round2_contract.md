# Tier-D Round-2 Falsification Contract (Pre-Registered)

Status: PRE-REGISTRATION — written BEFORE the test is run.
Created: 2026-06-10.
Companion test script (to be written and run only AFTER this file):
`native_tier_d_round2_test.py`.
Alters nothing existing; new files only.

## Why a second round is contract-compliant

Round 1 (`lepton_ladder_falsification_contract.md`, committed at git
`26fc757`) tested the then-available native vocabulary against the six
required branch coefficients and failed cleanly: 126/126 classifications
were MISS (`lepton_ladder_test_results.md`). Its T5 verdict froze the six
required values as the standing wall any future derivation must hit, and
its prohibition list forbade retuning THAT model.

Since then, the 2026-06-10 session derived NEW exact constants with ZERO
lepton input — all from interface/weld/threshold geometry
(`weld_interface_mode_results.md`, `weld_two_sided_results.md`,
`native_warped_dtn_hessian_spectrum.py` heritage re-derived this session,
and the spectrum-stage quotient/commutator ledger). Testing these against
the wall is a NEW pre-registered round with its own candidate list. It is
NOT a retune of round 1:

- no change to depths (5/7), eta, N, or gamma's form — the wall numbers
  themselves are taken exactly as round 1 froze them;
- no round-1 candidate is re-included in the new rational vocabulary
  (the round-1 declared rationals are an explicit EXCLUSION set below);
- one disclosed overlap: `D2` appeared in round 1's C_E1 list and was a
  MISS there. It re-enters here only because it is a member of the
  complete warped-DtN family {D1, D2, D3} that this session re-derived;
  its round-1 MISS classification stands and any round-2 result for `D2`
  on the C_E1 slot is redundant with round 1, not new information. It is
  retained so the family is tested mechanically, not cherry-picked.

## Build protocol (binding, already honored)

The candidate list below was assembled STRUCTURALLY — directly from the
session's derivation outputs (groups A-C) — before any candidate value
was compared to the wall numbers. The wall numbers are published in this
repo, so the list cannot be truly blind to them; as in round 1, this
means a %-level match is UNINFORMATIVE, only HIT-level matches that
survive look-elsewhere carry any weight, and nothing may be added,
removed, or reweighted after the run.

## Targets (frozen; from round 1, not restated here by digit)

The six wall numbers recorded in the "Standing constraint" section of
`lepton_ladder_test_results.md`: local-branch `C_M1`, `C_E1`,
`C_E1/C_M1`, and the warped-branch triple. The test script quotes them
verbatim from that doc at evaluation time. They are required
coefficients, not data: the lepton input is already absorbed in them and
no further lepton data enters this round.

## PART 1 — Pre-declared round-2 candidate list (COMPLETE)

All values exact (closed Bessel forms at mpmath 40 digits, or exact
rationals). Provenance per item. Nothing may be added after the run.

### Group A — warped DtN eigenvalues (this session's re-derivation; heritage `native_warped_dtn_hessian_spectrum.py`)

`D_ell = sqrt(ell(ell+1)) I_{7/2}(6 sqrt(ell(ell+1))) / I_{5/2}(6 sqrt(ell(ell+1)))`
(self-similar collar q = 1/3; beta = q/2, nu = 5/2, x0 = sqrt(lam)/beta).

```text
A1  D1 = sqrt(2) I_{7/2}(6 sqrt 2)/I_{5/2}(6 sqrt 2) ~= 0.9796633
        (warped ell=1 DtN eigenvalue; the H1-triplet block)
A2  D2 ~= 1.9857855          (ell=2 block; round-1 overlap disclosed above)
A3  D3 ~= 2.9893060          (ell=3 block)
A4  D2/D1 ~= 2.0270081       (DtN spectral step, ell=1 -> 2)
A5  D1^2 ~= 0.9597402        (squared triplet eigenvalue; two-action form)
A6  B = I_{7/2}(6 sqrt 2)/I_{5/2}(6 sqrt 2) ~= 0.6927266
        (the Bessel argument ratio = D1/sqrt(2); the warped-gamma exponent
         object, gamma_warped = 3 exp(-B/36))
A7  exp(-B/36)/exp(-1/36) = exp((1-B)/36) ~= 1.0085719
        (the exact warped/local gamma quotient — the inter-branch
         transfer-action mismatch)
```

### Group B — interface threshold objects (weld phases 2-3; `weld_interface_mode_results.md`, `weld_two_sided_results.md`)

`L0(lambda) = -(1-2q)/2 + (q tau0/2) I'_nu(tau0)/I_nu(tau0)`,
`nu = sqrt(1+4q(1-q))/q = sqrt(17)` at q = 1/3, `tau0 = 2 sqrt(lambda)/q`.
Verifier-grade closed form (agent `ae8caa64ef3d4b1ff`, 7-9 digits).

```text
B1  L0(2)        = 1.33835009   (binding threshold, lambda = ell(ell+1) = 2)
B2  L0(2)/(4/3)  ~= 1.0037626   (threshold vs the symmetric-pair 4q;
                                 the confirmed-mirage 0.376% object,
                                 entered mechanically, not romanced)
B3  2q/L0(2)     ~= 0.4981258   (the threshold deficit, gamma/gamma_c)
B4  L0(2)/(2q)   = 2.0075251    (inverse deficit; the recorded ~2 factor)
B5  L0(6)        = 2.29931870   (threshold at lambda = 6)
B6  L0(6)/L0(2)  ~= 1.7180248   (threshold spectral step)
```

### Group C — spectrum-stage exact rationals NOT in round 1's lists

Generative rule (mechanical; the script implements exactly this and
prints the realized list):

1. the isotropy constant `3` (= N; trivial inclusion, declared);
2. the quotient-completion shares `{1/9, 2/9, 6/9}` (spectrum doc
   §40-42) and their 6 pairwise quotients;
3. the commutator W-share complements `{3/8, 5/8}`
   (`native_commutator_kernel_image_split.py` heritage);
4. all products of <= 2 elements (singles and unordered pairs,
   repetition allowed, i.e. squares included) of the EXPLICIT banked
   ledger
   `{q=1/3, s=1/9, eta=1/18, eta/2=1/36, q/2=1/6, W(A3)=1/4, W(S5)=5/12,
     W(T8)=2/3, 8/9, 2/9, 3/8, 5/8}`;
5. DEDUPE by exact rational value (pooling 1-4);
6. EXCLUDE the round-1 declared rational candidates
   `{1, 35/36, 37/36, 2/3, 2, 35/18, 3/2, 5/3}` (the exclusion set is
   round 1's two DECLARED lists; round 1's 49 mechanical ratio quotients
   were combinations, not declared candidates, and do not extend the
   exclusion set — declared here so the rule is unambiguous).

Note recorded in advance: step 6 removes `6/9 = 2/3` (round-1 W(T8)) and
the pairwise quotients `2` and `1` wherever generated; this is intended.

### Slots and comparison forms

For each branch (local AND warped, identically — round 1 T4 rules apply
unchanged: no averaging, no per-observable branch choice; a cross-branch
split is a MISS for both):

```text
C_M1  : each candidate c compared as  c        (1*c — the 1 is the bare
        M1 normalization; identical to comparing c directly)
C_E1  : each candidate c compared as  c  AND  2*c
        (the 2 is the declared E1 relative-shape plane dimension from
         round 1 — pre-registered there, carried over, not new)
ratio : each candidate c compared as  c  AND  2*c
```

### Tolerances (binding; identical to round 1)

```text
HIT:   |fractional deviation| <= 1e-4   (0.01%)
LEAD:  |fractional deviation| <= 1e-3   (0.1%) — flagged, must survive
       look-elsewhere; NOT bankable by itself
MISS:  anything worse
```

### Look-elsewhere accounting (MANDATORY, per slot)

Reported next to every slot, and next to any HIT/LEAD:

1. **Uniform null**: K = number of comparisons in the slot, the
   comparison-value range, and `E = K * 2 * tol * |target| / range` for
   both tolerances. Crudeness stated as in round 1 (range estimated from
   the candidates themselves; candidates cluster, so this UNDERSTATES
   the accidental expectation near the clusters; order-of-magnitude
   only).
2. **Farey / dense-rational null** (the sharper null of
   `dimension_ladder_null_audit.md`, mandatory for the rational
   candidates): with Q = the maximum denominator appearing among the
   slot's rational comparison values, report (i) the Farey-density
   expectation of accidental reduced-rational matches
   `E = 2 * tol * |target| * (3/pi^2) * Q^2` at both tolerances, and
   (ii) the EXACT enumeration count of reduced fractions p/q, q <= Q,
   inside the HIT and LEAD windows of the target. This prices the whole
   vocabulary CLASS "rationals of this complexity", not just the K
   drawn from it — the brutal envelope. A rational HIT whose Farey
   expectation is of order 1 is worthless regardless of the uniform
   null.

### Verdict rules (identical to round 1 T5)

- No HIT anywhere: the round-2 vocabulary joins round 1's on the failed
  side of the wall; the six numbers remain the standing constraint;
  nothing is adjusted in response.
- LEAD surviving look-elsewhere: recorded for the named candidate ONLY,
  with rationale, for future derivation work. Not banked.
- HIT surviving look-elsewhere: still NOT a derivation — recorded as a
  sharp target; the boundary-Hessian derivation of that specific
  coefficient is required before any grade rises. No banking.

Explicitly FORBIDDEN after this file is written: adding/removing/
reweighting candidates, changing forms or tolerances, branch averaging,
reporting only the better branch, re-running with a modified list.

### The real target (restated)

The REAL Tier-D objective remains the boundary functional
`S_phi0[typed nodes]` and its Hessian (STATE.md item 0;
`native_typed_nodes_boundary_functional.py` lineage). This round is a
VOCABULARY TEST with the session's new exact objects — a cheap, honest
way to check whether the new constants already contain the wall numbers
— not the derivation, and no outcome here substitutes for it.

## PART 2 — QUARANTINE (post-hoc observation; EXCLUDED from Part 1)

**Contaminated by construction.** During the session the driver noticed,
BY INSPECTING THE TARGETS (not by derivation), that the local-branch
ratio `C_E1/C_M1` is close to

```text
2 (1 - s^2) = 2 * (80/81) = 160/81    (s = 1/9)
```

This observation is EXCLUDED from Part 1 and from all Part-1
look-elsewhere counts, because:

- `10/9` is not a banked share, and `80/81` is not generatable by the
  Group-C rule (no ledger pair multiplies to 80/81);
- the form `2(1 - s^2)` was found by target inspection — exactly the
  post-hoc fishing that the pre-registration discipline exists to fence
  off.

The script must PRICE it with a brutal null, all three computations
mandatory:

(a) density of rationals `p/q`, `q <= 81`, near the target: exact
    enumeration of reduced fractions inside the observed-deviation
    window and inside the HIT window, plus the Farey-density
    expectations for both windows at Q = 81;
(b) density of the post-hoc FORM FAMILIES near the target:
    `2(1 - 1/n)`, `2(1 - 1/n^2)` (counts inside both windows, plus the
    local-spacing chance probability at the nearest member), and
    `2 * (1 - 1/m)(1 - 1/n)` for `2 <= m, n <= 200` (product-of-two-
    near-1-rationals family; counts inside both windows) — noting any
    naming multiplicity (the same value reachable several ways is
    evidence the naming is cheap, not that the value is special);
(c) the honest conclusion, verbatim template:
    "observation recorded, p ~ [computed], status: QUARANTINED
    LEAD-CLASS — usable only if a derivation produces the form 2(1-s^2)
    independently."

The headline p is the most BRUTAL (largest) of the computed chance
probabilities. Whatever the numbers say, the observation's status after
this round is QUARANTINED LEAD-CLASS, not a lead, not a hit, not banked,
and it may never be added to a future candidate list as if it had been
pre-declared.

## Relation to existing rules

Round 1's contract rules (pre-registration, frozen tolerances, mandatory
look-elsewhere, T4 branch handling, T5 verdicts, failure allowed) carry
over verbatim. This round adds only: a new candidate list with new
provenance, the Farey-null requirement promoted from methodology
(`dimension_ladder_null_audit.md`) to mandatory per-slot accounting, and
the Part-2 quarantine protocol for post-hoc observations.
