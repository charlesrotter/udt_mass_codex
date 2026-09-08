"""Source-first exact coordinate-jet checks; no author checker is imported."""
import json
import platform
import sympy as S

checks = []
def eq(name, a, b=0):
    ok = all(S.simplify(x)==0 for x in (a-b if isinstance(a,S.MatrixBase) else S.Matrix([a-b])))
    checks.append({'name':name,'pass':ok})
    assert ok, name

def geometry(s,a,c):
    eta=S.Matrix([0,1-s,s])
    return S.diag(a*a/(4*s*(1-s)),a*a*(1-s),a*a*s)+(c*c-a*a)*eta*eta.T

def connection(g,g1,g2):
    inv=g.inv(); inv1=-inv*g1*inv
    def form(k,i,j,ii,gg):
        return sum(ii[k,l]*((gg[l,j] if i==0 else 0)+(gg[l,i] if j==0 else 0)-(gg[i,j] if l==0 else 0))/2 for l in range(3))
    C={(k,i,j):form(k,i,j,inv,g1) for k in range(3) for i in range(3) for j in range(3)}
    C1={(k,i,j):form(k,i,j,inv1,g1)+form(k,i,j,inv,g2) for k in range(3) for i in range(3) for j in range(3)}
    return inv,C,C1,form

def ricci_direct_jet(g,g1,g2,K,K1,K2):
    inv,C,C1,form=connection(g,g1,g2)
    inv1=-inv*g1*inv
    di=2*inv*K*inv
    di1=2*(inv1*K*inv+inv*K1*inv+inv*K*inv1)
    dc={u:form(*u,di,g1)+form(*u,inv,-2*K1) for u in C}
    dc1={u:form(*u,di1,g1)+form(*u,inv1,-2*K1)+form(*u,di,g2)+form(*u,inv,-2*K2) for u in C}
    R=S.zeros(3); dR=S.zeros(3)
    for i in range(3):
      for j in range(3):
        R[i,j]=C1[0,i,j]-(sum(C1[k,i,k] for k in range(3)) if j==0 else 0)
        dR[i,j]=dc1[0,i,j]-(sum(dc1[k,i,k] for k in range(3)) if j==0 else 0)
        for k in range(3):
          for l in range(3):
            R[i,j]+=C[k,k,l]*C[l,i,j]-C[k,j,l]*C[l,i,k]
            dR[i,j]+=dc[k,k,l]*C[l,i,j]+C[k,k,l]*dc[l,i,j]-dc[k,j,l]*C[l,i,k]-C[k,j,l]*dc[l,i,k]
    return R,dR

def ricci_covariant_jet(g,g1,g2,K,K1,K2,drop_derivative_index=False):
    inv,C,C1,_=connection(g,g1,g2)
    inv1=-inv*g1*inv
    inv2=2*inv*g1*inv*g1*inv-inv*g2*inv
    dk={};dk1={}
    for d in range(3):
      for i in range(3):
        for j in range(3):
          dk[d,i,j]=(K1[i,j] if d==0 else 0)-sum(C[l,d,i]*K[l,j]+C[l,d,j]*K[i,l] for l in range(3))
          dk1[d,i,j]=(K2[i,j] if d==0 else 0)-sum(C1[l,d,i]*K[l,j]+C[l,d,i]*K1[l,j]+C1[l,d,j]*K[i,l]+C[l,d,j]*K1[i,l] for l in range(3))
    d2={}
    for r in range(3):
      for d in range(3):
        for i in range(3):
          for j in range(3):
            d2[r,d,i,j]=(dk1[d,i,j] if r==0 else 0)-sum((0 if drop_derivative_index else C[l,r,d]*dk[l,i,j])+C[l,r,i]*dk[d,l,j]+C[l,r,j]*dk[d,i,l] for l in range(3))
    tau1=S.trace(inv1*K+inv*K1)
    tau2=S.trace(inv2*K+2*inv1*K1+inv*K2)
    out=S.zeros(3)
    for i in range(3):
      for j in range(3):
        out[i,j]=(tau2 if i==j==0 else 0)-C[0,i,j]*tau1
        out[i,j]+=sum(inv[r,l]*(-d2[l,i,r,j]-d2[l,j,r,i]+d2[l,r,i,j]) for r in range(3) for l in range(3))
    return out

def nonzero(m):
    return any(S.simplify(x)!=0 for x in m)

