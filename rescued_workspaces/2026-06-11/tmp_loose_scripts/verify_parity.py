# CLAIM: the 6 Dirac channels kappa in {-1,+1,-2,+2,-3,+3}, under rank-2 coupling Y_2 with
# parity selection Delta-l = even, split 6x6 into two 3x3 blocks:
#   Block A = {-1,+2,-3},  Block B = {+1,-2,+3}.
# For Dirac on S^2, each kappa has orbital l determined by kappa:
#   kappa = -(l+1) for j=l+1/2  (kappa<0 => l = -kappa-1=|kappa|-1)
#   kappa = +l     for j=l-1/2  (kappa>0 => l = kappa)
def l_of_kappa(k):
    return (-k-1) if k<0 else k
ch=[-1,1,-2,2,-3,3]
for k in ch:
    print(f"kappa={k:+d}  l={l_of_kappa(k)}  parity(l)={'even' if l_of_kappa(k)%2==0 else 'odd'}")
print()
# parity = parity of l. Delta-l = even means coupling connects same-parity l.
even=[k for k in ch if l_of_kappa(k)%2==0]
odd =[k for k in ch if l_of_kappa(k)%2==1]
print("even-l (l in {0,2}):",sorted(even))
print("odd-l  (l in {1,3}):",sorted(odd))
