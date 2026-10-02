"""ERC1 fixed conditional diagnostics; no native response identification or fit."""
import argparse, hashlib, json, math, platform, sys
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import sympy as sp

ROOT=Path(__file__).resolve().parent
ALPHA=1.0  # FREE: positive-alpha representative in chosen length units.
CASES=[('flat',0.,0.,0.,1),('constant_positive',.01,.04,0.,1),
       ('positive_curvature',0.,.1,0.,1),('negative_curvature',0.,-.1,0.,1),
       ('positive_offset',.01,.14,0.,1),('negative_offset',.01,-.06,0.,1),
       ('contracting',0.,.1,0.,-1),('flat_event',0.,0.,.03,1)]
SETTINGS=[(1e-9,1e-11,.1),(1e-11,1e-13,.05),(1e-13,1e-15,.025)]

def save_json(path,value):
    with Path(path).open('x') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

def symbolic(out):
    checks={}
    def zero(name,x):
        z=sp.simplify(x);checks[name]=str(z)
        if z!=0:raise AssertionError((name,z))
    t,x,y,z=sp.symbols('t x y z');coords=[t,x,y,z]
    a=sp.Function('a')(t); rr=sp.Function('R')(t)
    alpha,lam=sp.symbols('alpha Lambda',nonzero=True)
    g=sp.diag(-1,a*a,a*a,a*a); gi=g.inv()
    gamma=[[[sp.simplify(sum(gi[i,l]*(sp.diff(g[l,k],coords[j])+sp.diff(g[l,j],coords[k])-sp.diff(g[j,k],coords[l])) for l in range(4))/2) for k in range(4)]for j in range(4)]for i in range(4)]
    ric=sp.Matrix(4,4,lambda i,j:sp.simplify(sum(sp.diff(gamma[k][i][j],coords[k])-sp.diff(gamma[k][i][k],coords[j])+sum(gamma[k][i][j]*gamma[l][k][l]-gamma[l][i][k]*gamma[k][j][l] for l in range(4)) for k in range(4))))
    scalar=sp.simplify(sum(gi[i,j]*ric[i,j] for i in range(4) for j in range(4)))
    h,h1,h2,h3,R,P=sp.symbols('H H1 H2 H3 R P')
    adot={sp.diff(a,t):a*h,sp.diff(a,t,2):a*(h1+h*h)}
    zero('metric_scalar',scalar.subs(adot)-6*(h1+2*h*h))
    hes=sp.Matrix(4,4,lambda i,j:sp.diff(rr,coords[i],coords[j])-sum(gamma[k][i][j]*sp.diff(rr,coords[k]) for k in range(4)))
    box=sp.simplify(sum(gi[i,j]*hes[i,j] for i in range(4) for j in range(4)))
    Q=2*rr*ric-rr**2*g/2+2*(g*box-hes)
    # Treat rr as the actual scalar after checking the geometric identity.
    zero('Q_trace',sum(gi[i,j]*Q[i,j] for i in range(4) for j in range(4))-2*rr*(scalar-rr)-6*box)
    zero('Q00',Q[0,0].subs(adot)-(-6*rr*(h1+h*h)+rr**2/2+6*h*sp.diff(rr,t)))
    zero('Q11_over_a2',(Q[1,1]/a**2).subs(adot)-(2*rr*(h1+3*h*h)-rr**2/2-2*sp.diff(rr,t,2)-4*h*sp.diff(rr,t)))
    for i in range(4):
        for j in range(4):
            if i!=j:zero(f'offdiagonal_Ric_Q_{i}{j}',ric[i,j]+Q[i,j])
    for i in [2,3]:zero(f'spatial_Q_equality_{i}',Q[i,i]-Q[1,1])
    F=1+2*alpha*R
    hd=R/6-2*h*h; pd=-3*h*P-(R-4*lam)/(6*alpha)
    C=3*F*h*h-alpha*R*R/2+6*alpha*h*P-lam
    zero('constraint_propagation',sp.diff(C,h)*hd+sp.diff(C,R)*P+sp.diff(C,P)*pd+4*h*C)
    E00=3*h*h+alpha*(-6*R*(hd+h*h)+R*R/2+6*h*P)-lam
    Eii=-2*hd-3*h*h+alpha*(2*R*(hd+3*h*h)-R*R/2-2*pd-4*h*P)+lam
    zero('original_00_constraint',E00-C)
    zero('original_spatial_constraint',Eii-C/3)
    # Independent radial Hessian basis: nn and delta coefficients.
    r,m,mu,A=sp.symbols('r m mu A',positive=True)
    aa=1/(6*m*m); r1=A*sp.exp(-m*r)/r; U=-mu/r
    psi=U-aa*r1; phi=U+aa*r1
    lap=lambda f:sp.diff(f,r,2)+2*sp.diff(f,r)/r
    zero('weak_scalar_reconstruction',4*lap(phi)-2*lap(psi)-r1)
    zero('weak_00',2*lap(phi)-2*aa*lap(r1))
    D=phi-psi
    zero('weak_spatial_nn',sp.diff(D,r,2)-sp.diff(D,r)/r-2*aa*(sp.diff(r1,r,2)-sp.diff(r1,r)/r))
    zero('weak_spatial_delta',sp.diff(D,r)/r+lap(phi)-r1/2+2*aa*(lap(r1)-sp.diff(r1,r)/r))
    zero('weak_null_scalar_cancellation',psi+phi-2*U)
    # The flat-event Taylor coefficient is a dynamical implication, not input.
    deriv=lambda f:sp.diff(f,h)*hd+sp.diff(f,R)*P+sp.diff(f,P)*pd
    zero('flat_event_Hddot',deriv(hd).subs({h:0,R:0,lam:0})-P/6)
    result={'status':'PASS','exact_zero_checks':len(checks),'checks':checks,
            'ricci_from_original_connection':[[str(v) for v in row] for row in ric.tolist()],
            'scalar_from_metric':str(scalar),'Q00':str(Q[0,0]),'Q11':str(Q[1,1]),
            'constraint':str(C),'weak_time_potential':str(psi),'weak_spatial_potential':str(phi),
            'limits':'Finite symbolic component checks plus analytic arguments; not a complete law classification or UDT admission.'}
    save_json(out/'symbolic.json',result)
    return {'status':'PASS','checks':len(checks)}

