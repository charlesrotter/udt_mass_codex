#!/usr/bin/env python3
"""Source-first independent SD1 axial check; no parent scientific imports."""
import json
import platform
import time
import mpmath as mp

mp.mp.dps = 50
theta = mp.mpf(21)/40
k = mp.mpf(3)/4
c1, c2 = mp.cos(theta), mp.cos(2*theta)
beta = -mp.mpf(3)/2*k*mp.tan(theta)*(1+2*c1*c1)
began = time.monotonic()

def profile(s, Q, eta):
    t, xi = 1+s, mp.mpf(7)/10+s
    aa = [(Q-c2*eta)/c1, eta]
    hh = [-c2/c1, mp.mpf(1)]
    vals = [mp.mpf(0)]*4
    for j in (1, 2):
        w = k*j
        A = -3*mp.pi/4*mp.bessely(0,w)
        B = 3*mp.pi/4*mp.besselj(0,w)
        F = A*mp.besselj(0,w*t)+B*mp.bessely(0,w*t)
        Ft = -w*(A*mp.besselj(1,w*t)+B*mp.bessely(1,w*t))
        co, si = mp.cos(w*xi), mp.sin(w*xi)
        v, vD = F*co, Ft*co-w*F*si
        vals[0] += aa[j-1]*v
        vals[1] += aa[j-1]*vD
        vals[2] += hh[j-1]*v
        vals[3] += hh[j-1]*vD
    return vals

def records(Q, eta, d, n):
    nodes, weights = mp.gauss_quadrature(n, 'legendre')
    def quad(fn, end):
        return end/2*sum(weights[i]*fn(end*(nodes[i]+1)/2) for i in range(n))
    def lapse(s):
        def fn(u, derivative=False):
            P, DP, H, DH = profile(u,Q,eta)
            return (1+u)*(2*DP*DH if derivative else DP*DP)
        return quad(fn,s), quad(lambda u:fn(u,True),s)
    def integrands(s):
        P, DP, H, DH = profile(s,Q,eta)
        lam, dlam = lapse(s)
        common = mp.exp(lam/2)/(1+s)**mp.mpf('1.5')
        iy, iz = common*mp.exp(-P), common*mp.exp(P)
        return iy, iz, iy*(dlam/2-H), iz*(dlam/2+H)
    accum = [mp.mpf(0)]*4
    for i in range(n):
        row = integrands(d*(nodes[i]+1)/2)
        for j in range(4):
            accum[j] += d/2*weights[i]*row[j]
    Iy, Iz, Jy, Jz = accum
    P, DP, H, DH = profile(d,Q,eta)
    lam, dlam = lapse(d)
    R = mp.exp(lam/4)/(1+d)**mp.mpf('.25')
    Dy = k*mp.sqrt(1+d)*mp.exp(P/2)*Iy
    Dz = k*mp.sqrt(1+d)*mp.exp(-P/2)*Iz
    return dict(R=R,Dy=Dy,Dz=Dz,W=mp.log(Dy/Dz),
                dlogR=dlam/4,dW=H+Jy/Iy-Jz/Iz,
                expected_dW_coefficient=beta/3,
                expected_dlogR_coefficient=mp.mpf(3)/2*Q*beta/2)

def serial(x):
    if isinstance(x, dict): return {key:serial(value) for key,value in x.items()}
    if isinstance(x, list): return [serial(value) for value in x]
    if isinstance(x,mp.mpf): return mp.nstr(x,46)
    return x

cases = [(mp.mpf(0),mp.mpf(0)), (mp.mpf(0),mp.mpf('.15')),
         (mp.mpf('.3')*c1,mp.mpf('.15'))]
rows=[]
for Q,eta in cases:
    for d in (mp.mpf('.04'),mp.mpf('.02')):
        for n in (8,12):
            result=records(Q,eta,d,n)
            rows.append(dict(Q=Q,eta=eta,d=d,n=n,records=result))
            assert result['Dy']>0 and result['Dz']>0 and result['R']>0
            assert result['dW']<0
            print(json.dumps(serial(rows[-1])),flush=True)
symplus=records(mp.mpf(0),mp.mpf('.15'),mp.mpf('.08'),12)
symminus=records(mp.mpf(0),mp.mpf('-.15'),mp.mpf('.08'),12)
symerrors={key:abs(symplus[key]-symminus[other])
           for key,other in [('R','R'),('Dy','Dz'),('Dz','Dy')]}
assert max(symerrors.values())<mp.mpf('1e-45')
print(json.dumps(serial(dict(type='final',python=platform.python_version(),
    mpmath=mp.__version__,dps=mp.mp.dps,beta=beta,rows=rows,
    symmetry_errors=symerrors,elapsed_seconds=time.monotonic()-began))),flush=True)
