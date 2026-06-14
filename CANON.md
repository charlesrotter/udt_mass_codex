# CANON — Charles-Canonized Statements

Per the Self-Hardening Protocol, only Charles canonizes. This ledger
records canonization events: exact statement, date, what it forces,
provenance. Append-only.

## C-2026-06-10-1: The areal reading of positional dilation (R-areal)

**Statement:** Positional dilation grows with the AREAL radius: phi is a
function of r_areal (the invariant sphere size, sqrt(Area/4pi)), and the
B=1/A condition (g_tt * g_rr = -1) holds in the areal chart.

**Forces (banked theorems):**
- rho = r exactly (C2 theorem,
  native_positional_dilation_distance_readings.py): P0's areal choice is
  now a THEOREM, not a silent postulate.
- Branch (iii) of the discreteness map is CLOSED in the static sector
  (threshold rigidity theorem + areal reading): no saturating areal
  function, no static throats, no static threshold lifting.
- The beta(rho) derivation program is MOOT in statics.

**Provenance:** macro_sector_fork_resolution.md — the data-validated
macro stack (d_L = r(1+z), D_M = r, Misner-Sharp; Pantheon+ chi2/dof
0.94 beating LCDM at 0 free params; DESI BGS 0.90 sigma) operationally
instantiates this reading. Canonized by Charles 2026-06-10.

## C-2026-06-10-2: The finite-cell canon

**Statement:** Dilation is monotone on a finite domain terminated by a
physical boundary, mirrored across phi -> -phi. The universe is a finite
cell ([0, r_CMB], phi: 0 -> ln(1101) at the CMB boundary); matter cells
are finite inside-out cells (phi: 0 at the interface -> -infinity at the
core endpoint). There is no spatial infinity.

**Forces:**
- The open-domain threshold theorems lose their premise globally:
  branch (ii) (compact domain) is realized BY the cosmology.
  Discreteness is native and automatic; the box-control scaling is
  reinterpreted (the box is the universe).
- The matter cell's finite domain and its phi=0 interface are PHYSICAL
  structure (the mirror of the CMB boundary), not a hand-placed wall.
- The sharp open question becomes spectral SCALE-AUTONOMY: what makes
  particle-scale cells spectrally autonomous from the Gpc-scale global
  domain.
- The C=0 vs C>0 vacuum-selection question dissolves at macro scope
  (the cosmological profile is sourced; "vacuum gap").

**Provenance:** macro_sector_fork_resolution.md (legacy CG finite-domain
Class A closure, lines 846-859; current dispatches, Theory Rule 5).
Canonized by Charles 2026-06-10.

## C-2026-06-10-3: Program redirect for native discreteness

**Statement:** The native-discreteness program redirects to:
(a) the NONSTATIONARY phi-angular sector — the rung-2 weld
    (d_r(e^{-2phi0} H1) = 2 d_t(delta phi) + d_t K - ...), a derived,
    CMB-data-tested dynamical phi-angular coupling outside every static
    no-go — as the surviving home of the phi-angular interaction hunch;
(b) the transfer-ladder route (no continuum threshold needed);
(c) multi-cell/ensemble asymptotics (the orchestra).
Static throat/threshold-lifting mechanisms are retired per C-1.

**Provenance:** macro_sector_fork_resolution.md; AUDIT.md (S116 weld
derivation). Canonized by Charles 2026-06-10.

## Provenance annotation (2026-06-10, appended)

The origin prompts (2025-08-12, Grok; see PROVENANCE.md) bear on two
canon entries: C-1's areal reading is a later refinement — the original
"time dilation with distance" left the distance notion unspecified, and
R-areal was fixed by macro data. C-2's finite-cell canon matches the
founding intent directly — Prompt 2 already asserts redshift increasing
asymptotically "as you approach the universe boundary." Recorded as
provenance/consilience, not as evidence for either canon.

## C-2026-06-13-1: The nonstationary diagonal sector propagates in T

**Statement:** The whole metric, in its diagonal dilation-tie class
(g_tt = -e^{-2phi}, g_rr = +e^{2phi}), is STRICTLY HYPERBOLIC in time:
its own field equation has principal-part signature (-,+,+), with finite
positive wave speeds c_r^2 = e^{-4phi}, c_theta^2 = e^{-2phi}/r^2. The
metric PROPAGATES in T; it does not cell-collapse to an elliptic dead end.
The wave is physical (the Ricci scalar carries real phi_TT / phi_T^2).

**Forces (and what it does NOT force):**
- The banked negative #22 ("no sector propagates hyperbolically in T;
  cells do not evolve") is CONDITIONS-CHANGED on those clauses: they
  rested on a single sign error (v_a3.py time-kinetic term +f_T^2/f^2,
  Euclidean/elliptic, vs the Lorentzian -f_T^2/f^2). The original
  "Hadamard ill-posedness" WAS the sign error (high-k discriminator:
  corrected sign bounded; v_a3 sign blows up ~1e60).
