"""Source-first independent incidence and timing controls; no parent imports."""
from pathlib import Path
import json,platform,hashlib,sys
import mpmath as mp
mp.mp.dps=50
D=mp.mpf
OUT=Path(__file__).resolve().parent/'SOURCE_FIRST_RESULT.json'
rows=[]
case_count=0

def solve(m,a,H,E,bstar,x):
    global case_count
    case_count+=1
    assert case_count<=100
    h=1-3*m/a
    O=mp.sqrt(m/a**3-H**2)
    def s(y,b): return mp.sqrt(1+b*b*(H*H-y*y+2*m*y**3))
    def w(y): return mp.sqrt(H*H+(E*E-1)*y*y+2*m*y**3)
    def P(y,b): return mp.quad(lambda q:b/s(q,b),[y,1/a])
    def U(y,b): return mp.quad(lambda q:b*b/(s(q,b)*(1+s(q,b))),[y,1/a])
    def I(y,b): return mp.quad(lambda q:1/s(q,b)**3,[y,1/a])
    d=mp.quad(lambda y:1/(w(y)*(E*y+w(y))),[0,x])
    C=P(0,bstar)-O*U(0,bstar)
    eq=lambda b:P(x,b)-O*U(x,b)-C-O*d
    b=mp.findroot(eq,(bstar-D('.001'),bstar+D('.001')),tol=D('1e-45'))
    pp,uu,ii=P(x,b),U(x,b),I(x,b)
    sr,sa=s(x,b),s(1/a,b)
    ww=w(x)
    at=1/(E*x+ww)+ww*b*b/(1+sr)
    A=x*at
    Z=(1-O*b)/(mp.sqrt(h)*A)
    bx=(O/(ww*(E*x+ww))+b/sr-O*b*b/(sr*(1+sr)))/((1-O*b)*ii)
    wx=((E*E-1)*x+3*m*x*x)/ww
    sx=(b*bx*(H*H-x*x+2*m*x**3)+b*b*(-x+3*m*x*x))/sr
    atx=-(E+wx)/(E*x+ww)**2+wx*b*b/(1+sr)+2*ww*b*bx/(1+sr)-ww*b*b*sx/(1+sr)**2
    drift=ww*(1+x*(O*bx/(1-O*b)+atx/at))
    sn=b/at
    cs=(sr/(E*x+ww)-ww*b*b/(1+sr))/at
    jpar=A*a*sa*sr*ii/x
    jper=A*a*mp.sin(pp)/(b*x) if b else A*(1/x-a)
    return dict(m=m,a=a,H=H,E=E,bstar=bstar,x=x,b=b,bx=bx,te=-d-uu,
                P=pp,U=uu,I=ii,A=A,Z=Z,drift=drift,sin_alpha=sn,cos_alpha=cs,
                jpar=jpar,jper=jper,residual=abs(eq(b)),unit_error=abs(sn*sn+cs*cs-1))

def encoded(v):
    if isinstance(v,dict):return {k:encoded(x) for k,x in v.items()}
    if isinstance(v,list):return [encoded(x) for x in v]
    if isinstance(v,mp.mpf):return mp.nstr(v,49)
    return v

def save(status,error=None):
    OUT.write_text(json.dumps(encoded(dict(status=status,error=error,case_count=case_count,
        python=sys.version,platform=platform.platform(),mpmath=mp.__version__,precision=mp.mp.dps,
        implementation_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),rows=rows)),indent=2)+'\n')

try:
    m,a,H,E=map(D,['1','8','.02','1.3'])
    eps=D('1e-5');lam=D('3.7')
    maxima={'residual':D(0),'unit_error':D(0),'derivative_error':D(0),'homothety_error':D(0)}
    for bs in map(D,['0','2','-3']):
        errors=[]
        for x in map(D,['.001','.0001','.00001']):
            center=solve(m,a,H,E,bs,x)
            minus=solve(m,a,H,E,bs,x*(1-eps))
            plus=solve(m,a,H,E,bs,x*(1+eps))
            elapsed=mp.quad(lambda y:-1/(y*mp.sqrt(H*H+(E*E-1)*y*y+2*m*y**3)),[minus['x'],plus['x']])
            fd=(mp.log(plus['Z'])-mp.log(minus['Z']))/elapsed
            derr=abs(fd-center['drift'])/H
            scaled=solve(lam*m,lam*a,H/lam,E,lam*bs,x/lam)
            inv=['A','Z','sin_alpha','cos_alpha']
            weights=['b','te','jpar','jper']
            herr=max([abs(scaled[k]-center[k])/max(D(1),abs(center[k])) for k in inv]+[
                abs(scaled[k]/lam-center[k])/max(D(1),abs(center[k])) for k in weights]+[
                abs(lam*scaled['drift']-center['drift'])/H])
            row=dict(center=center,minus=minus,plus=plus,scaled=scaled,receiver_length_increment=elapsed,
                finite_receiver_drift=fd,derivative_relative_error=derr,homothety_error=herr)
            rows.append(row)
            save('RUNNING')
            for r in [center,minus,plus,scaled]:
                maxima['residual']=max(maxima['residual'],r['residual'])
                maxima['unit_error']=max(maxima['unit_error'],r['unit_error'])
                assert r['residual']<D('1e-35')
                assert r['unit_error']<D('1e-35')
            assert derr<D('2e-8')
            assert herr<D('1e-30')
            maxima['derivative_error']=max(maxima['derivative_error'],derr)
            maxima['homothety_error']=max(maxima['homothety_error'],herr)
            errors.append(abs(center['drift']/H-1))
            print('b*=',mp.nstr(bs),'x=',mp.nstr(x),'D/H=',mp.nstr(center['drift']/H,16),flush=True)
        assert errors[-1]<D('.01')
        assert errors[-1]<errors[0]
    save('PASS')
    print(json.dumps(encoded({'status':'PASS','case_count':case_count,'maxima':maxima}),indent=2))
except BaseException as e:
    save('FAIL',repr(e));raise
