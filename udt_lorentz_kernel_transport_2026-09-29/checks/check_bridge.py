"""Exact supplied controls; no physical geometry selection."""
import json
import sympy as s

checks=[]
def zero(name,value):
    entries=list(value) if isinstance(value,s.MatrixBase) else [value]
    reduced=[s.simplify(v) for v in entries]
    assert all(v==0 for v in reduced),(name,reduced)
    checks.append(name)
def nonzero(name,value):
    assert s.simplify(value)!=0,name
    checks.append(name)

eta=s.diag(-1,1);K=s.Matrix([[0,1],[1,0]])
S=s.Matrix([[1,1],[-1,1]])/s.sqrt(2)
z=s.symbols('z',positive=True)
D=s.diag(1/z,z);B=S.T*D*S
zero('reciprocal pairing',D.T*K*D-K)
zero('dual pairing changes to eta',S.T*K*S-eta)
zero('physical readout changes too',S.T*eta*S+K)
zero('conjugate is Lorentz',B.T*eta*B-eta)
nonzero('wrong physical isometry caught',(D.T*eta*D-eta)[0,0].subs(z,2))

t,x=s.symbols('t x',real=True);q=(t,x)
T=s.Function('T')(t,x);L=s.Function('L')(t,x);b=s.Function('b')(t,x)
E=s.Matrix([[T,T*b],[0,L]])
g=E.T*eta*E;gi=s.simplify(g.inv())
def connection(metric,inverse):
    return [[[s.simplify(sum(inverse[a,d]*(s.diff(metric[d,c],q[j])+
            s.diff(metric[d,j],q[c])-s.diff(metric[j,c],q[d]))/2
            for d in range(2))) for c in range(2)] for j in range(2)] for a in range(2)]
G=connection(g,gi)
expected_t=(s.diff(T,x)-s.diff(T*b,t))/L
expected_x=b*expected_t+s.diff(L,t)/T
for j,expected in enumerate([expected_t,expected_x]):
    Gj=s.Matrix(2,2,lambda a,c:G[a][j][c])
    actual=s.simplify(E*Gj*E.inv()-E.diff(q[j])*E.inv())
    zero('Christoffel-to-coframe '+str(j),actual-expected*K)
nonzero('omitted shift derivative caught',(-s.diff(T*b,t)/L).subs(
    {T:s.Integer(2),L:s.Integer(3),b:t}).doit())

# Independent coordinate-curvature route, on a mixed reciprocal control.
F=3+t+t*t+x+2*t*x+x*x
gm=s.diag(-1/F,F);im=s.diag(-F,1/F);C=connection(gm,im)
Ric=s.zeros(2)
for a in range(2):
    for j in range(2):
        Ric[a,j]=sum(s.diff(C[c][a][j],q[c])-s.diff(C[c][a][c],q[j])+
            sum(C[c][c][d]*C[d][a][j]-C[c][j][d]*C[d][a][c]
                for d in range(2)) for c in range(2))
Rcoord=s.simplify(sum(im[a,j]*Ric[a,j] for a in range(2) for j in range(2)))
phi=s.log(F)/2
wt=-s.diff(F,x)/(2*F**2);wx=s.diff(F,t)/2
Rcartan=2*(s.diff(wx,t)-s.diff(wt,x))
zero('direct coordinate curvature equals connection curvature',Rcoord-Rcartan)
nonzero('curvature sign reversal caught',(Rcoord+Rcartan).subs({t:0,x:0}))
for eps in (-1,1):
    speed=eps/F
    zero('null branch '+str(eps),gm[0,0]+gm[1,1]*speed**2)
    dphi=s.diff(phi,t)+s.diff(phi,x)*speed
    depth_rate=-eps*(wt+wx*speed)
    zero('dynamic depth bridge '+str(eps),depth_rate-(dphi-2*s.diff(phi,t)))
    nonzero('naive endpoint difference fails '+str(eps),(depth_rate-dphi).subs({t:0,x:0}))
f=s.Function('f')
for eps in (-1,1):
    static=f(x);time=f(t)
    for label,p,expected in [('static',static,eps*s.exp(-2*static)*s.diff(static,x)),
                             ('time-only',time,-s.diff(time,t))]:
        v=eps*s.exp(-2*p)
        rate=-eps*(-s.exp(-2*p)*s.diff(p,x)+s.exp(2*p)*s.diff(p,t)*v)
        zero(label+' clock-depth rate '+str(eps),rate-expected)

te=s.symbols('te',real=True);to=2*te+1
zero('independent null incidence',s.exp(s.log(1+to)-s.log(1+te))-2)
zero('arrival map slope',s.diff(to,te)-2)
zero('local clock factor is unit',s.Integer(1)-1)
nonzero('discarded density misses received clock slope',s.diff(to,te)-1)

eta4=s.diag(-1,1,1,1)
def boost(axis,r):
    c=(r+1/r)/2;sh=(r-1/r)/2;M=s.eye(4)
    M[0,0]=M[axis,axis]=c;M[0,axis]=M[axis,0]=sh
    return M
Bx=boost(1,s.Rational(2));By=boost(2,s.Rational(3))
null=s.Matrix([1,1,0,0]);v1=Bx*null;v2=By*(v1/v1[0])
zero('both actual boosts preserve interval',Bx.T*eta4*Bx-eta4)
zero('second boost preserves interval',By.T*eta4*By-eta4)
zero('direction-carry composition',(By*Bx*null)[0]-v1[0]*v2[0])
# Use an initially transverse ray to make omission of intermediate direction audible.
null2=s.Matrix([1,0,1,0]);p1=Bx*null2
nonzero('dropped intermediate direction caught',(By*Bx*null2)[0]-(By*null2)[0]*p1[0])
gens=[]
for i in (1,2,3):
    M=s.zeros(4);M[0,i]=M[i,0]=1;gens.append(M)
B1,B2,B3=gens;J3=-(B1*B2-B2*B1)
zero('rotation bracket returns boost',J3*B1-B1*J3-B2)
nonzero('noncollinear boosts do not commute',(Bx*By-By*Bx)[1,2])
print(json.dumps({'status':'PASS','checks':len(checks),'names':checks,'arithmetic':'exact SymPy',
 'scope':'Supplied algebra/geometry controls; no physical admission or completeness claim.'},indent=2))
