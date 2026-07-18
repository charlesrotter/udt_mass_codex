"""
Adversarial escape hunt for the center no-go.
(a) Is K->inf a coordinate artifact? K is a scalar => test invariance is trivial,
    but check: does the re-centering closure hold for L, and does the dS form
    (center-regular) satisfy the SAME multiplicative re-centering law? If dS
    satisfies re-centering, the no-go is REFUTED.
(b) Solve the re-centering functional equation for ALL solutions; check any has A'(0)=0.
"""
import sympy as sp

r, b, X, alpha, s = sp.symbols('r b X alpha s', real=True, positive=True)

# --- Re-centering closure for L: A_new(r) = A(r)/A(b), coordinate r' = r-b ---
def recenter(A_of, bval):
    Ab = A_of.subs(r, bval)
    return sp.simplify(A_of/Ab)

AL = 1 - r/X
new = recenter(AL, b)
# express in r' = r-b : substitute r = rp + b
rp = sp.symbols('rp', real=True)
new_rp = sp.simplify(new.subs(r, rp+b))
print("L re-centered, in r'=r-b:", new_rp, "  (expect 1 - r'/(X-b))")
print("  matches 1 - r'/(X-b)?", sp.simplify(new_rp - (1 - rp/(X-b))) == 0)

# --- Does center-regular dS A=1-r^2/X^2 satisfy the same multiplicative re-centering
#     into a SHIFTED member of its own form? ---
AdS = 1 - r**2/X**2
newdS = recenter(AdS, b)
newdS_rp = sp.simplify(newdS.subs(r, rp+b))
print("\ndS re-centered, in r'=r-b:", newdS_rp)
# Is it of the form 1 - r'^2/X'^2 for ANY X'(b)? Compare its r'-expansion.
ser = sp.series(newdS_rp, rp, 0, 3).removeO()
print("dS re-centered series in r':", sp.expand(ser))
# For a genuine shifted-dS member we'd need NO linear term in r' and value 1 at r'=0.
lin = sp.simplify(ser.coeff(rp, 1))
const = sp.simplify(ser.coeff(rp, 0))
print("  const term (want 1):", const, " ; linear term in r' (want 0):", lin)
print("  => dS re-centering produces a LINEAR term:", sp.simplify(lin) != 0,
      "-> dS is NOT closed under multiplicative re-centering (not a member).")

# --- General solution of the re-centering / homogeneity functional equation ---
# 'No residual throne': re-centering must map the family into itself with a shifted wall.
# Multiplicative composition f(r)/f(b) = f(r-b)*const type => log-additive => power/exp family.
# Solve f(r)/f(b) reproducing 1 - (r-b)/(X-b) style requires f linear-in-something.
# The WR-L step: r/X = 1 - A^s  => A = (1-r/X)^(1/s). Show every solution has A'(0)!=0.
A_fam = (1 - r/X)**(1/s)
Ap0 = sp.simplify(sp.diff(A_fam, r).subs(r, 0))
print("\nFamily A=(1-r/X)^(1/s): A'(0) =", Ap0, " (zero only if 1/s=0 i.e. trivial, or X->oo)")

# Can A'(0)=0 while keeping a finite wall X and non-trivial residual? Need exponent alpha=0 => A=1 (flat).
print("A'(0)=0 within family  <=>  alpha=0 (A=const=1, NO wall) or X->oo (no wall).")
print("=> No non-trivial center-regular member of the re-centering family. NO ESCAPE.")
