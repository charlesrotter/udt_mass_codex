"""Re-verify the two asymptotic exponents with exact Bessel-derivative fluxes.

Identities used (standard, exact):
  d/dx [x^-nu I_nu(x)] = +x^-nu I_{nu+1}(x)
  d/dx [x^-nu K_nu(x)] = -x^-nu K_{nu+1}(x)
"""
import mpmath as mp
mp.mp.dps = 60

q = mp.mpf(1)/3; beta = q/2; nu = mp.mpf(5)/2
PASS = 0; FAIL = 0
def check(name, ok, detail=""):
    global PASS, FAIL
    PASS += ok; FAIL += (not ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")

def x_of(y, lam): return mp.sqrt(lam)*y**beta/beta
def aR(y, lam):
    x = x_of(y, lam); return x**(-nu)*mp.besseli(nu, x)
def aS(y, lam):
    x = x_of(y, lam); return x**(-nu)*mp.besselk(nu, x)
def daR(y, lam):
    x = x_of(y, lam); return (x**(-nu)*mp.besseli(nu+1, x))*(beta*x/y)
def daS(y, lam):
    x = x_of(y, lam); return (-x**(-nu)*mp.besselk(nu+1, x))*(beta*x/y)
def w(y): return y**(2-q/2)
def D_of(lam):
    x0 = mp.sqrt(lam)/beta
    return mp.sqrt(lam)*mp.besseli(nu+1,x0)/mp.besseli(nu,x0)

# 1. deep-end flux exponent: w a a' ~ y^(1+q/2) = y^(7/6)
lam = mp.mpf(2)
ys = [mp.mpf('1e-12'), mp.mpf('1e-15')]
fl = [w(y)*aR(y,lam)*daR(y,lam) for y in ys]
slope = mp.log(fl[1]/fl[0])/mp.log(ys[1]/ys[0])
check("deep-end flux exponent -> 7/6", abs(slope - mp.mpf(7)/6) < mp.mpf('1e-4'), mp.nstr(slope,12))

# 2. two-end K with exact fluxes; off-diagonal exponent 5q/2 = 5/6, K_cc exponent too
def two_end_K(yc, lam):
    M = mp.matrix([[aR(yc,lam), aS(yc,lam)],[aR(1,lam), aS(1,lam)]])
    Mi = M**-1
    K = mp.zeros(2,2)
    for j,(uc,u0) in enumerate(((1,0),(0,1))):
        c = Mi*mp.matrix([uc,u0])
        K[0,j] = -w(yc)*(c[0]*daR(yc,lam)+c[1]*daS(yc,lam))
        K[1,j] =  w(mp.mpf(1))*(c[0]*daR(1,lam)+c[1]*daS(1,lam))
    return K

lam = mp.mpf(1)/2
rows = []
for yc in (mp.mpf('1e-10'), mp.mpf('1e-12'), mp.mpf('1e-14')):
    K = two_end_K(yc, lam)
    rows.append((yc, K[0,0], K[0,1], K[1,1]))
    print("   yc=", mp.nstr(yc,3), " K_cc=", mp.nstr(K[0,0],10), " K_c0=", mp.nstr(K[0,1],10),
          " K_00=", mp.nstr(K[1,1],14))
e_off = mp.log(abs(rows[2][2]/rows[1][2]))/mp.log(rows[2][0]/rows[1][0])
check("end-to-end coupling exponent -> 5/6", abs(e_off - mp.mpf(5)/6) < mp.mpf('1e-4'), mp.nstr(e_off,12))
e_cc = mp.log(abs(rows[2][1]/rows[1][1]))/mp.log(rows[2][0]/rows[1][0])
check("deep-end diagonal exponent -> 5/6", abs(e_cc - mp.mpf(5)/6) < mp.mpf('1e-3'), mp.nstr(e_cc,12))
check("K_00 -> D(lam)", abs(rows[2][3]-D_of(lam))/D_of(lam) < mp.mpf('1e-9'),
      f"{mp.nstr(rows[2][3],14)} vs {mp.nstr(D_of(lam),14)}")

# K_cc leading coefficient check: does K_cc ~ c yc^(5/6)? same exponent as coupling.
# also lam=2 exponents for E1-relevant modes
lam = mp.mpf(2)
rows2 = []
for yc in (mp.mpf('1e-12'), mp.mpf('1e-14')):
    K = two_end_K(yc, lam)
    rows2.append((yc, K[0,1]))
e2 = mp.log(abs(rows2[1][1]/rows2[0][1]))/mp.log(rows2[1][0]/rows2[0][0])
check("lam=2 end-to-end coupling exponent -> 5/6", abs(e2 - mp.mpf(5)/6) < mp.mpf('1e-4'), mp.nstr(e2,12))

print(f"TOTAL: {PASS} PASS, {FAIL} FAIL")
