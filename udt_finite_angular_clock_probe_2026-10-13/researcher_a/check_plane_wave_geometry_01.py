"""Original-metric tensor checks for the FAC1 plane-wave author control."""
import hashlib
import itertools
import json
from pathlib import Path
import platform
import time
import sympy as s


def main():
    started=time.monotonic()
    a,b,x,y=s.symbols('a b x y',real=True)
    coordinates=[a,b,x,y]
    g=s.Matrix([[(x*x-y*y)/2,-s.Rational(1,2),0,0],[-s.Rational(1,2),0,0,0],[0,0,1,0],[0,0,0,1]])
    inverse=g.inv()
    Gamma={}
    for A,B,C in itertools.product(range(4),repeat=3):
        value=s.simplify(sum(inverse[A,D]*(s.diff(g[D,B],coordinates[C])+s.diff(g[D,C],coordinates[B])-s.diff(g[B,C],coordinates[D]))/2 for D in range(4)))
        if value:Gamma[A,B,C]=value
    G=lambda A,B,C:Gamma.get((A,B,C),s.S.Zero)
    curvature={}
    # R[A,B,C,D] gives component A of R(partial_C,partial_D) partial_B.
    for A,B,C,D in itertools.product(range(4),repeat=4):
        value=s.simplify(s.diff(G(A,D,B),coordinates[C])-s.diff(G(A,C,B),coordinates[D])+sum(G(A,C,E)*G(E,D,B)-G(A,D,E)*G(E,C,B) for E in range(4)))
        if value:curvature[A,B,C,D]=value
    R=lambda A,B,C,D:curvature.get((A,B,C,D),s.S.Zero)
    Ric=s.Matrix(4,4,lambda B,D:s.simplify(sum(R(A,B,A,D) for A in range(4))))
    assert Ric==s.zeros(4)
    nonzero_derivatives=[]
    for E,A,B,C,D in itertools.product(range(4),repeat=5):
        value=s.simplify(s.diff(R(A,B,C,D),coordinates[E])+sum(G(A,E,F)*R(F,B,C,D)-G(F,E,B)*R(A,F,C,D)-G(F,E,C)*R(A,B,F,D)-G(F,E,D)*R(A,B,C,F) for F in range(4)))
        if value:nonzero_derivatives.append((E,A,B,C,D,str(value)))
    assert not nonzero_derivatives,nonzero_derivatives
    origin={x:0,y:0}
    U=s.Matrix([1,1,0,0])
    triad=[s.Matrix([0,0,1,0]),s.Matrix([0,0,0,1]),s.Matrix([1,-1,0,0])]
    g0=g.subs(origin)
    assert (U.T*g0*U)[0]==-1
    for i,j in itertools.product(range(3),repeat=2):
        assert (triad[i].T*g0*triad[j])[0]==int(i==j)
    def contract(V,W,Q,T):
        return s.simplify(sum(g0[A,F]*R(F,B,C,D).subs(origin)*V[C]*W[D]*Q[B]*T[A] for A,B,C,D,F in itertools.product(range(4),repeat=5)))
    electric=s.Matrix(3,3,lambda i,j:contract(triad[i],U,U,triad[j]))
    # B_ij = (1/2) epsilon_i^kl g(R(e_k,e_l)U,e_j).
    magnetic=s.Matrix(3,3,lambda i,j:s.simplify(sum(s.LeviCivita(i,k,l)*contract(triad[k],triad[l],U,triad[j])/2 for k,l in itertools.product(range(3),repeat=2))))
    electric_square=s.simplify(sum(v*v for v in electric))
    magnetic_square=s.simplify(sum(v*v for v in magnetic))
    result={'metric':str(g),'connection_nonzero':{str(k):str(v) for k,v in Gamma.items()},
            'curvature_nonzero':{str(k):str(v) for k,v in curvature.items()},
            'Ricci_zero':True,'covariant_Riemann_derivative_zero':True,
            'electric':str(electric),'magnetic':str(magnetic),
            'electric_square':str(electric_square),'magnetic_square':str(magnetic_square),
            'convention':'R(X,Y)=[nabla_X,nabla_Y]-nabla_[X,Y]; Eij=g(R(ei,U)U,ej)',
            'python':platform.python_version(),'sympy':s.__version__,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'duration_seconds':time.monotonic()-started}
    target=Path(__file__).with_name('plane_wave_geometry_01_result.json')
    with target.open('x') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
