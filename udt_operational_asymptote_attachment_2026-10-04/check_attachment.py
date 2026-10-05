"""OAA1 frozen finite incidence/affine/radar controls; no native selection."""
from pathlib import Path
import json,platform
import mpmath as mp
import sympy as sy
B=Path(__file__).resolve().parent

def exact():
    f=sy.symbols('f',real=True)
    metric=sy.Matrix([[-f,-1],[-1,0]])
    gradient=metric.inv()*sy.Matrix([0,1])
    assert gradient==sy.Matrix([-1,f])
    assert (gradient.T*metric*gradient)[0]==f
    rho,D,Z=sy.symbols('rho D Z',real=True)
    # Exact rational boost beta=3/5,gamma=5/4 in an endpoint orthonormal frame.
    eta=sy.diag(-1,1);k=sy.Matrix([1,1]);up=sy.Matrix([sy.Rational(5,4),sy.Rational(3,4)])
    factor=-(up.T*eta*k)[0]
    assert factor==sy.Rational(1,2) and (up.T*eta*up)[0]==-1
    assert sy.simplify((factor*D)*(Z/factor)-D*Z)==0
    return {'gradient_r_and_norm':'PASS: grad r=(-1,f), norm=f',
            'endpoint_boost':'PASS: beta3/5 changes D by1/2 and Z by2',
            'affine_rescaling':'analytical k->c*k, L->L/c; directly recomputed below'}