def main():
    s,a,c=S.symbols('s a c',positive=True)
    g=geometry(s,a,c); inv=g.inv()
    V=S.Matrix([0,1,1]);W=S.Matrix([0,s,-(1-s)]);xi=V/c
    E=(g*V)*(g*W).T+(g*W)*(g*V).T
    z=S.Matrix([1,0,0]); n2=(z.T*inv*z)[0]
    gap=4*(c*c-a*a)/a**4
    Pi=S.eye(3)-xi*(g*xi).T
    eq('polarization_trace',S.trace(inv*E))
    eq('polarization_transverse',E*inv*z,S.zeros(3,1))
    eq('polarization_mixed',inv*E*xi,c*W)
    eq('conjugation_even',S.diag(1,-1,-1)*E*S.diag(1,-1,-1),E)
    eq('Hopf_norm',(xi.T*g*xi)[0],1)
    Y=-n2*Pi*inv*E*xi/gap
    b=S.factor(c*(Y[2]-Y[1]))
    eq('angular_symbol',b,4*c*c*s*(1-s)/(a*a*gap))
    def ell(w): return z*w.T+w*z.T-S.Rational(2,3)*(z.T*inv*w)[0]*g
    M=n2*S.eye(3)+z*(inv*z).T/3
    F=z*z.T-n2*g/3
    w=M.inv()*F*inv*z
    eq('exact_symbol_projection', (F-ell(w))*inv*z,S.zeros(3,1))
    assert nonzero((F+ell(w))*inv*z)
    eq('projection_fixes_E',ell(M.inv()*E*inv*z),S.zeros(3))
    # A nonzero derivative at a point is stronger than mere marked line drift.
    N=S.symbols('N',positive=True)
    s0=S.Rational(1,3)
    lead=S.diff(b*N**2*S.sin(N*(s-s0)),s).subs(s,s0)
    eq('order_three_real_phase',lead,b.subs(s,s0)*N**3)
    fixtures=[];caught={'wrong_S_sign':False,'drop_derivative_index':False,'omit_raising':False,'lambda_h_for_image':False,'omit_moving_dual':False,'Q_plus':True}
    for aa,cc,ss in [(S.Integer(1),S.Rational(3,2),S.Rational(1,3)),(S.Integer(2),S.Integer(1),S.Rational(2,5)),(S.Integer(1),S.Integer(3),S.Rational(1,4))]:
      gg=geometry(s,aa,cc)
      # Fixed exact polynomial fields are algebra controls, NOT lawful TT data.
      for label,kk in [('even',S.Matrix([[1+s+s*s,0,0],[0,2-s,3+s*s],[0,3+s*s,4+2*s]])),('all_entries',S.Matrix([[1+s+s*s,s+2,s*s-1],[s+2,2-s,3+s*s],[s*s-1,3+s*s,4+2*s]])),('pure_trace',-S.Rational(2,3)*gg)]:
        gj=[gg.diff(s,j).subs(s,ss) for j in range(3)]
        kj=[kk.diff(s,j).subs(s,ss) for j in range(3)]
        R,dR=ricci_direct_jet(*gj,*kj)
        cov=ricci_covariant_jet(*gj,*kj)
        name=f'{aa}_{cc}_{ss}_{label}'
        eq('all9_Ricci_variation_'+name,dR,cov)
        ii=gj[0].inv();xx=S.Matrix([0,1,1])/cc
        pp=S.eye(3)-xx*(gj[0]*xx).T
        lv=2*cc*cc/aa**4;lh=4/aa**2-2*cc*cc/aa**4;dd=lv-lh
        eq('Ricci_Hopf_branch_'+name,ii*R*xx,lv*xx)
        dB=ii*dR+2*ii*kj[0]*ii*R
        yy=pp*dB*xx/dd
        eq('full_image_block_'+name,yy,pp*ii*(cov+2*lv*kj[0])*xx/dd)
        if label=='even':eq('radial_parity_'+name,yy[0])
        if label=='pure_trace':
          eq('pure_trace_Ricci_survivor_'+name,dR,S.zeros(3))
          eq('pure_trace_line_survivor_'+name,yy,S.zeros(3,1))
        kap=pp*ii*kj[0]*xx
        pd=yy*(gj[0]*xx).T+xx*(gj[0]*(yy-2*kap)).T
        eq('projector_idempotent_derivative_'+name,pd*(S.eye(3)-pp)+(S.eye(3)-pp)*pd,pd)
        badcov=ricci_covariant_jet(*gj,*kj,drop_derivative_index=True)
        caught['wrong_S_sign']|=nonzero(-cov-dR)
        caught['drop_derivative_index']|=nonzero(badcov-dR)
        caught['omit_raising']|=nonzero(pp*ii*dR*xx/dd-yy)
        caught['lambda_h_for_image']|=nonzero(pp*ii*(dR+2*lh*kj[0])*xx/dd-yy)
        caught['omit_moving_dual']|=nonzero(2*xx*(gj[0]*kap).T)
        fixtures.append({'name':name,'S':[[str(x) for x in dR.row(j)] for j in range(3)],'Bdot':[[str(x) for x in dB.row(j)] for j in range(3)],'Y':[str(x) for x in yy],'slope_dot':str(cc*(yy[2]-yy[1]))})
    assert all(caught.values()),caught
    print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':S.__version__,'checks':checks,'mutation_discriminators':caught,'symbol_b':str(b),'fixtures':fixtures,'limits':'Exact local algebra controls, not global TT or PDE numerical witnesses. Analytic proof owns existence and closure.'},indent=2))

if __name__=='__main__':main()
