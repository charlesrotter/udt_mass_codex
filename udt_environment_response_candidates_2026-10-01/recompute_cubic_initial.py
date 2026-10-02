"""Exposed saved-artifact anchor: rational series, no solver or CAS imports."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json,math
B=Path(__file__).resolve().parent
source=B/'parent_full/summary.json';data=json.loads(source.read_text())
case=next(c for c in data['cases'] if c['id']=='flat_event')
assert case['Lambda']==0 and case['initial'][0:2]==[0.,0.]
N=12;alpha=Q(1)  # FREE positive-alpha unit representative, frozen plan.
p0=Q(str(case['initial'][2]));zero=lambda:[Q(0) for _ in range(N+1)]
H,R,P,a=(zero() for _ in range(4));P[0]=p0;a[0]=1
def product(f,g):return [sum((f[i]*g[n-i] for i in range(n+1)),Q(0)) for n in range(N+1)]
for n in range(N):
    H[n+1]=(R[n]/6-2*product(H,H)[n])/(n+1)
    R[n+1]=P[n]/(n+1)
    P[n+1]=(-3*product(H,P)[n]-R[n]/(6*alpha))/(n+1)
    a[n+1]=product(a,H)[n]/(n+1)
# Using newly written degree n+1 coefficients cannot affect products at degree n.
inverse=zero();inverse[0]=1
for n in range(1,N+1):inverse[n]=-sum(a[k]*inverse[n-k] for k in range(1,n+1))
eta=zero()
for n in range(N):eta[n+1]=inverse[n]/(n+1)
def compose(f,g):
    out=zero();power=zero();power[0]=1
    for coef in f:
        for n in range(N+1):out[n]+=coef*power[n]
        power=product(power,g)
    return out
arrival=zero();arrival[1]=1
for n in range(2,N+1):arrival[n]=-compose(eta,arrival)[n]
adot=[(n+1)*a[n+1] for n in range(N)]+[Q(0)]
dlog=product(adot,inverse);loga=zero()
for n in range(N):loga[n+1]=dlog[n]/(n+1)
logp=compose(loga,arrival);logq=[(2**n-1)*v for n,v in enumerate(logp)]
assert a[3]==p0/36 and a[4]==0 and a[5]==-p0/4320
assert logp[3]==p0/36 and logq[3]==7*p0/36
assert logp[5]==-p0/4320 and logq[5]==-31*p0/4320
C=[3*x+6*alpha*y-alpha*z/2 for x,y,z in zip(product([Q(1)+2*alpha*R[0]]+[2*alpha*x for x in R[1:]],product(H,H)),product(H,P),product(R,R))]
assert all(x==0 for x in C[:N])
rows=[]
for saved in case['levels'][-1]['cubic']:
    L=Q(str(saved['L']))
    predp=float(sum(v*L**n for n,v in enumerate(logp)))
    predq=float(sum(v*L**n for n,v in enumerate(logq)))
    ep=abs(math.log(saved['p'])-predp);eq=abs(math.log(saved['q'])-predq)
    assert max(ep,eq)<5e-13
    rows.append({'L':float(L),'logp_series12':predp,'logq_series12':predq,'saved_logp_error':ep,'saved_logq_error':eq})
result={'status':'PASS','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'initial_P_exact':str(p0),
        'a_coefficients':[str(x) for x in a],'logp_coefficients':[str(x) for x in logp],
        'logq_coefficients':[str(x) for x in logq],'constraint_zero_coefficients_checked':N,
        'comparisons':rows,'exposure':'Parent exposed reconstruction from saved initial data and clock records; separate implementation and exact arithmetic, not fresh-context review or interval certification of the truncated series.'}
with (B/'CUBIC_RECOMPUTATION.json').open('x')as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'status':'PASS','a3':str(a[3]),'a5':str(a[5]),'saved_clock_comparisons':len(rows),'largest_log_error':max(max(r['saved_logp_error'],r['saved_logq_error']) for r in rows)}))
