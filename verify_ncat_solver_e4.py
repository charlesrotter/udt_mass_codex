import sympy as sp, random
r,th=sp.symbols('r theta',real=True)
phi=sp.Symbol('phi',real=True); kap,k=sp.symbols('kappa k',positive=True)
Grs,Gts,Gs=sp.symbols('Gr Gt G',real=True)

# CORRECT I4 from the derive script (== my independent derivation):
I4_correct = Grs**2*k**2*kap*sp.exp(-phi)*sp.sin(Gs)**2/(2*sp.sin(th)) \
           + Gts**2*k**2*kap*sp.exp(phi)*sp.sin(Gs)**2/(2*r**2*sp.sin(th))

# What the SOLVER codes (phase2_held.py line 49 / phase2_solve.py line 64):
# e4=(k**2*kap/2)*sinG2*(em2*Gr**2 + Gt**2*e2/R**2)*eph*sth
# where em2=e^{-2phi}, e2=e^{2phi}, eph=e^{phi}, sth=sin th
I4_solver = (k**2*kap/2)*sp.sin(Gs)**2*(sp.exp(-2*phi)*Grs**2 + Gts**2*sp.exp(2*phi)/r**2)*sp.exp(phi)*sp.sin(th)

print("I4_correct =", sp.simplify(I4_correct))
print("I4_solver  =", sp.simplify(I4_solver))
print("ratio solver/correct =", sp.simplify(I4_solver/I4_correct))
random.seed(2)
print("\nnumeric (k=2,kap=1):")
for _ in range(4):
    s={r:random.uniform(0.5,4),th:random.uniform(0.2,2.8),phi:random.uniform(-0.6,0.05),
       kap:1.0,k:2.0,Grs:random.uniform(-1,1),Gts:random.uniform(-1,1),Gs:random.uniform(0.1,3)}
    print(f"  correct={float(I4_correct.subs(s)):+.5f}  solver={float(I4_solver.subs(s)):+.5f}")
