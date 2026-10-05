"""Independent original-incidence finite record witness; no parent imports."""
import hashlib,json,platform,sys
from pathlib import Path
import mpmath as mp

mp.mp.dps=70
OUT=Path(__file__).parent
case_count=0

def incidence(params,ell,dps=70):
    global case_count
    case_count+=1
    if case_count>100: raise RuntimeError('CASE_BUDGET')
    with mp.workdps(dps):
        m,a,H,E,R0=map(mp.mpf,params)
        ell=mp.mpf(str(ell))
        assert E==1
        h=1-3*m/a; Omega=mp.sqrt(m/a**3-H**2)
        R=(mp.sqrt(2*m)/H*mp.sinh(mp.asinh(H*R0**mp.mpf('1.5')/mp.sqrt(2*m))+mp.mpf('1.5')*H*ell))**(mp.mpf(2)/3)
        x=1/R
        V=lambda q:mp.sqrt(H**2+(E**2-1)*q*q+2*m*q**3)
        s=lambda q,b:mp.sqrt(1+H*H*b*b-b*b*q*q+2*m*b*b*q**3)
        d=mp.quad(lambda q:1/(V(q)*(E*q+V(q))),[0,x])
        def integrals(b):
            P=mp.quad(lambda q:b/s(q,b),[x,1/a])
            U=mp.quad(lambda q:b*b/(s(q,b)*(1+s(q,b))),[x,1/a])
            return P,U
        def residual(b):
            P,U=integrals(b)
            return P-Omega*U-Omega*d
        b=mp.findroot(residual,Omega*a*x/(H*H),tol=mp.mpf('1e-60'),verify=True)
        res=abs(residual(b))
        assert res<mp.mpf('1e-45')
        vv=V(x); ss=s(x,b)
        alpha=1/(E*x+vv)+vv*b*b/(1+ss)
        Z=(1-Omega*b)/(mp.sqrt(h)*x*alpha)
        nphi=b/alpha
        nr=(ss/(E*x+vv)-vv*b*b/(1+ss))/alpha
        theta=mp.atan2(nphi,nr)
        assert abs(nphi*nphi+nr*nr-1)<mp.mpf('1e-50')
        return {k:mp.nstr(v,65) for k,v in dict(ell=ell,R=R,b=b,Z=Z,theta=theta,logZ=mp.log(Z),logtheta=mp.log(theta),incidence_residual=res).items()}

def main():
    params=[['1','10','0.005','1','20000000'],['2','20','0.0025','1','40000000']]
    rows=[]; windows=[]; summaries=[]
    for label,centres in [('short',['0','0.8','1.6']),('long',['0','100','200'])]:
        for centre in centres:
            per=[]
            for history,p in enumerate(params):
                endpoints=[]
                for sign in [-1,1]:
                    ell=mp.mpf(centre)+sign*mp.mpf('.01')
                    row=incidence(p,mp.nstr(ell,50)); row.update(history=history,span=label,centre=centre)
                    rows.append(row); endpoints.append(row)
                per.append({key:sum(mp.mpf(r[key]) for r in endpoints)/2 for key in ['logZ','logtheta']})
            win=dict(span=label,centre=centre)
            for key in ['logZ','logtheta']:
                win[key+'_history0']=mp.nstr(per[0][key],65)
                win[key+'_history1']=mp.nstr(per[1][key],65)
                win[key+'_midpoint']=mp.nstr((per[0][key]+per[1][key])/2,65)
                win[key+'_half_difference']=mp.nstr(abs(per[0][key]-per[1][key])/2,65)
            windows.append(win)
        selected=[r for r in windows if r['span']==label]
        peak={key: max(mp.mpf(r[key+'_half_difference']) for r in selected) for key in ['logZ','logtheta']}
        summaries.append(dict(span=label,peak_half_difference={k:mp.nstr(v,65) for k,v in peak.items()},compatible_both_channels=all(v<=mp.mpf('.0025') for v in peak.values())))
    precision=[]
    for row in [rows[0],rows[11],rows[12],rows[23]]:
        new=incidence(params[row['history']],row['ell'],90)
        err=max(abs(mp.mpf(new[k])-mp.mpf(row[k]))/max(1,abs(mp.mpf(new[k]))) for k in ['R','b','Z','theta','logZ','logtheta'])
        assert err<mp.mpf('1e-40')
        precision.append(dict(ell=row['ell'],history=row['history'],relative_discrepancy=mp.nstr(err,20)))
    assert summaries[0]['compatible_both_channels']
    result=dict(status='PASS',method='Independent high-precision original CPR incidence quadratures and exact E=1 proper-time radius; finite two-point log averages',python=sys.version,mpmath=mp.__version__,platform=platform.platform(),case_count=case_count,params=params,rows=rows,windows=windows,summaries=summaries,precision_replays=precision,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (OUT/'INDEPENDENT_RECORDS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','case_count','summaries','precision_replays']}))

if __name__=='__main__':main()
