# Depth-angular MIXING channel — first OBSERVE (exact sympy, float-free)

Date 2026-08-06 | branch grok | MODE OBSERVE (MIX-GAUGE & COUPLING-INERT get equal care;
no discreteness/mass aim — F-TARGET). Contract: `MAP_AND_PREREG.md` (frozen).
Ground (read, no code imported): `udt_ceff_profile_binding_test_2026-08-06/DERIVATION_NOTES.md`
sec.4 (mixing witness delta_t=0.648...!=log2); `udt_complete_pair_phi_orchestra_audit_2026-08-05/
EXACT_DERIVATION.md` (C_A=A^dag A, A^dag=g_p^-1 A^T g_q; conjugacy data endpoint-frame INVARIANT;
delta_t=-(1/2)log lambda_timelike). Scripts: `mixing_gate.py`, `mixing_gate2.py`,
`mixing_closure.py`, `mixing_transmit2.py` (all machine-confirmed).

## MODEL (as specified)
3 slots 0=clock(timelike), 1=x(radial), 2=y(screen); eta=diag(-1,1,1).
ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}dx^2 + R^2 dy^2 (reciprocal-lock + one live screen).
Comparison arrow (upper-unitriangular clock->screen mixing mu in the 0-2 block):
```
A = [[1/r, 0, mu],
     [0,   r, 0 ],
     [0,   0, s ]]      r=e^{delta}=e^{phi_q-phi_p}>0,  s=R_q/R_p>0,  mu real.
```
Strain C_A = A^dag A, A^dag = eta^{-1} A^T eta.

## Q0 / GATE (F-GAUGE) — is mu a non-gauge invariant?  VERDICT: INVARIANT (non-gauge).
```
C_A = [[1/r^2, 0,  mu/r     ],
       [0,     r^2, 0       ],
       [-mu/r, 0,  s^2 - mu^2]]
charpoly = (r^2 - L)*( L^2 - [(1 - mu^2 r^2 + r^2 s^2)/r^2] L + s^2 )
Trace(C) = r^2 + 1/r^2 + s^2 - mu^2      Inv2(C) = 1 + r^2 s^2 + s^2/r^2 - mu^2 r^2
Det(C)   = s^2   (mu-independent; mu is unipotent -> volume-preserving)
```
- mu enters the char-poly COEFFICIENTS (trace, Inv2) and hence the EIGENVALUES — not merely
  the eigenvectors. (Timelike eigenvalue depends on mu: the ground witness delta_t=0.648.)
- Endpoint frame changes act by A -> L_q A L_p^{-1}; since Lorentz L^dag=L^{-1}, the q-frame
  cancels and C_A -> L_p C_A L_p^{-1} (conjugation). Char-poly is therefore frame-INVARIANT.
  CONFIRMED explicitly: an O(1,2) boost L_p in the 0-2 plane (L_p^T eta L_p = eta) leaves the
  char-poly unchanged, and the char-poly STILL CONTAINS mu. => no endpoint frame change can
  set mu to 0 without changing the invariant spectrum. mu is NOT Lorentz-gauge.
- Reciprocal-lock invariant: lambda_timelike * lambda_radial (radial = r^2, the slot-1
  eigenline eta-orthogonal to the mixing plane) = 1 IFF mu = 0 (solve: lambda_time=1/r^2 <=> mu=0,
  exact). So mu is exactly the frame-invariant DEFECT of the reciprocal lock.
- Regular stratum: block discriminant (1/r^2+s^2-mu^2)^2 - 4 s^2/r^2 >= 0, i.e. real depth for
  mu<|1/r-s| or mu>1/r+s; ELLIPTIC (complex, no real depth) in between.

GATE PASSED: mu is a genuine non-gauge invariant. Lane proceeds to Q1/Q2. (NOT MIX-GAUGE.)

## Q1 — does the coupling TRANSMIT an angular consistency constraint to the DEPTH?

