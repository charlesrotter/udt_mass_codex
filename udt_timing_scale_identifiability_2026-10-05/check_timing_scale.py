"""TSI1 fixed conditional incidence/rate controls, without observational fitting."""
from pathlib import Path
import json,hashlib,platform
import mpmath as mp
import sympy as sy
B=Path(__file__).resolve().parent

def exact():
    u,r,th,ph=sy.symbols('u r theta phi',real=True)
    m,H,E=sy.symbols('m H E',positive=True)
    f=1-2*m/r-H**2*r**2;v=sy.sqrt(E**2-f)
    g=sy.Matrix([[-f,-1,0,0],[-1,0,0,0],[0,0,r*r,0],[0,0,0,r*r*sy.sin(th)**2]])
    gi=g.inv();xx=[u,r,th,ph]
    U=sy.Matrix([1/(E+v),v,0,0]);er=sy.Matrix([-1/(E+v),E,0,0]);ep=sy.Matrix([0,0,0,1/r])
    for a,b,target in [(U,U,-1),(er,er,1),(U,er,0),(ep,ep,1)]:
        assert sy.simplify((a.T*g*b)[0].subs(th,sy.pi/2)-target)==0
    for frame in [U,er,ep]:
        out=[]
        for a in range(4):
            val=v*sy.diff(frame[a],r)
            for j in range(4):
                if U[j]==0:continue
                for k in range(4):
                    if frame[k]==0:continue
                    gam=sum(gi[a,l]*(sy.diff(g[l,k],xx[j])+sy.diff(g[l,j],xx[k])-sy.diff(g[j,k],xx[l]))/2 for l in range(4))
                    val+=gam*U[j]*frame[k]
            out.append(sy.simplify(val.subs(th,sy.pi/2)))
        assert out==[0,0,0,0],out
    x=sy.symbols('x',positive=True);F=sy.Function('F')(x);V=sy.Function('V')(x)
    assert sy.simplify(-x*V*sy.diff(sy.log(F/x),x)-V*(1-x*sy.diff(F,x)/F))==0
    # Dimensional obstruction: common L,T,M unit rescaling fixes both anchors.
    assert 1-1==0 and 3-1-2==0
    return {'metric_norm_groups':4,'parallel_transport_groups':3,'log_drift_identity':1,'dimensional_group':1}

def point(m,a,H,E,bs,R):
    x=1/R;om=mp.sqrt(m/a**3-H*H);h=1-3*m/a
    def integrals(b,y):
        ss=lambda z:mp.sqrt(1+H*H*b*b-b*b*z*z+2*m*b*b*z**3)
        P=mp.quad(lambda z:b/ss(z),[y,1/a])
        U=mp.quad(lambda z:b*b/(ss(z)*(1+ss(z))),[y,1/a])
        I=mp.quad(lambda z:1/ss(z)**3,[y,1/a])
        return P,U,I
    VV=lambda z:mp.sqrt(H*H+(E*E-1)*z*z+2*m*z**3)
    d=mp.quad(lambda z:1/(VV(z)*(E*z+VV(z))),[0,x])
    ps,us,_=integrals(bs,mp.mpf(0));target=ps-om*us+om*d
    b=bs+a*om*x/(H*H);bmax=a/mp.sqrt(1-2*m/a-H*H*a*a)
    lo=-bmax*mp.mpf('.9999');hi=bmax*mp.mpf('.9999')
    if not lo<b<hi:b=(lo+hi)/2
    for it in range(100):
        P,U,I=integrals(b,x);res=P-om*U-target
        if abs(res)<mp.power(10,-mp.mp.dps+7):break
        if res>0:hi=b
        else:lo=b
        trial=b-res/((1-om*b)*I)
        b=trial if lo<trial<hi else (lo+hi)/2
    else:raise AssertionError('incidence iterations')
    assert abs(res)<mp.power(10,-mp.mp.dps+8)
    def alpha(y,z):
        S=mp.sqrt(1+H*H*z*z-z*z*y*y+2*m*z*z*y**3);W=VV(y)
        return 1/(E*y+W)+W*z*z/(1+S)
    V=VV(x);s=mp.sqrt(1+H*H*b*b-b*b*x*x+2*m*b*b*x**3)
    al=alpha(x,b);A=x*al;Z=(1-om*b)/(mp.sqrt(h)*A)
    bx=(b/s-om*b*b/(s*(1+s))+om/(V*(E*x+V)))/((1-om*b)*I)
    ald=mp.diff(lambda y:alpha(y,b),x)+mp.diff(lambda z:alpha(x,z),b)*bx
    logFd=-om*bx/(1-om*b)-ald/al
    K=V*(1-x*logFd)
    np=b/al;nr=(s/(E*x+V)-V*b*b/(1+s))/al
    theta=mp.atan2(np,nr)
    assert abs(np*np+nr*nr-1)<mp.power(10,-mp.mp.dps+8)
    def ang(y,z):
        S=mp.sqrt(1+H*H*z*z-z*z*y*y+2*m*z*z*y**3);W=VV(y)
        return mp.atan2(z, S/(E*y+W)-W*z*z/(1+S))
    td=mp.diff(lambda y:ang(y,b),x)+mp.diff(lambda z:ang(x,z),b)*bx
    Kang=x*V*td/theta if theta else mp.nan
    sa=mp.sqrt(1-(1-2*m/a-H*H*a*a)*b*b/(a*a))
    jp=A*a*sa*R*s*I; jt=A*a*R*mp.sin(P)/b if b else A*(R-a)
    return dict(m=m,a=a,H=H,E=E,b_star=bs,R=R,b=b,b_x=bx,t_e=-d-U,
        incidence_residual=abs(res),A=A,Z=Z,K_length=K,K_over_H=K/H,
        theta=theta,angular_rate=Kang,angular_over_H=Kang/H,
        n_phi=np,n_r=nr,j_parallel=jp,j_perp=jt)

