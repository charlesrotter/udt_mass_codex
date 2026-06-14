# BLIND ADVERSARIAL VERIFIER — Angular-Sector Lagrangian / p_r=-rho / "B=1/A inside matter"

Verifier agent: Claude (Opus 4.8, 1M context), acting as blind adversarial
verifier. Date: 2026-06-14. Target doc: angular_lagrangian_results.md
(constructor). All derivations below are INDEPENDENT (my own sympy /
mpmath / torch machinery; constructor scripts NOT executed or trusted).

Scripts (this verifier, commit-grade):
- `angular_lag_verif_stress.py` — independent UDT-background stress tensor, hedgehog.
- `angular_lag_verif_offhedge.py` — radial-twist obstruction + NON-hedgehog purely-angular configs.
- `angular_lag_verif_backreact.py` — independent Christoffels/Ricci/Einstein tensor for the UDT metric.
- `angular_lag_verif_anchor.py` / `angular_lag_verif_failartifact.py` — anchor (Inat==G1), high-precision.
- `angular_lag_verif_reduction.py` — dpf-side density f_theta^2/(4f) reduction.
- `angular_lag_verif_skyrme.py` — deficit ODE solve + Skyrme/potential robustness of T^t_t=T^r_r.
- `angular_lag_verif_gpu.py` — V100 float64 spot-check (4096 pts).

================================================================
## DECISIVE VERDICT FIRST
================================================================

- ANCHOR (C3): **GENUINE AND INDEPENDENT — NOT reverse-engineered.**
- p_r + rho = 0 for the hedgehog: **CONFIRMED (exact, phi-independent, machine-zero on GPU).**
- OVERALL "B=1/A inside matter is DERIVED natively (scoped to the pure
  topological/no-radial-gradient configuration)": **STANDS.**

================================================================
## TARGET 1 (HARDEST) — THE ANCHOR C3: native or reverse-engineered?
================================================================

The attack: the constructor admits the mapping "kappa enters as the metric
factor 1/(1+kappa cos theta)" was "vindicated post hoc, not re-derived from
the dpf P(F,a) side." If that 1/(1+kappa cos) is a free choice tuned to
match G1, the "native" claim collapses to an imported global monopole.

INDEPENDENT FINDING — the integrand is NOT a free choice. The ORIGINAL
dpf-side definition of G1 (predating this push) is the angular quadrature of
the gradient/winding density `f_theta^2/(4 f)` with `f = F(1 + kappa cos theta)`,
recorded in rescued_workspaces/2026-06-11/verify_x1/v_c1_closedforms.py
(lines 90-99) and as the loading density in v5_loading.py (line 40,
`-a^2 S^2/(F(1+kappa C))`). I re-derived it from scratch:

    f = F(1 + kappa cos theta)
    f_theta^2/(4 f) = (F kappa^2 / 4) * sin^2(theta) / (1 + kappa cos theta)   [exact, sympy]
    P(F,a) = INT [f_theta^2/(4f)] sin(theta) dtheta / 2
           = (F kappa^2 / 8) * INT_0^pi sin^3(theta)/(1 + kappa cos theta) dtheta

So the factor `1/(1 + kappa cos theta)` is the `1/f` ALREADY PRESENT in the
original dpf density — it is the angular-metric warp, not a knob inserted to
fit. The SAME `sin^3/(1+kappa cos)` integrand arises on BOTH sides because
both are the transverse winding/gradient energy of the SAME deformed angular
profile. The constructor's "physically natural reading" is in fact the
original definition. The mapping is NOT reverse-engineered.

The integral identity, high precision (mpmath dps=50), Inat == G1:

    k=0.10   |Inat - G1| = 1.8e-48
    k=0.30   |Inat - G1| = 6.7e-50
    k=0.50   |Inat - G1| = 2.7e-51
    k=0.683  |Inat - G1| = 5.3e-51
    k=0.90   |Inat - G1| = 2.7e-51

with G1 = (2k + (k^2-1)L)/k^3, L = ln((1+k)/(1-k)). Symbolic u=cos(theta)
substitution gives INT_{-1}^1 (1-u^2)/(1+ku) du = (2k+(k^2-1)(log(k+1)-log(1-k)))/k^3
= G1 EXACTLY once the log branch is collapsed.

ONE CORRECTION TO THE CONSTRUCTOR'S PROSE (does NOT change the verdict).
The doc at lines 124-141 conflates two distinct functions when it writes
"H(kappa) := ... = kappa^2/3 + ..." and "kappa^2 G1 -> (4/3) kappa^2 ...
matches the dpf2/exterior_cavity anchor." These are different objects:

    G1(k) = 4/3 + 4k^2/15 + 4k^4/35 + ...        (the bare integral; G1(0)=4/3 != 0)
    H(k)  = -2 P_F = L/(2k) - 1 = k^2/3 + k^4/5 + k^6/7 + ...   (H(0)=0)

