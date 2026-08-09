# RA1 — the mu-ON mode problem + the wall's endpoint character (derivation notes)

Date 2026-08-08 | branch grok | agent: RA1 derivation (Fable) | MODE: OBSERVE
Contract: `PREREGISTRATION.md` (frozen, committed 438ef424). Parent MAP:
`../udt_roadA_mode_quantization_MAP_2026-08-08.md` (CP1–CP4 ruled; **CP4: mu-on leads**).
NAMING NOTE [R2-A4]: the directory token "muon" reads "mu-ON" (mixing on) — NOT the
particle; paths are referenced, so the name stands with this disambiguation.
Machine check: `derive_ra1.py` -> `run_output.txt`; **49/49 keys True** (46 at first
delivery; post-review: the vacuous K14 replaced [R1-A1] and the gap-line keys K30a–c added
[R1-A2/R2-A1]). Every boxed claim cites its KEY. STATUS: **verified LEAD** — R1
SUSTAINED-AMENDED + R2 AMENDED, ALL amendments applied in place; see the CONSOLIDATED
section (end). Same-session reviews; external bar travels. NOT committed (owner's gate).

**SCOPE BANNER (stamps every statement): the mixing h(r) is ON from the FIRST metric line
(F-MUOFF honored; the h=0 case appears ONLY in D5, derived as a limit). Equatorial 3D
declared slice / c=1 / lock+areal-anchor wall background A=(1-r/R_w)^n / frozen h-class
h0(1-r/R_w)^q incl. the q->0 and q<0 edges / probe = the metric's own scalar box (tagged
THEORY(metric-native probe), F-LAWHUNT) / real omega, integer m / SS9 lock-form ansatz tag
TRAVELS (D2 inheritance).** Symbols only (F-RETRO machine-discharged, KEY RA1_K28).

## 0. Ground (cited at source; every object used is re-derived here)

- D2 CONSOLIDATED (`../udt_bao_origin_D2_timelive_transfer_2026-08-08/DERIVATION_NOTES.md`):
  the stationary mixing realization g_t,psi = h(r) (SS3), its **SS9 lock-form ansatz tag —
  TRAVELS on everything below**; the dragging structure dpsi/dr = h/(AS); SS3's center-
  regularity requirement on h (load-bearing for the D2-variant fork in §4 below).
- D4 CONSOLIDATED (`../udt_bao_origin_D4_oscillating_2026-08-08/`): the observer phase-pin
  B2 (A(0)=1 => cos phi_0 = 0 — a PROFILE-oscillation statement; NOT assumed to carry over,
  see §4); the freeze/ride/compress wall trichotomy B7 (used only in D6/W2).
- O1/O2/O3 CONSOLIDATED (`../udt_xmax_O1_asymptote_2026-08-07/` etc.): the wall = asymptote;
  the measure table (proper finite iff n<2; optical finite iff n<1 — cross-checked at KEY
  RA1_K27); the natural variables.
- `../udt_mixing_channel_lane_2026-08-06/`: mu = the reciprocal-lock defect; here mu enters
  as the metric mixing channel h (the D2 realization), visible as g^{t,psi} = h/D != 0
  [KEY RA1_K2] — the inverse-block entry where mu lives.

## 1. Premise ledger (every declared slice; chose-or-derived tags)

