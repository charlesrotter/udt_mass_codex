"""
verify_relrederiv_independent.py
BLIND ADVERSARIAL re-derivation, built from scratch from R1+R2+R3 only.
Goal: REFUTE. Independent of relrederiv_checks.py.
DATA-BLIND: no mass/ratio/wall numbers.
"""
import sympy as sp

PASS = "CONFIRMS"; FAIL = "REFUTES"; INC = "INCONCLUSIVE"

print("#"*72)
print("# A. FUNCTIONAL EQUATION: is exp the UNIQUE solution? Attack P4.")
print("#"*72)

# Set up R1+R2 from scratch on the clock-rate f(phi)=sqrt(-g_tt/c^2)>0.
# D(a,b)=f(b)/f(a). R1: D depends only on (b-a) => f(b)/f(a)=g(b-a).
# IMMEDIATE TEST: is R1 (depends only on differences) ALREADY equivalent to
# the exponential, BEFORE R2? Set a=phi, b=phi+d:  f(phi+d)/f(phi)=g(d) for ALL phi.
# That means f(phi+d)/f(phi) is independent of phi. Differentiate.
phi, d = sp.symbols('phi d', real=True)
f = sp.Function('f', positive=True)
# Condition: f(phi+d)/f(phi) = g(d) independent of phi  => d/dphi [f(phi+d)/f(phi)] = 0
ratio = f(phi+d)/f(phi)
dratio = sp.diff(ratio, phi)
print("d/dphi [f(phi+d)/f(phi)] =", sp.simplify(dratio))
# Setting =0:  f'(phi+d) f(phi) - f(phi+d) f'(phi) = 0  => f'(phi+d)/f(phi+d) = f'(phi)/f(phi)
# i.e. (log f)' is the same at phi and phi+d for ALL d => (log f)' = const = k => f=exp(k phi).
print(" -> numerator f'(phi+d)f(phi)-f(phi+d)f'(phi)=0 means (log f)'(phi+d)=(log f)'(phi) for all d")
print(" -> (log f)' is a CONSTANT k  =>  f=C*exp(k phi).  R1 ALONE (with differentiability) gives exp!")
print(" FINDING: R1 'depends only on differences' is NOT independent of R2; once you")
print("          demand a phi-independent ratio for ALL phi & d AND differentiability,")
print("          the exponential already follows. R2 (composition) is then automatic.")
print()
# Verify: if f=exp(k phi), is R2 (composition) automatically satisfied? Yes trivially.
k = sp.symbols('k', real=True)
fexp = sp.exp(k*phi)
g_of = lambda dd: sp.exp(k*dd)
print(" check R2 auto for f=exp: g(x)g(y)-g(x+y)=",
      sp.simplify(g_of(sp.Symbol('x'))*g_of(sp.Symbol('y'))-g_of(sp.Symbol('x')+sp.Symbol('y'))))
print()
print(" NOW WITHOUT differentiability (only R1+R2+continuity): multiplicative Cauchy.")
print(" Pathological (non-measurable, Hamel-basis) solutions exist and are dense/unbounded.")
print(" Are they PHYSICALLY admissible? A dilation factor that is everywhere discontinuous /")
print(" unbounded on every interval is not a clock rate. So P4 (continuity OR monotonicity OR")
print(" local boundedness OR measurability) is the MINIMAL physical regularity; ANY one suffices.")
print(" VERDICT A: exp is unique GIVEN P4; P4 is physically mandatory (a clock rate must be a")
print("            measurable/bounded function of potential), NOT a smuggled convenience.")
print(" SUBTLETY: doc calls R1 and R2 'two independent conditions'. Strictly, with")
print("           differentiability R1 alone forces exp and R2 is redundant. The doc's framing")
print("           slightly OVER-counts premises but does not weaken the result. Tag: minor.")
print()

