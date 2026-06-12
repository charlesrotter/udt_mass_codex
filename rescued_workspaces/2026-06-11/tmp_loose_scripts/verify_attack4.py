import numpy as np, math
# ATTACK 4: Born lever-arm legitimacy + reproduce Phase C phase numbers independently.
mu_g = math.pi*math.sqrt(math.pi/3)/13.0
r_CMB=9.164
cphi=math.cos(math.pi/5)
def phi0(rr):
    x=mu_g*rr; return 1.5*x-cphi*x**2+(2/3)*x**3
rg=np.linspace(1e-3,r_CMB-1e-3,8000)
W_TT=rg**2*np.exp(-3*phi0(rg))
W_EE=(r_CMB-rg)/(r_CMB*rg)*np.exp(2*phi0(rg))
W_bare=np.exp(2*phi0(rg))/rg**2
qs=np.linspace(20,700,40)
def kphase(W,q,deriv):
    if not deriv:
        c=np.trapz(W*np.cos(q*rg),rg); s=np.trapz(W*np.sin(q*rg),rg)
    else:
        c=np.trapz(W*(-np.sin(q*rg)),rg); s=np.trapz(W*(-np.cos(q*rg)),rg)
    return math.atan2(s,c)
def dist(d): a=abs(d)%180; return min(a,180-a)
def med(Wk,deriv):
    ds=[]
    for q in qs:
        bTT=kphase(W_TT,q,False); bN=kphase(Wk,q,deriv)
        d=math.degrees(((bN-bTT+math.pi)%(2*math.pi))-math.pi)
        ds.append(dist(d))
    return np.median(ds)
print("pure old (W_EE, no deriv):", round(med(W_EE,False),2), "deg  [S105 ~21 baseline]")
print("new bare kernel e2phi/r^2 (deriv):", round(med(W_bare,True),2), "deg")
print("new Born W_EE form (deriv):", round(med(W_new:=W_EE,True),2), "deg")
print()
# The core attack: WITHOUT born lever-arm the SAME field gives 37 deg, not quadrature.
# Is W_EE Born-form legitimate for the NEW gravitomagnetic deflection?
# The new accel coeff is e^{2phi}/r^2 * d_theta h_tr (SAME per-point kernel as scalar 2 e2phi/r^2 d_theta dphi).
# Born accumulation of an angular ACCEL into a deflection POTENTIAL adds (r_CMB-r)/(r_CMB r).
# This is geometric (lever arm of deflection at distance r mapped to observer), identical
# for ANY transverse acceleration. So applying W_EE Born to the new term is geometrically
# consistent IF the new term is genuinely a transverse-acceleration of the SAME ray.
# It is (a^theta). So Born is legitimate. BUT: note 37 deg (bare) is NOT quadrature; the
# 66 deg REQUIRES the (r_CMB-r) weighting to push it past 45. Let's see sensitivity:
print("Sensitivity: distance-from-inphase depends heavily on radial weight shape.")
for label,Wk in [("W_EE Born",W_EE),("bare e2phi/r2",W_bare),("flat W=1",np.ones_like(rg)),
                 ("r^2 e-3phi (TT-like) deriv",W_TT)]:
    print(f"  {label:28s}: {round(med(Wk,True),1)} deg")