| # | premise | tag |
|---|---|---|
| P-RA1-1 | background A=(1-r/R_w)^n, h=h0(1-r/R_w)^q, n,q symbolic | THEORY (frozen prereg §2; F-SHOP-CLASS); c0=1 as written in the prereg |
| P-RA1-2 | equatorial 3D chart (t,r,psi): ds^2 = -A dt^2 + dr^2/A + r^2 dpsi^2 + 2h dt dpsi | DECLARED slice (Category-A; D2 SS3 precedent). The prereg's literal 4D line-element (2h dt dpsi with no sin^2 theta) is AXIS-SINGULAR at the poles; the equatorial slice is the clean realization. Spherical generalization (h -> h(r) sin^2 theta, Kerr-like; generically non-separable) = NAMED INHERITANCE, not computed. Wall-classification robustness: near r=R_w every angular-weight difference is a bounded nonzero factor, and the sigma_eff classification is invariant under bounded factors (O2's squeeze pattern) — so D3 is insensitive to this slice; the CENTER indices are the slice-sensitive part (|m| here vs Legendre indices full-sphere), named |
| P-RA1-3 | probe = box psi = 0 of THIS metric | THEORY(metric-native probe) — a CHOICE of probe field, tagged; not "the" dynamics (F-LAWHUNT; W3 fenced) |
| P-RA1-4 | mode ansatz psi = R(r) e^{i(m psi - omega t)}, m integer (single-valuedness), omega REAL | DECLARED (observe-mode; complex-omega/QNM analysis out of scope, named) |
| P-RA1-5 | h0 > 0 WLOG | DERIVED convention: psi -> -psi flips h0's sign; chirality carried by sign(omega*m) |
| P-RA1-6 | weight = the omega^2 coefficient w = r^2/sqrt(AD); classification in L^2(w dr) | CHOSE (disclosed); made canonical by the exact isometry int |R|^2 w dr = int |v|^2 dx [KEY RA1_K9] — L^2(w) IS L^2(dx) of the Liouville variable |
| P-RA1-7 | endpoint classification performed at fixed real (m, omega) — the pencil caveat | DECLARED: omega enters both quadratically and linearly (frame-dragging pencil, as in Kerr); LP/LC is classified per fixed frozen coefficients; where the verdict is (m,omega)-dependent (the q<0 wedge) that dependence IS the reported result, per prereg §3 D3. EXTENDED [R1-A3]: the pencil's "mode set" is the root set {omega : omega^2 in spec(L_omega)}; since each eigenvalue branch of L_omega is analytic in omega, that set is DISCRETE unless a branch identically equals omega^2 (non-generic, no such branch exhibited) — the intrinsic-discreteness claims ride this analyticity premise, stated |
| P-RA1-8 | center behavior of h: the frozen class is NEAR-WALL; at r=0 it gives h(0)=h0 != 0, which VIOLATES D2 SS3's center-regularity. BOTH variants carried (§4): (a) SS3-regular completion (h -> 0 faster than the screen at r=0; cause = D2 SS3, banked ground) and (b) the literal class | FORK, disclosed (F-SHOP-CLASS: the completion's cause stated; nothing added to the near-wall class where D3 lives — D3 is endpoint-local at the wall and identical under both) |
| P-RA1-9 | SS9 lock-form ansatz (B=1/A time-live persistence) | INHERITED TAG from D2 — travels on every statement |
| P-RA1-10 | Weyl LP/LC machinery, Liouville transform, WKB, SL spectral theory | Category-A technique (MAP §3); criteria cited with applicability checked (§5) |

## 2. D1 — the exact radial equation (mixing in from the first line)