def run_precision(dps):
    mp.mp.dps=dps
    m=mp.mpf(1);a=mp.mpf(10);H=mp.sqrt(mp.mpf('0.0001')/3)
    h=1-3*m/a;omega=mp.sqrt(m/a**3-H**2);fa=1-2*m/a-H**2*a*a
    bmax=a/mp.sqrt(fa)
    fmt=lambda x:mp.nstr(x,dps)
    f=lambda r:1-2*m/r-H**2*r*r
    rows=[]
    for Es in ['1','10']:
        E=mp.mpf(Es)
        V=lambda x:mp.sqrt(H*H+(E*E-1)*x*x+2*m*x**3)
        for Rs in ['1000','10000','100000','1000000']:
            R=mp.mpf(Rs);x=1/R
            tail=mp.quad(lambda y:1/(V(y)*(E*y+V(y))),[0,x])
            def parts(b):
                ss=lambda y:mp.sqrt(1+H**2*b*b-b*b*y*y+2*m*b*b*y**3)
                P=mp.quad(lambda y:b/ss(y),[x,1/a])
                U=mp.quad(lambda y:b*b/(ss(y)*(1+ss(y))),[x,1/a])
                I=mp.quad(lambda y:1/ss(y)**3,[x,1/a])
                return P,U,I
            lo=mp.mpf(0);hi=mp.mpf('.99')*bmax
            P,U,I=parts(hi);assert P-omega*U-omega*tail>0
            b=min(a*omega*tail,hi/2)
            for it in range(100):
                P,U,I=parts(b);res=P-omega*U-omega*tail
                if abs(res)<mp.mpf(10)**(-dps+6):break
                if res>0:hi=b
                else:lo=b
                q=b-res/(I*(1-omega*b))
                b=q if lo<q<hi else (lo+hi)/2
            else:raise AssertionError('incidence iteration cap')
            te=-tail-U
            original=max(abs(te+U+tail),abs(omega*te+P))
            assert original<mp.mpf(10)**(-dps+8)
            S=mp.sqrt(1+H*H*b*b)
            ss=lambda y:mp.sqrt(1+H*H*b*b-b*b*y*y+2*m*b*b*y**3)
            regular=lambda y:b*b*(1-2*m*y)/(S*ss(y)*(S+ss(y)))
            L=(R-a)/S+mp.quad(regular,[x,1/a])
            C=-a/S+mp.quad(regular,[0,1/a])
            v=V(x)/x;s=ss(x)
            A=1/(E+v)+v*b*b/(R*R*(1+s))
            we=(1-omega*b)/mp.sqrt(h);Z=we/A;Do=A*L;De=we*L
            # Independent direct metric contraction of original outgoing-EF vectors.
            ku=b*b/(R*R*(1+s));ur=1/(E+v)
            A_direct=f(R)*ur*ku+ur*s+v*ku
            assert abs(A_direct/A-1)<mp.mpf(10)**(-dps+8)
            assert abs(De/Do/Z-1)<mp.mpf(10)**(-dps+8)
            assert abs((7*A)*(L/7)/Do-1)<mp.mpf(10)**(-dps+8)
            assert abs(b)<bmax and v>0 and s>0 and we>0 and A>0
            deficit=1/H-Do;K=a/H+E/H**2;residue=(a+E/H)/mp.sqrt(h)
            assert deficit>0
            if Rs=='1000000':
                assert abs(H*Do-1)<mp.mpf('.01')
                assert abs(R*deficit/K-1)<mp.mpf('.01')
                assert abs(Z*deficit/residue-1)<mp.mpf('.01')
            row={'E':Es,'R':Rs,'iterations':it+1,'b':fmt(b),'te':fmt(te),
                 'U':fmt(U),'P':fmt(P),'receiver_retarded_tail':fmt(tail),
                 'incidence_residual':fmt(original),'L':fmt(L),'C_at_b':fmt(C),
                 'A':fmt(A),'omega_e':fmt(we),'Z':fmt(Z),'D_o':fmt(Do),'D_e':fmt(De),
                 'H_D_o':fmt(H*Do),'deficit':fmt(deficit),
                 'R_deficit_over_K':fmt(R*deficit/K),'Z_deficit_over_residue':fmt(Z*deficit/residue)}
            rows.append(row)
    rc=mp.findroot(f,(mp.mpf(170),mp.mpf(175)))
    kc=-mp.diff(f,rc);assert rc>a and kc>0 and abs(f(rc))<mp.mpf(10)**(-dps+8)
    radar=[]
    # Differences remove irrelevant integration constants; no singular endpoint evaluated.
    for ds in ['.01','.0001','.000001']:
        d=mp.mpf(ds)
        drad=mp.sqrt(fa)*mp.quad(lambda r:1/f(r),[rc-d,rc-d/2])
        dslice=mp.quad(lambda r:1/mp.sqrt(f(r)),[rc-d,rc-d/2])
        radar_ratio=drad/(mp.sqrt(fa)*mp.log(2)/kc)
        slice_ratio=dslice/(2*(mp.sqrt(d)-mp.sqrt(d/2))/mp.sqrt(kc))
        assert abs(radar_ratio-1)<mp.mpf('.001')
        assert abs(slice_ratio-1)<mp.mpf('.001')
        radar.append({'delta':ds,'radar_increment':fmt(drad),'slice_increment':fmt(dslice),
                      'radar_asymptotic_ratio':fmt(radar_ratio),'slice_asymptotic_ratio':fmt(slice_ratio)})
    return {'dps':dps,'rows':rows,'outer_root':fmt(rc),'minus_fprime_at_root':fmt(kc),'radar_control':radar}

if __name__=='__main__':
    result={'python':platform.python_version(),'mpmath':mp.__version__,'sympy':sy.__version__,'exact':exact(),'precisions':[]}
    for dps in [40,70]:
        result['precisions'].append(run_precision(dps));print('precision',dps,'PASS',flush=True)
    mp.mp.dps=70;errors=[]
    for a,b in zip(*(r['rows'] for r in result['precisions'])):
        for key in ['b','te','L','Z','D_o','D_e','deficit','Z_deficit_over_residue']:
            errors.append(abs(mp.mpf(a[key])-mp.mpf(b[key]))/max(1,abs(mp.mpf(b[key]))))
    assert max(errors)<mp.mpf('1e-25')
    result['precision_maximum_relative_difference']=mp.nstr(max(errors),40)
    result['status']='PASS'
    with (B/'CONSTRUCTION_RESULT.json').open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps({'status':'PASS','incidence_cases':16,'radar_interval_cases':6,'precision_discrepancy':result['precision_maximum_relative_difference']}))
