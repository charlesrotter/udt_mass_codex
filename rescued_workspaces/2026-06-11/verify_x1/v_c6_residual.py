"""C6: over-determination residual of the demanded pair, computed independently.

Demanded pair: F0 = y^-q (q=1/3, s=q(1-q)/2=1/9), kappa_d(y) solving
H(kappa_d) = 2 s y^-q  (this makes the F-equation exact by construction).
a_d = F0 kappa_d / sqrt(3).
Residual in a-equation: R_a(y) = (y^2 a_d')' - 2 P_a(kappa_d).
X1 claim: R_a(1) = -1.108, term size |2P_a| = 1.005.
"""
import mpmath as mp
mp.mp.dps = 30
SQ3 = mp.sqrt(3)
q = mp.mpf(1)/3
s = q*(1-q)/2

def Lf(k): return mp.log((1+k)/(1-k))
def H(k):  return Lf(k)/(2*k) - 1
def Pa(k): return SQ3*(Lf(k)*(1+k**2) - 2*k)/(8*k**2)

def kd(y):
    target = 2*s*y**(-q)
    return mp.findroot(lambda k: H(k) - target, mp.mpf('0.68'))

def a_d(y):
    return y**(-q)*kd(y)/SQ3

def R_a(y):
    # (y^2 a')' = y^2 a'' + 2 y a'
    a1 = mp.diff(a_d, y)
    a2 = mp.diff(a_d, y, 2)
    return y**2*a2 + 2*y*a1 - 2*Pa(kd(y))

y0 = mp.mpf(1)
k1 = kd(y0)
print("kappa_d(1) =", mp.nstr(k1, 10), "(claim 0.6830951)")
print("2*Pa(kd(1)) =", mp.nstr(2*Pa(k1), 8), "(X1 term size 1.005)")
print("R_a(1) =", mp.nstr(R_a(y0), 8), "(X1 claim -1.108)")
# scan a few depths to show order-unity persistence
for yv in ['1.0', '0.8', '0.5', '0.3', '0.2']:
    yv = mp.mpf(yv)
    try:
        print(f"  y={float(yv):4.2f}: R_a={mp.nstr(R_a(yv),6):>12}  "
              f"2Pa={mp.nstr(2*Pa(kd(yv)),6):>10}  kd={mp.nstr(kd(yv),6)}")
    except Exception as e:
        print(f"  y={float(yv):4.2f}: kd does not exist (H range exceeded): {e}")
# H(k) < ln? H -> inf as k->1, so kd exists while 2 s y^-q in range and kd<1:
# H(1^-) = inf so kd exists for all y < 1 actually; check small y
