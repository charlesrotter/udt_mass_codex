"""Attack C: the C2 theorem and the gauge lemmas, independently."""
import sympy as sp

r = sp.Symbol("r", positive=True)
f = sp.Function("f", positive=True)(r)
rho = sp.Function("rho", positive=True)(r)

# areal chart: rho as coordinate. g_rhorho = g_rr (dr/drho)^2 = (1/f)/rho'^2
FG = sp.simplify(f * (1/f)/rho.diff(r)**2)
print("F*G =", FG, " | f-blind:", sp.diff(FG, f) == 0)
print("dsolve rho'^2 = 1:", sp.dsolve(sp.Eq(rho.diff(r)**2, 1), rho))

# Lemma 1: y with dy = sqrt(FG) dx
x = sp.Symbol("x", positive=True)
F = sp.Function("F", positive=True)(x)
G = sp.Function("G", positive=True)(x)
print("Lemma 1: g_yy = G*(dx/dy)^2 = G/(F*G) = 1/F:",
      sp.simplify(G*(1/sp.sqrt(F*G))**2 - 1/F) == 0)

# Lemma 2 WITH time rescaling allowed: t = k*ttilde, r = h(rtilde).
k = sp.Symbol("k", positive=True)
rt = sp.Symbol("rtilde", positive=True)
h = sp.Function("h", positive=True)(rt)
fh = sp.Function("f", positive=True)(h)
g_tt_new = -fh*k**2          # dt = k dttilde
g_rr_new = (1/fh)*h.diff(rt)**2
cond = sp.simplify(-g_tt_new*g_rr_new - 1)   # B=1/A in new chart
print("Lemma 2 attack: condition (with t-rescale k) reduces to k^2 h'^2 = 1:",
      sp.simplify(cond - (k**2*h.diff(rt)**2 - 1)) == 0)
print(" => h' = ±1/k: uniqueness up to ±/shift holds ONLY at fixed",
      "Killing-time normalization.")

# R-proper: g_ss = (1/f)*(dr/ds)^2 with ds = dr/sqrt(f) => dr/ds = sqrt(f)
print("R-proper: g_ss =", sp.simplify((1/f)*sp.sqrt(f)**2),
      "=> B=1/A in s-chart forces g_tt = -1, phi = 0")