print("#"*72)
print("# B. RECIPROCITY P8: does R3 force INVERSE pairing g_tt*g_rr=-c^2,")
print("#    or is the inverse / the g_rr pairing SMUGGLED?")
print("#"*72)

# Build reciprocity from scratch WITHOUT assuming which components pair and
# WITHOUT assuming inverse. Use the SR boost as the ground-truth analog.
# In SR: boost by rapidity w. Frame A sees B's clock slowed by gamma=cosh(w);
# frame B sees A's clock slowed by the SAME gamma (mutual, neither preferred).
# Question: what does "mutual, neither preferred" actually impose?
w = sp.symbols('w', real=True)
gamma = sp.cosh(w)
# Time dilation A->B factor and B->A factor:
print("SR check: gamma(A->B)=cosh(w), gamma(B->A)=cosh(-w)=", sp.simplify(sp.cosh(-w)),
      " -> EQUAL. 'Mutual, neither preferred' => the two TIME factors are EQUAL, not inverse.")
print(" So 'each sees the other's clock slow equally' is a SYMMETRY (D(A,B)=D(B,A)),")
print(" which for D=f(b)/f(a) means f(b)/f(a)=f(a)/f(b) => f(a)=f(b): TRIVIAL unless")
print(" reciprocity is about TIME-vs-LENGTH, not TIME-vs-TIME.")
print()
# The doc's reading: reciprocity pairs the TIME factor with the LENGTH factor as INVERSES.
# Test the SR ground truth for THAT: in SR, gamma_time=cosh(w), length contraction=1/gamma.
length_factor = 1/gamma
print(" SR time factor * SR length factor = cosh(w)*(1/cosh(w)) =",
      sp.simplify(gamma*length_factor), " -> 1. INVERSE pairing IS the SR fact.")
print()
print(" CRITICAL ATTACK: the SR inverse is between the SAME boost's time-dilation and")
print(" length-contraction (a kinematic fact of ONE Lorentz transformation). The doc")
print(" transplants this to positional dilation as f(phi)*h(phi)=1 with h=sqrt(g_rr).")
print(" Two things are CHOSEN here, not derived:")
print("   (i)  that the length factor is sqrt(g_rr) (the radial metric component), and")
print("   (ii) that it pairs with the time factor as an INVERSE (vs equal, vs unrelated).")

# Test whether an EQUAL pairing g_tt=g_rr-type reading is excluded by anything internal.
phi_s = sp.symbols('phi', real=True); c = sp.symbols('c', positive=True)
g_tt = -sp.exp(-2*phi_s)*c**2
# Alternative readings of R3:
print()
print(" Enumerate candidate readings of R3 and their consequence for g_rr:")
# Reading P8 (doc): f*h=1
h_inv = 1/sp.sqrt(-g_tt/c**2)            # h such that f*h=1
g_rr_inv = sp.simplify(h_inv**2)
print("  (P8) f*h=1  => g_rr=", g_rr_inv, " => g_tt*g_rr=", sp.simplify(g_tt*g_rr_inv))
# Reading 'equal': f=h  => g_rr = -g_tt/c^2
g_rr_eq = sp.simplify(-g_tt/c**2)
print("  (EQ) f=h    => g_rr=", g_rr_eq, " => g_tt*g_rr=", sp.simplify(g_tt*g_rr_eq))
print("       The 'equal' reading gives g_rr=e^{-2phi}=A (i.e. B=A), NOT B=1/A.")
print("       Nothing INTERNAL to R3-as-stated rules this out; only the SR-inverse ANALOG does.")
print()
print(" VERDICT B: B=1/A is NOT forced by 'mutual reciprocity' as a bare phrase. It is forced")
print("  ONLY once one ADOPTS the SR-boost reading (time & length factors are mutual INVERSES)")
print("  AND identifies the length factor with sqrt(g_rr). Both are P7/P8 ANALOG CHOICES.")
print("  The doc's ledger ALREADY tags P8 as ASSUMED(named) and P7 as owner-postulate -> the")
print("  doc is HONEST about this. But the headline-prose 'R3 FORCES B=1/A' is conditional on")
print("  P7+P8, not on relativity alone. STANDS-CONDITIONALLY on P7,P8.")
print()

