# Adversarial Review 1 — the null-Lagrangian claim (E[phi] ≡ 0 on the reciprocal lock)

Reviewer: independent adversarial pass (Opus). Date 2026-08-06. Branch grok.
Method: fresh sympy 1.13.1, exact symbolic, ZERO import of the probe's code (q1..q4).
Metric reviewed: ds^2 = -e^{-2phi(r)}dt^2 + e^{2phi(r)}dr^2 + r^2 dOmega^2 (reciprocal lock a=-phi, b=+phi).
Status: UNBANKED review. Not committed.

## 0. Reviewer self-audit (a bug I found in MY OWN first pass — recorded for honesty)

My first Einstein routine assembled the mixed tensor as `g^{m a}(R_{a n} - 1/2 delta R)` —
i.e. it multiplied the (1/2)R term by an EXTRA g^{mm}. That is WRONG: G^m_n = g^{m a}R_{a n}
- (1/2) delta^m_n R. The error VANISHES wherever R=0, so it passed Schwarzschild AND the
lock->Schwarzschild subcase (both vacuum, R=0) and only surfaced on non-vacuum profiles, where
it manufactured a spurious G^t_t != G^r_r that briefly looked like a refutation of the probe.
Independent cross-checks (standard Ricci-component formulas R_tt,R_rr,R_thth; de Sitter/interior
tests) located it. Corrected routine matches all references exactly. Lesson banked: validating a
tensor routine ONLY on vacuum metrics (R=0) cannot catch a (1/2)R-term bug. The probe's numbers
were right; my first pass was wrong. Everything below uses the corrected, cross-validated routine.

## 1. Q1 — Einstein tensor and G^t_t = G^r_r on the lock  [CONFIRMED, exact]