### (a) Kinematic transmit (eigenvalue level): YES.
With mu!=0 the timelike eigenvalue lambda_time = [(1/r^2+s^2-mu^2) + sqrt(disc)]/2 depends on
BOTH the screen ratio s(=R) AND mu. The depth delta_t=-(1/2)log lambda_time is no longer the
pure boost eigenvalue 1/r^2: the screen sector enters it through the mixing.

### (b) Group law & C2 closure (endpoint-descent of the depth cocycle).
The arrows close under composition:
```
A(a1,s1,m1) A(a2,s2,m2) = A( a1 a2,  s1 s2,  a1 m2 + m1 s2 )     (a=1/r=e^{-delta})
```
Mixing cocycle condition (groupoid consistency of a p->q assignment):
```
m(p,r) = a(p,q) m(q,r) + m(p,q) s(q,r).
```
- A CONSTANT mixing m=mu is INCONSISTENT: it requires a(p,q)+s(q,r)=1 (i.e. e^{-Dphi}+R-ratio=1),
  impossible for independent p,q,r unless mu=0. A nonzero mixing must be the forced cocycle form
  m(p,q) = a(p,q) k(q) - s(p,q) k(p)  (observer field k) — mixing is inseparably tied to (phi,R).
- Depth additivity DEFECT: delta_t(A1 A2) - delta_t(A1) - delta_t(A2) = 0 at m=0 (exact), but
  != 0 for m!=0 (rational witness ~ 0.0121). So the invariant mixing BREAKS endpoint-descent:
  the depth acquires loop holonomy — it is no longer a pure potential difference.
- LOOP OBSTRUCTION vs depth profile (the transmit test). Triangle p,q,r with FREE phi_i, R_i and
  the forced coboundary mixing scaled by t; loop depth-sum expanded in t:
