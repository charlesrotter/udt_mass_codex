from math import comb
from fractions import Fraction as Fr

# Diophantine self-consistency (CG §13.10):
#   (2j+1)^2 * (2l+1) * (2kmax+1) = C(2l + 2kmax + 1, 2l+1)
# i.e. (spin^2) * a * b = dim Sym^a(R^b), with a=2l+1, b=2kmax+1 (both odd).
# Claim: (j,l,kmax)=(1/2,1,3) -> 4*3*7 = C(9,3) = 84, UNIQUELY.
# Target-blind exhaustive search.

print("Exhaustive search of  (2j+1)^2 * a * b = C(a+b-1, a),  a=2l+1, b=2kmax+1 odd")
print("="*72)
sols = []
# j half-integer or integer: 2j+1 = s in 2..12 (j=1/2..11/2 and integers)
for s in range(2, 13):                 # s = 2j+1  (s=2 -> j=1/2)
    for l in range(0, 60):
        a = 2*l+1
        for kmax in range(1, 60):
            b = 2*kmax+1
            lhs = s*s * a * b
            rhs = comb(a+b-1, a)        # = dim Sym^a(R^b) = C(2l+2kmax+1, 2l+1)
            if lhs == rhs:
                sols.append((s, l, kmax, a, b, lhs))

print(f"{'2j+1':>5} {'j':>5} {'l':>3} {'kmax':>5} {'a=2l+1':>7} {'b=2k+1':>7} {'value':>8}")
for s,l,kmax,a,b,val in sols:
    j = Fr(s-1,2)
    star = "   <== the pion triple (84)" if (s,l,kmax)==(2,1,3) else ""
    print(f"{s:>5} {str(j):>5} {l:>3} {kmax:>5} {a:>7} {b:>7} {val:>8}{star}")

print("\nTotal solutions found:", len(sols))

# focus: solutions with s=2 (j=1/2)
s2 = [x for x in sols if x[0]==2]
print(f"\nSolutions with j=1/2 (s=2):  {len(s2)}")
for s,l,kmax,a,b,val in s2:
    print(f"   l={l}, kmax={kmax}: 4*{a}*{b} = C({a+b-1},{a}) = {val}")

# also report the degenerate small-value family (a=1 etc.) to be honest
print("\nNote any trivial/degenerate solutions (a=1 i.e. l=0, or b=1):")
for s,l,kmax,a,b,val in sols:
    if a==1 or b==1:
        print(f"   s={s} l={l} kmax={kmax} (a={a},b={b}) val={val}  [degenerate]")

print("\n" + "="*72)
print("ADVERSARIAL WIDENING: s=1..16 (incl. scalar j=0), l=0..120, kmax=0..120")
print("="*72)
allsol=[]
for s in range(1,17):
    for l in range(0,121):
        a=2*l+1
        for kmax in range(0,121):
            b=2*kmax+1
            if s*s*a*b==comb(a+b-1,a):
                allsol.append((s,l,kmax,a,b))
nondegen=[x for x in allsol if x[3]>1 and x[4]>1]
trivial=[x for x in allsol if x[3]==1 or x[4]==1]
print(f"non-degenerate (a>1 and b>1): {len(nondegen)}")
for s,l,kmax,a,b in nondegen:
    print(f"   2j+1={s} (j={Fr(s-1,2)}), l={l}, kmax={kmax}: {s}^2*{a}*{b}=C({a+b-1},{a})={s*s*a*b}")
print(f"degenerate (a=1 or b=1) count: {len(trivial)}  (a=1 => l=0 s-wave; these are the trivial Sym^1 identities)")
# show that for j=1/2 specifically, uniqueness is total
print("\nj=1/2 (s=2), non-degenerate solutions across the full widened range:")
print([ (l,kmax) for s,l,kmax,a,b in nondegen if s==2 ])