def weak_clocks():
    mu,A=.2,.1  # FREE: exterior geometric amplitudes, no source/mass identification.
    psi=lambda r:-mu/r-ALPHA*A*math.exp(-r/math.sqrt(6*ALPHA))/r
    pe,po=psi(1.),psi(2.); rows=[]
    for eps in [1/16,1/32,1/64,1/128]:
        logp=.5*(math.log1p(2*eps*po)-math.log1p(2*eps*pe))
        first=eps*(po-pe); error=abs(logp-first)
        bound=eps*eps*(pe*pe+po*po)/(1-2*eps*max(abs(pe),abs(po)))**2
        assert error<=bound
        p=math.exp(logp);q=1/p
        rows.append(dict(epsilon=eps,p=p,q=q,pq=p*q,logp=logp,linear=first,error=error,remainder_bound=bound))
    return rows

def rhs(t,y,lam):
    H,R,P,a,eta=y
    return np.array([R/6-2*H*H,P,-3*H*P-(R-4*lam)/(6*ALPHA),a*H,1/a])

def initial(case):
    name,lam,R,P,branch=case;F=1+2*ALPHA*R
    discr=(6*ALPHA*P)**2+12*F*(ALPHA*R*R/2+lam)
    assert F>.25 and discr>=0
    H=(-6*ALPHA*P+branch*math.sqrt(discr))/(6*F)
    return np.array([H,R,P,1.,0.])

def margin(y):
    H,R,P,a,eta=y
    return min(a-.25,1+2*ALPHA*R-.25,2-abs(H),2-abs(R),2-abs(P))

