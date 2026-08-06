# c_eff <-> depth-profile binding test (reciprocal-radial vs angular-required)

Date: 2026-08-06 | Branch: grok | Mode: OBSERVE (both outcomes first-class; no target)
Method: exact sympy 1.13.1, float-free. No production/code imports; grounded by reading
`udt_complete_pair_phi_orchestra_audit_2026-08-05/{EXACT_DERIVATION.md,AUDIT_REPORT.md}`.
Script: `ceff_binding.py` (all checks below are machine-confirmed True/as-stated).

## THE QUESTION
Is c_eff intertwined with the depth PROFILE already at the BARE RADIAL (reciprocal-
subgroup) level, or does the binding essentially REQUIRE the angular/screen sector?

## Banked objects used (verbatim from the audit)
- Frame-covariant strain: `C_A = A^dagger A`, `A^dagger = g_p^-1 A^T g_q`.
- Signed depth extractor: `delta_t(A) = -(1/2) log(lambda_timelike of C_A)`; reduces to
  founded phi on the reciprocal subgroup.
- Screen family: `delta_a(p,q) = log[N(p)/N(q)] + a log[R(q)/R(p)]`, N = timelike Killing
  norm, R = screen area radius, `a` free/unselected.

---

## PART 0 -- the c_eff = c_E * lambda_t identity (reciprocal lock, NO screen)

Reciprocal-lock radial metric `ds^2 = -e^{-2phi} c_E^2 dt^2 + e^{2phi} dx^2`.
Coordinate cone ratio (a GAUGE quantity -- F-GAUGE):
```
c_eff = sqrt(-g_tt/g_xx) = c_E * e^{-2phi}              [CONFIRMED exact]
```
Reciprocal-subgroup strain `C_D = D_r^dagger D_r` with `D_r=diag(r^-1,r,1,1)`, `r=e^phi`,
on `eta=diag(-1,1,1,1)`:
```
C_D = diag(e^{-2phi}, e^{+2phi}, 1, 1)                  [CONFIRMED]
lambda_timelike = e^{-2phi}   (the eta=-1 slot)         [CONFIRMED]
delta_t = -(1/2) log(lambda_timelike) = phi            [CONFIRMED]
```
THE IDENTITY, both directions machine-verified:
```
c_eff = c_E * lambda_timelike                           [CONFIRMED True]
phi   = -(1/2) log(c_eff/c_E)                           [CONFIRMED True]
```
So `lambda_timelike = c_eff/c_E = e^{-2phi}`: c_eff and phi are ONE eigenvalue read two
ways. This uses ONLY the pure reciprocal subgroup -- NO screen/angular structure is
invoked or needed. lambda_t and phi=delta_t are frame-INVARIANT (eigenvalue/extractor);
c_eff itself is a coordinate speed (gauge). The identity ties the gauge readout c_eff to
the invariant eigenvalue lambda_t within the reciprocal-lock chart (F-GAUGE noted).

---

## PART 1 -- OPTION B: radial profile binding (reciprocal subgroup only)

Comparison arrow p->q = natural chart identification A=I reading g_p vs g_q, radial
2-slot metrics in reciprocal lock. Strain `C2 = g_p^-1 A^T g_q A`:
```
C2 = diag( e^{-2(phi_q-phi_p)}, e^{+2(phi_q-phi_p)} )
lambda_t(p->q) = e^{-2(phi_q-phi_p)}                    [CONFIRMED]
```
Profile (q varies, p fixed reference):
```
c_eff(q)/c_eff(p) = lambda_t(p->q)                     [CONFIRMED True]
delta_t(p->q)     = phi_q - phi_p   (the depth profile) [CONFIRMED]
```
MUTUAL FIXING at the radial level (both directions verified):
- c_eff(q) determines phi(q):  `phi_q = -(1/2) log(c_eff(q)/c_E)`   [CONFIRMED True]
- phi(q) determines c_eff(q):  `c_eff(q) = c_E e^{-2phi_q}`         [CONFIRMED True]

=> Given the radial comparison ALONE, `c_eff(q) <-> phi(q)` is a fixed, invertible pair.
The profile and c_eff form a fully-bound pair with NO residual freedom from the screen
sector. This is the content of Option B, and it holds exactly.

---

## PART 2 -- OPTION A: turn the screen/angular sector ON. Does `a` enter c_eff?

