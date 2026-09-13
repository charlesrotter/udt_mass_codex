"""Source-first independent full-coordinate Ricci anchor; no author imports."""
import json, platform
import mpmath as mp
mp.mp.dps=40

def field(t,x,modes):
    P=mp.mpf('0'); lam=4*mp.log(mp.mpf(3)/4); vals=[]
    for n,aa,ph in modes:
        w=mp.mpf(n)*3/4; aa=mp.mpf(str(aa)); ph=mp.mpf(str(ph))
        A=-3*mp.pi/4*mp.bessely(0,w); B=3*mp.pi/4*mp.besselj(0,w)
        f=A*mp.besselj(0,w*t)+B*mp.bessely(0,w*t)
        fp=-w*(A*mp.besselj(1,w*t)+B*mp.bessely(1,w*t))
        th=w*x+ph; P+=aa*f*mp.cos(th)
        Lj=t*t*(fp*fp+w*w*f*f)/2+t*f*fp/2-mp.mpf(9)/8
        lam+=aa*aa*(Lj+t*f*fp*mp.cos(2*th)/2)
        vals.append((w,aa,f,fp,th))
    for i,(w,a,f,fp,th) in enumerate(vals):
        for v,b,h,hp,ps in vals[i+1:]:
            lam+=t*a*b*((w*f*hp+v*h*fp)/(w+v)*mp.cos(th+ps)+(w*f*hp-v*h*fp)/(w-v)*mp.cos(th-ps))
    return P,lam

def diagonal(t,x,modes):
    p,l=field(t,x,modes); N2=mp.exp(l/2)/mp.sqrt(t)
    return [-N2,N2,t*mp.exp(p),t*mp.exp(-p)]

def metric_jets(t,x,modes):
    g=diagonal(t,x,modes); d=[[mp.mpf(0) for k in range(4)] for a in range(4)]
    dd=[[[mp.mpf(0) for k in range(4)] for b in range(4)] for a in range(4)]
    for k in range(4):
        fun=lambda u,v:diagonal(u,v,modes)[k]
        for a in range(2):
            d[a][k]=mp.diff(fun,(t,x),(1-a,a))
            for b in range(2):
                dd[a][b][k]=mp.diff(fun,(t,x),(2-a-b,a+b))
    return g,d,dd

def original_ricci(t,x,modes):
    g,d,dd=metric_jets(t,x,modes)
    G=[[[mp.mpf(0) for c in range(4)] for b in range(4)] for a in range(4)]
    dG=[[[[mp.mpf(0) for c in range(4)] for b in range(4)] for a in range(4)] for e in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                Q=(d[b][a] if a==c else 0)+(d[c][a] if a==b else 0)-(d[a][b] if b==c else 0)
                G[a][b][c]=Q/(2*g[a])
                for e in range(4):
                    dQ=(dd[e][b][a] if a==c else 0)+(dd[e][c][a] if a==b else 0)-(dd[e][a][b] if b==c else 0)
                    dG[e][a][b][c]=dQ/(2*g[a])-Q*d[e][a]/(2*g[a]**2)
    R=mp.matrix(4)
    for a in range(4):
        for b in range(4):
            R[a,b]=sum(dG[c][c][a][b]-dG[b][c][a][c]+sum(G[c][a][b]*G[e][c][e]-G[e][a][c]*G[c][b][e] for e in range(4)) for c in range(4))
    return R

if __name__=='__main__':
    records=[]
    for tt,xx,modes in [('1','.7',[(1,.3,0),(2,.15,1.0471975511965976)]),('2.3','1.1',[(1,.3,0),(2,-.15,.6)]),('5.4','-.8',[(1,.4,.2),(3,-.2,.8),(5,.1,-.5)])]:
        t=mp.mpf(tt); x=mp.mpf(xx); P,L=field(t,x,modes)
        pt=mp.diff(lambda u:field(u,x,modes)[0],t); px=mp.diff(lambda z:field(t,z,modes)[0],x)
        lt=mp.diff(lambda u:field(u,x,modes)[1],t); lx=mp.diff(lambda z:field(t,z,modes)[1],x)
        ric=original_ricci(t,x,modes)
        res=max(abs(r) for r in ric); ct=lt-t*(pt*pt+px*px); cx=lx-2*t*pt*px
        assert res<mp.mpf('1e-32'),str(ric)
        assert abs(ct)<mp.mpf('1e-32') and abs(cx)<mp.mpf('1e-32')
        records.append(dict(t=tt,x=xx,modes=modes,ricci_max=str(res),lambda_t_residual=str(ct),lambda_x_residual=str(cx)))
    print(json.dumps(dict(python=platform.python_version(),mpmath=mp.__version__,dps=mp.mp.dps,independence='no author code; full diagonal coordinate metric differentiation',records=records),indent=2))
