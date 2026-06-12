import numpy as np
exec(open('/tmp/proto.py').read().split("# phase-anchor scan")[0])
F=make_fields(6000,1e-3); r=F['r']; sq=np.sqrt(F['S'])
for k,lab in (('WEE_E','Einstein'),('WEE_N','native')):
    V=F[k]*sq; w2=V**2
    c=np.concatenate([[0.0],np.cumsum(0.5*(w2[1:]+w2[:-1])*np.diff(r))]); c/=c[-1]
    print(lab, "kernel mass interior to 5 Gpc:", f"{np.interp(5.0,r,c):.2e}")
# pointwise ratio interior
m=(r>0.5)&(r<5.0)
rat=np.abs(F['WEE_N'][m]/F['WEE_E'][m])
print("pointwise |W_N/W_E| on 0.5-5 Gpc: min %.2f max %.2f"%(rat.min(),rat.max()))
for lo in (1.0,2.0):
    m=(r>lo)&(r<5.0); rat=np.abs(F['WEE_N'][m]/F['WEE_E'][m])
    print(f"pointwise |W_N/W_E| on {lo}-5 Gpc: min %.2f max %.2f"%(rat.min(),rat.max()))
