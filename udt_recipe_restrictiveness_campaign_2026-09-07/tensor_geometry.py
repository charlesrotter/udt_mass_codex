"""Exact coordinate tensor methods only; no physical equations or recipes selected."""
import itertools
import sympy as s

def geometry(g, coords):
    n=len(coords); gi=g.inv(); ix=range(n)
    G=[[[s.simplify(sum(gi[a,h]*(s.diff(g[h,c],coords[b])+s.diff(g[h,b],coords[c])-s.diff(g[b,c],coords[h])) for h in ix)/2) for c in ix] for b in ix] for a in ix]
    R={}
    for a,b,c,d in itertools.product(ix,repeat=4):
        R[a,b,c,d]=s.expand(sum(g[d,e]*(s.diff(G[e][b][c],coords[a])-s.diff(G[e][a][c],coords[b])+sum(G[e][a][m]*G[m][b][c]-G[e][b][m]*G[m][a][c] for m in ix)) for e in ix))
    Ric=s.Matrix(n,n,lambda b,c:s.simplify(sum(gi[a,d]*R[a,b,c,d] for a,d in itertools.product(ix,repeat=2))))
    return gi,G,R,Ric

def quadratic(g, W):
    """Full Weyl/FIRST-dual contraction in explicitly supplied slot convention."""
    gi=g.inv(); ix=range(4); nz=[(a,b,gi[a,b]) for a in ix for b in ix if gi[a,b]!=0]
    dual={}
    volume=s.sqrt(-g.det())
    for a,e,c,h in itertools.product(ix,repeat=4):
        dual[a,e,c,h]=s.expand(volume*sum(s.LeviCivita(a,e,r,t)*vr*vt*W[m,n,c,h] for r,m,vr in nz for t,n,vt in nz)/2)
    B={}
    for a,b,c,d in itertools.product(ix,repeat=4):
        B[a,b,c,d]=s.expand(sum(ve*vh*(W[a,e,c,h]*W[b,f,d,i]+dual[a,e,c,h]*dual[b,f,d,i]) for e,f,ve in nz for h,i,vh in nz))
    return B,dual
