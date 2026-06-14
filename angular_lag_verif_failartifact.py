import sympy as sp, mpmath as mp
mp.mp.dps=40
th,k=sp.symbols('theta kappa',positive=True)
# substitution u=cos th: INT_{-1}^{1} (1-u^2)/(1+k u) du
u=sp.symbols('u',real=True)
I=sp.integrate((1-u**2)/(1+k*u),(u,-1,1))
print("sympy INT_{-1}^1 (1-u^2)/(1+ku) du:", sp.simplify(I))
L=sp.log((1+k)/(1-k)); G1=(2*k+(k**2-1)*L)/k**3
print("I - G1 (simplified):", sp.simplify(I-G1))
# numeric
for kv in [0.2,0.5,0.8,0.95]:
    iv=mp.quad(lambda x:(1-x**2)/(1+kv*x),[-1,1])
    Lv=mp.log((1+kv)/(1-kv)); g1=(2*kv+(kv**2-1)*Lv)/kv**3
    print(f"  k={kv}: I={mp.nstr(iv,15)} G1={mp.nstr(g1,15)} |diff|={mp.nstr(abs(iv-g1),3)}")
