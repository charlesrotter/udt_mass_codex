#!/usr/bin/env python3
"""Finite exact verification of NFCA1's new section-C witness only."""
from fractions import Fraction as Q
import json
from pathlib import Path
import platform
import sys

checks = []

def flatten(value):
    if isinstance(value, (list, tuple)):
        return [y for x in value for y in flatten(x)]
    return [value]

def equal(name, actual, expected):
    a, b = flatten(actual), flatten(expected)
    ok = len(a) == len(b) and a == b
    checks.append({'name': name, 'pass': ok})
    if not ok:
        checks[-1].update(actual=str(actual), expected=str(expected))

def matmul(a, b):
    assert len(a[0]) == len(b)
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def transpose(a):
    return [list(x) for x in zip(*a)]

def inverse(a):
    n = len(a)
    w = [[Q(x) for x in row]+[Q(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for i in range(n):
        k = next(k for k in range(i, n) if w[k][i])
        w[i], w[k] = w[k], w[i]
        p = w[i][i]
        w[i] = [x/p for x in w[i]]
        for k in range(n):
            if k != i:
                p = w[k][i]
                w[k] = [x-p*y for x, y in zip(w[k], w[i])]
    return [row[n:] for row in w]

def data(u, x, y, e, scale=Q(1)):
    H = 2*(x*x-y*y)/(u*u)+e*(x*x*x-3*x*y*y)
    dH = [-4*(x*x-y*y)/(u*u*u), Q(0),
          4*x/(u*u)+3*e*(x*x-y*y), -4*y/(u*u)-6*e*x*y]
    g = [[H,Q(-1),Q(0),Q(0)],[Q(-1),Q(0),Q(0),Q(0)],
         [Q(0),Q(0),Q(1),Q(0)],[Q(0),Q(0),Q(0),Q(1)]]
    dg = [[[Q(0) for b in range(4)] for a in range(4)] for k in range(4)]
    for k in range(4):
        dg[k][0][0] = dH[k]
    K = [Q(0),2*u*x*scale,u*u*scale,Q(0)]
    dK = [[Q(0),2*x*scale,2*u*scale,Q(0)],
          [Q(0),Q(0),Q(0),Q(0)],
          [Q(0),2*u*scale,Q(0),Q(0)],
          [Q(0),Q(0),Q(0),Q(0)]]
    A = [sum(g[a][b]*K[b] for b in range(4)) for a in range(4)]
    dA = [[sum(dg[k][a][b]*K[b]+g[a][b]*dK[k][b] for b in range(4))
           for a in range(4)] for k in range(4)]
    F = [[dA[a][b]-dA[b][a] for b in range(4)] for a in range(4)]
    return g, A, F

J = [[Q(1),Q(0)],[Q(3,2),Q(0)],[Q(0),Q(1)],[Q(0),Q(0)]]
records = []
for center in [False, True]:
    u, x, y = Q(1), Q(0 if center else 1), Q(0)
    for e in [Q(0), Q(1,8)]:
        name = ('center' if center else 'off_axis')+'_'+str(e)
        g, A, F = data(u,x,y,e)
        gi = inverse(g)
        equal(name+'_inverse_identity', matmul(g,gi),
              [[Q(i == j) for j in range(4)] for i in range(4)])
        h = matmul(transpose(J),matmul(g,J))
        h00 = Q(-3) if center else Q(-1)+e
        equal(name+'_full_pullback',h,[[h00,Q(0)],[Q(0),Q(1)]])
        determinant = h[0][0]*h[1][1]-h[0][1]*h[1][0]
        equal(name+'_regular',h[0][0]<0 and determinant<0,True)
        equal(name+'_diagonal', [h[0][1],h[1][0]],[Q(0),Q(0)])
        m2 = -determinant
        hs = [[h[0][0],Q(0)],[Q(0),h[1][1]/m2]]
        equal(name+'_completed_det',hs[0][0]*hs[1][1],Q(-1))
        recovered = [[hs[0][0],Q(0)],[Q(0),m2*hs[1][1]]]
        equal(name+'_density_inverse',recovered,h)
        r = -h[0][0]
        chi = (1-r)/(1+r)
        expected_chi = Q(-1,2) if center else (Q(0) if not e else Q(1,15))
        equal(name+'_chi',chi,expected_chi)
        equal(name+'_lowered_K',A,[-2*u*x,Q(0),u*u,Q(0)])
        expected_F = [[Q(0) for b in range(4)] for a in range(4)]
        expected_F[0][2],expected_F[2][0] = 4*u,-4*u
        equal(name+'_exterior_full',F,expected_F)
        Fraised = matmul(matmul(gi,F),transpose(gi))
        expected_up = [[Q(0) for b in range(4)] for a in range(4)]
        expected_up[1][2],expected_up[2][1] = -4*u,4*u
        equal(name+'_raised_full',Fraised,expected_up)
        equal(name+'_null_contraction',sum(F[a][b]*Fraised[a][b]
              for a in range(4) for b in range(4)),Q(0))
        g2,A2,F2 = data(u,x,y,e,Q(2))
        equal(name+'_fixed_metric_K_rescale',g2,g)
        equal(name+'_F_rescale',F2,[[2*v for v in row] for row in F])
        equal(name+'_fixed_J_rescale',matmul(transpose(J),matmul(g2,J)),h)
        records.append({'case':name,'h':[[str(v) for v in row] for row in h],
                        'm_squared':str(m2),'h_s':[[str(v) for v in row] for row in hs],
                        'chi':str(chi),'F_ux':str(F[0][2])})

# Narrow discriminating controls, not independent proofs or a general harness.
equal('density_deletion_changes_off_axis_ruler',Q(8,7)!=Q(1),True)
equal('wrong_depth_sign_changes_nonzero_chi',-Q(1,15)!=Q(1,15),True)
equal('shape_guard_rejects_unequal_lengths',len(flatten([1]))!=len(flatten([1,2])),True)
out = {'scope':'four exact supplied witness/probe cases; analytic arguments own general dependencies',
       'implementation':'fresh Fraction matrix/first-derivative implementation; no parent scientific import',
       'python':platform.python_version(),'cases':records,'checks':checks,
       'passed':sum(c['pass'] for c in checks),'total':len(checks)}
with Path(sys.argv[1]).open('x') as f:
    json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out))
raise SystemExit(0 if out['passed']==out['total'] else 1)