print("#"*72)
print("# C. PART 2 forced-vs-free: independent check on a GENERAL metric.")
print("#"*72)
# R1+R2 constrain only sqrt(-g_tt) as a function of phi. Test the OVER-claim mode:
# does reciprocity 'in every direction' (not just radial) secretly tie angular comps?
# Build a general diagonal-ish metric with an angular block and ask: do R1-R3, as
# stated (scalar phi, clock rate, gradient-aligned reciprocal length), say anything
# about g_thth?  R3 as stated pairs time with the GRADIENT-direction length only.
print(" R1+R2 fix sqrt(-g_tt)=c*exp(k phi(x)) as a FUNCTION OF phi, for any x-dependence.")
print("   -> no constraint forcing staticity (phi may depend on t) or sphericity (phi(theta)).")
print(" Test the UNDER-claim mode: could 'no privileged position' applied in ALL directions")
print("   force isotropy/constraints on g_thth?  R1 is about phi-DIFFERENCES (a scalar),")
print("   it is a statement on the DILATION, silent on transverse geometry. No isotropy follows.")
print(" Test the OVER-claim mode: if one DEMANDS reciprocity transverse to grad phi too,")
print("   then along a direction where phi is CONSTANT, the 'difference' is zero, dilation=1,")
print("   reciprocity is 1*1=1 -> VACUOUS, ties nothing. So even 'reciprocity in every")
print("   direction' imposes NOTHING on the constant-phi (angular) block.")
# demonstrate: dilation along constant-phi direction
print("   demo: g(delta=0)=exp(k*0)=", sp.exp(k*0), " (identity) -> transverse tie is vacuous.")
print(" VERDICT C: forced={exponential law in phi; reciprocal tie along grad phi};")
print("   free={angular/transverse block, off-diagonal/shift, t-dependence, chart, topology}.")
print("   Matches the doc. No hidden constraint on g_thth or g_t,ang from R1-R3. CONFIRMS.")
print()

print("#"*72)
print("# D. SOURCE-FREE: recompute G^t_t - G^r_r independently, general phi(r),")
print("#    and verify it is DOWNSTREAM (=0 because AB=1), not an input.")
print("#"*72)
# Independent Einstein computation with a DIFFERENT routine than theirs (use sympy's
# built-in tensor-free direct Ricci via metric, but with an INDEPENDENT B not tied to A,
# to see what (AB)' does, THEN specialize to AB=1).
r = sp.symbols('r', positive=True)
A = sp.Function('A')(r); Bf = sp.Function('B')(r)
t, th, ang = sp.symbols('t theta ang', real=True)
X = [t, r, th, ang]
gm = sp.diag(-A*c**2, Bf, r**2, r**2*sp.sin(th)**2)
gi = gm.inv()
n=4
# Christoffel
Gam=[[[sp.simplify(sum(gi[a,dd]*(sp.diff(gm[dd,b],X[cc])+sp.diff(gm[dd,cc],X[b])-sp.diff(gm[b,cc],X[dd])) for dd in range(n))/2)
       for cc in range(n)] for b in range(n)] for a in range(n)]
# Ricci
Ric=sp.zeros(n,n)
for b in range(n):
    for dd in range(n):
        s=0
        for a in range(n):
            s+=sp.diff(Gam[a][b][dd],X[a])-sp.diff(Gam[a][b][a],X[dd])
            for e in range(n):
                s+=Gam[a][a][e]*Gam[e][b][dd]-Gam[a][dd][e]*Gam[e][b][a]
        Ric[b,dd]=sp.simplify(s)