Corrected mixed components on the lock (independently derived; verbatim match to DERIVATION_NOTES):

    G^t_t = G^r_r = e^{-2phi} ( -2 r phi' - e^{2phi} + 1 ) / r^2
    G^th_th = G^ph_ph = e^{-2phi} ( 2 r phi'^2 - r phi'' - 2 phi' ) / r

General static check (a(r),b(r) free), independently reproduced:

    G^t_t - G^r_r = 2(-a' - b') e^{-2b} / r      [match to probe's formula = 0, exact]

G^t_t depends on b ONLY; the reciprocal lock a=-phi,b=+phi gives a'+b'=0 => G^t_t = G^r_r
IDENTICALLY (difference simplifies to exactly 0). The probe's load-bearing structural fact is
CORRECT.

## 2. Q2 — the reduced action and E[phi]  [NULL CONFIRMED, exact]

sqrt(-g) = r^2 sin(theta) is phi-FREE on the lock (independently confirmed: e^{-2phi}*e^{2phi}=1).
Reduced radial integrand (drop 4pi, sin th, t-length):

    L = R * r^2 = 2( -2 r^2 phi'^2 + r^2 phi'' + 4 r phi' + e^{2phi} - 1 ) e^{-2phi}.

Full 2nd-order Euler-Lagrange E[phi] = dL/dphi - d/dr(dL/dphi') + d^2/dr^2(dL/dphi''):

    E[phi] = 0   IDENTICALLY, for EVERY phi(r).   [independently reproduced, exact]

The reduced EH action on the reciprocal-lock slice IS a null Lagrangian. Confirmed. This is not
G=0 relabelled (it is 0=0) and it is not machinery-blindness: control ansaetze below return
NONZERO E. The probe did NOT under-claim (there is genuinely no bulk phi-law here) and did NOT
mis-compute the nullity.

### Mechanism — CONFIRMED and sharpened to an exact identity
For a=A*phi, b=B*phi the reduced EL equals the projected field equation EXACTLY:

    E[phi] = -2 sqrt(-g) ( A * G^t_t + B * G^r_r )     [E - projection = 0, exact, all cases]

For the lock (A=-1,B=1): E[phi] = -2 sqrt(-g) (G^r_r - G^t_t) -- EXACTLY the probe's stated
mechanism, annihilated by the lock's G^t_t=G^r_r. The probe's "phi-variation = (G^r_r - G^t_t)"
is correct (as the lock specialization of the identity above).

### Q2(b) profile admission — CONFIRMED exact
 - L-profile e^{-2phi}=1-r/X:   G^t_t = -2/(X r) != 0  -> free-g FORBIDS (matches probe).
 - Schwarzschild e^{-2phi}=1-k/r: G^t_t = 0            -> free-g allows.
 - quadratic e^{-2phi}=1-(r/X)^2: G^t_t = -3/X^2 != 0  -> forbidden.
All solve E[phi]=0 trivially (everything does). Admission is VACUOUS, exactly as the probe's
honest reading states. The owner-favorable "UNBLOCK" reading is correctly refused.

## 3. Q3 — LOCK-SPECIFICITY  [CONFIRMED not-generic; NARROW refinement of "lock-specific"]

Closed-form null condition, independently derived for a=A*phi, b=B*phi (symbolic A,B):

    E[phi] = 2 (A + B) ( e^{2 B phi} - 1 ) e^{(A-B) phi}.

E[phi] == 0 for ALL phi  <=>  (A + B) = 0   OR   B = 0.

 - Generic single-function reduction is NONZERO (e.g. a=-phi,b=phi/2: E=(1-e^{phi})e^{-3phi/2};
   a=-2phi,b=phi: E=-2e^{-phi}+2e^{-3phi}). So nullity is NOT a generic 1-field artifact --
   the probe's core Q3 claim is CONFIRMED.
 - The reciprocal-lock LINE a+b=0 (ANY overall scale, incl. a=-phi/2,b=phi/2) is null -- CONFIRMED.
 - REFINEMENT (adversarial catch): the lock is NOT the unique null case. The line b=0 (g_rr=1,
   any a=A*phi) is ALSO null -- because b=0 forces the mass function, hence G^t_t, to vanish
   identically (E=-2 sqrt(-g) A G^t_t with G^t_t==0). So the exact null locus is the UNION
   {a+b=0} U {b=0}, not the single lock line. This does NOT rescue an UNBLOCK and does not touch
   the probe's metric (which sits on a+b=0); it corrects the phrasing "lock-specific" to
   "null locus = {a+b=0} U {b=0}; generic single-function is non-null." NARROW, not a break.

## 4. Q4 — THE BOUNDARY TERM  [computed exactly; nontrivial but STANDARD, not profile-selecting]

L is an exact total derivative L = dF/dr with (verified dF/dr - L = 0 exactly):

    F(phi,phi',r) = 2 r^2 e^{-2phi} phi' + 2 r (1 - e^{-2phi})
                  = 2 r^2 e^{-2phi} phi' + 4 m(r),   m(r) = (r/2)(1 - e^{-2phi})  [Misner-Sharp mass].

So on the lock S_EH = integral L dr = F(edge) - F(center): a PURE boundary term equal to the
Misner-Sharp mass/energy functional (plus a phi'-piece). Its boundary variation:

    dF/dphi  = 4 r (1 - r phi') e^{-2phi},     dF/dphi' = 2 r^2 e^{-2phi}  (!= 0).

Honest adjudication (not inflated): the boundary term is NONTRIVIAL -- it is literally the
gravitational mass/energy at the edge, and dF/dphi' != 0 signals the usual GHY situation (a
counterterm is needed for a clean Dirichlet problem). BUT: (i) it imposes NO bulk phi-equation
(E==0, the interior profile is completely undetermined by this action); (ii) requiring
stationarity fixes only boundary DATA (phi and/or phi' at x_max), which is exactly the standard
GR boundary/GHY data (the mass) -- NOT a new native phi-law and NOT a bulk-profile selector.
The finite-cell edge does carry a nontrivial boundary OBJECT (the Misner-Sharp mass), but it does
NOT carry a nontrivial profile-selecting phi-CONDITION. The live lead is real as "the EH content
on the lock is entirely the edge mass," but it does not become a mechanism or a native law here.

## 5. Verdict

NULL-CONFIRMED. E[phi] ≡ 0 is EXACT on the reciprocal lock; independently reproduced along with
every component, the projection identity/mechanism, the profile-admission claims, and the total-
derivative structure. The probe neither under-claimed a missed phi-law (there is none from EH on
the lock) nor mis-computed the nullity. Two honest refinements, both NARROW: (1) the exact null
locus is {a+b=0} U {b=0}, so "lock-specific" is slightly too strong (generic single-function IS
non-null, as claimed); (2) the boundary term is the nontrivial Misner-Sharp mass but is the
standard GR/GHY edge term -- it fixes boundary data, it does not impose a profile-selecting phi-
condition. Free-metric collapse to GR (e^{-2phi}=1-k/r) reconfirmed as the wall.
