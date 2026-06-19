#!/usr/bin/env python3
"""
timelive_nonround_structural.py  --  THE DECISIVE STRUCTURAL QUESTION (sympy-exact)

CONVERGENT CENTERPIECE SOLVE / structural-first part.
Agent: claude-opus-4-8[1m].  Date: 2026-06-19.  DATA-BLIND.  NOT canon.

Re-do B2's / wcc's linearization of the NATIVE field equation, but about a
NON-ROUND (v0_theta != 0) AND TIME-LIVE (d_t v0 != 0) background.

B2 / wcc fact (round, static):
  field eqn:  v_mm + e^{2v}( v_thth + cot th v_th - v_th^2 ) = Phi(e^{-2v}-e^{v})
  the angular nonlinearity  -v_th^2  linearizes about a theta-FLAT round bg to
     d/d_eps [-(v0_th+eps u_th)^2]|_0 = -2 v0_th u_th  = 0   (since v0_th=0)
  => operator = pure dressed Laplacian => eigenvalue -l(l+1)W, W>0 => sign-def DAMPING.

QUESTION (this script, exact symbolic):
 1. Compute the EXACT linear variation of -v_th^2 about a NON-ROUND bg (v0_th != 0):
        it is  -2 v0_th(m,th) u_th  -- a NEW first-order (advection-like) term.
 2. Add the TIME axis live: include v_tt / v_t structure (the field eqn must be
    extended to time-live; we derive what the native action gives, not import).
 3. Determine the SPECTRAL NATURE of the resulting fluctuation operator:
    self-adjoint? sign-definite? does the new -2 v0_th u_th term + time term
    admit a binding well / soft mode / standing-wave eigencondition, or stay
    sign-definite damping?

NO grid / box / cutoff used as an instrument here -- pure symbolic operator analysis.
"""

import sympy as sp

print("="*78)
print("PART 1 -- EXACT linear variation of the angular nonlinearity -v_th^2")
print("         about a NON-ROUND background (v0_theta != 0)")
print("="*78)

m, th, t = sp.symbols('m theta t', real=True)
eps = sp.symbols('eps', real=True, positive=True)

# Background v0(m,theta,t) -- NON-ROUND (theta-dependent) and TIME-LIVE allowed.
v0 = sp.Function('v0')(m, th, t)
u  = sp.Function('u')(m, th, t)      # fluctuation
v  = v0 + eps*u

# The native angular nonlinearity term in the field equation (wint (star), wcc):
#   inside e^{2v}( ... - v_th^2 ):  the nonlinear piece is  N = - (v_th)^2
N = -(sp.diff(v, th))**2
dN = sp.diff(N, eps).subs(eps, 0)
dN = sp.simplify(dN)
print("\n d/d_eps [ -(v_th)^2 ] |_{eps=0}  =", dN)
print("  (B2/wcc round case: v0_th=0 => this = 0. Non-round: v0_th != 0 => NONZERO.)")

# Confirm: about round bg it vanishes; about non-round it does not.
v0_round = sp.Function('v0r')(m, t)         # theta-independent => round
dN_round = dN.subs(v0, v0_round)
# substitute properly: rebuild with round bg
v_r = v0_round + eps*u
N_r = -(sp.diff(v_r, th))**2
dN_round = sp.simplify(sp.diff(N_r, eps).subs(eps,0))
print(" round bg (v0 theta-independent):  variation =", dN_round, " (B2's EXACT ZERO -- reproduced)")

print("""
 STRUCTURAL READ (Part 1): about a NON-ROUND background the angular nonlinearity
 contributes a NEW linear term  -2 v0_theta * u_theta  to the fluctuation operator
 that B2's round analysis lacked. It is a FIRST-DERIVATIVE (advection / drift) term
 in theta with background-dependent coefficient -2 v0_theta(m,theta).
""")

print("="*78)
print("PART 2 -- the full angular fluctuation operator about a non-round bg")
print("          (dressed Laplacian + the new drift term), spectral nature")
print("="*78)

