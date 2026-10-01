"""Full symmetric metric components on 3D grids; CONDITIONAL Ric=0, H=0.

Pure harmonic reduction, no matter, damping, filtering or fitted response.
All numeric discretizations and periodic chart are supplied comparison choices.
"""
import torch

class Engine:
    def __init__(self,n,period,device):
        self.n=n;self.period=period
        f=2*torch.pi*torch.fft.fftfreq(n,d=period/n,device=device,dtype=torch.float64)
        self.freq=torch.meshgrid(f,f,f,indexing='ij')

    def gradients(self,a,ft=None):
        if ft is None:ft=torch.fft.fftn(a,dim=(0,1,2))
        extra=(None,)*(a.ndim-3)
        return [torch.fft.ifftn(1j*k[(...,)+extra]*ft,dim=(0,1,2)).real for k in self.freq]

    def geometry(self,g,v,ft=None):
        spatial=self.gradients(g,ft)
        dg=torch.stack([v,*spatial],dim=-3)
        inv=torch.linalg.inv(g)
        dinv=-torch.einsum('...mp,...apq,...qn->...amn',inv,dg,inv)
        lower=(dg.transpose(-3,-2)+dg.movedim(-3,-1)-dg)/2
        connection=torch.einsum('...ad,...dbc->...abc',inv,lower)
        harmonic=torch.einsum('...ab,...cab->...c',inv,connection)
        return inv,dinv,dg,connection,harmonic

    def rhs(self,g,v):
        fg=torch.fft.fftn(g,dim=(0,1,2));inv,dinv,dg,conn,_=self.geometry(g,v,fg)
        dv=self.gradients(v)
        wave=torch.zeros_like(g)
        for i in range(3):
            wave+=2*inv[...,0,i+1,None,None]*dv[i]
            for j in range(i,3):
                d2=torch.fft.ifftn(-self.freq[i][...,None,None]*self.freq[j][...,None,None]*fg,dim=(0,1,2)).real
                wave+=(1 if i==j else 2)*inv[...,i+1,j+1,None,None]*d2
        nonlinear=torch.einsum('...nab,...amb->...mn',dinv,dg)
        nonlinear=nonlinear+nonlinear.transpose(-2,-1)
        nonlinear+=2*torch.einsum('...abn,...bam->...mn',conn,conn)
        acceleration=-(wave+nonlinear)/inv[...,0,0,None,None]
        return v,(acceleration+acceleration.transpose(-2,-1))/2

    def step(self,g,v,dt):
        a,b=self.rhs(g,v);c,d=self.rhs(g+dt*a/2,v+dt*b/2)
        e,f=self.rhs(g+dt*c/2,v+dt*d/2);h,j=self.rhs(g+dt*e,v+dt*f)
        return g+dt*(a+2*c+2*e+h)/6,v+dt*(b+2*d+2*f+j)/6