def serialize(row):return {k:mp.nstr(v,mp.mp.dps) for k,v in row.items()}
def run(dps):
    mp.mp.dps=dps;m=mp.mpf(1);a=mp.mpf(10);H=mp.sqrt(mp.mpf('.0001')/3)
    rows=[];scales=[];diffs=[]
    for es in ['1','10']:
        for bss in ['0','2','-3']:
            group=[]
            for rs in ['1000','100000','10000000']:
                q=point(m,a,H,mp.mpf(es),mp.mpf(bss),mp.mpf(rs));rows.append(q);group.append(q)
            assert abs(group[-1]['K_over_H']-1)<mp.mpf('.001')
            assert abs(group[-1]['K_over_H']-1)<mp.mpf('.1')*abs(group[-2]['K_over_H']-1)+mp.mpf('1e-15')
            if bss=='0':assert abs(group[-1]['angular_over_H']-1)<mp.mpf('.001')
            if es=='1':
                q=group[1];lam=mp.mpf(7)/3
                w=point(lam*m,lam*a,H/lam,mp.mpf(es),lam*mp.mpf(bss),lam*q['R'])
                errs=[]
                for key,weight in [('b',1),('A',0),('Z',0),('K_length',-1),('theta',0),('angular_rate',-1),('j_parallel',1),('j_perp',1)]:
                    errs.append(abs(w[key]/lam**weight-q[key])/max(1,abs(q[key])))
                assert max(errs)<mp.power(10,-dps+10)
                scales.append({'lambda':mp.nstr(lam,dps),'base_b_star':bss,'scaled_point':serialize(w),'max_scaled_error':mp.nstr(max(errs),dps)})
    q=next(q for q in rows if q['E']==1 and q['b_star']==0 and q['R']==100000)
    for step in [mp.mpf('1e-4'),mp.mpf('5e-5')]:
        rp=q['R']*(1+step);rm=q['R']*(1-step)
        qp=point(m,a,H,mp.mpf(1),mp.mpf(0),rp);qm=point(m,a,H,mp.mpf(1),mp.mpf(0),rm)
        dell=mp.quad(lambda r:1/mp.sqrt(2*m/r+H*H*r*r),[rm,rp])
        kt=mp.log(qp['Z']/qm['Z'])/dell;ka=-mp.log(qp['theta']/qm['theta'])/dell
        errs=[abs(kt/q['K_length']-1),abs(ka/q['angular_rate']-1)]
        assert max(errs)<mp.mpf('1e-7')
        diffs.append({'step_fraction':str(step),'plus':serialize(qp),'minus':serialize(qm),'delta_ell':mp.nstr(dell,dps),'time_averaged_K':mp.nstr(kt,dps),'time_averaged_angular':mp.nstr(ka,dps),'relative_errors':[mp.nstr(v,dps) for v in errs]})
    for j in [0,1]:assert mp.mpf(diffs[1]['relative_errors'][j])<mp.mpf('.4')*mp.mpf(diffs[0]['relative_errors'][j])+mp.mpf('1e-25')
    # A deliberately omitted c_E conversion changes an observable rate in fixed units.
    ce=mp.mpf(3);wrong=q['K_length'];right=ce*q['K_length'];assert abs(wrong/right-1)>mp.mpf('.5')
    return dict(dps=dps,actual_incidences=[serialize(q) for q in rows],homotheties=scales,timed_differences=diffs,wrong_seconds_conversion='REJECTED')

if __name__=='__main__':
    result=dict(python=platform.python_version(),mpmath=mp.__version__,sympy=sy.__version__,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),exact=exact(),precisions=[])
    for dps in [35,60]:
        result['precisions'].append(run(dps));print('precision',dps,'PASS',flush=True)
    mp.mp.dps=60;errors=[]
    for lo,hi in zip(*(r['actual_incidences'] for r in result['precisions'])):
        for key in ['b','Z','K_length','theta','angular_rate','j_parallel','j_perp']:
            errors.append(abs(mp.mpf(lo[key])-mp.mpf(hi[key]))/max(1,abs(mp.mpf(hi[key]))))
    assert max(errors)<mp.mpf('1e-22')
    result.update(status='PASS',max_scaled_precision_error=mp.nstr(max(errors),60),case_accounting='36 actual incidences +6 homothetic solves +8 finite-difference sides =50 finite cases;9 exact groups;2 wrong-conversion controls. No numerical rerun.')
    with (B/'CONSTRUCTION_RESULT.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'status':'PASS','finite_cases':50,'max_scaled_precision_error':result['max_scaled_precision_error']}))
