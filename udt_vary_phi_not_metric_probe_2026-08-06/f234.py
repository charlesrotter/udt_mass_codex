import sympy as sp
r,cc = sp.symbols('r c', positive=True)
Rt = sp.symbols('Rt', positive=True)   # Rt := A/B (ratio), free-standing
Pr = sp.symbols('Pr', positive=True)   # Pr := A*B (product), free-standing
# c_eff^2 = c^2 * Rt ; A*B = Pr independent.
print("c_eff^2 = c^2 * (A/B). c_eff fixes ONLY the ratio A/B; A*B is independent.\n")

# --- F2: proper-measured light speed = c_eff ---
# proper dl/dtau for a radial null ray = c * sqrt(B/A)*sqrt(A/B) = c  (invariant, no r-dep)
dl_dtau = cc*sp.sqrt(1/Rt)*sp.sqrt(Rt)      # = c  identically
dl_dtau = sp.powsimp(dl_dtau, force=True)
print("F2: proper dl/dtau(light) =", dl_dtau, " (invariant c, r-INDEPENDENT)")
# impose = c_eff = c sqrt(Rt):  c = c sqrt(Rt) -> Rt=1 -> A=B
sol = sp.solve(sp.Eq(dl_dtau, cc*sp.sqrt(Rt)), Rt)
print("    impose dl/dtau=c_eff -> A/B =", sol, "=> A=B, c_eff=c CONST (degenerate);")
print("    then A*B = A^2 = FUNCTION but c_eff variation KILLED.\n")

# --- F3: g_tt*g_xx = -c_eff^2 literally ---
A,B = sp.symbols('A B', positive=True)
eqF3 = sp.Eq(-cc**2*A*B, -cc**2*A/B)         # g_tt g_xx = -c_eff^2
solB = sp.solve(eqF3, B)
print("F3: g_tt*g_xx=-c_eff^2 -> B =", solB, "=> B=1 forced; A*B=A=FUNCTION (un-blind), degenerate ruler.\n")

# --- F4: c_eff the field u; natural reciprocal readings ---
u = sp.symbols('u', positive=True)   # u = c_eff/c
for name,(Af,Bf) in {
 "4a A=u,   B=1/u  ": (u,1/u),
 "4b A=u^2, B=1/u^2": (u**2,1/u**2),
 "4c A=u^2, B=1    ": (u**2,sp.Integer(1)),
 "4d A=1,   B=1/u^2": (sp.Integer(1),1/u**2),
}.items():
    ratio=sp.simplify(Af/Bf); prod=sp.simplify(Af*Bf)
    ok = sp.simplify(ratio-u**2)==0
    tag = "FUNCTION (UN-BLIND)" if prod!=1 else "CONST=1 (BLIND)"
    print(f"F4 {name}: A/B={ratio} c_eff-consistent?{ok}; A*B={prod} => {tag}")
