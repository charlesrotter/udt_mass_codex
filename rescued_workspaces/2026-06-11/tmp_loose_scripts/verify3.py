import sympy as sp
from sympy import gcd
n = sp.symbols('n')

# R1: P = 2n(n+1)/(2n-1). 2n-1 odd, coprime to 2 and to n? gcd(2n-1,n)=gcd(-1,n)=1; gcd(2n-1,n+1)=gcd(2n-1, 2n+2 -(2n-1)? ) check
# Integer iff (2n-1) | 2n(n+1). Since gcd(2n-1,2)=1, gcd(2n-1,n)=1 -> need (2n-1)|(n+1). (n+1)<(2n-1) for n>=3 -> impossible except small.
for k in range(1,200):
    val = 2*k*(k+1)
    if val % (2*k-1)==0:
        print("R1 integer at n=",k, "value=", val//(2*k-1))
print("---")
# R3: 2n(n+1)/(2n+3). (2n+3)|2n(n+1). gcd(2n+3,2)=1. need (2n+3)|n(n+1). 4n(n+1)=(2n+3)(2n-1)+3 -> (2n+3)|3 -> 2n+3 in {3} ->n=0 only.
for k in range(1,500):
    if (2*k*(k+1)) % (2*k+3)==0:
        print("R3 integer at n=",k)
print("done R3")
# R2,R4: denom (2n+1)^2. 4n(n+1)= (2n+1)^2 -1, so gcd(2n(n+1),(2n+1))=? (2n+1)| numerator? numerator R2 = 2n(n+1)(2n-1). (2n+1) coprime to 2n,(n+1)?,(2n-1). gcd(2n+1,2n-1)=gcd(2n+1,2)=1. So (2n+1)^2 never divides -> never integer for n>=1.
for k in range(1,1000):
    num=2*k*(k+1)*(2*k-1); 
    if num % (2*k+1)**2==0: print("R2 integer n=",k)
    num4=2*k*(k+1)*(2*k+3)
    if num4 % (2*k+1)**2==0: print("R4 integer n=",k)
print("done R2/R4")
# R5: num 2n(n+1)(2n-1), den (2n-3)(2n+1)
for k in range(1,2000):
    num=2*k*(k+1)*(2*k-1); den=(2*k-3)*(2*k+1)
    if den!=0 and num%den==0: print("R5 integer n=",k, num//den)
print("done R5")
# R6: num 2n(n+1)(2n-3), den (2n-1)(2n+1)
for k in range(1,2000):
    num=2*k*(k+1)*(2*k-3); den=(2*k-1)*(2*k+1)
    if num%den==0: print("R6 integer n=",k, num//den)
print("done R6")
