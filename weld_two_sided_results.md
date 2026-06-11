# Weld Two-Sided Results

Status: working audit, not canonical.
Created: 2026-06-10.
Script: `native_symmetric_pair_reduction.py` (34 symbolic/exact +
numerical PASSes; new 2026-06-10). Recon finding cites banked text
directly (no new computation needed). Alters nothing existing; new
files only.

## Headline: weld phase 3 is COMPLETE — THE TWO-SIDED ROUTE IS CLOSED

Phase 2 ended with one named candidate (`weld_interface_mode_results.md`
consequence 2): the deficit at the most natural BC is a clean factor
~2 (2.0075, lambda=2), and the banked corpus contains TWO-SIDED
interface structure — does it supply a compound shell with total
`gamma > gamma_c = L0`? Phase 3 answers with two findings, one from
recon of the banked corpus and one theorem-grade closure of the
adjacent non-banked configuration. Both negative. The route is closed.

### Finding 1 (RECON, banked content): the corpus's two-sided structure supplies NO second shell

What the "two-sided" banked material actually is:

- **The two-sided content is the transfer-kernel COMPOSITION LAW**,
  not a second interface: `eta/2` per side gluing to `eta` — a
  conditional identity ("exact if the transfer kernel is one side of
  a symmetric composable phi0 boundary action"). Cite: negative_phi
  doc sections 263 (half-action from symmetric gluing, lines
  18758-18830) and 380; `native_half_action_from_symmetric_gluing.py`.
- **The interface stress is a SINGLE jump**: `Delta Pi = q/2`
  (`Pi_inner = -q/2`, `Pi_outer = 0` — the exterior is FLAT, CANON
  C-2 zero tail). Cite: sections 165-166 (lines 11098-11183).
- **Naive per-side stress doubling is explicitly FORBIDDEN** by the
  banked double-count guards ("two half-boundaries glue to ONE full
  boundary action"; "two nominal nodes constrained to the same edge
  variable count ONCE"). Cite: sections 217-219 (lines 15350-15419);
  `native_interface_vs_warped_double_count_test.py` ("warped branch
  must prove it replaces, not multiplies, the C1 side action").
- **Exterior mirroring is NOT USED** anywhere in the banked chain:
  the phi -> -phi mirror (section 235) is a sign/bridge statement at
  the phi=0 surface, not a mirrored profile in r; the banked cell
  glues to the flat exterior, full stop.
- **No native sub-cavity / nested shell exists**: zero matches for
  any such structure in the native doc (grep-audited).

So the banked corpus delivers exactly the phase-2 single shell,
`gamma = 2q = 2/3`. There is no licensed compound configuration to
compute.

### Finding 2 (SYMMETRY-REDUCTION THEOREM): even the non-licensed symmetric pair delivers nothing

`native_symmetric_pair_reduction.py` computes the one adjacent
NON-licensed configuration anyway — the matter cell glued to the even
continuation of its own profile about r = R (doubled slope jump
`Delta phi' = -q/R`, doubled delta strength `Gamma = 4q`) — purely to
close the question, because `4q = 4/3` sits 0.376% below
`L0 = 1.33835009`. Result (exact, three-line reduction):

```text
EVEN sector:  u'(R+) = -u'(R-) (symmetry) + jump u'(R+) - u'(R-) = -(4q/R)u(R)
              =>  u'(R-) = +(2q/R) u(R)
              =  phase-2 BC-c EXACTLY, gamma_eff = 2q, same L0,
                 same 2.0075 deficit — UNCHANGED by pairing.
ODD sector:   u(R) = 0  =  phase-2 BC-b (Dirichlet) EXACTLY —
              the delta does no work; never binds, for ANY Gamma
              (theorem level, strictly worse).
```

Numeric cross-check (that the reduction argument is implemented
right): the full two-domain symmetric problem (interior collar
`[r_min, R]` with `f = (R/r)^{1/3}`, `E0 = s/r²`, reflected
coordinate on `[R, 2R - r_min]`, doubled delta at R) has spectrum
equal to the UNION of the phase-2 BC-c and BC-b spectra to 4+ digits,
parity-classified eigenvectors + independent shooting:

```text
top even omega² = -3.4667814 (lam=2),  -10.376405 (lam=6)   [= BC-c]
top odd  omega² = -27.334956 (lam=2),  -41.213694 (lam=6)   [= BC-b]
```

No positive eigenvalue anywhere. **The tantalizing 4/3-vs-L0
proximity (0.376%) is a CONFIRMED MIRAGE**: the symmetric pair never
delivers an effective `4q` to any single sector — the factor 2 in
`Gamma = 4q` is consumed by the even/odd split, never by binding.
Comparing the total jump against the single-sector threshold is
exactly the double-count the banked guards forbid at the action
level. The null-test discipline that refused to romance 2.0075-vs-2
in phase 2 is vindicated.

## Consequences

1. **The interface-shell route to native oscillation is now closed at
   every banked and adjacent-non-banked configuration**: single shell
   (phase 2), compound/two-sided (phase 3). The exact obstruction
   stands: the geometry supplies `gamma = 2q <= 1` (`q < 1/2` by
   finite action) while binding needs `L0 >= 1.338` (`lambda >= 2`).
   Native oscillation via interface shells would need `gamma > L0` —
   i.e. structure the static spherical single-center geometry does
   not contain.
2. **Remaining routes (per CANON C-3)**: (a) **true ensembles** —
   non-concentric multi-cell configurations (symmetry-breaking,
   genuinely new machinery — the orchestra route, now the LAST
   standing weld-sector route); (b) **the transfer ladder**
   (untouched, six wall numbers); (c) **the macro discriminator**
   (queued).
3. **Honest scope note**: the weld-sector negatives are all within
   Reading A's linear normal-mode scope — nonlinear/nonstationary
   structures (breathers proper) remain outside every theorem proved
   so far.

## Verification note

The reduction theorem is corollary-grade: it reuses phase 2's
blind-verified threshold machinery (agent `ae8caa64ef3d4b1ff`, 7-9
digit reproduction of `L0`, the Bessel closed form `nu = sqrt(17)`,
and the headline spectra) and adds only the even/odd decomposition —
which is cross-checked numerically in-script (two-domain FD spectrum
= union of the phase-2 spectra to 4+ digits, parity residuals
~1e-13, independent shooting agreement, r_min control). The recon
finding cites banked text directly.

## Next targets

1. **Decision point for Charles**: invest in the ensemble route (new
   machinery — non-spherical multi-cell mode problems) vs pivot weld
   effort to the macro discriminator + the transfer-ladder
   coefficient derivation (the Tier-D functional against the six wall
   numbers).
2. **Recorded for future audits**: the `E0 < 0` window remains the
   one standing oscillation mechanism, and it requires a native
   source with NEGATIVE `E0` — no banked source supplies it. Any
   future sector that does (flag it) re-opens the window immediately.
