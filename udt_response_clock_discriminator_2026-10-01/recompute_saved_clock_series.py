#!/usr/bin/env python3
"""Exposed exact reconstruction from saved a coefficients; no old solver/helpers."""
from fractions import Fraction as Q
from pathlib import Path
import json,hashlib,sys
B=Path(__file__).resolve().parent
SOURCE=Path('udt_environment_response_candidates_2026-10-01/CUBIC_RECOMPUTATION.json')
N=13
z=lambda:[Q(0) for _ in range(N+1)]
def add(*vs):return [sum((v[i] for v in vs),Q(0))for i in range(N+1)]
def mul(a,b):return [sum((a[j]*b[i-j] for j in range(i+1)),Q(0))for i in range(N+1)]
def scale(a,c):return [Q(c)*v for v in a]
def derivative(a):return [(i+1)*a[i+1] for i in range(N)]+[Q(0)]
def inverse(a):
 assert a[0]!=0
 b=z();b[0]=Q(1)/a[0]
 for n in range(1,N+1):b[n]=-sum((a[k]*b[n-k]for k in range(1,n+1)),Q(0))/a[0]
 return b
def power(a,n):
 if n<0:return power(inverse(a),-n)
 out=z();out[0]=Q(1)
 for _ in range(n):out=mul(out,a)
 return out
def compose(a,t):
 assert t[0]==0
 out=z();powt=z();powt[0]=Q(1)
 for c in a:out=add(out,scale(powt,c));powt=mul(powt,t)
 return out
def clock_from_a(a):
 t=z()
 for n in range(N):t[n+1]=compose(a,t)[n]/Q(n+1)
 p=derivative(t);rate=mul(derivative(p),inverse(p));logp=z()
 for n in range(1,N+1):logp[n]=rate[n-1]/Q(n)
 return t,p,logp
def expressions(p):
 d1=derivative(p);d2=derivative(d1);d3=derivative(d2)
 U=scale(mul(power(d1,2),power(p,-4)),3)
 V=add(scale(mul(mul(d1,d3),power(p,-6)),36),scale(mul(power(d2,2),power(p,-6)),-18),scale(mul(mul(power(d1,2),d2),power(p,-7)),-72))
 H=mul(d1,power(p,-2));R=scale(mul(d2,power(p,-3)),6)
 dt=lambda a:mul(derivative(a),inverse(p))
 K=dt(H);P=dt(R);J=add(scale(mul(R,K),2),dt(P),scale(mul(H,P),-1))
 return U,V,K,J

def main():
 saved=json.loads(SOURCE.read_text());a=[Q(x)for x in saved['a_coefficients']]+[Q(0)]
 assert len(a)==N+1
 t,p,lp=clock_from_a(a);lq=[(Q(2)**n-Q(1))*lp[n]for n in range(N+1)]
 assert lp[:13]==[Q(x)for x in saved['logp_coefficients']]
 assert lq[:13]==[Q(x)for x in saved['logq_coefficients']]
 b3,b5=lp[3],lp[5];alpha=-b3/(120*b5)
 assert alpha==1 and lp[4]==0
 U,V,K,J=expressions(p);c=add(U,scale(V,alpha));shape=add(K,scale(J,alpha))
 assert all(v==0 for v in c[:10]),c[:10]
 assert all(v==0 for v in shape[:9]),shape[:9]
 # Existing cubic proper-time control; original curve is not an equation solution.
 control=z();control[0]=Q(1);control[3]=b3
 ct,cp,clp=clock_from_a(control);cU,cV,cK,cJ=expressions(cp)
 assert clp[3]==b3 and clp[5]==0
 assert cU[4]==27*b3*b3 and cV[4]==0
 assert cK[1]==6*b3 and cJ[1]==0
 assert cU[4]!=0 and cK[1]!=0
 result={'status':'PASS','source':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':sys.version.split()[0],'method':'Exact Fraction arrival recursion t_L=a(t), no old evolution or series helpers. Exposed saved artifact, not fresh prediction.','matched_saved_logp_coefficients':13,'matched_saved_logq_coefficients':13,'b3':str(b3),'b5':str(b5),'reconstructed_alpha':str(alpha),'zero_constraint_coefficients_checked':10,'zero_shape_coefficients_checked':9,'control':{'proper_a':'1+(1/1200)t^3','logp_cubic':str(clp[3]),'logp_quintic':str(clp[5]),'constraint_L4_independent_alpha':str(cU[4]),'shape_L1_independent_alpha':str(cK[1]),'rejected_for_this_equation':True},'limits':'Finite exact series correspondence and supported coefficients only; no finite-interval remainder bound, noisy-data calibration or native physical admission.'}
 with (B/'SAVED_SERIES_RESULT.json').open('x')as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
