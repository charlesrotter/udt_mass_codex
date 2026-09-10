"""Construction check: exact smooth 4D witnesses, no metric field equation.
Free real kappa and b; local positive-lapse domain. Standard R(X,Y) commutator.
SymPy exact arithmetic, one CPU process; no GPU/grid/tolerance. Output /tmp only.
Scope: check proposed witnesses, not independent proof/review or physical adoption.
"""
import sys,json,hashlib,pathlib
import sympy as s
root=pathlib.Path(__file__).parent
x=s.symbols('t x y z', real=True)
t,xx,y,z=x
kap,b=s.symbols('kappa b', real=True)
p={xx:0,y:0,z:0}
lines=[]
def say(label,value):
    line=f'{label}: {value}'
    print(line,flush=True);lines.append(line)
def simp(M):
    return M.applyfunc(s.simplify) if isinstance(M,s.MatrixBase) else s.simplify(M)
def inspect(label,g,U):
    inv=simp(g.inv()); uc=simp(g*U)
    Gamma=[[[s.simplify(sum(inv[a,d]*(s.diff(g[d,c],x[e])+s.diff(g[d,e],x[c])-s.diff(g[c,e],x[d])) for d in range(4))/2) for e in range(4)] for c in range(4)] for a in range(4)]
    B=s.Matrix(4,4,lambda a,c:s.simplify(s.diff(uc[c],x[a])-sum(Gamma[d][a][c]*uc[d] for d in range(4))))
    theta=s.simplify(s.trace(inv*B)); P=s.eye(4)+uc*U.T
    projected=simp(P*B*P.T); h=g+uc*uc.T
    shear=simp((projected+projected.T)/2-theta*h/3)
    twist=simp((projected-projected.T)/2)
    twist2=s.simplify(sum(inv[a,c]*inv[d,e]*twist[a,d]*twist[c,e] for a in range(4) for c in range(4) for d in range(4) for e in range(4)))
    accel=s.Matrix(4,1,lambda a,_:s.simplify(sum(U[c]*s.diff(U[a],x[c]) for c in range(4))+sum(Gamma[a][c][d]*U[c]*U[d] for c in range(4) for d in range(4))))
    diva=s.simplify(sum(s.diff(accel[a],x[a]) for a in range(4))+sum(Gamma[a][a][c]*accel[c] for a in range(4) for c in range(4)))
    ric00=s.simplify(sum(s.diff(Gamma[a][0][0],x[a])-s.diff(Gamma[a][a][0],t) for a in range(4))+sum(Gamma[a][a][d]*Gamma[d][0][0]-Gamma[a][0][d]*Gamma[d][a][0] for a in range(4) for d in range(4)))
    ricuu=s.simplify(ric00*U[0]**2)
    assert all(U[i]==0 for i in range(1,4))
    say(label+' metric determinant',s.factor(g.det()))
    say(label+' unit norm',simp((U.T*g*U)[0]))
    say(label+' symmetric gradient',simp((B+B.T)/2))
    say(label+' theta',theta);say(label+' shear',shear)
    say(label+' acceleration',accel);say(label+' divergence acceleration',diva)
    say(label+' twist squared',twist2)
    say(label+' Ric_UU direct coordinate curvature',ricuu)
    say(label+' Ric_UU at p',s.simplify(ricuu.subs(p)))
    say(label+' div a at p',s.simplify(diva.subs(p)))
    say(label+' twist squared at p',s.simplify(twist2.subs(p)))
    say(label+' accel at p',simp(accel.subs(p)))
    nx,ny,nz=s.symbols('n_x n_y n_z',real=True)
    k=s.Matrix([1,nx,ny,nz]); q=s.simplify(-(k.T*B.subs(p)*k)[0])
    say(label+' all-direction q at p',q)
    assert simp((U.T*g*U)[0])==-1
    assert theta==0 and shear==s.zeros(4)
    assert q==0
    assert s.simplify(ricuu-twist2-diva)==0
    return {'Ric_UU':str(ricuu),'Ric_UU_p':str(s.simplify(ricuu.subs(p))), 'div_a':str(diva),'twist2':str(twist2),'q_p':str(q)}
say('python',sys.version);say('sympy',s.__version__)
N=1+kap*(xx**2+y**2+z**2)/2
out={}
out['static_lapse']=inspect('static_lapse',s.diag(-N*N,1,1,1),s.Matrix([1/N,0,0,0]))
co=s.eye(4);co[0,1]=-b*y/2;co[0,2]=b*xx/2
g=co.T*s.diag(-1,1,1,1)*co
out['unit_killing_twist']=inspect('unit_killing_twist',g,s.Matrix([1,0,0,0]))
(root/'CHECK_OUTPUT.txt').write_text('\n'.join(lines)+'\n')
(root/'CHECK_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
(root/'SHA256SUMS').write_text(''.join(hashlib.sha256((root/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in ['check_witnesses.py','CHECK_OUTPUT.txt','CHECK_RESULT.json']))
print('PASS construction coordinate witnesses (same-context exact check)')
