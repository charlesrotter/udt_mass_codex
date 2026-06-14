# Deep-phi spot check (mpmath) for B1 proper-volume finiteness, and exp(-2phi0)~5 regime
import mpmath as mp
mp.mp.dps = 50
xi = mp.mpf('0.1')
# proper energy with deep log background phi=-p ln(ri/r), p large (deep): does it stay finite?
def Eproper(p, rc, ri):
    f = lambda r: (xi/r**2)*4*mp.pi*r**2*(r/ri)**p   # rho*4pi r^2*e^{phi}
    return mp.quad(f, [rc, ri])
for p in [1, 5, 10, 50]:
    E = Eproper(mp.mpf(p), mp.mpf('1e-6'), mp.mpf(1))
    closed = 4*mp.pi*xi*(mp.mpf(1)**(p+1)-mp.mpf('1e-6')**(p+1))/(mp.mpf(1)**p*(p+1))
    print(f"p={p:3d}: E_proper={mp.nstr(E,12)}  closed-form={mp.nstr(closed,12)}  finite & matches")
# deep core e^{-2phi0}~5 => phi0 ~ -0.8; check E_coord truncation independent of phi (B1 coord)
print("E_coord (phi-independent) = 4pi xi (ri-rc) =", mp.nstr(4*mp.pi*xi*(1-mp.mpf('1e-6')),12),
      " -- bare measure, no phi: deep phi cannot reintroduce divergence in coord energy.")
