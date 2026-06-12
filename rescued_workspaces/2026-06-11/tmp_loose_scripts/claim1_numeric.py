import numpy as np

# Direct numerical scattering test of a phi-step at fixed radius.
# To isolate the impedance question we work in the large-r / locally-Cartesian
# regime where the r^2 geometry is slowly varying compared to the wavelength,
# so the operator reduces to the planar problem:
#   d/dx( e^{-2phi} g' ) + (w^2/c^2) e^{2phi} g = 0
# (drop the 1/r^2 prefactor and r^2 since they are continuous & smooth at the step).
# This is exactly the 1D form whose interface matching is [g]=0, [e^{-2phi} g']=0.
#
# Region a (x<0): phi=phi_a ;  Region b (x>0): phi=phi_b.
# In each region g'' + k^2 g = 0 with k = (w/c) e^{2phi}.
# Incident + reflected in a:  g = e^{i k_a x} + R e^{-i k_a x}
# Transmitted in b:           g = T e^{i k_b x}
# Match g and p g' = e^{-2phi} g' at x=0:
#   1 + R = T
#   e^{-2phi_a} i k_a (1 - R) = e^{-2phi_b} i k_b T
# Let A = e^{-2phi} k  (= p*k since p prefactor e^{-2phi}); then
#   A_a (1-R) = A_b T = A_b (1+R)  -> R = (A_a - A_b)/(A_a + A_b)

c = 1.0; w = 1.0
def test(pa, pb):
    ka = (w/c)*np.exp(2*pa)
    kb = (w/c)*np.exp(2*pb)
    Aa = np.exp(-2*pa)*ka   # = w/c
    Ab = np.exp(-2*pb)*kb   # = w/c
    R = (Aa-Ab)/(Aa+Ab)
    return R, Aa, Ab

for pa,pb in [(0.0,0.5),(0.3,0.9),(-0.4,1.2),(0.0,3.0)]:
    R,Aa,Ab = test(pa,pb)
    print(f"phi_a={pa:+.2f} phi_b={pb:+.2f}: A_a={Aa:.4f} A_b={Ab:.4f} -> R={R:.3e}")

# Now WRONG (acoustic) convention for comparison: if one (incorrectly) matched
# g and g' (continuity of derivative, ignoring the e^{-2phi} weight in flux):
print("\nIf instead matched [g']=0 (acoustic, WRONG for this operator):")
for pa,pb in [(0.0,0.5),(0.3,0.9)]:
    ka=(w/c)*np.exp(2*pa); kb=(w/c)*np.exp(2*pb)
    R=(ka-kb)/(ka+kb)
    print(f"  phi_a={pa} phi_b={pb}: R={R:.4f}  (= -tanh(phi_b-phi_a)={-np.tanh(pb-pa):.4f})")