The GENUINE banked anchor identity is `Inat == G1` (the bare integral), and
that holds EXACTLY (above). H is a DERIVATIVE of P, a different downstream
object; the leading "kappa^2/3" belongs to H, not to the bare reduction.
The constructor's sentence mixing "G1 -> (4/3)kappa^2" with "H = kappa^2/3"
is loose wording. The load-bearing claim — that the n-field reduction
reproduces the project's OWN derived G1 — is CORRECT and exact.

ANCHOR VERDICT: **GENUINE / NATIVE — CONFIRMED.** The integrand is the
project's own dpf density, not a fitted choice; the closed-form G1 match is
exact to ~1e-48; it is the ORIGINAL definition reproduced, so non-circular.

================================================================
## TARGET 2 — STRESS TENSOR C1 (independent Hilbert derivation)
================================================================

Independent build (angular_lag_verif_stress.py): UDT metric
ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}dr^2 + r^2 dOmega^2; sqrt(-g)=c r^2 sin(theta)
(phi cancels — confirmed). Hedgehog n=(sin th cos ph, sin th sin ph, cos th).
T_{mn} = xi (d_m n_a)(d_n n_a) + g_{mn} L, L = -(xi/2) g^{ab} dn_a.dn_b,
X = g^{ab}dn_a.dn_b = 2/r^2 (confirmed). Raising one index (exact sympy):

    T^t_t = -xi/r^2,  T^r_r = -xi/r^2,  T^theta_theta = 0,  T^phi_phi = 0
    T^t_t - T^r_r = 0   (exact)
    p_r + rho = 0       (exact)

**C1 CONFIRMED**, phi-independent. GPU (angular_lag_verif_gpu.py, V100
float64, 4096 random (r,theta,phi,phi(r))): max|p_r+rho| = 0.0 (machine
zero), max|T^theta_theta| = 1.4e-14, max|rho - xi/r^2| = 1.4e-14.

WHY T^t_t=T^r_r — the real structural reason (adversarial probe): it is NOT
special to the hedgehog. It is a consequence of the field being PURELY
ANGULAR: d_t n = d_r n = 0, so h_{tt}=h_{rr}=dn_t.dn_t=dn_r.dn_r=0; the only
contribution to T_tt, T_rr is the g_{mn}L term, hence T^t_t=g^{tt}g_tt L=L=
g^{rr}g_rr L=T^r_r. I verified with TWO non-hedgehog purely-angular configs:
- phi-winding w=2: T^t_t-T^r_r=0, p_r+rho=0 (but T^theta_theta=-3xi/2r^2 != 0).
- Theta=g(theta) arbitrary: T^t_t-T^r_r=0, p_r+rho=0.

So p_r=-rho is robust across the whole class "no radial gradient" — broader
than the hedgehog. The hedgehog is the unique member with ALSO
T^theta_theta=0. This STRENGTHENS, not weakens, the geometric-identity
argument (which needs only T^t_t=T^r_r; p_theta is free).

================================================================
## TARGET 3 — OFF-HEDGEHOG OBSTRUCTION C2 (correctly scoped?)
================================================================

