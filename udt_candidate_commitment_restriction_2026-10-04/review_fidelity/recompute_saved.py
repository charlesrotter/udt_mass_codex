import hashlib
import json
import resource
from pathlib import Path
import mpmath as mp

resource.setrlimit(resource.RLIMIT_AS, (2*1024**3,2*1024**3))
base = Path(__file__).resolve().parent
source = base.parent/'CONSTRUCTION_RESULT.json'
data = json.loads(source.read_text())
rows = next(z['rows'] for z in data['finite'] if z['dps']==70)
out = []
for dps in [50,90]:
    mp.mp.dps = dps
    m,a,L = mp.mpf(1),mp.mpf(10),mp.mpf('0.0001')
    H=mp.sqrt(L/3); h=1-3*m/a; om=mp.sqrt(m/a**3-L/3)
    f=lambda r:1-2*m/r-L*r*r/3
    tol=mp.mpf('1e-40') if dps==50 else mp.mpf('1e-62')
    for row in rows:
        E,R,b,te = map(mp.mpf,[row['E'],row['R'],row['b'],row['te']])
        v=lambda r:mp.sqrt(E*E-f(r))
        s=lambda r:mp.sqrt(1-f(r)*b*b/(r*r))
        points=sorted(set([a,2*a,10*a,R]))
        P=mp.quad(lambda r:b/(r*r*s(r)),points)
        U=mp.quad(lambda r:b*b/(r*r*s(r)*(1+s(r))),points)
        tail=mp.quad(lambda r:1/(v(r)*(E+v(r))),[R,2*R,10*R,mp.inf])
        residual=max(abs(te+U+tail),abs(om*te+P))
        # Direct EF matrix contraction, no copied rationalized frequency formula.
        ur=(1/(E+v(R)),v(R),mp.mpf(0),mp.mpf(0))
        kr=(b*b/(R*R*(1+s(R))),s(R),mp.mpf(0),b/(R*R))
        g=[[-f(R),-1,0,0],[-1,0,0,0],[0,0,R*R,0],[0,0,0,R*R]]
        A=-sum(g[i][j]*ur[i]*kr[j] for i in range(4) for j in range(4))
        Z=(1-om*b)/(mp.sqrt(h)*A)
        product=H*Z*(-mp.sqrt(h)*te)
        ze=abs(Z/mp.mpf(row['Z'])-1)
        pe=abs(product/mp.mpf(row['H_Z_delta_tau_e'])-1)
        assert residual<tol,(dps,row['E'],row['R'],'residual',str(residual))
        assert ze<tol and pe<tol,(dps,row['E'],row['R'],'contraction')
        errors=list(map(mp.mpf,row['arrival_relative_errors']))
        assert max(errors)<mp.mpf('1e-6') and errors[1]/errors[0]<mp.mpf('.4')
        out.append({'dps':dps,'E':row['E'],'R':row['R'],
                    'original_r_incidence_residual':mp.nstr(residual,30),
                    'saved_Z_relative_error':mp.nstr(ze,30),
                    'saved_product_relative_error':mp.nstr(pe,30),
                    'reported_derivative_error_ratio':mp.nstr(errors[1]/errors[0],30)})
result={'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'mpmath':mp.__version__,'cases':len(out),'rows':out,'verdict':'PASS'}
(base/'SAVED_RECOMPUTE_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
