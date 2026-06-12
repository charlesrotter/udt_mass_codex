import math
pi=math.pi
me=0.511
# TASK 2: alpha and eigenvalue-pion
I2=0.82296
print("=== TASK 2: the 'clean' observables ===")
alpha_inv = 36*pi/I2
print(f"alpha^-1 = 36*pi/I2 = {alpha_inv:.2f}  (PDG 137.036, err {(alpha_inv-137.036)/137.036*100:.2f}%)")
# is 36 fit? what integer makes it exact?
n_exact = 137.036*I2/pi
print(f"  numerator making alpha exact = {n_exact:.3f}  (claimed 36)")
print(f"  36 vs {n_exact:.3f}: off by {(36-n_exact)/n_exact*100:.2f}%  -> 36 is the nearest integer? floor/ceil: {math.floor(n_exact)},{math.ceil(n_exact)}")

# eigenvalue pion
E1=0.94282
C=4*pi**2*me*6.9875
print(f"\nm_pi = E1*C = {E1*C:.2f}  (PDG 139.57? or charged 139.57, neutral 134.98)")
print(f"  C=4pi^2 me r* = {C:.3f}")
print(f"  84pi*me = {84*pi*me:.2f}")
# proton 6pi^5 me
print(f"\nm_p=6pi^5 me={6*pi**5*me:.2f}")
