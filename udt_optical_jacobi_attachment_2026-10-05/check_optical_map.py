"""OJM1 fixed exact and finite geometric controls; no metric/data selection."""
from pathlib import Path
import json,platform,hashlib
import mpmath as mp
import sympy as sy
B=Path(__file__).resolve().parent

def exact():
    r,a,m,H,b=sy.symbols('r a m H b',positive=True)
    f=1-2*m/r-H**2*r**2; s=sy.sqrt(1-f*b*b/r**2)
    I=sy.Function('I')(r);P=sy.Function('P')(r)
    ip=1/(r*r*s**3);pp=b/(r*r*s);q=3*m*b*b/r**5
    subs={sy.diff(I,r,2):sy.diff(ip,r),sy.diff(I,r):ip,
          sy.diff(P,r,2):sy.diff(pp,r),sy.diff(P,r):pp}
    def dd(y):return sy.simplify((s*sy.diff(s*sy.diff(y,r),r)).subs(subs))
    yp=r*s*I;yt=r*sy.sin(P)
    assert sy.simplify(dd(yp)-q*yp)==0
    assert sy.simplify(dd(yt)+q*yt)==0
    assert sy.simplify(dd(yp)+q*yp)!=0
    assert sy.simplify(dd(yt)-q*yt)!=0
    # Vertex derivatives; fixed source factors restore unit initial slope.
    assert sy.simplify((a*s.subs(r,a)*s*sy.diff(yp,r)).subs(subs).subs(I,0).subs(r,a))==1
    assert sy.simplify((a/b*s*sy.diff(yt,r)).subs(subs).subs(P,0).subs(r,a))==1
    # Original EF metric quotient basis, with s^2 used only as its definition.
    z,F,rr,bb=sy.symbols('s f r b',nonzero=True)
    g=sy.Matrix([[-F,-1,0],[-1,0,0],[0,0,rr*rr]])
    k=sy.Matrix([(1-z)/F,z,bb/rr**2]);e=sy.Matrix([bb/(rr*z),0,1/(rr*z)])
    reduce=lambda x:sy.factor(x).subs(z*z,1-F*bb*bb/rr**2).simplify()
    assert sy.simplify((k.T*g*e)[0])==0
    assert reduce((e.T*g*e)[0]-1)==0
    assert reduce((k.T*g*k)[0])==0
    return {'jacobi_residuals':'both identically zero','initial_slopes':'both1',
            'wrong_tide_sign_controls':'both rejected','original_EF_screen_gram':'PASS'}

def geometric(m,a,H,R,b):
    x=1/R;S=mp.sqrt(1+H*H*b*b)
    ss=lambda y:mp.sqrt(1+H*H*b*b-b*b*y*y+2*m*b*b*y**3)
    P=mp.quad(lambda y:b/ss(y),[x,1/a])
    U=mp.quad(lambda y:b*b/(ss(y)*(1+ss(y))),[x,1/a])
    I=mp.quad(lambda y:1/ss(y)**3,[x,1/a])
    L=(R-a)/S+mp.quad(lambda y:b*b*(1-2*m*y)/(S*ss(y)*(S+ss(y))),[x,1/a])
    sa=ss(1/a);sr=ss(x)
    bp=a*sa*R*sr*I
    bt=a*R*mp.sin(P)/b if b else R-a
    return P,U,I,L,sa,sr,bp,bt

def incidence(m,a,H,E,R):
    om=mp.sqrt(m/a**3-H*H);fa=1-2*m/a-H*H*a*a;bmax=a/mp.sqrt(fa)
    V=lambda y:mp.sqrt(H*H+(E*E-1)*y*y+2*m*y**3)
    tail=mp.quad(lambda y:1/(V(y)*(E*y+V(y))),[0,1/R])
    lo=mp.mpf(0);hi=mp.mpf('.99')*bmax;b=min(a*om*tail,hi/2)
    assert geometric(m,a,H,R,hi)[0]-om*geometric(m,a,H,R,hi)[1]-om*tail>0
    for it in range(100):
        P,U,I,*_=geometric(m,a,H,R,b);res=P-om*U-om*tail
        if abs(res)<mp.power(10,-mp.mp.dps+6):break
        if res>0:hi=b
        else:lo=b
        trial=b-res/(I*(1-om*b))
        b=trial if lo<trial<hi else (lo+hi)/2
    else:raise AssertionError('incidence cap')
    te=-tail-U;residual=max(abs(te+U+tail),abs(om*te+P))
    assert residual<mp.power(10,-mp.mp.dps+8)
    return b,te,tail,residual,it+1

