"""
BLIND VERIFIER — CLAIM 2: time-live converts sign-definite damping to omega^2>0 standing waves.
Two parts:
 (PART A) the LOGIC: sign-definite-negative L_space + positive M + a -omega^2 (wave) time term => omega^2>0.
 (PART B) the SIGN of the d_t^2 coefficient in the l=2 quadrupole vacuum equation, recomputed FROM SCRATCH
          (independent full Christoffel->Ricci->Einstein). Confirm it is a WAVE (d_t^2 and d_r^2 OPPOSITE
          relative sign, Lorentzian) and NOT a diffusion/elliptic operator.
"""
import sympy as sp

print("="*70)
print("CLAIM 2 PART A — the logic of the eigenproblem sign")
print("="*70)
# Field eqn in harmonic balance: +d_t^2 u + L_space u = 0 (vacuum wave), u = U e^{i w t}.
# d_t^2 -> -w^2.  => -w^2 M U + L_space U = 0  with M>0 the d_t^2 coefficient (positive).
# => w^2 = <U, L_space U> / <U, M U>.
# Claim: L_space sign-definite NEGATIVE => w^2 = (neg)/(pos)?? Let's be careful with the convention.
# The doc writes L_space[U]=w^2 M[U] with w^2 = -<U,L_space U>/<U,M U>, L_space=-l(l+1)W (negative).
# Then -<U,L_space U> = +l(l+1)<U,W U> > 0, divided by M>0 => w^2>0. Confirm the algebra:
l = sp.Symbol('l', positive=True)
W, M = sp.symbols('W M', positive=True)
U = sp.Symbol('U', real=True)
Lspace = -l*(l+1)*W            # sign-definite negative (the wcc/B2 damping)
# eigenproblem as posed in doc: L_space U = w2 M U  => w2 = L_space/M (scalar mode proxy)
# But the doc's omega^2 = -<U,L_space U>/<U,M U>. The two differ by a sign convention in how the
# d_t^2 term is moved. The PHYSICS test is: hyperbolic time term => +d_t^2 in the wave eqn.
# Wave eqn: M d_t^2 u = -(-L_space) u  i.e.  M u_tt = L_space u (with L_space negative restoring).
# u=U e^{iwt}: -M w^2 U = L_space U => w^2 = -L_space/M = +l(l+1)W/M > 0.
w2 = sp.simplify(-Lspace/M)
print("Wave eqn  M u_tt = L_space u,  L_space = -l(l+1)W (negative restoring).")
print("u=U e^{i w t} => w^2 = -L_space/M =", w2, "  > 0 for l>=1, W,M>0 :  STANDING WAVE.")
print("CONTRAST: if the time term were ELLIPTIC/DIFFUSIVE (M u_tt = +(-L_space) u i.e. wrong sign),")
print("          w^2 = +L_space/M = -l(l+1)W/M < 0 => EXPONENTIAL (decay/growth), NOT oscillation.")
print("So the verdict omega^2>0 hinges ENTIRELY on the d_t^2 sign relative to the spatial operator (Part B).")

print()
print("="*70)
print("CLAIM 2 PART B — recompute d_t^2 sign in l=2 quadrupole vacuum eqn FROM SCRATCH")
print("="*70)
t, r, th, ph, eps, c = sp.symbols('t r theta phi epsilon c', positive=True)
h = sp.Function('h')(t, r)
P2 = (3*sp.cos(th)**2 - 1)/sp.Rational(1,1)/2   # P2(cos th) = (3cos^2-1)/2

# Background round metric (flat round bg per phase0 B2 existence test): Minkowski in spherical coords.
# g_tt = -c^2, g_rr = 1, g_thth = r^2(1+eps h P2), g_psps = r^2 sin^2 th (1 - eps h P2).
coords = [t, r, th, ph]
g = sp.zeros(4,4)
g[0,0] = -c**2
g[1,1] = 1
g[2,2] = r**2*(1 + eps*h*P2)
g[3,3] = r**2*sp.sin(th)**2*(1 - eps*h*P2)
ginv = g.inv()

def christoffel(g, ginv, coords):
    n = 4
    Gam = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = 0
                for d in range(n):
                    s += ginv[a,d]*(sp.diff(g[d,b],coords[cc]) + sp.diff(g[d,cc],coords[b]) - sp.diff(g[b,cc],coords[d]))
                Gam[a][b][cc] = sp.Rational(1,2)*s
    return Gam

print("Building Christoffel (exact)...")
Gam = christoffel(g, ginv, coords)

def ricci(Gam, coords):
    n=4
    Ric = sp.zeros(n,n)
    for a in range(n):
        for b in range(n):
            s = 0
            for cc in range(n):
                s += sp.diff(Gam[cc][a][b], coords[cc]) - sp.diff(Gam[cc][a][cc], coords[b])
                for d in range(n):
                    s += Gam[cc][cc][d]*Gam[d][a][b] - Gam[cc][b][d]*Gam[d][a][cc]
            Ric[a,b] = s
    return Ric

print("Building Ricci (exact, this takes a moment)...")
Ric = ricci(Gam, coords)

# Linearize to O(eps): take d/d_eps at eps=0 of G_thth. Compute Einstein G_thth = R_thth - 1/2 g_thth R.
print("Computing Ricci scalar and G_thth to O(eps)...")
Rscalar = 0
for a in range(4):
    for b in range(4):
        Rscalar += ginv[a,b]*Ric[a,b]

G_thth = Ric[2,2] - sp.Rational(1,2)*g[2,2]*Rscalar
# linear order in eps:
G_thth_lin = sp.diff(G_thth, eps).subs(eps, 0)
G_thth_lin = sp.simplify(G_thth_lin)
print("\nG_thth (O(eps)) =")
sp.pprint(G_thth_lin)

# Extract coefficients of h_tt and h_rr
htt = sp.Derivative(h, t, t)
hrr = sp.Derivative(h, r, r)
poly = sp.expand(G_thth_lin)
coef_tt = poly.coeff(htt)
coef_rr = poly.coeff(hrr)
coef_tt = sp.simplify(coef_tt)
coef_rr = sp.simplify(coef_rr)
print("\ncoeff of h_tt =", coef_tt)
print("coeff of h_rr =", coef_rr)
ratio = sp.simplify(coef_tt/coef_rr)
print("ratio coeff(h_tt)/coeff(h_rr) =", ratio)
print("Is the d_t^2 coefficient nonzero (theta-dependent, survives)?", coef_tt != 0)

# Lorentzian test: for a WAVE, coeff(h_tt)/coeff(h_rr) must be NEGATIVE (opposite relative sign)
# and (with c) ~ -1/c^2. Evaluate sign at a generic theta (avoid the P2 node).
sign_ratio = ratio.subs({th: sp.pi/3, c: 1})
print("ratio at theta=pi/3, c=1 =", sp.simplify(sign_ratio))
print()
if sp.simplify(sign_ratio) < 0:
    print(">>> coeff(h_tt) and coeff(h_rr) have OPPOSITE sign => LORENTZIAN WAVE operator (d_t^2, d_r^2 opposite).")
    print(">>> This is a WAVE (-omega^2 in harmonic balance), NOT a diffusion/elliptic term.  CLAIM 2 sign CONFIRMED.")
else:
    print(">>> SAME sign => elliptic/parabolic (diffusion). Would give omega^2<0. CLAIM 2 REFUTED.")

# Also confirm the 1/c^2 structure (wave speed): ratio should be -1/c^2 * (theta factor)
print("\nFull ratio symbolic:", sp.simplify(ratio*c**2))