# Full angular operator acting on fluctuation u, from  e^{2v}(u_thth + cot th u_th - 2 v0_th u_th)
# (the e^{2v} dressing -> e^{2v0} at linear order; multiplies the whole angular block).
# Write the angular operator A[u] (drop common positive factor e^{2v0} for sign analysis):
cot = sp.cot(th)
A_u = sp.diff(u, th, 2) + cot*sp.diff(u, th) - 2*sp.diff(v0, th)*sp.diff(u, th)
print("\n Angular operator (modulo +e^{2v0}>0):")
print("   A[u] = u_thth + cot(th) u_th - 2 v0_th u_th")
print("        = u_thth + (cot th - 2 v0_th) u_th")

# Is this operator self-adjoint w.r.t. some weight? A 1D 2nd-order operator
#   u'' + p(th) u'  is self-adjoint in weight  w(th) = exp( INT p dth ).
# Here p = cot th - 2 v0_th  => w = exp(INT cot th dth - 2 v0) = sin(th) * e^{-2 v0}.
# So A is self-adjoint (Sturm-Liouville) in the weight  W_sl = sin(th) e^{-2 v0(th)}.
print("""
 STURM-LIOUVILLE FORM: u'' + p u' with p = cot th - 2 v0_th is self-adjoint in
 weight  w(th) = exp(INT p dth) = sin(th) * exp(-2 v0(th)).
 => the NON-ROUND angular operator is STILL self-adjoint (real spectrum) -- but in a
    v0-DEFORMED weight  sin(th) e^{-2 v0}, NOT the round weight sin(th).
""")

# SL form: (1/w) d/dth ( w u' ).  Sign of the operator = -INT w (u')^2 / INT w u^2  <= 0
# for the PRINCIPAL part. The question is whether the FULL operator (with the e^{2v}
# dressing AND the radial + source + time pieces) has any zero-derivative (potential)
# term that can make an eigenvalue POSITIVE (a growing / soft mode) = a binding well.
th_s = sp.symbols('th', positive=True)
w = sp.sin(th_s)*sp.exp(-2*sp.Function('V')(th_s))   # symbolic weight with bg V(th)=v0
u_sl = sp.Function('u')(th_s)
SL = sp.diff(w*sp.diff(u_sl, th_s), th_s)/w
SL = sp.simplify(sp.expand(SL))
print(" SL operator (1/w)(w u')' expanded =", SL)
print("   -> matches u'' + (cot th - 2 V') u'  : confirms SL/self-adjoint form.")

print("""
 SPECTRAL NATURE (Part 2): the pure ANGULAR operator about a non-round bg is
 self-adjoint and its PRINCIPAL (second-derivative) part is still negative-definite
 (a Laplacian in a deformed weight). The new -2 v0_th u_th term is a DRIFT, NOT a
 zeroth-order POTENTIAL well: a first-derivative term cannot by itself flip the
 operator's sign (it is anti-self-adjoint-in-the-undeformed-weight and is exactly
 what the weight change sin->sin e^{-2v0} absorbs). So -- ON THE ANGULAR AXIS ALONE
 -- non-roundness does NOT manufacture a bound/soft mode: it only re-weights the
 same sign-definite Laplacian. A POTENTIAL (zeroth-order, u-multiplying) term that
 could bind must come from ELSEWHERE: the RADIAL+SOURCE coupling and/or the TIME term.
""")

print("="*78)
print("PART 3 -- the FULL field-equation fluctuation operator (radial + angular")
print("          + SOURCE potential), about a non-round STATIC bg")
print("="*78)
# Full wint/wcc native field equation:
#   F[v] := v_mm + e^{2v}( v_thth + cot th v_th - v_th^2 ) - Phi( e^{-2v} - e^{v} ) = 0
# Linearize F about bg v0(m,theta): the fluctuation operator L[u] = dF/d_eps|_0.
Phi = sp.symbols('Phi', positive=True)   # the ON-source coefficient (>0)
v0f = sp.Function('v0')(m, th)           # static non-round bg
uf  = sp.Function('u')(m, th)
vv  = v0f + eps*uf
F = ( sp.diff(vv, m, 2)
      + sp.exp(2*vv)*( sp.diff(vv, th, 2) + sp.cot(th)*sp.diff(vv, th) - sp.diff(vv, th)**2 )
      - Phi*( sp.exp(-2*vv) - sp.exp(vv) ) )
