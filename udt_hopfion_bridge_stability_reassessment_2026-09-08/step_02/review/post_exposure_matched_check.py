"""Source-first direct toric block Ricci variation. No project imports."""
import json
import platform
import sys
import sympy as s

x=s.symbols('x', real=True)
def simp(M):
    return M.applyfunc(s.cancel) if isinstance(M,s.MatrixBase) else s.cancel(M)
def geometry(w1,w2):
    F=w1*x+w2*(1-x)
    eta=s.Matrix([x/F,(1-x)/F])
    zeta=s.Matrix([w2/F,-w1/F])
    A=1/(4*x*(1-x)*F)
    H=simp(x*(1-x)/F*zeta*zeta.T+eta*eta.T)
    inv=simp(s.Matrix([[H[1,1],-H[0,1]],[-H[1,0],H[0,0]]])/H.det())
    Hp=H.diff(x); Hpp=Hp.diff(x); T=simp(inv*Hp)
    Rxx=simp(-s.trace(inv*Hpp)/2+s.trace(T*T)/4+s.diff(A,x)*s.trace(T)/(4*A))
    Rab=simp(-Hpp/(2*A)+s.diff(A,x)*Hp/(4*A*A)-s.trace(T)*Hp/(4*A)+Hp*inv*Hp/(2*A))
    R=simp(Rxx/A+s.trace(inv*Rab))
    return A,H,eta,inv,Rxx,Rab,R

records=[]; hostile=[]; checks=0
for w1,w2,x0 in [(s.Rational(1,4),s.Rational(1,2),s.Rational(1,3)),
                  (s.Rational(2),s.Rational(7,4),s.Rational(2,5)),
                  (s.Rational(1,2),s.Rational(1,2),s.Rational(1,4))]:
    A,H,eta,inv,Rxx,Rab,R=geometry(w1,w2)
    xi=s.Matrix([w1,w2]); Y=s.Matrix([1-x,-x])
    assert simp(Rab*xi-2*eta)==s.zeros(2,1)
    assert simp(Rxx-(R-2)*A/2)==0
    checks+=2
    at=lambda z: simp(z.subs(x,x0)) if hasattr(z,'subs') else z
    R0=at(R); R1=at(s.diff(R,x)); R2=at(s.diff(R,x,2))
    for C in [s.Rational(-3),s.Rational(3)]:
      for eps in [-1,1]:
        root=s.Rational(8)*eps; b0=-C+root
        b1=R1/root; b2=R2/root-R1**2/root**3
        b=b0+b1*(x-x0)+b2*(x-x0)**2/2
        hA=(b-C)*A; hH=(b-C)*H-2*b*eta*eta.T
        a,ap=at(A),at(s.diff(A,x)); ha,hap=at(hA),at(s.diff(hA,x))
        M,Mp,Mpp=at(H),at(H.diff(x)),at(H.diff(x,2))
        I=at(inv); Z,Zp,Zpp=at(hH),at(hH.diff(x)),at(hH.diff(x,2))
        dI=-I*Z*I; T=I*Mp; dT=dI*Mp+I*Zp
        dRab=simp(-Zpp/(2*a)+Mpp*ha/(2*a*a)
            +(hap*Mp+ap*Zp)/(4*a*a)-ap*Mp*ha/(2*a**3)
            -(s.trace(dT)*Mp+s.trace(T)*Zp)/(4*a)+s.trace(T)*Mp*ha/(4*a*a)
            +(Zp*I*Mp+Mp*dI*Mp+Mp*I*Zp)/(2*a)-Mp*I*Mp*ha/(2*a*a))
        dRxx=simp(-s.trace(dI*Mpp+I*Zpp)/2+s.trace(dT*T)/2
            +(hap/a-ap*ha/a**2)*s.trace(T)/4+ap*s.trace(dT)/(4*a))
        e=at(eta); y=at(Y); D=(6-R0)/2
        mixed=simp((y.T*dRab*xi)[0]); predicted=simp(s.Rational(5,4)/a*b1*(at(eta.diff(x)).dot(y)))
        assert mixed==predicted
        dAsharp=simp(I*dRab+dI*at(Rab))
        P=xi*e.T; Q=s.eye(2)-P
        jgrad=simp(2*at(w1*x+w2*(1-x))*b1*y)
        V=simp(s.Rational(5,2)/D*jgrad)
        assert simp(Q*dAsharp*xi-D*V)==s.zeros(2,1)
        dP=simp(V*e.T+xi*(M*V).T)
        Asharp=simp(I*at(Rab))
        assert simp(dAsharp*P+Asharp*dP-dP*Asharp-P*dAsharp)==s.zeros(2)
        assert simp(dP*P+P*dP-dP)==s.zeros(2)
        assert simp(M*dP-dP.T*M+Z*P-P.T*Z)==s.zeros(2)
        Lambda=R0/2+C*C-root*root/4
        kh=(C-b0)/2;kv=(C+b0)/2
        assert simp(R0+(2*kh+kv)**2-2*kh*kh-kv*kv-2*Lambda)==0
        checks+=7
        if b1:
            assert mixed != -predicted and mixed != 0 and mixed != predicted*s.Rational(3,5)
            assert simp(Q*dAsharp*xi+D*V)!=s.zeros(2,1)
            hostile.append(dict(weights=[str(w1),str(w2)],C=str(C),root=str(root),
                wrong_sign=str(2*mixed),omitted_gradient=str(mixed),wrong_coefficient=str(mixed*s.Rational(2,5)),
                wrong_gap=str(2*D*V)))
        inverse_effect=simp(dAsharp-I*dRab)
        assert inverse_effect != s.zeros(2)
        checks+=1
        records.append(dict(weights=[str(w1),str(w2)],x=str(x0),C=str(C),root=str(root),
            Lambda=str(Lambda),R=str(R),Rprime=str(R1),bprime=str(b1),
            mixed=str(mixed),V=[str(q) for q in V],projector_derivative=str(dP),
            inverse_metric_effect=str(inverse_effect),HS2=str(s.trace(dP*dP)),ambient_vertical=str((e.T*inverse_effect*xi)[0]),full_radial_Ricci_derivative=str(dRxx)))

from pathlib import Path
saved=json.loads((Path(__file__).resolve().parent/'author_replay.stdout').read_text())
comparisons=[]
for actual, author in zip(records,saved['fixtures'],strict=True):
    assert actual['weights']==author['weights'] and actual['x']==author['x']
    assert actual['C']==author['C'] and actual['root']==author['root_D']
    assert actual['Lambda']==author['Lambda']
    assert ['0']+actual['V']==author['Y']
    assert actual['HS2']==author['projector_HS_squared']
    assert actual['ambient_vertical']==author['full_raising_correction']
    comparisons.append({'weights':actual['weights'],'x':actual['x'],'C':actual['C'],'root':actual['root'],'Y':author['Y'],'projector_HS_squared':actual['HS2'],'full_raising_correction':actual['ambient_vertical']})
print(json.dumps({'kind':'post-exposure independent toric-block recomputation against saved author quantities; no author engine imported','independent_checks':checks,'matched':comparisons,'versions':{'python':sys.version,'sympy':s.__version__}},indent=2))
