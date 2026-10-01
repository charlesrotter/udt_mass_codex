#!/usr/bin/env python3
"""Reviewer-owned scalar-loop metric-jet checks. No producer imports or Torch."""
import hashlib
import json
from pathlib import Path
import numpy as np


def geometry(g, d, dd):
    """d[a,m,n]=partial_a g_mn; dd[a,b,m,n]=partial_a partial_b g_mn."""
    inv = np.linalg.inv(g)
    dinv = np.empty((4, 4, 4))
    for a in range(4):
        dinv[a] = -inv @ d[a] @ inv
    G = np.zeros((4, 4, 4))
    dG = np.zeros((4, 4, 4, 4))
    for a in range(4):
        for m in range(4):
            for n in range(4):
                for b in range(4):
                    first = d[m,b,n] + d[n,b,m] - d[b,m,n]
                    G[a,m,n] += .5 * inv[a,b] * first
                    for k in range(4):
                        second = dd[k,m,b,n] + dd[k,n,b,m] - dd[k,b,m,n]
                        dG[k,a,m,n] += .5 * (dinv[k,a,b] * first + inv[a,b] * second)
    ric = np.zeros((4, 4))
    E = np.zeros((4, 4))
    C = np.zeros(4)
    dC = np.zeros((4, 4))
    for m in range(4):
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    C[m] += g[m,a] * inv[b,c] * G[a,b,c]
                    for k in range(4):
                        dC[k,m] += (d[k,m,a] * inv[b,c] * G[a,b,c]
                                    + g[m,a] * dinv[k,b,c] * G[a,b,c]
                                    + g[m,a] * inv[b,c] * dG[k,a,b,c])
        for n in range(4):
            for a in range(4):
                ric[m,n] += dG[a,a,m,n] - dG[n,a,m,a]
                for b in range(4):
                    ric[m,n] += G[a,m,n] * G[b,a,b] - G[a,m,b] * G[b,n,a]
                    E[m,n] += (inv[a,b] * dd[a,b,m,n]
                               + dinv[n,a,b] * d[a,m,b]
                               + dinv[m,a,b] * d[a,n,b]
                               + 2 * G[a,b,n] * G[b,a,m])
    correction = dC + dC.T
    for m in range(4):
        for n in range(4):
            correction[m,n] -= 2 * sum(G[a,m,n] * C[a] for a in range(4))
    return dict(ric=ric, reduced=E, harmonic_lower=C, dharmonic_lower=dC,
                identity_error=E + 2*ric - correction, inverse=inv, christoffel=G)


def kasner(s, p=(-2/7, 3/7, 6/7)):
    q = np.array([1., *p])
    diagonal = np.exp(2*q*s) * np.array([-1., 1., 1., 1.])
    g = np.diag(diagonal)
    d = np.zeros((4,4,4)); dd = np.zeros((4,4,4,4))
    d[0] = np.diag(2*q*diagonal)
    dd[0,0] = np.diag(4*q*q*diagonal)
    return g, d, dd


def gauge_wave(x, amplitude=.13, modes=(1, 2, 2)):
    k = np.array(modes, dtype=float)
    w = np.linalg.norm(k); n = k/w
    v = np.array([-w, *k]); phase = np.dot(v,x)
    F = 1-amplitude*np.sin(phase)
    B = np.zeros((4,4)); B[0,0] = -1; B[1:,1:] = np.outer(n,n)
    g = np.diag([-1.,1.,1.,1.]) + (F-1)*B
    d = (-amplitude*np.cos(phase))*v[:,None,None]*B[None,:,:]
    dd = amplitude*np.sin(phase)*v[:,None,None,None]*v[None,:,None,None]*B[None,None,:,:]
    return g,d,dd


def harmonic_adm(gamma, dgamma, K):
    """Independent scalar-loop construction at alpha=1,beta=0; no equations of motion."""
    inv = np.linalg.inv(gamma)
    G3 = np.zeros((3,3,3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                G3[i,j,k] = .5*sum(inv[i,l]*(dgamma[j,l,k]+dgamma[k,l,j]-dgamma[l,j,k]) for l in range(3))
    g = np.zeros((4,4)); g[0,0] = -1; g[1:,1:] = gamma
    d = np.zeros((4,4,4)); d[1:,1:,1:] = dgamma
    d[0,1:,1:] = -2*K
    d[0,0,0] = 2*np.sum(inv*K)
    for i in range(3):
        d[0,0,i+1] = d[0,i+1,0] = sum(gamma[i,j]*inv[k,l]*G3[j,k,l]
                                                    for j in range(3) for k in range(3) for l in range(3))
    return g,d,np.zeros((4,4,4,4))


def main():
    rng = np.random.default_rng(41291)
    identity = []; adm = []; bad_adm = []
    for _ in range(12):
        r = rng.normal(size=(4,4))*.04
        g = np.diag([-1.,1.,1.,1.]) + r+r.T
        d = rng.normal(size=(4,4,4))*.12; d=(d+d.transpose(0,2,1))/2
        dd = rng.normal(size=(4,4,4,4))*.12
        dd=(dd+dd.transpose(1,0,2,3))/2; dd=(dd+dd.transpose(0,1,3,2))/2
        identity.append(float(abs(geometry(g,d,dd)['identity_error']).max()))
        a = rng.normal(size=(3,3))*.1
        gamma = np.eye(3)+a@a.T
        ds=rng.normal(size=(3,3,3))*.1; ds=(ds+ds.transpose(0,2,1))/2
        K=rng.normal(size=(3,3))*.1; K=(K+K.T)/2
        gg,dg,ddg=harmonic_adm(gamma,ds,K)
        adm.append(float(abs(geometry(gg,dg,ddg)['harmonic_lower']).max()))
        wrong=dg.copy(); wrong[0,0,0]*=-1
        bad_adm.append(float(abs(geometry(gg,wrong,ddg)['harmonic_lower']).max()))
    controls={}
    for name,constructor,points in (
        ('kasner',kasner,[-.4,0,.3,.7]),
        ('oblique_gauge_wave',gauge_wave,[[.1,.2,.3,.4],[.2,.7,-.1,.3],[.6,-.2,.1,.7]])):
        values=[geometry(*constructor(p)) for p in points]
        controls[name]={key:float(max(abs(v[key]).max() for v in values))
                        for key in ['ric','reduced','harmonic_lower','dharmonic_lower','identity_error']}
    # Catchproof: violating the Kasner quadratic condition creates nonzero Ricci.
    bad_kasner = float(abs(geometry(*kasner(.2,p=(.2,.3,.5)))['ric']).max())
    result={'status':'PASS','scope':'Independent random metric-jet algebra, harmonic ADM velocities, analytic controls only; no numerical-history validation yet.',
            'random_jet_count':len(identity),'max_reduction_identity_error':max(identity),
            'max_adm_harmonic_error':max(adm),'min_wrong_lapse_velocity_detected':min(bad_adm),
            'bad_kasner_ricci':bad_kasner,'controls':controls,
            'numpy_version':np.__version__,'producer_imports':False,
            'reviewer_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    assert max(identity)<1e-12 and max(adm)<1e-13 and min(bad_adm)>1e-4 and bad_kasner>.1
    assert max(x for control in controls.values() for x in control.values())<1e-12
    out=Path(__file__).with_name('INDEPENDENT_JETS_RESULT.json')
    with out.open('x') as f: json.dump(result,f,indent=2,sort_keys=True); f.write('\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__': main()
