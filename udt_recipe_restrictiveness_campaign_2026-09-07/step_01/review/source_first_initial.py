"""Independent metric first variation; no author scientific imports."""
import itertools
import json
import platform
import sympy as s

u,v,x,y,k=s.symbols('u v x y k', real=True)
coords=(u,v,x,y)
H=x**3-3*x*y**2
g=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
h=s.zeros(4); h[0,3]=h[3,0]=x*x; h[0,0]=k*v*y
inv=g.inv(); dinv=-inv*h*inv
I=range(4)
simp=s.simplify
G={}; dG={}
for a,b,c in itertools.product(I,repeat=3):
    t=[s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d]) for d in I]
    dt=[s.diff(h[d,c],coords[b])+s.diff(h[d,b],coords[c])-s.diff(h[b,c],coords[d]) for d in I]
    G[a,b,c]=simp(sum(inv[a,d]*t[d] for d in I)/2)
    dG[a,b,c]=simp(sum(dinv[a,d]*t[d]+inv[a,d]*dt[d] for d in I)/2)
R={}; dR={}
# R[a,b,c,d] = component a of R(partial_c,partial_d) partial_b.
for a,b,c,d in itertools.product(I,repeat=4):
    R[a,b,c,d]=simp(s.diff(G[a,d,b],coords[c])-s.diff(G[a,c,b],coords[d])+sum(G[a,c,e]*G[e,d,b]-G[a,d,e]*G[e,c,b] for e in I))
    dR[a,b,c,d]=simp(s.diff(dG[a,d,b],coords[c])-s.diff(dG[a,c,b],coords[d])+sum(dG[a,c,e]*G[e,d,b]+G[a,c,e]*dG[e,d,b]-dG[a,d,e]*G[e,c,b]-G[a,d,e]*dG[e,c,b] for e in I))
ric=s.Matrix(4,4,lambda a,b: simp(sum(R[c,a,c,b] for c in I)))
dric=s.Matrix(4,4,lambda a,b: simp(sum(dR[c,a,c,b] for c in I)))
assert ric==s.zeros(4)
sol=s.solve(list(dric),k,dict=True)
assert len(sol)==1
ks=sol[0][k]
assert dric.subs(k,ks)==s.zeros(4)

# Full seed linearization for L=partial_v. Nullness forces z^u=0.
# Because h_vv=0, the linearized seed has z=zv partial_v+zx partial_x+zy partial_y.
zv,zx,zy=s.symbols('zv zx zy',real=True)
z=s.Matrix([0,zv,zx,zy]); L=s.Matrix([0,1,0,0])
Tang=s.Matrix([[1,0,0],[-2,0,0],[0,1,0],[0,0,1]])
seed_algebra=s.Matrix(4,3,lambda a,i:simp(sum(Tang[b,i]*(sum(G[a,b,c]*z[c] for c in I)+dG[a,b,1].subs(k,ks)) for b in I)))

# Covariant curvature Q[a,b,c,d] = g(R(a,b)c,d).
Q={}; dQ={}
for a,b,c,d in itertools.product(I,repeat=4):
    Q[a,b,c,d]=simp(sum(g[d,e]*R[e,c,a,b] for e in I))
    dQ[a,b,c,d]=simp(sum(h[d,e]*R[e,c,a,b]+g[d,e]*dR[e,c,a,b] for e in I)).subs(k,ks)

# Pointwise kernel variation checks all ambient curvature endomorphism slots.
point={u:0,v:0,x:1,y:0}
kernel_eq=[simp(dR[a,1,b,c].subs(k,ks)+sum(R[a,d,b,c]*z[d] for d in I)) for a,b,c in itertools.product(I,repeat=3)]
kernel_sol=s.solve(kernel_eq,(zv,zx,zy),dict=True)
kernel_point=s.solve([q.subs(point) for q in kernel_eq],(zv,zx,zy),dict=True)

# Full B first variation including metric inverse and Hodge dual variation.
# det(g_epsilon)=-1 identically for this ansatz, so lower volume is fixed.
eps=lambda a,b,c,d:s.LeviCivita(a,b,c,d)
star={}; dstar={}
for a,e,c,h0 in itertools.product(I,repeat=4):
    star[a,e,c,h0]=simp(sum(s.Rational(1,2)*eps(a,e,m,n)*inv[m,p]*inv[n,q]*Q[p,q,c,h0] for m,n,p,q in itertools.product(I,repeat=4) if eps(a,e,m,n)))
    dstar[a,e,c,h0]=simp(sum(s.Rational(1,2)*eps(a,e,m,n)*((dinv[m,p]*inv[n,q]+inv[m,p]*dinv[n,q])*Q[p,q,c,h0]+inv[m,p]*inv[n,q]*dQ[p,q,c,h0]) for m,n,p,q in itertools.product(I,repeat=4) if eps(a,e,m,n))).subs(k,ks)
B={}; dB={}
for a,b,c,d in itertools.product(I,repeat=4):
    base=0; variation=0
    for e,f,hh,ii in itertools.product(I,repeat=4):
        contractions=Q[a,e,c,hh]*Q[b,f,d,ii]+star[a,e,c,hh]*star[b,f,d,ii]
        base += inv[e,f]*inv[hh,ii]*contractions
        variation += (dinv[e,f]*inv[hh,ii]+inv[e,f]*dinv[hh,ii])*contractions
        variation += inv[e,f]*inv[hh,ii]*(dQ[a,e,c,hh]*Q[b,f,d,ii]+Q[a,e,c,hh]*dQ[b,f,d,ii]+dstar[a,e,c,hh]*star[b,f,d,ii]+star[a,e,c,hh]*dstar[b,f,d,ii])
    B[a,b,c,d]=simp(base)
    dB[a,b,c,d]=simp(variation).subs(k,ks)
N=36*(x*x+y*y)
assert all(simp(val-(N if ix==(0,0,0,0) else 0))==0 for ix,val in B.items())
# Tangency to a fourth power at beta=-N^(1/4)du admits only >=3 u slots.
badroot={str(ix):val for ix,val in dB.items() if ix.count(0)<3 and val!=0}
normalroot={str(ix):val for ix,val in dB.items() if val!=0}
# Relative first root variation beta1/beta0 per component, from one mixed slot.
root_ratios=[simp(dB[0,0,0,a]/N/(4 if a==0 else 1)) for a in I]

print(json.dumps(dict(python=platform.python_version(),sympy=s.__version__,convention='R[a,b,c,d]=component a of R(c,d)b',
 h=h.tolist(),Ric0=ric.tolist(),Ric1=dric.tolist(),required_k=ks,
 seed_connection_terms=seed_algebra.tolist(),kernel_solution=kernel_sol,kernel_point_solution=kernel_point,
 B0_nonzero={str(ix):val for ix,val in B.items() if val!=0},B1_nonzero=normalroot,
 root_tangent_forbidden_components=badroot,relative_root_variation=root_ratios),indent=2,default=str))
