"""Exact diagnostics; comparison actions/metrics are not UDT-admitted inputs."""
import json, platform
import sympy as s

t,x,y,z=s.symbols('t x y z', real=True)
r,ell=s.symbols('r ell', positive=True)
alpha=s.symbols('alpha', real=True)
coords=(t,x,y,z)
checks=[]

def zero(name, expression):
    values=list(expression) if isinstance(expression,s.MatrixBase) else [expression]
    reduced=[s.simplify(s.trigsimp(s.expand_trig(v), method="fu")) for v in values]
    assert all(v==0 for v in reduced), (name,reduced)
    checks.append({'name':name,'kind':'exact identity'})

def nonzero(name, expression):
    reduced=s.simplify(s.trigsimp(expression))
    assert reduced!=0, (name,reduced)
    checks.append({'name':name,'kind':'nonzero diagnostic','value':str(reduced)})

def geometry(g):
    gi=g.inv()
    gamma=[[[s.simplify(sum(gi[a,d]*(s.diff(g[d,b],coords[c])+
        s.diff(g[d,c],coords[b])-s.diff(g[b,c],coords[d])) for d in range(4))/2)
        for c in range(4)] for b in range(4)] for a in range(4)]
    ric=s.Matrix(4,4,lambda a,b:s.simplify(sum(
        s.diff(gamma[c][a][b],coords[c])-s.diff(gamma[c][a][c],coords[b])+
        sum(gamma[c][c][d]*gamma[d][a][b]-gamma[c][b][d]*gamma[d][a][c]
        for d in range(4)) for c in range(4))))
    scalar=s.simplify(s.trace(gi*ric))
    hess=s.Matrix(4,4,lambda a,b:s.simplify(s.diff(scalar,coords[a],coords[b])-
        sum(gamma[c][a][b]*s.diff(scalar,coords[c]) for c in range(4))))
    box=s.simplify(s.trace(gi*hess))
    ein=s.simplify(ric-scalar*g/2)
    algebraic=s.simplify(2*scalar*ric-scalar**2*g/2)
    q=s.simplify(algebraic+2*(g*box-hess))
    def tf(tensor):return s.simplify(tensor-s.trace(gi*tensor)*g/4)
    def div(tensor):
        return s.Matrix([s.simplify(sum(gi[a,c]*(s.diff(tensor[a,b],coords[c])-
            sum(gamma[d][c][a]*tensor[d,b]+gamma[d][c][b]*tensor[a,d]
                for d in range(4))) for a in range(4) for c in range(4)))
            for b in range(4)])
    return ric,scalar,ein,q,algebraic,tf,div

gp=s.diag(-1,1,r*r,r*r*s.sin(y)**2)
rp,sp,ep,qp,ap,tfp,dp=geometry(gp)
zero('product Ricci from metric',rp-s.diag(0,0,1,s.sin(y)**2))
zero('product scalar from metric',sp-2/r**2)
nonzero('product is not Einstein',tfp(rp)[0,0])
response=ep+alpha*qp
zero('product conserved family',dp(response))
zero('product tracefree multiplier',tfp(response)-(1+2*alpha*sp)*tfp(rp))
special=s.simplify(response.subs(alpha,-r*r/4))
zero('diagnostic pure trace response',special+gp/(2*r*r))
zero('diagnostic DDR holds',tfp(special))
nonzero('diagnostic full response not zero',special[0,0])
nonzero('wrong identification with Einstein shape fails',tfp(ep-special)[0,0])

gv=s.diag(-1,t**4,t**4,t**4)
rv,sv,ev,qv,av,tfv,dv=geometry(gv)
zero('variable scalar from metric',sv-36/t**2)
zero('variable Q components',qv-s.diag(-648/t**4,216,216,216))
zero('variable family divergence',dv(ev+alpha*qv))
nonzero('omitting Hessian breaks divergence',dv(av)[0])
nonzero('Q changes tracefree equation',tfv(qv)[0,0])
rs,ss,es,qs,_,_,_=geometry(ell**2*gv)
zero('Einstein covariant homothety weight zero',es-ev)
zero('Q covariant homothety weight minus two',qs-qv/ell**2)
nonzero('fixed nonzero alpha is not weight zero',(es+alpha*qs-ev-alpha*qv)[0,0])
zero('Ricci and Einstein have same shape',tfv(rv)-tfv(ev))
nonzero('Ricci is not offshell conserved',dv(rv)[0])
zero('Einstein is offshell conserved on control',dv(ev))
zero('nonvanishing response multiple same shape ratio',tfv((1+sv**2)*ev)-(1+sv**2)*tfv(ev))
nonzero('same-zero-set multiplier changes divergence',dv((1+sv**2)*ev)[0])

print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':s.__version__,
 'scope':'Exact diagnostic metrics and inherited f(R) identity; not proof of general classification or UDT admission.',
 'items':checks},indent=2))