Metric (P-RA1-2, mixing ON): det g = -D/A with **D = A r^2 + h^2** [KEY RA1_K1]; the t-psi
block determinant is -D < 0 everywhere [RA1_K1b] — for q <= 0 the block stays LORENTZIAN at
the wall (D(R_w) = h0^2 > 0): the mixing removes the block's horizon-like degeneration even
as A -> 0. Inverse [RA1_K2]: g^{tt} = -r^2/D, **g^{t,psi} = h/D (mu's seat)**, g^{psi,psi}
= A/D, g^{rr} = A. Assembling box psi = 0 with the mode ansatz (machine-checked end to end
[RA1_K3]):

  **(W A R')' + W (r^2 omega^2 + 2 h omega m - A m^2)/D * R = 0,   W = sqrt(D/A) = sqrt(-g)**

Sturm–Liouville identification [RA1_K4a,b]: p = sqrt(A D), weight w = r^2/sqrt(A D), with
the EXACT identity **p * w = r^2 for every h** [RA1_K4c]. The pencil numerator completes to
the frame-dragging form NATIVELY [RA1_K6]:

  N = r^2 omega^2 + 2 h omega m - A m^2 = r^2 (omega - m Omega)^2 - m^2 D/r^2,
  **Omega(r) = -g_{t,psi}/g_{psi,psi} = -h/r^2**  (the dragging frequency).

Proper-variable form (d ell_p = dr/sqrt(A)) [RA1_K5]: (sqrt(D) R_ell)_ell + (N/sqrt(D)) R
= 0 — SL coefficients (p_ell, w_ell) = (sqrt(D), r^2/sqrt(D)), same invariant p*w = r^2.
**h-carriers (for D5)** [RA1_K7]: the 2 h omega m cross term of N; the h^2 term of D; Omega
itself. All vanish at h -> 0; nothing else carries h.

**The exact Liouville normal form (the classification instrument)** [RA1_K8, machine
identity at generic A, h, R]: with x = int_0^r r' dr'/sqrt(A D) and v = sqrt(r) R,

  **-v_xx + [ Q_c(x) + m^2 A/r^2 - 2 omega m h/r^2 ] v = omega^2 v,   Q_c = (sqrt r)_xx/sqrt r,**

and int |R|^2 w dr = int |v|^2 dx EXACTLY [RA1_K9]: the natural variable x is the
mixing-deformed generalization of O2's measures — at h=0, dx = dr/A (the OPTICAL row);
at bounded wall-mixing (q=0), dx ~ (R_w/h0) dr/sqrt(A) near the wall (PROPER-rate): the
mixing rotates the wall's natural measure from optical toward proper.

## 3. D3 (THE CORE) — the Weyl classification at the wall

**Method.** In the normal form the wall's character reduces to: (i) is x_wall = int r dr/
sqrt(AD) FINITE (endpoint at finite x) or INFINITE; (ii) how does the potential U = Q_c +
m^2 A/r^2 - 2 omega m h/r^2 behave there. Criteria used (cited, Category-A): Weyl's
alternative (Coddington–Levinson ch. 9); the inverse-square test at a finite endpoint
(Reed–Simon II Thm X.10): U >= (3/4)/d^2 near the endpoint => LIMIT-POINT; U <= c/d^2 with
c < 3/4 => LIMIT-CIRCLE (d = distance to endpoint). Applicability: U real, continuous on a
punctured neighborhood — holds on the frozen class. At an infinite endpoint with U -> const:
LIMIT-POINT (classical). Both solutions' L^2(w)-membership is tested in x via the exact
isometry [RA1_K9] — no weight ambiguity.

**Near-wall asymptotics (u = 1 - r/R_w -> 0+)** [RA1_K10–K12]: with D ~ R_w^2 u^n + h0^2
u^{2q}, p = sqrt(AD) ~ u^{sigma_eff}, w ~ u^{-sigma_eff} where

  **sigma_eff(n, q; h0) = (n + min(n, 2q))/2   (h0 != 0);   sigma_eff = n at h0 = 0.**

dx ~ u^{-sigma_eff} du, so x_wall is finite iff **sigma_eff < 1** [RA1_K13a–c, decidable
three-key restatement]. For q > 0 every U-term vanishes at the wall and is SUBCRITICAL in
the inverse-square sense — the conjugation term's s-exponent is (2 sigma-1)/(1-sigma) > -2
identically [RA1_K15], the dragging (u^q) and centrifugal (u^n) terms map to positive
s-powers [RA1_K14] — so for q >= 0 the classification depends on (n, q) ONLY, and near the
wall the equation is exactly free, -v_xx = omega^2 v: solutions e^{+-i omega x}.

**THE (n,q)-PLANE MAP (h0 != 0; witnesses machine-checked per region [RA1_K16, K17a–c]):**

| region | classification | spectrum character (this end) |
|---|---|---|
| **R1: n < 1** (any q) | LIMIT-CIRCLE (sigma_eff < 1 always) | a wall BC exists/is required (one extra datum); with §4's observer end: PURELY DISCRETE — ladder possible. Same verdict mu-off (mixing-preserved) |
| **R2: 1 <= n < 2, q < (2-n)/2** | LIMIT-CIRCLE — **MIXING-CREATED** (mu-off this whole band is limit-point) | as R1: ladder possible, one wall datum required. Includes the q=0 bounded edge (criterion there: n < 2 = O2's PROPER-finiteness) and n=1 with q < 1/2 |
| **R2b [post-review, R1-A2/R2-A1]: the line n = 2, q < 0** | LIMIT-CIRCLE — **MIXING-CREATED** (sigma_eff = 1 + q < 1 [RA1_K30a]; dragging exponent e = -1 exactly, subcritical [RA1_K30b]; mu-off n=2 is LP) | ladder possible, one wall datum; glues R2's band continuously to R4/R5. Both reviews found this omission independently; note it ran AGAINST the ladder-favorable reading (anti-curation) |
| **R2': 1 <= n < 2, q >= (2-n)/2; and n >= 2, q > 0** | LIMIT-POINT (sigma_eff >= 1; boundary lines log-divergent [RA1_K13c]) | x_wall = infinity, U -> 0: essential spectrum = [0, infinity) in omega^2 — every real omega is CONTINUUM; no real-frequency discrete modes (omega^2 < 0 excluded for real omega; center end contributes no essential spectrum, §4) |
| **R3: n >= 2, q = 0** | LIMIT-POINT | continuum with a FRAME-DRAGGING SHIFTED edge: U(inf) = -2 omega m h0/R_w^2, continuum condition omega^2 + 2 omega m h0/R_w^2 >= 0, edge roots {0, -2 m h0/R_w^2} [RA1_K24] — asymmetric in sign(omega m): superradiance-adjacent fingerprint |
| **R4: n > 2, q < 2-n** (deep divergent mixing) | LIMIT-CIRCLE (dragging subcritical, e = 2q/(2-n-2q) > -2 [RA1_K17c]) | ladder possible with a wall datum |
| **R5 THE CHIRAL WEDGE: n > 2, 2-n < q < (2-n)/2** | **SIGN-SPLIT** [RA1_K17b,c; K19a–c]: dragging term supercritical (e < -2). m = 0: LC. m != 0: omega m h0 > 0 (co-rotating) => attractive divergence => LC (both WKB solutions L^2 [RA1_K19b]); omega m h0 < 0 (counter-rotating) => repulsive => LP (growing branch not L^2 [RA1_K19c]) | co-rotating: BC-dependent discrete (fall-to-center type, extension-dependent, unbounded-below caution); counter-rotating: LP with U -> +infinity at FINITE x_wall = CONFINING — **purely discrete WITHOUT any extra BC datum (natural quantization) (counter-rotating channel of the deep-mixing wedge n>2, 2-n<q<(2-n)/2 ONLY — divergent h at the wall; scalar-probe W1, equatorial slice, fixed-(m,omega) pencil scope)** [R2-A2]; sigma_ess EMPTY, bounded below (R1's independent essential-spectrum derivation); rides P-RA1-7's analyticity premise [R1-A3]; the mode set splits by chirality |
| **R6 the critical line: q = 2-n, n > 2** | coefficient-critical: the dragging term contributes EXACTLY c_crit/s^2 with **c_crit = -8 omega m R_w^2/(h0 (n-2)^2)** [RA1_K18a–c]; LC iff c_crit < 3/4 | the classification depends on the MAGNITUDES (m, omega, h0, R_w) — the mixing's sharpest fingerprint: the wall's character is set by how fast and which way the mode co-rotates with the drag. CAUTION [R2-A5], matching R5: for c_crit strongly negative (co-rotating, c_crit << -1/4) the LC verdict is of fall-to-center type — discrete per self-adjoint extension but EXTENSION-DEPENDENT and unbounded below |
| **R-ray [post-review, R2-A1]: the boundary ray q = (2-n)/2, n > 2** | sigma_eff = 1 EXACTLY [RA1_K30c] — x_wall log-divergent (infinite endpoint); the dragging term ~ u^q grows EXPONENTIALLY in x there | m = 0: LP continuum. m != 0 (chirality persists at infinity): counter-rotating => confining => LP purely discrete; co-rotating => attractive-exponential => LIMIT-CIRCLE at infinity (int |U|^{-1/2} dx < oo criterion, cited; classic -e^{2ax} example). Consolidation-level classification: the exponent facts are machine-keyed, the endpoint criteria cited |

**The mixing's fingerprint on the classification, explicit (prereg D3 demand):** (i) h0
acts as a SWITCH (h0 = 0 vs != 0) selecting sigma_eff = n vs (n + min(n,2q))/2 — magnitude-
independent for q > 0; (ii) m and omega are classification-inert for q >= 0 [RA1_K14] but
DECIDE the verdict in the wedge/critical zone q < 0 via sign(omega m h0) and c_crit — a
chirality structure with no mu-off counterpart; (iii) at q = 0 the essential-spectrum edge
shifts by the dragging (R3). The pencil caveat (P-RA1-7) stamps (ii)–(iii).

## 4. D2 — the observer end r -> 0 (derived, not inherited)

**The D4 phase-pin does NOT carry over as a phase condition** — it was a statement about
the PROFILE oscillation's phase (cos phi_0 = 0 from A(0)=1). The probe's own observer-end
structure, derived fresh, forks on P-RA1-8:

**(a) SS3-regular variant (h -> 0 faster than the screen at the center; cause = D2 SS3):**
near r=0: A -> 1 (the banked anchor), D -> r^2, p -> r, w -> r. Frobenius indicial equation
a^2 - m^2 = 0, indices a = +-|m| [RA1_K20a,b]. In normal form U -> (m^2 - 1/4)/x^2 (the
conjugation contributes exactly -1/4 [RA1_K20c]): |m| >= 1 => coefficient >= 3/4 =>
LIMIT-POINT at the center — the regular solution r^{|m|} is selected AUTOMATICALLY; m = 0
=> coefficient -1/4, marginal LIMIT-CIRCLE — the BC is axis regularity (bounded, no log).
Either way the observer end supplies EXACTLY ONE admissibility condition — the same
STRUCTURAL role as D4's pin (half the boundary structure), different content: an axis-
regularity selection, not a phase pin. The center is NONOSCILLATORY for every omega
(coefficient >= -1/4), so it contributes NO essential spectrum: the spectrum's character is
decided at the WALL (as the MAP framed).

**(b) The literal frozen class at the center (h(0) = h0 != 0):** p(0) = h0 != 0 [RA1_K21a]
— r = 0 becomes a REGULAR point of the ODE; the mixing REMOVES the centrifugal barrier
(g^{psi,psi} = A/D -> 1/h0^2, finite [RA1_K21b]). No regularity selection is forced by the
equation; but the manifold carries a spinning-string/NUT-like AXIS DEFECT (g_{t,psi} != 0
on a degenerating circle): the observer condition would need a posited axis datum. This is
the near-wall class's center pathology, disclosed (P-RA1-8); it does not touch D3 (endpoint-
local). The D2-inherited variant (a) is the realization consistent with banked ground.

## 5. D4 — the ladder's structure where it exists (symbols only)

In the discrete regions (R1, R2 with the wall datum; R5-counter-rotating with NO extra
datum) both endpoints confine within FINITE x-length x_w = int_0^{R_w} r dr/sqrt(A D):

- **Quantization form:** the wall BC (LC regions: a self-adjoint-extension angle theta_w;
  R5-counter: intrinsic) + the center condition => a discrete set omega_k(m). Asymptotics
  by Weyl counting on the free interior (-v_xx ~ omega^2 v): N(omega) ~ omega x_w/pi, i.e.
  **asymptotic level spacing Delta omega -> pi/x_w** — the finite MIXING-DEFORMED length
  x_w replaces O2's optical length (mu-off, R1: x_w = optical length exactly; the ladder
  rides the OPTICAL measure — connecting to O2's row structure; the mu-on x_w interpolates
  optical -> proper as the mixing stiffens).
- **Mixing shortens the cavity:** r/sqrt(AD) <= 1/A exactly (difference h^2/(A^2 D) >= 0
  [RA1_K23]) => x_w(h0) <= x_opt, monotone: turning the mixing up WIDENS the asymptotic
  spacing. In R2 the mu-off x_opt is INFINITE while x_w(h0 != 0) is finite: the spacing
  pi/x_w -> 0 as h0 -> 0 — the mixing-created ladder DENSIFIES into the mu-off continuum
  (a continuous deformation, not a jump).
- **The m-fingerprint (the mixing's ladder signature):** first-order pencil perturbation
  gives delta omega = -m <h/r^2>_k = +m <Omega>_k [RA1_K22]:
  **omega_k(m) - omega_k(-m) = 2 m <Omega>_k** — a Zeeman-like ROTATIONAL SPLITTING, linear
  in h0: modes are dragged by the mode-averaged dragging frequency; the +-m degeneracy of
  the mu-off ladder is broken. Spacing pi/x_w is m-independent at leading order; the
  m-dependence sits in the offset (and in the wedge, in the classification itself).

## 6. D5 — the mu-off limit h -> 0, DERIVED from D1–D4 (CP4-compliant order)

Limits [RA1_K25a–c, K26, K27]: p -> A r, w -> r/A, N -> r^2 omega^2 - A m^2, dx -> dr/A
(optical), sigma_eff -> n. **Classification h=0: LC at the wall iff n < 1** — exactly O2's
OPTICAL-finiteness criterion [RA1_K27].

| structure | mu-on | mu-off | verdict |
|---|---|---|---|
| R1 (n<1) ladder | LC, spacing pi/x_w(h0) | LC, spacing pi/x_opt | SURVIVES; mixing only deforms spacing [RA1_K23] |
| R2 (1<=n<2, q<(2-n)/2) ladder | LC | LP (continuum) | **MIXING-CREATED**; densifies continuously into the continuum as h0 -> 0 |
| chirality wedge R5/R6 + sign-split + c_crit | present | absent | **MIXING-CREATED** (no counterpart) |
| Zeeman splitting 2m<Omega> | present | zero (+-m degenerate) | **MIXING-CREATED** |
| q=0 shifted continuum edge (R3) | present | edge at 0 | **MIXING-CREATED** |
| n >= 2 (q>0) continuum | LP | LP | mixing-robust continuum |

**The mixing's role stated plainly: the mixing never destroys a discrete region — it opens
new ones (within the frozen power-law class, equatorial W1 scope)** [R2-A2 stamp; R1 proved
it as a theorem, not just unfalsified: sigma_eff <= n < 1 for all q when n < 1, and no
wedge can enter n < 1 — plus a 32-point counterexample grid, none found]. It converts the
band 1 <= n <= 2 (which contains the O2 finite-proper family's upper half; the n=2 edge via
R2b) from continuum to ladder-capable, splits the wall's character by chirality deep in the
divergent-mixing zone, and stamps any ladder with a rotational m-splitting.

## 7. D6 (RA3) — the W2 kinematic cross-check (dynamics-free)

Question: does the wall's asymptotic structure impose a SECOND condition on the D4 profile-
oscillation wavelength lambda as PROFILE data (the observer pin being the first)? From the
banked D4 trichotomy (B7, cited): SUBCRITICAL cells (nm < 1) — the oscillation FREEZES,
finitely many cycles, admissibility imposes no wall condition; CRITICAL (nm = 1) — infinite
log-periodic cycles, the constraint is an amplitude threshold on epsilon, none on lambda;
SUPERCRITICAL — caustics restructure z(r) but D4-ADMITTED stands, no lambda condition.
**W2 verdict: the wall's asymptote supplies NO second kinematic condition — lambda remains
a one-parameter continuum of free profile data with only the observer pin.**
**Agreement with W1: CONSISTENT, and sharper.** W1 says discreteness arises only where the
wall is LC — and LC means a boundary condition EXISTS/IS REQUIRED but its selection is one
extra datum the geometry itself does not supply (except R5-counter-rotating, where the
mixing's confinement quantizes intrinsically). W2 says the kinematics supplies no such
datum. Read together: on the banked background the discreteness question lands exactly on
ONE missing boundary datum at the wall — with the single derived exception that a
counter-rotating mode in the deep-mixing wedge needs NO datum at all: there the mu-on
geometry **quantizes BY ITSELF (counter-rotating channel of the deep-mixing wedge n>2,
2-n<q<(2-n)/2 ONLY — divergent h at the wall; scalar-probe W1, equatorial slice,
fixed-(m,omega) pencil scope)** [R2-A2]. No tension found.

## 8. Falsifier discharge (prereg §4)

- **F-MUOFF (primary):** the mixing is in the FIRST metric line of the script; every D1–D4
  object is derived with h symbolic and nonzero; h = 0 appears ONLY in the S10/D5 block (and
  K7's h-carrier IDENTIFICATION, after the mu-on system is posed), as a derived limit. NO
  load-bearing step was performed at h = 0 before the mu-on system was posed. DOES NOT FIRE.
  HONESTY NOTE [R2-A3]: **K29 is a necessary structural witness only (a presence-of-h
  vocabulary check) — it could not catch a patched-in h; the ORDER claim is discharged by
  script-construction inspection (R2 performed it, clean) plus both reviews, not by the key
  alone.**
- **F-RETRO:** symbols only; no Planck numbers, no fitted n, no observational values; the
  float-atom scan over the audited expressions is clean [RA1_K28]. Region witnesses are
  small rationals chosen for region COVERAGE (the O2 witness pattern), not fitted values.
- **F-TEMPLATE:** posed as endpoint-character observation; all landings carried first-class
  — and the landing IS the mixed one (no peak-making framing anywhere).
- **F-SHOP-CLASS:** the h-class used exactly as frozen (h0 u^q + the q->0 and q<0 edges);
  the ONE addition is the center-completion fork (P-RA1-8), cause stated = D2 SS3's banked
  center-regularity requirement; it touches only §4(a)-vs-(b), never D3.
- **F-LAWHUNT:** box psi tagged THEORY(metric-native probe) throughout; no action/law
  posited; W3 untouched.
- **F-SCOPE:** no CMB contact, no positions/ratios, no heights/amplitudes; RA2 remains
  gated.
- Anti-hang: single foreground process, pure sympy CPU, 480 s cap, runtime ~1 min; no
  monitors. **Decidable-form restatements (disclosed, per the arc precedent):** first run
  46 keys with 4 False, ALL form/decidability issues, none a claim change: K5 compared with
  a wrong multiplier (sqrt(A)/W instead of the correct sqrt(A) — fixed and re-derived); K18a/
  K18c blocked on powsimp because (n-2)'s sign was undeclared (restated with n = 2 + nu,
  nu > 0); K24 compared solve's roots as an ordered list (restated as a set).
  **FIFTH restatement, review-caught [R1-A1]: the first-run K14 was VACUOUS** — an
  identically-zero tautology that verified nothing about dragging subcriticality (the
  underlying claim is true and was independently verified by R1); replaced by a real
  positive-exponent check. Key-evidence weight notes [R1-A4]: K18b checks the LEADING-order
  integrand only (the exact c_crit was recomputed by R1 from the unapproximated integrand —
  correct); K22 machine-checks the final linear solve only (the perturbation formula itself
  was independently confirmed by R1's pencil solve).
- POST-REVIEW script touch (disclosed): K14 replaced [R1-A1]; the S7b block (K30a–c: the
  n=2, q<0 line + the boundary ray) added [R1-A2/R2-A1]. Re-run fresh: **49/49 True**. No
  pre-existing claim's check was altered.

## 9. LANDED OUTCOME (prereg §5)

**RA1-MIXED(by region) — the expected rich outcome, now with the map drawn.** On the mu-on
wall background the probe's mode problem has: a LIMIT-CIRCLE (ladder-possible) territory —
the FULL union [R1-A2/R2-A1 completion] **{n < 1, any q} u {1 <= n < 2, q < (2-n)/2} u
{n = 2, q < 0} u {n > 2, q < 2-n}** — everything except the n < 1 slab MIXING-CREATED; a
LIMIT-POINT continuum territory {sigma_eff >= 1, q >= (2-n)/2} incl. all n >= 2 with q > 0
(with a dragging-shifted continuum edge at q = 0, and the boundary ray q = (2-n)/2, n > 2
classified per the R-ray row); and a CHIRAL WEDGE {n > 2, 2-n < q < (2-n)/2} where the
wall's character is decided by sign(omega m h0) — counter-rotating modes are **quantized
INTRINSICALLY (no boundary datum) (counter-rotating channel of the deep-mixing wedge n>2,
2-n<q<(2-n)/2 ONLY — divergent h at the wall; scalar-probe W1, equatorial slice,
fixed-(m,omega) pencil scope; rides P-RA1-7's analyticity premise)** [R2-A2/R1-A3],
co-rotating ones are LC — with the critical-line coefficient c_crit = -8 omega m R_w^2/
(h0 (n-2)^2) vs 3/4 as the exact (m, omega, h0)-dependent classification law (R6
unbounded-below caution attached [R2-A5]). Every ladder carries the mixing's Zeeman-like
rotational splitting omega_k(m) - omega_k(-m) = 2 m <Omega>_k and Weyl spacing pi/x_w on
the mixing-shortened length x_w <= x_opt. In LC regions with the observer end (one derived
admissibility condition — an axis-regularity selection, NOT the D4 phase-pin, which does
not carry over) the spectrum is PURELY DISCRETE once the one wall datum is chosen; in LP
regions it is purely continuum for real omega. The mu-off limit (D5, derived last) keeps
only {n < 1} discrete-capable — everything else the wall offers is the mixing's doing.
W2 cross-check: consistent; the missing ingredient is exactly one wall datum, which the
kinematics does not supply and which, in the wedge's counter-rotating channel alone, the
mu-on geometry supplies itself (scope as stamped above).

Check count: **49/49 machine keys True** (`run_output.txt`). Deliverables D1–D6 all land.

STATUS: see CONSOLIDATED below (both reviews in; verified LEAD).

— RA1 derivation agent, 2026-08-08.

## CONSOLIDATED (2026-08-08; post-review; supersedes §9's pre-review status)

**Reviews (both in, same session):**
- `ADVERSARIAL_REVIEW_1_recompute.md` — R1, blind full recompute (written BEFORE opening
  `derive_ra1.py`; 32/32 own keys, `review1_recompute.py`/`review1_output.txt`) +
  completeness attack: **SUSTAINED-AMENDED**. Region map re-derived by R1's own classifier,
  17/17 agreement; the CHIRAL WEDGE survived its hardest attack — **the essential spectrum
  of the counter-rotating channel independently derived EMPTY (both ends nonoscillatory for
  every lambda, finite interval): genuinely purely discrete AND bounded below** — and
  c_crit recomputed EXACTLY from the unapproximated integrand. No kill found.
- `ADVERSARIAL_REVIEW_2_scope.md` — R2, falsifier/scope/ledger adjudication: **AMENDED**;
  **NO falsifier fires** (F-MUOFF, F-RETRO incl. the clean freeze timeline 438ef424 with no
  retro-edit, F-TEMPLATE, F-SHOP-CLASS, F-LAWHUNT all adjudicated DOES-NOT-FIRE); the one
  region omission ran AGAINST the ladder-favorable reading — anti-curation, honest.

**Amendments applied in place (ALL of them):** R1-A1 = K14 vacuous key disclosed as a fifth
restatement and REPLACED by a real check (§8, in-script); R1-A2/R2-A1 = the region map
COMPLETED — the R2b line {n=2, q<0} (LC, mixing-created [RA1_K30a,b]) and the boundary ray
q=(2-n)/2, n>2 (R-ray row [RA1_K30c]) added to §3 and the §9 union; R1-A3 = the pencil-
analyticity step made explicit (P-RA1-7 extended; stamped on the wedge rows); R1-A4 =
K18b leading-order-only and K22 final-solve-only evidence notes (§8); R2-A2 = inline scope
stamps inside every quotable bolded span (§6 headline, §7, §3 R5, §9); R2-A3 = K29's
thinness stated, F-MUOFF discharge rests on script-order inspection + reviews (§8);
R2-A4 = the mu-ON naming disambiguation (header); R2-A5 = the R6 unbounded-below caution
(§3). Post-review script touch disclosed; re-run fresh **49/49**.

**Strengthenings the reviews delivered:** (1) the wedge's intrinsic quantization is now
backed by an independent essential-spectrum derivation (sigma_ess EMPTY, bounded below —
bound-state-like, not continuum-above-threshold); (2) x = the mixing-deformed O2 measure is
MACHINE-EXACT (h=0: optical; q=0 wall rate: proper — R1's independent check); (3) the
mu-off LC criterion n<1 = O2's optical-finiteness is an EXACT coincidence, recomputed;
(4) **"the mixing never destroys a discrete region" is now PROVEN within the frozen class**
(R1's theorem: sigma_eff <= n < 1 for all q when n < 1, no wedge enters n < 1; 32-point
counterexample grid empty), not merely unfalsified.

**THE COMPLETED MAP (headline form; scope banner rides):** LC/ladder-possible = {n < 1,
any q} u {1 <= n < 2, q < (2-n)/2} u {n = 2, q < 0} u {n > 2, q < 2-n} — all but the first
slab MIXING-CREATED. LP/continuum = {q >= (2-n)/2, sigma_eff >= 1} (q=0, n>=2: dragging-
shifted edge; the n>2 boundary ray chirality-split per R-ray). CHIRAL WEDGE {n > 2,
2-n < q < (2-n)/2}: counter-rotating = intrinsically discrete (no wall datum; scope
stamped), co-rotating = LC (fall-to-center caution); critical line c_crit = -8 omega m
R_w^2/(h0 (n-2)^2) vs 3/4. Ladders carry the Zeeman splitting 2m<Omega>_k and spacing
pi/x_w, x_w <= x_opt. Mu-off keeps only {n < 1}.

**LANDING: RA1-MIXED(by region)** with the full LC union above; D1–D6 all land; **49/49
machine keys** + R1's independent 32/32.

**Four-check line:** pre-registered (frozen contract, committed 438ef424 BEFORE derivation;
timeline machine-verified by R2) — YES; full-space or bounded-slice-justified — bounded
DECLARED slices, every simplification ledgered (P-RA1-1..10; equatorial slice with D3-
insensitivity argued; the (n,q) plane covered incl. edges, gaps closed by review) — YES;
blind-verified on the load-bearing premises — YES (R1 zero-context full recompute incl.
the essential-spectrum attack; R2 falsifier adjudication + hand recomputes); forced
premises audited — YES (P-RA1-7 pencil premise extended and stamped; P-RA1-8 center fork;
K29/K14 evidence-weight honesty applied). Ceiling honored: **verified LEAD** (same-session
reviews; the external replication bar travels).

**Inheritance list (what RA1 does NOT settle):** (1) the full-sphere non-separable
realization (named inheritance, P-RA1-2); (2) the wall BC datum in plain-LC regions — one
missing boundary datum, supplied natively ONLY in the wedge's counter-rotating channel;
(3) complex-omega/QNM analysis (P-RA1-4); (4) the axis datum for the literal-class center
variant (§4b); (5) W3/dynamics — the probe is a tagged choice (F-LAWHUNT); (6) RA2 = the
projection through the banked dictionaries + the MAP-§4 comparison discipline (blind
ladder-ratio structure vs the pre-stated non-integer measured ratios; positions/ratios
only) — **GATED on Charles's go**.

— consolidation by the RA1 derivation agent, 2026-08-08. NOT committed (owner's gate).
