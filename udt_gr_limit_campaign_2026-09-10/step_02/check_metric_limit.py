#!/usr/bin/env python3
"""Exact symbolic scope checks; not a numerical development or limit proof."""
import json
import platform
import sympy as s

t, r, theta, phi = s.symbols('t r theta phi', real=True)
c = s.symbols('c', positive=True)
d = s.symbols('d', nonzero=True, real=True)
n = s.symbols('n', integer=True, positive=True)
f = s.Function('f')(r)
x = (t, r, theta, phi)
h = s.diag(-f, 1/f, r**2, r**2*s.sin(theta)**2)
counts = {'tensor_component_identities': 0, 'diagnostic_identities': 0,
          'rational_probes': 0, 'required_nonzero_controls': 0}

def check(a, b, group):
    assert s.simplify(a-b) == 0, (a, b)
    counts[group] += 1

def nonzero(a):
    assert s.simplify(a) != 0, a
    counts['required_nonzero_controls'] += 1

def geometry(g):
    gi = g.inv()
    gamma = [[[s.simplify(sum(gi[a, z] *
                (s.diff(g[z, j], x[i]) + s.diff(g[z, i], x[j])
                 - s.diff(g[i, j], x[z])) for z in range(4))/2)
                for j in range(4)] for i in range(4)] for a in range(4)]
    ric = s.zeros(4)
    for i in range(4):
        for j in range(4):
            ric[i, j] = s.simplify(sum(
                s.diff(gamma[a][i][j], x[a])
                - s.diff(gamma[a][i][a], x[j])
                + sum(gamma[a][a][b]*gamma[b][i][j]
                      - gamma[a][j][b]*gamma[b][i][a] for b in range(4))
                for a in range(4)))
    scalar = s.simplify(s.trace(gi*ric))
    return gamma, ric, scalar, s.simplify(ric-scalar*g/4)

gh, rh, sh, tfh = geometry(h)
gg, rg, sg, tfg = geometry(h/c**2)
A = -s.diff(f, r, 2)/2-s.diff(f, r)/r
B = (1-f-r*s.diff(f, r))/r**2
expected = h*s.diag(A, A, B, B)
for i in range(4):
    for j in range(4):
        check(rh[i,j], expected[i,j], 'tensor_component_identities')
        check(rg[i,j], rh[i,j], 'tensor_component_identities')
        check(tfg[i,j], tfh[i,j], 'tensor_component_identities')
        for a in range(4):
            check(gg[a][i][j], gh[a][i][j], 'tensor_component_identities')
R_expected = -s.diff(f,r,2)-4*s.diff(f,r)/r+2*(1-f)/r**2
check(sh, R_expected, 'tensor_component_identities')
check(sg, c**2*sh, 'tensor_component_identities')

# Scalar Hessian radial orthonormal component, from full connection.
Hh = s.simplify(f*(s.diff(sh,r,2)-gh[1][1][1]*s.diff(sh,r)))
Hg = s.simplify(c**2*f*(s.diff(sg,r,2)-gg[1][1][1]*s.diff(sg,r)))
check(Hg, c**4*Hh, 'tensor_component_identities')
check(Hh, f*s.diff(sh,r,2)+s.diff(f,r)*s.diff(sh,r)/2,
      'tensor_component_identities')

# Exact known optional quadratic-response degeneracy, not new nonselection.
z = 1+d/r**2
rz = s.simplify(rh.subs(f,z).doit())
hz = h.subs(f,z)
M = s.simplify(hz.inv()*rz)
Sz = s.simplify(M-s.trace(M)*s.eye(4)/4)
Qz = s.simplify(M*M-s.trace(M*M)*s.eye(4)/4)
for i in range(4):
    for j in range(4):
        check(M[i,j], s.diag(-d/r**4,-d/r**4,d/r**4,d/r**4)[i,j],
              'tensor_component_identities')
        check(Qz[i,j], 0, 'tensor_component_identities')
nonzero(Sz[1,1])

fn = 1+s.cos(n*(r-1))/n**6
Rn = s.simplify(sh.subs(f,fn).doit())
Rn_expected = s.cos(n*(r-1))/n**4 + 4*s.sin(n*(r-1))/(n**5*r) \
              - 2*s.cos(n*(r-1))/(n**6*r**2)
check(Rn, Rn_expected, 'diagnostic_identities')
values = [s.simplify(s.diff(Rn,r,j).subs(r,1)) for j in range(3)]
targets = [1/n**4-2/n**6, 4/n**4+4/n**6,
           -1/n**2-6/n**4-12/n**6]
for a,b in zip(values,targets):
    check(a,b,'diagnostic_identities')
Hn = s.simplify(Hh.subs(f,fn).doit().subs(r,1))
check(Hn,(1+1/n**6)*targets[2],'diagnostic_identities')
ratio = s.factor(-Hn/values[0])
check(s.limit(ratio/n**2,n,s.oo),1,'diagnostic_identities')
check(s.limit(n**4*values[0],n,s.oo),1,'diagnostic_identities')
check(s.limit(n**2*Hn,n,s.oo),-1,'diagnostic_identities')
table=[]
for nv in (2,3,5,10,100):
    lower=1-s.Rational(1,nv**6)
    assert lower >= s.Rational(63,64)
    counts['rational_probes'] += 1
    rv=values[0].subs(n,nv)
    hv=Hn.subs(n,nv)
    assert rv>0 and hv<0 and -hv/rv>nv**2
    counts['rational_probes'] += 1
    table.append({'n':nv,'f_lower':str(lower),'R_at_1':str(rv),
                  'Hrr_at_1':str(hv),'minus_H_over_R':str(-hv/rv)})

# Narrow negative controls: wrong rescaling, dropped angular term,
# and suppressed-Hessian inference must NOT become identities.
nonzero(sg-sh)
nonzero((-s.diff(f,r,2)-4*s.diff(f,r)/r).subs(f,z).doit())
nonzero(s.limit(n**2*Hn,n,s.oo))
print(json.dumps({'status':'PASS','python':platform.python_version(),
    'sympy':s.__version__,'arithmetic':'exact symbolic and rational',
    'counts':counts,'shape':'4x4 full spherical coordinate metric',
    'R_at_1':str(values[0]),'R_prime_at_1':str(values[1]),
    'R_second_at_1':str(values[2]),'Hrr_at_1':str(Hn),
    'ratio':str(ratio),'probes':table,
    'limits':'No DDR assertion for oscillatory metric; no convergence/existence proof from probes; component zeros include structural identities.'},
    indent=2,sort_keys=True))