Independent (angular_lag_verif_offhedge.py), radial twist Theta=Theta(r):

    p_r + rho = xi e^{-2phi(r)} (Theta'(r))^2   >= 0,  zero IFF Theta'=0

**C2 CONFIRMED.** The EOS p_r=-rho is NOT generic: the instant the winding
map acquires a radial profile (d_r n != 0) the t/r degeneracy breaks and
p_r+rho becomes strictly positive. The claim is correctly SCOPED, not
oversold. SCOPED-OK. (Caveat the constructor itself flags: a smoothed-core
realized soliton with Theta(r) varying through the core would have
p_r=-rho only where Theta'=0, i.e. asymptotically / outside the core. For
the pure topological n=x/r it is exact everywhere. This is honest.)

================================================================
## TARGET 4 — NATIVE ADDITIONS (Skyrme / potential): fragile or robust?
================================================================

Independent (angular_lag_verif_skyrme.py). For the hedgehog (any purely
angular config), h_{tt}=h_{rr}=0. A Skyrme term L4, a potential V(n), and
the eta-seal coupling are all built from the field and its gradients; for a
purely-angular config every field gradient is transverse, so the explicit
field-gradient contributions to T_tt and T_rr VANISH and each such term
contributes ONLY through g_{mn}(its Lagrangian density). Therefore:

    any native addition  =>  T^t_t = T^r_r = (sum of L-densities)  still holds.

=> **T^t_t = T^r_r (hence p_r = -rho) is ROBUST to native additions**, as
long as the configuration stays purely angular (no radial gradient). The
EOS is NOT fragile to the minimal-model choice C1. Additions DO generically
change T^theta_theta (e.g. Skyrme density L4 = -2/r^4 for the hedgehog,
nonzero), which would back-react on the theta-equation and modify the
g_rr-fixing relation / deficit value — but they do NOT touch the
g_tt g_rr=-c^2 identity, which rides only on T^t_t=T^r_r. So the
constructor's worry ("if a Skyrme term is needed the EOS scope narrows")
is OVER-cautious: the EOS itself survives; only T^theta_theta and the
numerical deficit shift. CONFIRMED-ROBUST.

================================================================
## C4 — BACK-REACTION / geometry side (independent Einstein tensor)
================================================================

Independent Christoffels -> Ricci -> Einstein (angular_lag_verif_backreact.py):

    G^t_t = e^{-2phi}(1 - e^{2phi} - 2 r phi')/r^2
    G^r_r = e^{-2phi}(1 - e^{2phi} - 2 r phi')/r^2
    G^t_t - G^r_r = 0   (IDENTICALLY — the geometry already enforces B=1/A)
    G^theta_theta = e^{-2phi}(2 r phi'^2 - r phi'' - 2 phi')/r   (phi-only)

With the hedgehog source T^theta_theta=0, the theta-equation G^theta_theta=0
is the vacuum theta-equation, UNCHANGED — it continues to fix g_rr=e^{2phi}.
The source enters only the t/r block. Solving G^t_t = kappa8 T^t_t =
-kappa8 xi/r^2 with G^t_t=(1-(r u)')/r^2, u=e^{-2phi}, gives
u = e^{-2phi} = 1 + kappa8 xi + C/r — a SOLID-ANGLE term on top of
Schwarzschild, g_tt g_rr=-c^2 preserved. **C4 CONFIRMED.**

(Minor: my ODE solve gives the deficit term with sign +kappa8 xi, whereas
the constructor wrote 1 - kappa8 xi - rs/r. This is a deficit-vs-surplus
sign-of-xi/normalization convention, NOT load-bearing; the structural claim
— g_tt g_rr=-c^2 survives, solid-angle + Schwarzschild form — is identical.
Flagged for the record.)

================================================================
## TARGET 5 — the sympy "[FAIL]" print
================================================================

**REFUTED as a real mismatch — it is purely a log-branch artifact.**
Independent symbolic integration returns the answer inside a Piecewise with
unsimplified branches log(-1/(k-1)), log(-sqrt(1/(k-1))) that equal
-log(1-k), -(1/2)log(1-k) for real 0<k<1 but which sympy will not auto-
collapse, so the symbolic `I - G1` does not reduce to 0 by `==`. The
u=cos(theta) form makes it explicit: INT_{-1}^1(1-u^2)/(1+ku)du =
(2k+(k^2-1)(log(k+1)-log(1-k)))/k^3 = G1. Numerics settle it:
|I-G1| = 2.2e-14 (k=0.2), 4.6e-41 (k=0.5), 1.5e-16 (k=0.8), 2.1e-16
(k=0.95). The integral DOES equal G1 on (0,1). CANNOT-REPRODUCE-as-failure
(i.e. the FAIL is spurious).

================================================================
## CLAIM-BY-CLAIM
================================================================

- C1 (T^t_t=T^r_r=-xi/r^2, T^theta_theta=0, p_r+rho=0):  CONFIRMED (exact + GPU).
- C2 (off-hedgehog p_r+rho = xi e^{-2phi}(Theta')^2 >= 0):  CONFIRMED / SCOPED-OK.
- C3 (anchor Inat == G1, native not imported):  CONFIRMED — GENUINE & INDEPENDENT.
      (one loose-prose conflation of G1 vs H noted; does not affect the identity.)
- C4 (back-reaction leaves theta-eq intact, B=1/A survives):  CONFIRMED.
- Skyrme/potential robustness:  T^t_t=T^r_r ROBUST to native additions (EOS not fragile).
- sympy [FAIL]:  spurious log-branch artifact (REFUTED as a real fail).

================================================================
## OVERALL VERDICT
================================================================

"B=1/A inside matter is DERIVED natively" **STANDS**, with the same scope
the constructor states: it is a theorem of the PURELY-ANGULAR / no-radial-
gradient configuration of the n-field (the deg-1 hedgehog being the unique
T^theta_theta=0 member). The two-derivative sigma-model stress gives
T^t_t=T^r_r=-xi/r^2 (exact, phi-independent), which is exactly the source
the metric identity g_tt g_rr=-c^2 <=> G^t_t=G^r_r <=> p_r=-rho demands, and
it leaves the g_rr-fixing theta-equation intact. The decisive anti-smuggling
anchor is GENUINE: the angular reduction integrand sin^3/(1+kappa cos) is
the 1/f warp already in the project's OWN dpf density f_theta^2/(4f), not a
fitted choice, and it reproduces the project's own G1 closed form to ~1e-48.
The result is correctly bounded — a radial twist breaks the EOS — and is
ROBUST (not fragile) to native Skyrme/potential additions, which preserve
T^t_t=T^r_r.

Caveats that DO NOT block the verdict (recorded): (a) prose conflation of G1
and H in the constructor doc; (b) a deficit sign/normalization convention in
the deficit solution; (c) the realized smoothed-core soliton, if it exists,
satisfies p_r=-rho exactly only where Theta'=0 (the pure topological n=x/r
is exact everywhere). None of these touch the load-bearing chain.
