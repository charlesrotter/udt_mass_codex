"""
running_rate_bianchi_absorb.py  (agent, 2026-06-18) MODE: OBSERVE
Task 2: Bianchi -> source-conservation law for G_mu^nu = kappa(phi) T_mu^nu.
Task 3: physical-vs-absorbable test (dimensionless ruler ratio).
Task 4: phi-law from the trace.
Task 5: forced-vs-absorbable exponent.

We work covariantly/algebraically, not tied to the radial chart, for the
conservation law (it must hold as a tensor identity).
"""
import sympy as sp

phi = sp.symbols('phi', real=True)
a   = sp.symbols('a', real=True)      # matter mass-dilation exponent m(phi)~e^{-a phi}; CHOSEN-OPEN
G, c0, hbar = sp.symbols('G c0 hbar', positive=True)

print("="*70)
print("TASK 2 — Bianchi identity => source law")
print("="*70)
# nabla_mu G^{mu nu} = 0 identically (contracted Bianchi). Candidate G^{mu nu}=kappa T^{mu nu}.
# => nabla_mu(kappa T^{mu nu}) = 0  => kappa nabla_mu T^{mu nu} + (nabla_mu kappa) T^{mu nu} = 0
# => nabla_mu T^{mu nu} = -(nabla_mu ln kappa) T^{mu nu}
kappa = (8*sp.pi*G/c0**4)*sp.exp(8*phi)
dln_kappa_dphi = sp.simplify(sp.diff(sp.log(kappa), phi))
print("kappa(phi) =", kappa)
print("d ln kappa / d phi =", dln_kappa_dphi, "   (so nabla_mu ln kappa = 8 partial_mu phi)")
print()
print("RESULT:  nabla_mu T^{mu nu} = -(8) (partial_mu phi) T^{mu nu}")
print("         i.e. nabla^mu T_{mu nu} = -8 (partial^mu phi) T_{mu nu}")
print()
print("Interpretation: source NOT ordinarily conserved; exchanges with phi along gradients.")

print()
print("="*70)
print("TASK 3 — PHYSICAL vs ABSORBABLE  (the make-or-break)")
print("="*70)
# The corpus criterion (udt_field_equations_derivation_results.md sec 2b):
# a departure is PHYSICAL iff a DIMENSIONLESS ratio of a matter-built ruler to a
# metric-built ruler RUNS with phi. Units/coordinate/field redefinitions move both
# together and cancel in the ratio.
#
# Metric proper ruler (radial):    e^{phi} dr        -> exponent +1
# Matter Compton ruler lambda_C = hbar/(m c).  Locally measured c=c0 (observer-frame, Sense 1).
#   m(phi) ~ m0 e^{-a phi}.   So lambda_C ~ e^{+a phi}? careful: lambda_C ~ 1/m ~ e^{+a phi}
# Ratio R(phi) = lambda_C / (metric ruler) ~ e^{a phi} / e^{phi} = e^{(a-1)phi}
# but the corpus wrote e^{-(a+1)phi}; sign of a convention. We instead DERIVE what the
# running-coupling law FORCES, independent of the a-convention, via a field redefinition attempt.

print("""
ABSORBABILITY ATTEMPT (explicit). The skeptic: 'kappa(phi)=e^{8phi} is just units;
rescale T (or coordinates) and recover G_munu = const * T_munu = GR.'

Field redefinition of the source: define  T~_munu := kappa(phi)/kappa0 * T_munu
with kappa0 = 8 pi G/c0^4 (the constant GR value). Then the field equation reads
    G_munu = kappa0 * T~_munu   (looks like GR with constant coupling).
""")
# Is T~ a legitimate stress tensor (conserved, physical)? Test its conservation law:
# nabla^mu T~_munu = nabla^mu(e^{8phi} T_munu) = e^{8phi}[nabla^mu T_munu + 8 partial^mu phi T_munu]
#                  = e^{8phi}[ -8 partial phi T + 8 partial phi T ] = 0  by Task 2.
print("Check: nabla^mu T~_munu = e^{8phi}[ nabla^mu T_munu + 8 partial^mu phi T_munu ]")
print("       = e^{8phi}[ -8 partial phi T + 8 partial phi T ] = 0.")
print(">>> T~ IS covariantly conserved. So *formally* G_munu = kappa0 T~_munu is GR with")
print("    an ordinary conserved source T~.  The running coupling, BY ITSELF, is ABSORBED")
print("    into a redefinition of what we call the stress tensor.")
print()
print("THE NON-TRIVIAL QUESTION: is T~ or T the PHYSICAL stress? They differ by e^{8phi}.")
print("This is decided ONLY by the matter ruler (Compton wavelength of real matter), i.e.")
print("by how the matter's OWN mass dilates relative to the metric rulers. That is the")
print("dimensionless-ratio test below — the running coupling alone does NOT decide it.")
print()

# The dimensionless invariant that cannot be moved by ANY redefinition:
print("DIMENSIONLESS FINGERPRINT (cannot be rescaled away):")
ruler_metric = sp.exp(phi)              # proper radial ruler exponent +1
# Compton ruler with locally-constant c0 and m~e^{-a phi}:
ruler_compton = sp.exp(a*phi)           # lambda_C ~ hbar/(m c0) ~ e^{+a phi}
ratio = sp.simplify(ruler_compton/ruler_metric)
print("  ratio = lambda_C / (proper ruler) =", ratio, " = e^{(a-1)phi}")
print("  runs with phi  <=>  a != 1   (this convention).  phi-independent (absorbable) <=> a=1.")
print()
print("KEY OBSERVATION: the running-coupling exponent '8' does NOT appear in the")
print("dimensionless ratio. The ratio is set by 'a' (matter mass dilation), NOT by kappa.")
print("=> The depth-running of kappa is, on its own, the ABSORBABLE (units/T-redefinition)")
print("   kind. The PHYSICAL non-absorbable departure lives in the matter ruler (a), which")
print("   the field-equation form does not fix.")

print()
print("="*70)
print("TASK 5 — is the exponent 8 forced?")
print("="*70)
print("""
kappa = 8 pi G / c(phi)^4, c(phi)=c0 e^{-2phi} => c^4 = c0^4 e^{-8phi} => kappa ~ e^{+8phi}.
The '8' = 4 * 2  (the power 4 on c, times the dilation rate 2 in c=c0 e^{-2phi}).
BUT: by Task 3, the ENTIRE e^{8phi} can be absorbed into T~. So the physical steepness
is NOT 8 — 8 is the absorbable (varying-c^4) part. The physical, non-absorbable steepness
is whatever survives in the dimensionless ratio = governed by (a-1) [this convention] /
the corpus's (a+1), i.e. the matter mass-dilation exponent, which is UNFORCED by the law.
""")