- It does NOT lift the no-shaped-matter conclusion: the fate polynomial
  2 f q v_h (f q v_r - v_h)^3 is f_T-free, so MOTION NEVER SOURCES SHAPE.
  The diagonal metric evolves but makes no nonstationary matter by itself.
- It CONFIRMS the C-2026-06-10-3 redirect's bet that the live home of the
  phi-angular interaction is the NONSTATIONARY sector, and it relocates
  the program's open frontier to the OFF-DIAGONAL angular row (where the
  centrifugal term is reported to flip attractive, where the gap test
  needs the measure-weighted self-adjoint eigenproblem, and where the
  "e_T never timelike" record is least settled).

**Provenance:** solution_space_map.md (queue-head open-ended scan);
ns_scan_results.md; blind verifier ns_scan_verifier_results.md
(agent a9cfcd85385bff920), independent re-derivation + high-k test.
Canonized by Charles 2026-06-13.

## Standing flag (Charles, 2026-06-10, appended)

The Planck blackbody derivation in the macro/CMB work relies on
quarantined or withdrawn mass-emergence theories. Macro observables that
ride it may be used as HYPOTHETICAL/common-mode layers only, never as
derived foundations. Do not build on sand: any macro computation must
carry a provenance grade per layer, and weld-discrimination conclusions
must be differential (conditional on the flagged common pipeline).

## C-2026-06-14-1: B=1/A is SOURCED inside matter by the angular sector

**Statement:** Inside matter, the defining UDT relation g_tt g_rr = -c^2
(equivalently B = 1/A, the two radial dials locked) is not merely postulated
but DERIVED: UDT's own angular-sector field — the unit 3-vector n_a whose
winding density is the H1 area form omega_H1 = eps_abc n_a dn_b ^ dn_c (the
same object carrying N=3, q=1/3) — sourced by the minimal covariant
two-derivative Lagrangian L = -(xi/2) g^{mu nu} d_mu n_a d_nu n_a built from
the UDT metric measure, produces a stress tensor with T^t_t = T^r_r in any
PURELY-ANGULAR (no-radial-gradient) configuration. Since the metric identity
g_tt g_rr = -c^2 <=> G^t_t = G^r_r <=> p_r = -rho, this T^t_t = T^r_r source
is exactly what the relation demands; it leaves the theta-equation that fixes
g_rr = e^{2phi} intact (deg-1 hedgehog: T^theta_theta = 0). Hence B=1/A holds
inside matter as a THEOREM of the angular source, not a choice.

**Scope / boundaries (binding — do not overstate):**
- Holds for any purely-angular config (d_r n = 0); the degree-1 hedgehog
  n = x/r is the unique member with also T^theta_theta = 0.
- ROBUST to native additions: a Skyrme term, a potential V(n), or the
  eta-seal coupling all preserve T^t_t = T^r_r (they change T^theta_theta and
  the solid-angle-deficit value only). So B=1/A does NOT hinge on the
  minimal-model choice; the SPECTRUM (masses) will, but the EOS does not.
- BREAKS under a radial twist: for Theta = Theta(r),
  p_r + rho = xi e^{-2phi}(Theta'(r))^2 >= 0, zero iff Theta' = 0. A
  realized smoothed-core soliton satisfies p_r = -rho exactly only where
  Theta' = 0; the pure topological n = x/r is exact everywhere.
- A canonical SCALAR cannot do this (p_r + rho = e^{-2phi} phi'^2 > 0): the
  source MUST be the angular/topological sector. phi RESPONDS.

**Forces:**
- RESOLVES the B=1/A fork (external_input_notes.md fork #1, the queue head)
  in favor of KEEP. Model A ("relax B=1/A inside matter; a scalar sources a
  two-function interior") is excluded for the topological sector: the
  one-function form is sourced, not relaxed.
- STRENGTHENS C-2026-06-10-1: the areal-reading B=1/A, previously a
  vacuum-validated postulate, is now derived inside matter via the angular
  source. The relation g_tt g_rr = -c^2 is the first defining UDT relation
  shown to be SOURCED by a derived UDT object rather than postulated.
- Confirms the convergent direction (our findings + two external models): the
  angular/topological sector is the SOURCE of matter, phi is the response
  (slaved via p_r = -rho). This is the program's FIRST constructive positive.

**Provenance:** angular_lagrangian_results.md (constructor, Claude Opus 4.8,
agent a440405d389552f39); angular_lagrangian_verifier_results.md (BLIND
adversarial verifier, Claude Opus 4.8, agent a4edbefa0e29edfa2) — anchor
genuineness independently re-derived from the original dpf density
(rescued_workspaces/.../v_c1_closedforms.py:90-99), I_native == G1 to ~1e-48;
sympy-exact stress tensor + V100 float64 machine-zero over 4096 points. Two
non-blocking errata recorded (G1/H prose; deficit sign convention).
Canonized by Charles 2026-06-14.
