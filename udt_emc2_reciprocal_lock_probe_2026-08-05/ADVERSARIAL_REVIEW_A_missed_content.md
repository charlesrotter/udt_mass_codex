# Adversarial Review A — hunt missed UDT content (attack OE-SR-LOCAL)

Reviewer: blind adversarial pass, independent recompute (own conventions, sympy,
no import of driver code). Date 2026-08-05. Target: the DEFLATIONARY conclusion that
`E=mc^2` yields no new UDT content and the reciprocal lock is invisible to the
energy-mass relation.

## 1. Independent recompute of the mass-shell reduction — CONFIRMED

Signature (-,+), `g_tt=-e^{-2phi}c^2`, `g_xx=e^{2phi}`, mass shell
`g^{ab}p_a p_b=-m^2c^2`, `p_t=-E`, `p_x=P`. Solving from scratch:

- Conserved energy: `E^2 = c^2 e^{-4phi}(P^2 + c^2 m^2 e^{2phi})` — matches driver eq 1.
- Static observer `u^t=e^{phi}` (from `g_tt(u^t)^2=-c^2`); `E_loc=-p_a u^a = E e^{phi}`.
- `phat=P e^{-phi}`. Then `E_loc^2 = P^2 c^2 e^{-2phi} + m^2 c^4`, and
  `E_loc^2 - [(mc^2)^2+(phat c)^2] = 0` IDENTICALLY. **The SR reduction is a true
  identity. phi/B drop out. OE-SR-LOCAL, as a statement about strictly LOCAL
  (one-observer, one-point) invariants, is CORRECT and I could not break it.**

## 2. But the reduction is a TETRAD TAUTOLOGY, not a lock result

I redid the reduction for a GENERIC static diagonal metric with INDEPENDENT
`g_tt=-A`, `g_xx=B`: `E_loc^2 - [(mc^2)^2+(phat c)^2] = 0` STILL, with B dropping.
The orthonormal-frame dispersion is `eta^{ab}p_a p_b=-m^2c^2` for ANY metric by
construction of the tetrad; the driver's `E_loc=E/sqrt(-g_tt/c^2)`, `phat=P/sqrt(g_xx)`
IS the tetrad projection, so it hides ALL metric dependence — g_tt via the clock leg,
g_xx via the ruler leg — and returns SR by identity. So "the lock is invisible locally"
is TRUE but UNDER-INFORMATIVE: it would be equally true of Schwarzschild, de Sitter, or
any static GR metric. The local test does not probe the lock AT ALL. This does not
refute OE-SR-LOCAL; it exposes that the null is a tautology, and warns that the
HEADLINE "E=mc^2 yields no new UDT content" is drawing a UDT conclusion from a
UDT-blind computation.

## 3. Momentum check: `phat=P/sqrt(g_xx)` is the physically correct momentum

UDT's positional dilation stretches rulers by `e^{phi}` — but `g_xx=e^{2phi}` ALREADY
IS that ruler statement (proper length `dl=sqrt(g_xx)dx=e^{phi}dx`). de Broglie
`phat=h/lambda_proper=P e^{-phi}` reproduces the orthonormal momentum; there is no
SECOND `e^{phi}` to apply (doing so would double-count the metric). So no UDT-preferred
momentum reintroduces phi. Driver is right here.

## 4. Where I HUNTED for re-entry — results

(a) **Energy-comparison cocycle (redshift) — solo: lock-blind.** `E_loc(phi)=E e^{phi}`
depends ONLY on `g_tt` (via `u=xi/sqrt(-xi.xi)`, `xi=d_t`). A moving particle's ENTIRE
local kinematics along its worldline — `E_loc(phi)`, `phat(phi)=(1/c)sqrt(E^2e^{2phi}-m^2c^4)`,
`v(phi)` — is fixed by `g_tt` + SR; `g_xx` NEVER enters any local energy-momentum
observable. So the energy-mass sector is genuinely g_tt-only, and the lock (a g_tt–g_xx
relation) leaves no fingerprint in solo energy invariants, local OR two-depth. This
strongly SUPPORTS the driver.

(b) **Orchestra / cross-sector invariant — the lock RE-ENTERS (strongest point).**
The lock's genuine invariant content is `sqrt(-det g)=c` (constant; I verified), i.e.
local `clock_rate x ruler_scale = e^{-phi}c * e^{phi} = c`, depth-INDEPENDENT — a
UDT-specific reciprocity generic GR lacks. Cast as a MEASURABLE energy-sector statement:
between two depths, the gravitational ENERGY-shift `Z=E_loc(2)/E_loc(1)=e^{phi2-phi1}`
(a pure energy-comparison, load-bearing) and the RULER-dilation
`L=sqrt(g_xx2/g_xx1)=e^{phi2-phi1}` are FORCED EQUAL by the lock: `Z=L`. In generic
static GR `Z=sqrt(A1/A2)` and `L=sqrt(B2/B1)` are INDEPENDENT and unequal. So the
energy-comparison leg is HALF of a lock-revealing invariant: solo it looks like GR
redshift, but paired with the ruler cocycle it yields `Z=L`, the reciprocal-lock
fingerprint. This is exactly the orchestra pattern (solo instruments look generic; the
ensemble reveals the structure). **It refutes the broad headline "E=mc^2 / the energy
sector yields no new UDT content" — the energy-comparison IS one required leg of a
lock-specific invariant.** It does NOT refute the narrow claim "solo LOCAL energy-mass
invariants are lock-blind."

(c) **Spin / higher-multipole — scoped out, lock re-enters at dipole.** At the
free-particle (monopole) level SR-local holds. The FIRST energy-sector place the lock
can re-enter is the Mathisson–Papapetrou–Dixon spin–curvature coupling `~R_{abcd}S^{cd}u^b`:
the Riemann tensor of this family depends on both metric functions, and the lock
CONSTRAINS it, so a spinning particle's energy carries a locked relation generic GR
(independent g_tt,g_xx) does not. Unexplored; legitimately outside the free-particle
stamp — but it means the deflationary conclusion must be narrowed to
FREE-PARTICLE/MONOPOLE.

(d) **Global x_max asymptote (2c):** at `x_max` the redshift `e^{phi}` diverges, but
this is a `g_tt` (horizon-redshift) effect; the lock adds no NEW invariant there.

## 5. Verdict

NARROW. The narrow OE-SR-LOCAL identity (solo local energy-mass invariants reduce to SR,
phi/B absent) is CONFIRMED and robust — indeed trivially so (tetrad tautology, any
metric). But the deflationary HEADLINE ("E=mc^2 yields no new UDT content / the lock is
invisible to the energy sector") is TOO STRONG on three counts: (i) the local null is
UDT-blind by construction, so it cannot license a UDT conclusion; (ii) the
energy-comparison cocycle is a LOAD-BEARING leg of a genuine lock invariant `Z=L`
(redshift = ruler-dilation, equiv. `sqrt(-det g)=c`) that generic GR lacks — the lock is
NOT invisible to the energy sector once paired with the ruler sector (orchestra); (iii)
the null is scoped to monopole — spin–curvature energy is where the lock next re-enters.
Recommend: keep OE-SR-LOCAL but restate it narrowly (SOLO local free-particle energy-mass
invariant), and reclassify the `Z=L` reciprocity as a POSITIVE cross-sector energy-sector
fingerprint of the lock (not merely "motion"), since its energy-comparison leg is
essential.