```
O(t^0) = 0   (mixing-off: pure depth CLOSES for ALL phi — phi unconstrained at mu=0)
O(t^1) = 0   (linear order in mixing does not obstruct)
O(t^2) = f(phi_P,phi_Q,phi_R, R_i, k_i) != 0,  with d/dphi_i (O(t^2)) != 0 (exact, nonzero).
```
=> At mu!=0 the C2 closure obstruction is a nonzero function OF THE DEPTH PROFILE phi. Demanding
endpoint-descent (loop=0) now imposes a relation involving phi that was ABSENT at mu=0. The
angular/mixing consistency condition TRANSMITS to the depth. (Onset is O(mu^2), matching the
one-form's blindness to mixing at first order — the effect lives in the non-abelian curvature.)

HONEST CAVEAT (F-STEER): the closure relation couples phi to the FREE mixing field k(observer);
it does not by itself UNIQUELY pin phi(x) (tune k for any phi). It is a genuine transmit ROUTE
(the depth now feels an angular constraint), not yet a closed depth-LAW. Also finite mixing
generically pushes a loop leg off the regular stratum (elliptic — no real depth).

## Q2 — does closure SELECT / QUANTIZE mu?  VERDICT: NO.
Pure mixing holonomy (net depth & screen trivial, residual m0): C-block trace=2-m0^2, det=1,
disc=m0^2(m0^2-4). For 0<|m0|<2 eigenvalues are complex with |lambda|=1 => an ELLIPTIC ROTATION,
angle cos(theta)=1-m0^2/2 — CONTINUOUS in m0. Hyperbolic for |m0|>2. Constant mu is inconsistent;
closure admits a CONTINUOUS coboundary family (parameter k). No discrete set is forced. mu is
NOT quantized/selected by consistency (no discreteness seed here; not hunted — F-TARGET).

## LANDED OUTCOME CLASS
COUPLING-TRANSMITS (with caveat): mu is a non-gauge invariant (gate passed); the depth eigenvalue
depends on mu and R, and the C2 closure obstruction depends on the depth profile phi (absent at
mu=0) — an angular consistency constraint now reaches the depth. It is a ROUTE, not a completed
profile-law (the constraint entangles phi with the free mixing field k), and mu is NOT quantized.
Single load-bearing step: the O(t^2) loop depth-sum has nonzero d/dphi_i (exact) while O(t^0)=0.
Not committed. Two adversarial reviews owed before any banking.

## CONSOLIDATED (2026-08-06): GATE holds, TRANSMIT refuted -> COUPLING-INERT (both reviews concur)

Files: ADVERSARIAL_REVIEW_1_gate_transmit.md (NARROW: gate holds, transmit does not),
ADVERSARIAL_REVIEW_2_law_route.md (ENTANGLES-ONLY -> COUPLING-INERT-IN-EFFECT). Both independent.

**GATE — CONFIRMED non-gauge (solid).** mu enters the frame-invariant char-poly coefficients;
lambda_time*lambda_radial = 1 IFF mu=0 -> mu is the invariant DEFECT of the reciprocal lock. R1
attacked with the FULL O(1,2) at both endpoints incl. the parabolic/null rotation the probe skipped;
conjugation fixes the spectrum; no orthonormal frame removes mu. Real first-class invariant.

**TRANSMIT — REFUTED.** R2 re-derived the O(mu^2) obstruction with the observer field k SYMBOLIC
(driver evaluated at fixed k -- the error): o2 = C(phi)*l(k)^2 (rank-1), so closure o2=0 <=> l(k)=0,
a condition on k ALONE; phi enters only as the amplitude of the violation. k=0 closes the loop for
EVERY phi (telescoping identity) -> closure EXCLUDES NO profile -> phi UNCONSTRAINED. R1 independently:
the whole O(t^2) transmit lives in the coboundary (pure-gauge) orbit of zero mixing, zeroed by tuning
free k for any phi. The "loop holonomy" is just non-additivity of the nonlinear eigenvalue extractor,
NOT a depth curvature. mu unquantized (Q2 NO, confirmed). mu is PERMISSIBLE-but-UNFORCED (metric-
allowed off-diagonal, not a hard import, but unselected -- a free DOF to observe, not native structure).

**F-STEER CAUGHT (both):** driver named the k-absorption caveat correctly, then still stamped the
owner-favorable COUPLING-TRANSMITS bin instead of the fitting COUPLING-INERT. Corrected: COUPLING-INERT.

**SESSION-CULMINATING PATTERN:** the c_eff/depth PROFILE is left UNCONSTRAINED by EVERY structure
examined -- EH (volume-blind), vary-phi (null Lagrangian), integrability C2 (screen-only), Noether C3
(N-blind), and now the depth-angular mixing coupling (k-absorbed). The profile behaves like FREE
boundary/initial DATA, not a bulk/relational law-determined quantity. Honest inference (not a proven
theorem): there may be NO native bulk/relational law that pins the profile -- it is a datum, and P-opt
(the SNe selector) is then a genuine independent posit, consistent with the 2026-08-05 P-opt findings.
The one solid positive from this lane: mu, the invariant reciprocal-lock defect. Nothing banks;
four-check N/A; major juncture for Charles.

## FINAL BLIND VERIFICATION (2026-08-06): PASS with a SCOPE CARVE-OUT (see BLIND_VERIFICATION_FINAL.md)

- **mu = reciprocal-lock defect: CONFIRMED generically, SCOPED s != r.** Assignment-free spectral
  matching forces mu^2*(r-s)(r+s)/s^2 = 0: for s != r no diagonal reciprocal strain reproduces the
  mu != 0 spectrum -> (r,s,mu) not over-parametrized; ordering-robust. **CARVE-OUT both prior
  reviews missed:** on the locus s = r (with |mu| < |1/r - r|), mu IS pure gauge — exact witness
  frame pair exhibited (r=s=1/2, mu=sqrt(7)/2). R1's "no O(1,2) frame pair removes mu" is FALSE on
  that locus. The recorded invariant carries the **s != r scope** from now on.
- **COUPLING-INERT: CONFIRMED, strengthened.** Rank-1 (o2 = C(phi)*l(k)^2) proven SYMBOLICALLY for
  every generic profile (all 2x2 Hessian minors vanish identically); closure is k-only; k=0 closes
  for all phi. Identity, not instance luck.
- Doc nit: line-27 factored-charpoly constant term should be s^2/r^2 (no downstream effect).
