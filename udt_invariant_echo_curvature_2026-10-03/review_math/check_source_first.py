"""Independent exact sphere-product incidence control; bounded IEC1 review."""
from pathlib import Path
import json,sys,platform
import sympy as S
import mpmath as mp

OUT=Path(__file__).parent
z,x,y=S.symbols('z x y') # z=L²
R=S.Rational
def trunc(v,n=4):
    return S.Poly(S.expand(v),z).slice(0,n).as_expr() if False else S.Add(*[S.expand(v).coeff(z,i)*z**i for i in range(n)])
def mul(a,b,n=5):return trunc(a*b,n)
def cos(c):return sum((-1)**j*c**(2*j)*z**j/S.factorial(2*j) for j in range(5))
def sinsin(c,d):return sum((-1)**(j+k)*c**(2*j+1)*d**(2*k+1)*z**(j+k+1)/(S.factorial(2*j+1)*S.factorial(2*k+1)) for j in range(4) for k in range(4-j))
def series_sub(f,xx,yy,n=4):
    ans=0
    for i in range(n):
        ans += z**i*trunc(S.expand(f).coeff(z,i).subs({x:xx,y:yy}),n-i)
    return trunc(ans,n)
def root(f,which,first,other):
    v=S.Integer(first)
    for j in range(1,4):
        c=S.Symbol('c')
        xx,yy=(v+c*z**j,other) if which=='x' else (other,v+c*z**j)
        eq=S.expand(series_sub(f,xx,yy,j+1)).coeff(z,j)
        sol=S.solve(eq,c)
        assert len(sol)==1
        v += S.factor(sol[0])*z**j
    xx,yy=(v,other) if which=='x' else (other,v)
    assert series_sub(f,xx,yy)==0
    return v
def lograt(num,den):
    # Constant signs cancel; ratio is1 at z=0.
    a=trunc(num/num.subs(z,0)-1);b=trunc(den/den.subs(z,0)-1)
    return trunc(sum((-1)**(j+1)*(a**j-b**j)/j for j in range(1,4)))
def run(u,g,a):
    b2=1-a*a;h2=1+a*a*u*u;r2=a*a*g*g/h2
    # No radicals needed: cos(hL), (a*g/h)sin(hL) times sin(uL(y-x)).
    ch=sum((-1)**j*h2**j*z**j/S.factorial(2*j) for j in range(5))
    cross=sum((-1)**(j+k)*a*g*h2**j*(u*(y-x))**(2*k+1)*z**(j+k+1)/(S.factorial(2*j+1)*S.factorial(2*k+1)) for j in range(4) for k in range(4-j))
    f=trunc(mul(mul(cos(u*x),cos(u*y)),ch)+mul(sinsin(u*x,u*y),1+(ch-1)*r2)-cross-cos(g*(y-x)+a*u),5)
    assert f.subs(z,0)==0
    f=S.expand(f/z)
    assert S.simplify(f.subs(z,0)-((y-x)**2-1)/2)==0
    relay=root(f,'y',1,S.Integer(0));echo=root(f,'x',2,relay)
    fx=S.diff(f,x);fy=S.diff(f,y)
    lp=lograt(-series_sub(fx,0,relay),series_sub(fy,0,relay))
    lq=lograt(-series_sub(fy,echo,relay),series_sub(fx,echo,relay))
    # log[p/(2-p²)]=3t+4t²+8t³+O(t⁴), t=log p.
    defect=trunc(lq-(3*lp+4*lp**2+8*lp**3))
    T=u*u*b2;V2=u**4*a*a*b2;W2=u*u*g*g*b2
    mp.mp.dps=80
    um=mp.mpf(str(u.p))/int(u.q);gm=mp.mpf(str(g.p))/int(g.q);am=mp.mpf(str(a.p))/int(a.q)
    hm=mp.sqrt(1+am*am*um*um);rm=am*gm/hm
    def FF(s,t,L):
        return mp.cos(um*s)*mp.cos(um*t)*mp.cos(hm*L)+mp.sin(um*s)*mp.sin(um*t)*(1+(mp.cos(hm*L)-1)*rm*rm)-rm*mp.sin(hm*L)*mp.sin(um*(t-s))-mp.cos(gm*(t-s)+am*um*L)
    numeric=[]
    for L in [mp.mpf(1)/10,mp.mpf(1)/20,mp.mpf(1)/40,mp.mpf(1)/80]:
        bb=mp.findroot(lambda t:FF(0,t,L),(L*.95,L*1.05),maxsteps=100)
        aa=mp.findroot(lambda s:FF(s,bb,L),(L*1.9,L*2.1),maxsteps=100)
        pp=-mp.diff(lambda s:FF(s,bb,L),0)/mp.diff(lambda t:FF(0,t,L),bb)
        qq=-mp.diff(lambda t:FF(aa,t,L),bb)/mp.diff(lambda s:FF(s,bb,L),aa)
        dd=mp.log(qq)-mp.log(pp/(2-pp*pp))
        exact=lambda q:mp.mpf(str(q.p))/int(q.q)
        expected=sum(exact(S.factor(defect.coeff(z,j)))*L**(2*j) for j in range(1,4))
        res=max(abs(FF(0,bb,L)),abs(FF(aa,bb,L)))
        assert 0<bb<aa and pp>0 and qq>0 and 2-pp*pp>0 and res<mp.mpf('1e-65')
        numeric.append(dict(L=str(L),relay=str(bb),echo=str(aa),p=str(pp),q=str(qq),D=str(dd),residual=str(res),remainder_over_L8=str((dd-expected)/L**8)))
    rec=dict(u=str(u),gamma=str(g),a=str(a),relay=str(relay),echo=str(echo),logp=str(S.factor(lp)),logq=str(S.factor(lq)),D=str(S.factor(defect)),D_coefficients=[str(S.factor(defect.coeff(z,j))) for j in range(1,4)],T=str(T),V2=str(V2),W2=str(W2),TW2_over3=str(T*W2/3),numeric=numeric)
    print(json.dumps(rec),flush=True)
    return rec

cases=[(R(3,4),R(5,4),R(0)),(R(3,4),R(5,4),R(3,5)),(R(3,4),R(5,4),R(-3,5)),(R(0),R(1),R(3,5))]
rows=[run(*p) for p in cases]
(OUT/'SOURCE_FIRST_RESULT.json').write_text(json.dumps(dict(python=sys.version,platform=platform.platform(),sympy=S.__version__,mpmath=mp.__version__,families=1,parameter_cases=len(cases),finite_incidence_cases=16,rows=rows),indent=2)+'\n')
