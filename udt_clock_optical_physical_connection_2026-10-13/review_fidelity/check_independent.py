"""Exact reviewer controls, independently authored before author-code exposure."""
import hashlib
import itertools
import json
from pathlib import Path
import platform
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
Q = s.Rational
eta = (-1, 1, 1, 1)
inds = range(4)
I4 = list(itertools.product(inds, repeat=4))
checks = []

def equal(name, actual, expected):
    residual = s.simplify(actual-expected)
    assert residual == 0, (name, actual, expected, residual)
    checks.append(name)

def B(i,j,k,l):
    return eta[j]*eta[i]*int(j == k and i == l)-eta[i]*eta[j]*int(i == k and j == l)

def contract(A, x,y,z,w):
    return s.expand(sum(A[i,j,k,l]*x[i]*y[j]*z[k]*w[l] for i,j,k,l in I4))

def ricci(A):
    return s.Matrix(4,4,lambda j,k:sum(eta[i]*A[i,j,k,i] for i in inds))

def mink(x,y):
    return sum(eta[i]*x[i]*y[i] for i in inds)

base = {a:B(*a) for a in I4}
product = {a:B(*a) if all(i > 0 for i in a) else 0 for a in I4}
ric = ricci(product)
scalar = sum(eta[i]*ric[i,i] for i in inds)
equal('ultrastatic total scalar', scalar, 6)
U = s.Matrix([Q(5,3), Q(4,3), 0, 0])
E = [s.Matrix([Q(4,3),Q(5,3),0,0]),s.eye(4)[:,2],s.eye(4)[:,3]]
equal('boost normalization',mink(U,U),-1)
evalues = []
nullvalues = []
for j,n in enumerate(E):
    equal(f'rest basis orthogonality {j}',mink(U,n),0)
    equal(f'rest basis unit {j}',mink(n,n),1)
    evalues.append(contract(product,n,U,U,n))
    for sign in (-1,1):
        k = U+sign*n
        equal(f'null {j} {sign}',mink(k,k),0)
        nullvalues.append((k.T*ric*k)[0])
equal('boosted longitudinal tide',evalues[0],0)
equal('boosted first transverse tide',evalues[1],Q(16,9))
equal('boosted second transverse tide',evalues[2],Q(16,9))
M=-sum(evalues)/3
N=sum(nullvalues)/6
equal('ultrastatic scalar projector',M+N/4,Q(1,2))

def diagonal_curvature(entries):
    out={a:s.Integer(0) for a in I4}
    for (i,j),v in entries.items():
        out[i,j,j,i]=out[j,i,i,j]=v
        out[j,i,j,i]=out[i,j,i,j]=-v
    return out

w=Q(1,10)
kappa=Q(1,5)
sw=diagonal_curvature({(1,0):-2*w,(2,0):w,(3,0):w,
                       (1,2):-w,(1,3):-w,(2,3):2*w})
ko={a:sw[a]+kappa*base[a] for a in I4}
equal('Schwarzschild Ricci norm',sum(x*x for x in ricci(sw)),0)
equal('Kottler Ricci identity',sum((ricci(ko)[i,j]-3*kappa*eta[i]*int(i==j))**2
                                for i in inds for j in inds),0)
equal('matched full curvature difference',sum((ko[a]-sw[a]-kappa*base[a])**2 for a in I4),0)
e0=s.eye(4)[:,0]
sw_area=[]
for j in (1,2,3):
    n=s.eye(4)[:,j]
    sw_area.append(Q(2,3)*contract(sw,n,e0,e0,n))
assert sw_area == [-Q(2,15),Q(1,15),Q(1,15)]
checks.append('Schwarzschild total directional sign fails in one frame')

# Differential Bianchi of q_a B_bcde: matrix from q to cyclic residue.
rows=[]
for a,b,c,d,e in itertools.product(inds,repeat=5):
    row=[int(a==f)*B(b,c,d,e)+int(b==f)*B(c,a,d,e)+int(c==f)*B(a,b,d,e)
         for f in inds]
    if any(row): rows.append(row)
rank=s.Matrix(rows).rank()
assert rank == 4
checks.append('differential-Bianchi scalar-gradient kernel is zero')

# Original Minkowski endpoint separation and null incidence, without C1.
l,acc,z=s.symbols('l acc z',real=True)
T=s.sinh(2*acc*l)/acc
X=(s.cosh(2*acc*l)-1)/acc
interval=s.simplify(T*T-X*X)
relative_area=s.simplify(interval/(4*l*l))
equal('accelerated exact interval area',relative_area,s.sinh(acc*l)**2/(acc*l)**2)
series=s.series(relative_area,l,0,4).removeO()
equal('accelerated integrated coefficient',series.coeff(l,2),acc**2/3)
raycut=interval/(2*(T-X*z))
rayseries=s.series(raycut/l,l,0,3).removeO().expand()
equal('accelerated source-angle first order',rayseries.coeff(l,1),acc*z)
equal('accelerated source-angle second order',rayseries.coeff(l,2),acc**2*(z*z-Q(1,3)))

freeze=ROOT/'CANDIDATE_FREEZE.json'
data=json.loads(freeze.read_text())
manifest=[]
repo=ROOT.parent
for path,expected in data['sha256'].items():
    actual=hashlib.sha256((repo/path).read_bytes()).hexdigest()
    assert actual==expected,(path,actual,expected)
    manifest.append(path)

pins={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest()
      for p in (Path(__file__).resolve(),HERE/'CHECK_PLAN.md',freeze,ROOT/'INITIAL_CANDIDATE.md')}
print(json.dumps({'status':'PASS','versions':{'python':platform.python_version(),'sympy':s.__version__},
 'checks':checks,'check_count':len(checks),'ultrastatic':{'electric':[str(x) for x in evalues],
 'M':str(M),'N':str(N),'K':str(M+N/4)},'Schwarzschild_directional_area':[str(x) for x in sw_area],
 'gradient_Bianchi_rank':rank,'accelerated_area_series':str(series),
 'accelerated_ray_series':str(rayseries),'frozen_files_verified':len(manifest),'sha256':pins},indent=2))
