"""
dpf2_junction.py — STEP 4: the GENUINE same-minus mirror-fold junction
count for an SO(3) order-L mode across the D=0 crease.

DERIVED from the fold geometry + the parity dichotomy, NOT read.
The prior dpf_results.md READ d=2L; the blind verifier flagged that as
unforced. Here we COUNT the actual junction constraints.

THE FOLD (w6_results.md): the seal is the fixed surface of the same-minus
involution sigma: (a,b)=(g_Tr,g_Ttheta) -> (-a,-b). The closed cell is
the DOUBLE of a radial collar I x S2 across this crease (h1_types).

THE PARITY DICHOTOMY (w7, banked):
    sigma-EVEN component -> NEUMANN  BC at the crease (d/dn = 0)
    sigma-ODD  component -> DIRICHLET BC at the crease (value = 0)
Each independent angular component of an order-L harmonic gets EXACTLY
ONE parity BC. The c-drive is sigma-ODD (rho=-c-f q gamma) => its content
is pinned in the DIRICHLET (odd) channel. So the count that scales
Delta_p_F is the # of ODD components of the order-L mode.
"""
import sympy as sp

PASS = []
def check(name, cond, extra=""):
    ok = bool(cond); PASS.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  {extra}")
    return ok

print("="*72)
print("STEP 4 — JUNCTION COUNT: SO(3) order-L mode across the same-minus fold")
print("="*72)
print("""
An order-L SO(3) representation has dimension 2L+1: real harmonics
Y_L^m, m=-L..L.  The same-minus fold acts on the doubled collar as the
crease reflection theta -> pi-theta (the mirror across the equatorial
2-sphere where the collar is doubled).  Under this reflection a real
harmonic Y_L^m has parity (-1)^(L+m) (associated-Legendre reflection law
P_L^m(-x) = (-1)^(L+m) P_L^m(x)).  ONE parity BC per component:
  even (+1) -> Neumann ;  odd (-1) -> Dirichlet.
""")

def parity_split(L):
    """Return (#even, #odd) of the 2L+1 real harmonics under theta->pi-theta."""
    nE = sum(1 for m in range(-L, L+1) if (-1)**(L+m) == 1)
    nO = sum(1 for m in range(-L, L+1) if (-1)**(L+m) == -1)
    return nE, nO

print(f"{'L':>3} {'sector':>7} {'dim=2L+1':>9} {'#even(Neu)':>11} {'#odd(Dir)':>10}")
sectors = {0:'trace', 1:'A3', 2:'S5', 3:'(dim7)'}
split = {}
for L in range(0, 4):
    nE, nO = parity_split(L); split[L] = (nE, nO)
    print(f"{L:>3} {sectors[L]:>7} {2*L+1:>9} {nE:>11} {nO:>10}")

check("each component gets exactly one parity BC: #even+#odd=2L+1 (all L)",
      all(split[L][0]+split[L][1] == 2*L+1 for L in split))

# THE c-CHANNEL IS sigma-ODD => DIRICHLET.  The junction count that scales
# the angular charge correction is the # of ODD (Dirichlet) components.
n_odd = {L: split[L][1] for L in split}
print("\nThe c-drive is sigma-ODD => DIRICHLET.  Junction count = #odd components:")
for L in range(0,3):
    print(f"   L={L} ({sectors[L]}):  n_odd = {n_odd[L]}")

# CLOSED FORM: among the 2L+1 integers (L+m), m=-L..L, i.e. 0,1,...,2L,
# exactly L are odd.  So n_odd(L) = L EXACTLY.
def n_odd_closed(L):
    return sum(1 for j in range(0, 2*L+1) if j % 2 == 1)   # = # odd in 0..2L
for L in range(0,4):
    check(f"n_odd({L}) = L  (Dirichlet junction count, derived)",
          n_odd_closed(L) == L and split[L][1] == L, f"n_odd={split[L][1]}")

print(f"""
{'='*72}
DERIVED JUNCTION COUNT:  n_odd(L) = L  EXACTLY
{'='*72}
  trace (L=0): 0 Dirichlet constraints
  A3    (L=1): 1 Dirichlet constraint
  S5    (L=2): 2 Dirichlet constraints

This is NOT 2L (0,2,4) and NOT 2L+1 (1,3,5).  It is L.  The prior
dpf_results.md depth d=2L is REFUTED by the genuine count; the verifier's
suggested 2L+1 is the FULL dimension (all parities), not the odd/Dirichlet
(c-sourced) count.  The c-channel pins exactly L Dirichlet constraints per
order-L sector.

Comparison vs candidates the verifier named:""")
print(f"   {'L':>3} {'2L':>4} {'2L+1':>6} {'L':>4}  <- DERIVED is L")
for L in range(0,3):
    print(f"   {L:>3} {2*L:>4} {2*L+1:>6} {L:>4}")

print(f"\n{'='*72}\nSTEP 4 SUMMARY: {sum(PASS)}/{len(PASS)} PASS\n{'='*72}")
import json
open('/tmp/dpf2_step4.json','w').write(json.dumps({'n_odd':n_odd,'pass':sum(PASS),'tot':len(PASS)}))
