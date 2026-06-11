# HANDOFF — Resume Instructions and Session Record

Rewritten 2026-06-11 at session close (Claude, project driver),
superseding the 2026-06-10 version (its content lives in git history
and the results docs; nothing load-bearing was lost — see "must not
lose" below). Read order for a new session:
1. STATE.md — the SESSION-CLOSE SNAPSHOT section is the authoritative
   resume point (frontier, verified stack, queue).
2. CLAUDE.md — the charter: Charles's six principles + the 2026-06-11
   additions (interrogation discipline: declare metric-led vs
   template-led; premise-scoped negatives; hypothesis discipline; GPU
   usage + the two recorded torch pitfalls).
3. NEGATIVES_REGISTRY.md — 21 premise-scoped entries; check before
   treating ANY banked negative as blocking.
4. Results docs in the order STATE lists them, as needed.

## Who drives and how

Charles handed direction to Claude 2026-06-10; Charles canonizes
(CANON.md, append-only). Charles's standing default (2026-06-11,
binding): SOLUTION-SPACE FRAMING — "it's an equation with limited
variables; what answer solves it?"; all degrees of freedom
simultaneously; full nonlinearity; never per-component. He regards
the mechanism-template detour as AI-training bias he had to drag the
project past — do not make him do it again. Commit per result; push
to github.com/charlesrotter/udt_mass_codex.

## The state in three sentences (2026-06-11 close)

The static sector is CLASSIFIED BY THEOREM (pde_p1_results.md,
61/61): under C1 alone the complete static solution set is
{f spherical, q = 0, w arbitrary} — formed angular cells are not
static solutions. THE FORK IS ADJUDICATED
(nonstationary_opener_results.md, VN-ruled): motion never sources
shape (the fate polynomial is f_T-free); no sector of C1 propagates
hyperbolically in T; formed cells admit no bounded-in-T continuation.
C1 ALONE HOLDS NO MATTER — the SINGLE FORCED OBJECT is the native
w-stiffness sector (EH-remainder species, the program's oldest named
target, reached independently by two eras). The only T-bounded
oscillatory sector: the attractive seal family h > h_c (the
theta-dial — its selector = the persistence condition).
Along the way, verified: cells condense from the medium under
c* = 0.499 gamma^2 (diagonal class); LIKE CELLS ATTRACT inverse-square
with CHARGE = MISNER-SHARP MASS (Q = 2 p_F, E_int = 8 pi m1 m2/d);
isolation is impossible; the angular flip makes the old silence
record diagonal-class-conditional with ell >= 2 real-frequency
candidates.

## Must-not-lose facts

- THE SAME-MINUS STRUCTURE IS NOW A THEOREM (upgraded by VN,
  nonstationary_opener_results.md): the flip is derived by the unique
  nondegenerate time-row elimination — no longer a premise. Rejecting
  it would unwind the fork adjudication itself. (If the branch
  convention were ever overturned: fate polynomial and ellipticity
  survive; only the growth/oscillation assignment inverts.)
- The six lepton wall numbers stand UNHIT (local C_M1=0.977679087638,
  C_E1=1.93121474779, ratio=1.97530536575 + warped triple; contract
  at 26fc757); three pre-registered rounds missed (126/126, 740/740,
  12/12); the live thread is the interface sub-rung objects
  (mass_audit_results.md: angular floor, (e-1) measure correction,
  Delta-p_F — C < 1 direction, phi-angular sourced) GATED on the
  species-bridge (nonstationary/ensembles).
- QUARANTINES (no status without independent derivation): 160/81 for
  the wall ratio; M(0) ~ 2ell+1 (explained as uniform asymptotic);
  chat ~ 1/2 (refuted exact); the ~10 collapse triple; ladder
  near-integer ratios. The sand flag stands (Planck blackbody rides
  quarantined work; macro_contamination_map.md scoping).
- CANON RESIDUES AWAITING CHARLES (wording only, both
  compute-settled): the mirror-class exterior sentence ("the
  embedded-cell exterior is the unique smooth continuation of the
  interface jet", NOT "exactly y^-q"); the "inside a cell" vocabulary
  choice (weld-sphere interior vs f >= 1 region — nothing physical
  rides on it).
- CONVENTIONS ARE LOAD-BEARING: classifier (absolute f_min + horizon,
  stated with every c*); seal-shell figures carry (gamma, eps, cutoff);
  three-term extrapolations are not bankable; erratum of record: the
  seal curvature law is 24a^2/y^4 (not the 12 printed in
  fork_tests_results.md/old STATE).
- Provenance: origin chats (dozens-hundreds, pre-metric six-week
  failure period included) EXIST, archival deferred until success
  (PROVENANCE.md); origin screenshot archived in-repo.
- AUDIT.md (untracked) = the S116 macro dispatch copy from
  /home/udt-admin/UDT — left untracked by Charles's arrangement.

## Queue (mirrors STATE)

1. DERIVE THE NATIVE w-STIFFNESS SECTOR — the single forced object
   (the nonstationary opener ran and adjudicated the fork; secular
   stability answered: no bounded-in-T continuation, all rescues
   refuted, no breather support at probe level). Acceptance tests
   banked: shaped-matter solutions + preserve the data-validated
   spherical/macro sector. Then the theta-dial selector.
2. ell >= 2 corrected-class spectrum, rescoped (trust-bounded
   diagonal/Class-B, or nonstationary).
3. Tier-D re-pose once the species-bridge exists (pre-registration
   mandatory; data-blind).
4. Macro program (Charles's roadmap, in memory:
   macro-consilience-roadmap): finish CMB; MESA stellar evolution;
   SPARC dim-baryon (sparc_native_force_law_note.md — verifier-ruled
   status appended); weak lensing; CMB dipole (= the off-center
   embedding question). Consilience ledger only after these.

## Process notes

- Maximize subagents; present process plans; verifier-before-record
  (this session: every headline was amended or strengthened by its
  blind pass — four banked-number errata caught); pre-register before
  testing; calibrate, never dramatize (Charles called out "break it
  open" inflation — the honest register is attrition/convergence).
- GPU: V100 via torch float64 (nvidia-smi/NVML broken — ignore);
  pitfalls recorded in CLAUDE.md (batched solve_triangular broadcast
  corruption; large-batch eigensolve corruption — matmul-only
  reductions + CPU asserts).
- Background agents that end their turn mid-compute: set a process
  watcher (self-match-proof pgrep pattern), then relaunch a collector
  on the workspace.
- Charles asks for lay summaries regularly; keep the directionality
  right: matter = fast time (f > 1, c_eff = f), deep universe = slow
  time/redshift.
