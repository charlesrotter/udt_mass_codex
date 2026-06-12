"""BLIND VERIFIER — Claim 2: two-sided Calderon projector algebra."""
import sympy as sp

Dm, Dp, u, lam = sp.symbols('D_minus D_plus u lambda', positive=True)

C = sp.Matrix([[Dp, 1], [Dm*Dp, Dm]]) / (Dm + Dp)
I2 = sp.eye(2)
Cf = sp.simplify(I2 - C)

print("idempotent C^2-C = 0:", sp.simplify(C*C - C) == sp.zeros(2))
print("complement (I-C)^2-(I-C)=0:", sp.simplify(Cf*Cf - Cf) == sp.zeros(2))
print("C (I-C) = 0:", sp.simplify(C*Cf) == sp.zeros(2))

v_core = sp.Matrix([1, Dm])      # core graph p = D_- u
v_far  = sp.Matrix([1, -Dp])     # far graph  p = -D_+ u
print("fixes (1, D_-):", sp.simplify(C*v_core - v_core) == sp.zeros(2,1))
print("annihilates (1, -D_+):", sp.simplify(C*v_far) == sp.zeros(2,1))

print("\nrank/trace:", C.rank(), sp.simplify(sp.trace(C)))

print("\nDirichlet-fiber limit D_+ -> oo:")
Clim = sp.Matrix([[sp.limit(C[i, j], Dp, sp.oo) for j in range(2)] for i in range(2)])
sp.pprint(Clim)
print("banked Cauchy graph projector (corpus 381): [[1,0],[lambda,0]] with lambda=eta/2=1/36")
print("limit equals banked form iff lambda_g = D_-; equality to banked projector requires D_- = 1/36")

print("\nSymmetric weld D_-=D_+=D:")
Cs = C.subs({Dm: sp.Symbol('D'), Dp: sp.Symbol('D')})
sp.pprint(sp.simplify(Cs))
D = sp.Symbol('D', positive=True)
# one-sided harmonic energy with boundary value u: S_side = (1/2) D u^2 per side
S_glued = sp.Rational(1,2)*D*u**2 + sp.Rational(1,2)*D*u**2
print("glued quadratic form (1/2 D + 1/2 D) u^2 =", sp.simplify(S_glued))
print("-> exponent per side (1/2)D u^2; with D=eta/2 and u=1: eta/4 per side??  CHECK normalization:")
print("   if per-side action booked as eta/2 (corpus 380), then identification is")
print("   S_side = (eta/2) u^2 (no 1/2), i.e. D u^2 with D = eta/2 -- normalization convention-dependent")