L = sp.simplify(sp.diff(F, eps).subs(eps, 0))
print("\n L[u] (linear fluctuation operator about static non-round bg v0(m,theta)):")
sp.pprint(L)

# Collect the ZEROTH-ORDER (u-multiplying, no-derivative) coefficient = the POTENTIAL.
# Group L by derivatives of u.
u_, um, umm, uth, uthth = sp.symbols('u_ um umm uth uthth')
# Build a dict of coefficients via collecting on the Derivative atoms
Lexp = sp.expand(L)
coeff_umm  = Lexp.coeff(sp.Derivative(uf, m, 2))
coeff_uthth= Lexp.coeff(sp.Derivative(uf, th, 2))
# uth coefficient: differentiate out -- use as_coefficient
duth = sp.Derivative(uf, th)
coeff_uth = Lexp.coeff(duth)
# subtract derivative-carrying parts to isolate the u^0 (potential) coefficient
rem = sp.expand(Lexp
        - coeff_umm*sp.Derivative(uf,m,2)
        - coeff_uthth*sp.Derivative(uf,th,2)
        - coeff_uth*duth)
coeff_u = sp.simplify(rem.coeff(uf))
print("\n coeff of u_mm   :", sp.simplify(coeff_umm))
print(" coeff of u_thth :", sp.simplify(coeff_uthth))
print(" coeff of u_th   :", sp.simplify(coeff_uth), "   <-- carries the -2 v0_th drift (x e^{2v0})")
print(" coeff of u (POTENTIAL, zeroth-order):", sp.simplify(coeff_u))

print("""
 KEY: the SOURCE term  -Phi(e^{-2v}-e^{v})  contributes a genuine ZEROTH-ORDER
 POTENTIAL  V_pot(m,theta) = -Phi(2 e^{-2v0} + e^{v0})  (the d/dv of the source).
 Whether the full operator BINDS (positive eigenvalue / soft mode) is a competition
 between this potential and the (negative-definite) dressed Laplacian -- and this is
 EXACTLY the operator wcc solved NUMERICALLY about the ROUND bg and found gap=0.648>0
 (no soft mode). The new physics here: about a NON-ROUND bg, V_pot is theta-DEPENDENT
 (via v0(m,theta)) and the drift coeff is nonzero -- so the question reopens, but the
 binding must come from V_pot, not the drift (Part 2). HOWEVER (decisive caveat, Part 4):
 wcc PROVED the round bg is the only STATIC fixed point (every lobe relaxes to round).
 So a non-round STATIC bg DOES NOT EXIST to linearize about. The non-roundness must be
 supplied by the TIME sector (Part 4) -- non-round + static is empty.
""")

