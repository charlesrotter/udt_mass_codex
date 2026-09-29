"""Independent Fraction controls; no candidate or source implementation imported."""
from fractions import Fraction as F
import json, platform

def mm(a,b): return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def tr(a): return list(map(list,zip(*a)))
def vec(a,v): return [sum(x*y for x,y in zip(r,v)) for r in a]
def diag(v): return [[x if i==j else F(0) for j in range(len(v))] for i,x in enumerate(v)]
def boost(t,j):
    c=(t+1/t)/2; s=(t-1/t)/2
    a=diag([F(1)]*4);a[0][0]=a[j][j]=c;a[0][j]=a[j][0]=s
    return a

def null_read(a,n):
    v=vec(a,[F(1),*n]);return v[0],[x/v[0] for x in v[1:]]
results={}
def check(name,predicate):
    results[name]=bool(predicate)
    assert predicate,name
eta=diag([-F(1),F(1),F(1),F(1)])
eta2=diag([-F(1),F(1)]);k=[[F(0),F(1)],[F(1),F(0)]]
n=[[F(1),F(1)],[-F(1),F(1)]];ni=[[F(1,2),-F(1,2)],[F(1,2),F(1,2)]]
t=F(2);d=diag([1/t,t]);b=mm(mm(n,d),ni)
check('dual_pair_preserved',mm(mm(tr(d),k),d)==k)
check('physical_readout_not_preserved',mm(mm(tr(d),eta2),d)!=eta2)
check('basis_changes_form',mm(mm(tr(n),eta2),n)==[[F(0),-F(2)],[-F(2),F(0)]])
check('conjugate_is_physical_boost',mm(mm(tr(b),eta2),b)==eta2)
check('conjugate_sign',b==[[F(5,4),F(3,4)],[F(3,4),F(5,4)]])
bx=boost(F(3),1);by=boost(F(2),2);prod=mm(bx,by)
for label,a in [('x',bx),('y',by),('product',prod)]:
    check('metric_'+label,mm(mm(tr(a),eta),a)==eta)
ell=[F(1),F(0),F(0)]
f1,n1=null_read(by,ell);f2,n2=null_read(bx,n1);f,n2direct=null_read(prod,ell)
check('direction_carried_product',f==f1*f2 and n2==n2direct)
check('wrong_uncarried_product_rejected',f!=f1*null_read(bx,ell)[0])
check('noncollinear_not_symmetric',prod!=tr(prod))
mid=boost(F(4),3);midinv=boost(F(1,4),3)
new1=mm(mid,by);new2=mm(bx,midinv)
check('intermediate_clock_frame_cancels',mm(new2,new1)==prod)
fm,nm=null_read(new1,ell)
check('intermediate_factors_cancel',fm*null_read(new2,nm)[0]==f)
check('inverse_same_comparison',null_read(mm(boost(F(1,2),2),boost(F(1,3),1)),n2)[0]==1/f)
r=F(2);w=F(1);gamma=(r+1/r+r*w*w)/2;a=gamma-1/r
check('screen_clock_unit',gamma*gamma-a*a-w*w==1)
check('screen_keeps_ratio',gamma-a==1/r)
check('screen_strict_gap',gamma>(r+1/r)/2)
check('screen_exact_mutual',1/gamma==F(4,9))
p=F(2);q=F(3);rad=(p*q-1)/(p*q+1)
check('two_way_can_redshift_both',p>1 and q>1 and rad==F(5,7))
check('two_way_not_inverse',p*q!=1)
print(json.dumps({'python':platform.python_version(),'arithmetic':'Fraction exact','checks':results,'count':len(results),'values':{'f1':str(f1),'f2_carried':str(f2),'f_total':str(f),'f_wrong_uncarried':str(f1*null_read(bx,ell)[0]),'screen_mutual':str(1/gamma),'radar_beta':str(rad)}},indent=2))