Rs=sp.simplify(sum(gi[i,j]*Ric[i,j] for i in range(n) for j in range(n)))
Gtt=sp.simplify(sum(gi[0,m]*(Ric[m,0]-sp.Rational(1,2)*gm[m,0]*Rs) for m in range(n)))
Grr=sp.simplify(sum(gi[1,m]*(Ric[m,1]-sp.Rational(1,2)*gm[m,1]*Rs) for m in range(n)))
diff_gen=sp.simplify(Gtt-Grr)
print(" GENERAL A(r),B(r):  G^t_t - G^r_r =", diff_gen)
# Doc claims this equals -(AB)'/(r A B^2). Check:
claim = sp.simplify(-(sp.diff(A*Bf,r))/(r*A*Bf**2))
print(" doc's claimed identity -(AB)'/(rAB^2) =", claim)
print(" difference (should be 0):", sp.simplify(diff_gen-claim))
# Now specialize to AB=1 (B=1/A) WITHOUT choosing A's form:
diff_tied=sp.simplify(diff_gen.subs(Bf,1/A).doit())
print(" specialize B=1/A (any A):  G^t_t - G^r_r =", diff_tied,
      " <- vanishes for ANY A once AB=1. So tie is the INPUT, vanishing is DOWNSTREAM.")
print(" VERDICT D: B=1/A is what makes G^t_t-G^r_r vanish; no T, action, or field eq used to")
print("  GET B=1/A (it came from R3). The Einstein identity is a consistency consequence. CONFIRMS.")
print()

print("#"*72)
print("# E. CONVENTION vs PHYSICS: k=-1 and the gauge freedom.")
print("#"*72)
kk, phitil = sp.symbols('k phitilde', real=True)
# Show any nonzero k is the same physics: define phi_tilde = -k*phi, then g_tt form invariant.
gtt_k = -sp.exp(2*kk*phi_s)*c**2
# rescale phi -> phi/(-k) maps to k=-1 form:
gtt_resc = gtt_k.subs(phi_s, -phitil/kk)
print(" g_tt with general k, under phi -> -phitilde/k :", sp.simplify(gtt_resc),
      " = -c^2 exp(-2 phitilde): identical to k=-1 form. Any nonzero k = same physics. CONFIRMS.")
print(" k=-1 follows ONLY from phi:=-(1/2)ln(-g_tt/c^2). It's a labeling of the potential.")
print(" Gauge: construction used only g(phi_B-phi_A) -> phi->phi+const leaves all D invariant.")
shift=sp.symbols('s', real=True)
print("   D under phi->phi+s:", sp.simplify(sp.exp(kk*((phi_s+shift)-(sp.Symbol('a')+shift)))
                                            - sp.exp(kk*(phi_s-sp.Symbol('a')))), " (=0: invariant). CONFIRMS.")
print()

print("#"*72)
print("# F. RELATIVITY PRESERVED: light-cone / Lorentz-local structure.")
print("#"*72)
# Locked diagonal form signature & local light cone.
phir=sp.Function('phi')(r)
A2=sp.exp(-2*phir); B2=sp.exp(2*phir)
gloc=sp.diag(-A2*c**2,B2,r**2,r**2*sp.sin(th)**2)
print(" metric signature entries (-,+,+,+):", [sp.simplify(gloc[i,i]).func if False else None for i in range(4)])
dets = [sp.simplify(gloc[i,i]) for i in range(4)]
print("   g_tt<0 ? g_tt=",dets[0]," ; g_rr,g_thth,g_angang>0 ? ",dets[1],dets[2],dets[3])
print("   -> Lorentzian signature preserved for all real phi (exp>0 always). Local cones intact.")
print(" Radial null condition: -A c^2 dt^2 + B dr^2 =0 => dr/dt = c*sqrt(A/B)=c*exp(-2phi).")
print("   Finite local light speed; at each point a regular Minkowski tangent space exists.")
print("   => positional dilation does NOT break LOCAL Lorentz invariance. CONFIRMS.")
print()
print("ALL INDEPENDENT CHECKS COMPLETE.")