def evolve(case,setting,end):
    name,lam,*_=case;y0=initial(case);assert margin(y0)>0
    def stop(t,y):return margin(y)
    stop.terminal=True;stop.direction=-1
    rt,at,step=setting
    sol=solve_ivp(lambda t,y:rhs(t,y,lam),(0,end),y0,method='DOP853',rtol=rt,atol=at,max_step=step,dense_output=True,events=stop)
    if not sol.success:raise RuntimeError((name,sol.message))
    return sol

WEIGHTS={d:np.array([float(x) for x in sp.finite_diff_weights(d,list(range(-4,5)),0)[d][-1]]) for d in [1,2,3]}

def from_saved(path,lam):
    with np.load(path) as data:t=data['t'];H,R,P,a,eta=data['y']
    step=float(t[1]-t[0]); core=slice(4,-4)
    diff=lambda values,d:np.correlate(values,WEIGHTS[d],mode='valid')/step**d
    hd,hdd,hddd=(diff(H,d) for d in [1,2,3]);hh=H[core]
    rg=6*(hd+2*hh*hh);rp=6*(hdd+4*hh*hd);rpp=6*(hddd+4*hd*hd+4*hh*hdd)
    q00=-6*rg*(hd+hh*hh)+rg*rg/2+6*hh*rp
    qii=2*rg*(hd+3*hh*hh)-rg*rg/2-2*rpp-4*hh*rp
    e00=3*hh*hh+ALPHA*q00-lam
    eii=-2*hd-3*hh*hh+ALPHA*qii+lam
    n00=1+3*hh*hh+np.abs(ALPHA*q00)+abs(lam)
    nii=1+2*np.abs(hd)+3*hh*hh+np.abs(ALPHA*qii)+abs(lam)
    geom=(rg-R[core])/(1+np.abs(R[core]))
    ad=diff(a,1)-a[core]*hh; an=ad/(1+np.abs(a[core]*hh))
    C=3*(1+2*ALPHA*R)*H*H-ALPHA*R*R/2+6*ALPHA*H*P-lam
    cn=C/(1+3*np.abs((1+2*ALPHA*R)*H*H)+abs(ALPHA)*R*R/2+6*abs(ALPHA)*np.abs(H*P)+abs(lam))
    return {'subdivisions':len(t)-1,'step':step,'original_tensor_absolute':float(max(np.max(np.abs(e00)),np.max(np.abs(eii)))),
            'original_tensor_normalized':float(max(np.max(np.abs(e00/n00)),np.max(np.abs(eii/nii)))),
            'geometry_R_normalized':float(np.max(np.abs(geom))),'metric_clock_normalized':float(np.max(np.abs(an))),
            'constraint_normalized':float(np.max(np.abs(cn))),'a_min':float(a.min()),'F_min':float((1+2*ALPHA*R).min())}

def clocks(sol,L):
    end=float(sol.t[-1]);eta_end=float(sol.y[4,-1]);row={'L':L}
    if eta_end<L:return {**row,'status':'FIRST_NOT_REACHED_WITHIN_WINDOW'}
    tb=brentq(lambda t:sol.sol(t)[4]-L,0,end,xtol=5e-14,rtol=1e-14)
    p=float(sol.sol(tb)[3]);row.update(first_arrival=tb,p=p)
    if eta_end<2*L:return {**row,'status':'ECHO_NOT_REACHED_WITHIN_WINDOW'}
    ta=brentq(lambda t:sol.sol(t)[4]-2*L,0,end,xtol=5e-14,rtol=1e-14)
    total=float(sol.sol(ta)[3]);row.update(status='BOTH_REACHED',echo_arrival=ta,q=total/p,total=total)
    return row

def save_grids(sol,folder,lam):
    rows=[]
    for n in [32,64,128]:
        p=folder/f'grid_{n}.npz';assert not p.exists()
        t=np.linspace(0,sol.t[-1],n+1);np.savez(p,t=t,y=sol.sol(t))
        rows.append(from_saved(p,lam))
    return rows