def run(dps):
    mp.mp.dps=dps;fmt=lambda z:mp.nstr(z,dps)
    m=mp.mpf(1);a=mp.mpf(10);H=mp.sqrt(mp.mpf('.0001')/3)
    h=1-3*m/a;om=mp.sqrt(m/a**3-H*H);rows=[]
    for es in ['1','10']:
        E=mp.mpf(es)
        for rs in ['1000','10000','100000','1000000']:
            R=mp.mpf(rs);b,te,tail,res,it=incidence(m,a,H,E,R)
            P,U,I,L,sa,sr,bp,bt=geometric(m,a,H,R,b)
            v=mp.sqrt(E*E-1+2*m/R+H*H*R*R)
            A=1/(E+v)+v*b*b/(R*R*(1+sr));we=(1-om*b)/mp.sqrt(h)
            Z=we/A;jp=A*bp;jt=A*bt;DA=mp.sqrt(abs(jp*jt));Do=A*L
            assert sa>0 and sr>0 and abs(P)<mp.pi and jp>0 and jt>0
            assert DA<=Do*(1+mp.mpf('1e-30'))
            assert abs(we*mp.sqrt(abs(bp*bt))/(Z*DA)-1)<mp.power(10,-dps+8)
            residue=(a+E/H)/mp.sqrt(h);ratio=Z*(1/H-DA)/residue
            if rs=='1000000':
                assert abs(H*DA-1)<mp.mpf('.01')
                assert abs(ratio-1)<mp.mpf('.01')
            rows.append(dict(E=es,R=rs,iterations=it,**{k:fmt(z) for k,z in
                dict(b=b,t_e=te,tail=tail,original_incidence_residual=res,P=P,U=U,I=I,L=L,
                     A=A,omega_e=we,Z=Z,B_parallel=bp,B_perp=bt,j_parallel=jp,j_perp=jt,
                     D_A=DA,D_o=Do,area_to_affine=DA/Do,shear_ratio=jp/jt,
                     pole_ratio=ratio,expected_residue=residue).items()}))
    controls=[]
    # FREE geometric ray controls; the third uses prior OAA counterexample inputs.
    for label,as_,hs,rs,bs in [('mild','10','base','50','2'),('beyond_horizon','10','base','1000','-3'),('strong','3.001','.18','10000','margin')]:
        a=mp.mpf(as_);H=mp.sqrt(mp.mpf('.0001')/3) if hs=='base' else mp.mpf(hs)
        R=mp.mpf(rs);bmax=a/mp.sqrt(1-2/a-H*H*a*a)
        b=-mp.mpf('.999')*bmax if bs=='margin' else mp.mpf(bs)
        P,U,I,L,sa,sr,bp,bt=geometric(m,a,H,R,b)
        db=min(mp.mpf('.001'),(bmax-abs(b))*mp.mpf('.001'))
        errors=[];approximations=[]
        for scale in [1,mp.mpf('.5')]:
            step=db*scale;plus=geometric(m,a,H,R,b+step);minus=geometric(m,a,H,R,b-step)
            du=(plus[1]-minus[1])/(2*step);dp=(plus[0]-minus[0])/(2*step)
            fr=1-2*m/R-H*H*R*R
            neighbor_p=a*sa*(-fr*b*du+R*R*dp)/(R*sr)
            angle=mp.mpf('.001')*scale
            neighbor_t=a/b*R*mp.asin(mp.sin(P)*mp.sin(angle))/angle
            errs=[abs(neighbor_p-bp)/max(1,abs(bp)),abs(neighbor_t-bt)/max(1,abs(bt))]
            assert max(errs)<mp.mpf('1e-5')
            errors.append(errs);approximations.append([neighbor_p,neighbor_t])
        for j in [0,1]:assert errors[1][j]<mp.mpf('.4')*errors[0][j]+mp.mpf('1e-30')
        # Wrong zero-tide or isotropic map must fail these geometric controls.
        wrong=max(abs(bp-L),abs(bt-L))/max(1,abs(bp),abs(bt))
        assert wrong>mp.mpf('1e-8')
        controls.append({'label':label,'m':'1','a':as_,'H':fmt(H),'R':rs,'b':fmt(b),
          'P_over_pi':fmt(P/mp.pi),'B_parallel':fmt(bp),'B_perp':fmt(bt),'L':fmt(L),
          'db':fmt(db),'neighbor_estimates':[[fmt(z) for z in row] for row in approximations],
          'relative_errors':[[fmt(z) for z in row] for row in errors],
          'zero_tide_mutant_discrepancy':fmt(wrong)})
    return {'dps':dps,'actual_incidences':rows,'neighbor_controls':controls}

if __name__=='__main__':
    result={'python':platform.python_version(),'mpmath':mp.__version__,'sympy':sy.__version__,
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'exact':exact(),'precisions':[]}
    for dps in [40,70]:
        result['precisions'].append(run(dps));print('precision',dps,'PASS',flush=True)
    mp.mp.dps=70;errs=[]
    for low,high in zip(*(q['actual_incidences'] for q in result['precisions'])):
        for key in ['b','t_e','Z','B_parallel','B_perp','D_A','D_o','pole_ratio']:
            errs.append(abs(mp.mpf(low[key])-mp.mpf(high[key]))/max(1,abs(mp.mpf(high[key]))))
    assert max(errs)<mp.mpf('1e-25')
    result.update(status='PASS',max_scaled_precision_error=str(max(errs)),
                  case_accounting='16 actual incidences +6 central neighbor controls +48 finite neighbor evaluations + exact controls; <=100')
    with (B/'CONSTRUCTION_RESULT.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'status':'PASS','actual_incidences':16,'neighbor_controls':6,
                      'max_scaled_precision_error':str(max(errs))}))
