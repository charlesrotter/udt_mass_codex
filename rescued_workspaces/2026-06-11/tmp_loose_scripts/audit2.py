import math
pi=math.pi
# TASK 3: how many simple O(1) formulas land near r*=6.9875 and phi0=-0.8090?
print("=== TASK 3: O(1) formula density near r*~6.99 and phi0~-0.809 ===")
rstar=6.9875
cands=[]
# simple closed forms of magnitude ~7
import itertools
forms={
 "2*pi+ln(2)":2*pi+math.log(2),
 "7":7.0,
 "9/4*pi":9/4*pi,
 "2*pi+0.7":2*pi+0.7,
 "e+4":math.e+4,
 "3+pi+0.85":3+pi+0.85,
 "sqrt(48.8)":math.sqrt(48.8),
 "20/e":20/math.e,
 "2*pi":2*pi,
 "7.0":7.0,
 "12/sqrt(3)":12/math.sqrt(3),
 "11/phi":11/((1+math.sqrt(5))/2),
}
for n,v in forms.items():
    e=abs(v-rstar)/rstar
    if e<0.02: print(f"  r*: {n}={v:.4f} err={e*100:.2f}%")
# the three given r*-cluster values:
print("  given r*-cluster: 6.965, 7.044, 6.988 ; spread", (7.044-6.965)/6.988*100,"%")
phi0=-0.80902
print(f"\n  phi0=-cos(pi/5)={-math.cos(pi/5):.5f}, alpha-exact=-0.8073, agree to {abs(-0.80902+0.8073)/0.8073*100:.2f}%")
print("  Note: cos(pi/5)=(1+sqrt5)/4 = golden-ratio/2 =", ((1+math.sqrt(5))/2)/2)