def residual_gate(rows):
    names=['original_tensor_normalized','geometry_R_normalized','metric_clock_normalized']
    for key in names:
        coarse,fine=rows[0][key],rows[-1][key]
        assert fine<=1e-7,(key,'absolute gate',fine)
        assert fine<=coarse/2 or max(coarse,fine)<=1e-9,(key,'refinement',coarse,fine)
    assert max(r['constraint_normalized'] for r in rows)<=1e-9

def execute(mode,out):
    summary={'mode':mode,'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,
             'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Conditional response diagnostics only; no native UDT admission or empirical fit.'}
    if mode=='symbolic':summary['symbolic']=symbolic(out);summary['weak_clock_rows']=weak_clocks()
    elif mode=='smoke':
        case=CASES[-1];sol=evolve(case,SETTINGS[1],1.);rows=save_grids(sol,out,case[1]);residual_gate(rows)
        c=clocks(sol,.25);assert c['status']=='BOTH_REACHED';assert clocks(sol,2.)['status']=='FIRST_NOT_REACHED_WITHIN_WINDOW'
        assert margin(np.array([0.,0.,0.,.2,0.]))<0
        summary.update(status='PASS',residuals=rows,clock=c,nfev=sol.nfev,domain_event_registered=True,
                       manual_stop='Existing inspected TPS1 capture forwards SIGINT/SIGTERM; no separate interruption replay needed for this short bounded ODE.')
    else:
        allrows=[]
        for case in CASES:
            name,lam,*_=case;entry={'id':name,'Lambda':lam,'initial':initial(case).tolist(),'levels':[]}
            for level,setting in enumerate(SETTINGS):
                folder=out/name/f'level_{level}';folder.mkdir(parents=True)
                sol=evolve(case,setting,6.);rows=save_grids(sol,folder,lam)
                cs=[clocks(sol,L) for L in [.25,1.,2.]]
                run={'setting':list(setting),'end':float(sol.t[-1]),'domain_stop':bool(sol.t_events[0].size),'nfev':sol.nfev,'residuals':rows,'clocks':cs}
                if level==2:
                    residual_gate(rows)
                    if name=='flat_event':
                        beta=case[3]/36;run['cubic']=[dict(**clocks(sol,L),predicted_log_p=beta*L**3,predicted_log_q=7*beta*L**3) for L in [1/8,1/16,1/32]]
                save_json(folder/'result.json',run);entry['levels'].append(run)
            for idx in range(3):
                ref=entry['levels'][-1]['clocks'][idx]
                for run in entry['levels'][:-1]:
                    candidate=run['clocks'][idx];assert candidate['status']==ref['status']
                    for key in ['first_arrival','echo_arrival','p','q','total']:
                        if key in ref:assert abs(candidate[key]-ref[key])<=1e-7*(1+abs(ref[key]))
            if name in ['flat','constant_positive']:
                hh=math.sqrt(lam/3)
                for c in entry['levels'][-1]['clocks']:
                    if c['status']=='BOTH_REACHED':
                        analytic_p=1/(1-hh*c['L']);analytic_total=1/(1-2*hh*c['L'])
                        assert abs(c['p']-analytic_p)<1e-10;assert abs(c['total']-analytic_total)<1e-10
            allrows.append(entry)
        summary.update(status='PASS',cases=allrows,case_count=len(allrows),solve_count=3*len(allrows))
    save_json(out/'summary.json',summary)
    print(json.dumps({'mode':mode,'status':summary.get('status','PASS'),'case_count':summary.get('case_count'),'solve_count':summary.get('solve_count'),'output':str(out)}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['symbolic','smoke','full']);p.add_argument('output');args=p.parse_args()
    output=ROOT/args.output;output.mkdir(parents=True,exist_ok=False)
    execute(args.mode,output)