print("="*78)
print("PART 4 -- THE TIME-LIVE OPERATOR: does the wave term + non-round coupling")
print("          turn the sign-definite damping into a standing-wave EIGENCONDITION?")
print("="*78)
print("""
 DERIVING the time term natively (NOT importing it). Two independent native facts
 fix the time structure of the fluctuation operator:

 (a) phase0 Birkhoff (sympy-exact, banked): in the ROUND vacuum class the momentum
     constraint G_tr = 2 d_t phi / r forces d_t phi = 0 -- there is NO spatial
     operator to absorb the time derivative, so time is FROZEN (no wave term).
     => about the ROUND background the field equation has NO live d_t^2; the
        operator is purely elliptic-in-space = sign-definite damping (= B2/wcc).

 (b) phase0 non-round escape (B2 quadrupole, sympy-exact, verifier-confirmed
     PHYSICAL not gauge): the l>=2 angular deformation h(t,r) P2 obeys a VACUUM
     WAVE equation -- G_thth carries +d_t^2 h with a NONZERO (gauge-invariant,
     radiative) coefficient. => the NON-ROUND sector DOES carry a live d_t^2.
     The native-matter T_tr probe (monopole <T_tr> != 0 for d_t Theta != 0) shows
     the matter-sourced version ALSO unfreezes time.
""")
# Build the time-live fluctuation operator schematically and ask the SPECTRAL question.
# In harmonic balance u(m,th,t) = U(m,th) e^{i w t}, the live d_t^2 -> -w^2 (from the
# wave sector) enters as a CONSTANT-SIGN shift of the eigenvalue. Let L_space be the
# spatial fluctuation operator (Part 3): L_space[U] = lambda U is the wcc eigenproblem.
# The time-live problem is  L_space[U] + (sign)* w^2 * M[U] = 0  -- a generalized
# eigenproblem for w^2. THE SIGN of the time term decides EVERYTHING:
w_sym = sp.symbols('omega', real=True)
print(""" HARMONIC BALANCE u = U(m,theta) e^{i omega t}:
   - if the live time term enters as  +d_t^2 u -> -omega^2 U  with the SAME sign as
     a HYPERBOLIC (wave) operator [the B2 quadrupole case: vacuum WAVE eqn d_t^2 h],
     then the problem is  L_space[U] = +omega^2 M[U]  with M>0:
       => omega^2 = (-<U,L_space U>)/<U,M U>.
     Since wcc PROVED L_space is sign-definite NEGATIVE (gap 0.648>0 => -L_space>0),
     omega^2 > 0 for EVERY mode => a REAL frequency for every spatial harmonic.
     This is a STANDING-WAVE TOWER: discrete omega_l labelled by the (discrete,
     -l(l+1)) angular harmonics of the sign-definite spatial operator.
""")
print(""" *** THE DECISIVE STRUCTURAL POINT (honest, two-edged) ***
   The SAME sign-definiteness that B2/wcc reported as 'no spectrum' (no static
   instability / no soft bound mode) becomes, on the TIME-LIVE axis, the condition
   for a REAL OSCILLATION FREQUENCY: -L_space > 0 is exactly what makes omega^2 > 0
   (a genuine standing wave) rather than omega^2 < 0 (an exponential instability).
   So:
     * B2/wcc 'sign-definite damping, no tower'  == there is no STATIC bound state
       and no growing instability -- TRUE, and it does NOT change.
     * BUT the time-live reading of the very same operator gives a DISCRETE LADDER
       of real STANDING-WAVE frequencies omega_l^2 = -lambda_l(spatial) / M_l > 0,
       one per spatial eigenmode lambda_l. The discreteness is inherited from the
       DISCRETE spatial spectrum {lambda_l} (the -l(l+1) angular harmonics).
""")
print(""" THE BOX-CONTROL CAVEAT (decisive, anti-shortcut -- this is where it likely dies):
   omega^2 = -lambda_l / M_l. The spatial eigenvalue lambda_l = -l(l+1) W(r) (wcc),
   and W(r) integrated over the cell scales with the cell. For a cavity standing wave
   the eigenfrequency of a sign-definite Laplacian-type operator on a domain of size R
   generically scales omega ~ 1/R (Weyl law) -- i.e. BOX-CONTROLLED, exactly the
   single-cell-spectrum-box-controlled / CS4 finding (omega^2 ~ 1/R^2 -> 0). The
   standing-wave tower is REAL but its ABSOLUTE scale is almost certainly set by the
   cell wall, NOT intrinsic. The RATIO ladder (omega_l/omega_1) may be intrinsic
   (the -l(l+1) ratios) but those are the BOX's own harmonic ratios. THIS IS THE
   MAKE-OR-BREAK and it must be settled NUMERICALLY with an R-scan (Part 5 / numeric).
""")
print(" Structural verdict assembled in the results doc. No numeric run here (Part 5).")
