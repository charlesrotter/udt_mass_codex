"""Independent stdlib exact conformal metric residuals from saved log-p jets."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json,platform
N=10
def series(*values): return [Q(x) for x in values]+[Q(0)]*(N-len(values))
one=series(1)
def add(a,b): return [x+y for x,y in zip(a,b)]
def scale(c,a): return [Q(c)*x for x in a]
def mul(a,b): return [sum((a[j]*b[k-j] for j in range(k+1)),Q(0)) for k in range(N)]
def derivative(a): return [Q(i+1)*a[i+1] for i in range(N-1)]+[Q(0)]
def reciprocal(a):
    out=series(1/a[0])
    for k in range(1,N):out[k]=-sum((a[j]*out[k-j] for j in range(1,k+1)),Q(0))/a[0]
    return out
def exponential(a):
    assert a[0]==0
    out=one.copy()
    # p'=log(p)' p determines the exponential coefficients.
    for k in range(1,N):out[k]=sum((Q(j)*a[j]*out[k-j] for j in range(1,k+1)),Q(0))/k
    return out

base=Path(__file__).resolve().parents[1]
source=base/'EXACT_RESULT.json'
data=json.loads(source.read_text())
rows=[]
for row in data['saved_clock_jets']:
    b3,b4,b5=(Q(row[k]) for k in ('b3','b4','b5'))
    logp=series(0,0,0,b3,b4,b5)
    p=exponential(logp); invp=reciprocal(p); p2=mul(p,p)
    ellprime=mul(derivative(p),invp)
    ellsecond=derivative(ellprime)
    ric00=scale(-3,ellsecond)
    ricii=add(ellsecond,scale(2,mul(ellprime,ellprime)))
    # Actual scalar curvature, using g^{ab} Ric_ab.
    R=mul(mul(invp,invp),add(scale(-1,ric00),scale(3,ricii)))
    R2=mul(R,R);R3=mul(R2,R)
    def residual(alpha,beta):
        f=add(R,add(scale(alpha,R2),scale(beta,R3)))
        F=add(one,add(scale(2*alpha,R),scale(3*beta,R2)))
        Fprime=derivative(F); Fsecond=derivative(Fprime)
        # g00 Box F-Hess00 F = 3 ellprime Fprime.
        C=add(mul(F,ric00),add(scale(Q(1,2),mul(p2,f)),scale(3,mul(ellprime,Fprime))))
        # gii Box F-Hessii F = -Fsecond-ellprime Fprime.
        D=add(mul(F,ricii),add(scale(Q(-1,2),mul(p2,f)),add(scale(-1,Fsecond),scale(-1,mul(ellprime,Fprime)))))
        return C,D
    _,d0=residual(Q(0),Q(0))
    _,da=residual(Q(1),Q(0));_,db=residual(Q(0),Q(1))
    aa=[da[i]-d0[i] for i in (0,1)];bb=[db[i]-d0[i] for i in (0,1)]
    rhs=[-d0[i] for i in (0,1)]
    det=aa[0]*bb[1]-aa[1]*bb[0]
    assert det != 0
    alpha=(rhs[0]*bb[1]-rhs[1]*bb[0])/det
    beta=(aa[0]*rhs[1]-aa[1]*rhs[0])/det
    assert alpha==Q(row['alpha']) and beta==Q(row['beta'])
    C,D=residual(alpha,beta)
    assert C[:4]==[Q(0)]*4 and D[:2]==[Q(0)]*2
    assert aa==[-288*b4,-1440*b5]
    assert bb==[-7776*b3*b3,-93312*b3*b4]
    old=-720*alpha*b5-77760*beta*b3*b4-6*b3
    repaired=-720*alpha*b5-46656*beta*b3*b4-6*b3
    assert repaired==D[1]/2==0
    if row['name']=='cubic_completion': assert old==Q(243,50000000)
    rows.append({'name':row['name'],'alpha_from_tensor':str(alpha),'beta_from_tensor':str(beta),
                 'P0_from_metric':str(derivative(R)[0]),'original_00_coefficients':[str(q) for q in C[:4]],
                 'original_spatial_coefficients':[str(q) for q in D[:2]],
                 'alpha_spatial_coefficient_pair':list(map(str,aa)),
                 'beta_spatial_coefficient_pair':list(map(str,bb)),
                 'old_checker_error':str(old),'repaired_checker_error':str(repaired)})
print(json.dumps({'status':'PASS','python':platform.python_version(),'library':'stdlib fractions; no parent helper imports',
                  'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'rows':rows,
                  'scope':'Exact finite metric-jet residuals; no full-interval or observed law claim'},indent=2))