Full 4-slot metrics with screen `= R^2` in the two spacelike screen slots; same natural
split-preserving arrow A=I. Strain `C4 = g_p^-1 A^T g_q A`:
```
C4 = diag( e^{-2(phi_q-phi_p)}, e^{+2(phi_q-phi_p)}, (R_q/R_p)^2, (R_q/R_p)^2 )
```
Machine-confirmed:
- `lambda_timelike(4-slot) = e^{-2(phi_q-phi_p)}`; contains NO R.        [R_in_timelike_eig = False]
- timelike eigenvalue unchanged by turning screen on.                    [True]
- the screen radius lands in the SPACELIKE screen eigenvalues `(R_q/R_p)^2`. [R_in_screen_eig = True]
- radial cone `c_eff = c_E e^{-2phi_q}` contains NO R.                   [ceff_no_R = True]

The screen family, and where `a` lives:
```
delta_a(p,q) = (phi_q - phi_p) + a * log(R_q/R_p)
d(delta_a)/da = log(R_q/R_p)                            [pure SCREEN; no phi]
delta_a|_{a=0} = phi_q - phi_p = delta_t (radial)      [CONFIRMED True]
a_touches_timelike (delta a-piece depends on phi?) = False
```
So `a` enters delta_a ONLY through the screen term `log(R_q/R_p)`, i.e. through the
SPACELIKE screen block / `log det Q_A` (the audit's block character
`delta_a = delta_quotient + a log det Q_A`). It does NOT enter the timelike eigenvalue,
hence NOT c_eff. The angular sector ADDS a separable additive constant `a` without
altering the radial `c_eff <-> phi` identity.

VERDICT (for the screen-area coefficient `a`): OPTION B.
Single load-bearing step: the timelike eigenvalue of C_A lives in the clock/Killing block
`e^{-2(phi_q-phi_p)}`, set entirely by the Killing-norm ratio N; the screen radius R sits
in orthogonal spacelike slots, so `a log R` can never enter the timelike eigenspace.

---

## PART 3 -- F-STEER honesty probe: the DISTINCT channel that CAN touch c_eff

Not steering to B: there IS an angular-sector operation that changes the timelike
eigenvalue -- but it is NOT the coefficient `a`. It is the off-diagonal clock->screen
MIXING witness (EXACT_DERIVATION.md sec.4), a unipotent (lower-triangular) arrow:
```
A = [[1/2,0,0,0],[0,2,0,0],[1/4,0,1,0],[0,0,0,1]]
clock-screen block of C_A: charpoly L^2 - (19/16) L + 1/4     [CONFIRMED]
timelike eig = (19 - sqrt(105))/32
delta_t_mix = -(1/2) log[(19-sqrt(105))/32] != log 2 = delta_quotient   [CONFIRMED !=]
```
So off-diagonal clock-screen MIXING DOES modulate the timelike-strain depth (hence would
touch c_eff). BUT this is a different angular operation from the screen-area coefficient
`a`: the audit's own character `delta_a = delta_quotient + a log det Q_A` states unipotent
mixing "does not enter this ordinary character, while screen area does." `a` parameterizes
diagonal screen AREA, not off-diagonal mixing. The two channels are disjoint here.

Consequence for the verdict's SCOPE: the c_eff<->phi binding is complete at the radial
level against the SCREEN-AREA sector (`a`) -- Option B for the question as posed (which
carries R and the free `a`). It is NOT immune to clock-screen MIXING, an unselected,
separate off-diagonal channel not present in the delta_a family. That mixing channel is
the only route by which "angular structure" could re-enter c_eff, and it is not `a`.

---

## VERDICT

**B** -- c_eff <-> depth-profile is bound at the bare radial (reciprocal-subgroup) level;
the angular/screen sector as parameterized by the free coefficient `a` is SEPARABLE and
ADDITIONAL. `a` does NOT enter the timelike eigenvalue, hence not c_eff.

- INVARIANT claims: lambda_timelike, delta_t=phi, and the profile delta_t(p->q)=phi_q-phi_p
  are frame-invariant. c_eff is a coordinate (gauge) speed; the invariant tied to it is
  the ratio c_eff(q)/c_eff(p) = lambda_t(p->q) (F-GAUGE surfaced).
- SCOPE / open channel: block-triangular clock-screen MIXING (sec.4) can change the
  timelike eigenvalue, but it is a distinct unselected channel, not `a`. Verdict B is
  scoped to the screen-area family delta_a; the mixing channel remains an open A-type route
  not exercised by `a`.
- No physics selected; `a` and the mixing coefficient both remain unselected by present
  premises (consistent with the grounding audit's OPEN status).
