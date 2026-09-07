"""Direct Christoffel/Riemann check of the local exact two-function wave family."""
from fractions import Fraction as Q
import json
import platform

# Supplied algebraic metric jet, not physical calibration or selected wave.
# Coordinates (u,v,x,y); A,A',A'',B,B',B'' all varied independently.
records = []
for aval,bval in [(Q(3),Q(-2)), (Q(0),Q(5)), (Q(-7,3),Q(0))]:
    ap, app, bp, bpp = Q(5),Q(7),Q(11),Q(13)
    x,y = Q(2,3),Q(-4,5)
    shape = x*x-y*y
    h = aval*shape+2*bval*x*y
    dh = [ap*shape+2*bp*x*y, Q(0), 2*aval*x+2*bval*y, -2*aval*y+2*bval*x]
    ddh = [[Q(0) for _ in range(4)] for _ in range(4)]
    ddh[0][0] = app*shape+2*bpp*x*y
    ddh[0][2] = ddh[2][0] = 2*ap*x+2*bp*y
    ddh[0][3] = ddh[3][0] = -2*ap*y+2*bp*x
    ddh[2][2], ddh[3][3] = 2*aval,-2*aval
    ddh[2][3] = ddh[3][2] = 2*bval
    g = [[h,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]]
    inv = [[0,-1,0,0],[-1,-h,0,0],[0,0,1,0],[0,0,0,1]]
    assert all(sum(g[i][k]*inv[k][j] for k in range(4)) == int(i==j)
               for i in range(4) for j in range(4))

    def dg(a,b,c):
        return dh[c] if a==b==0 else Q(0)

    def ddg(a,b,c,d):
        return ddh[c][d] if a==b==0 else Q(0)

    def dinv(a,b,c):
        return -sum(inv[a][i]*dg(i,j,c)*inv[j][b] for i in range(4) for j in range(4))

    gamma = [[[sum(inv[a][e]*(dg(e,b,c)+dg(e,c,b)-dg(b,c,e))/2
                    for e in range(4)) for c in range(4)] for b in range(4)]
             for a in range(4)]

    def dgamma(a,b,c,d):
        return sum((dinv(a,e,d)*(dg(e,b,c)+dg(e,c,b)-dg(b,c,e))
                    +inv[a][e]*(ddg(e,b,c,d)+ddg(e,c,b,d)-ddg(b,c,e,d)))/2
                   for e in range(4))

    rup = [[[[dgamma(a,d,b,c)-dgamma(a,c,b,d)
              +sum(gamma[a][c][e]*gamma[e][d][b]-gamma[a][d][e]*gamma[e][c][b]
                   for e in range(4)) for d in range(4)] for c in range(4)]
            for b in range(4)] for a in range(4)]
    ric = [[sum(rup[a][b][a][d] for a in range(4)) for d in range(4)] for b in range(4)]
    assert all(v==0 for row in ric for v in row)
    lower = [[[[sum(g[a][e]*rup[e][b][c][d] for e in range(4)) for d in range(4)]
               for c in range(4)] for b in range(4)] for a in range(4)]
    assert lower[0][2][0][2] == -aval
    assert lower[0][3][0][3] == aval
    assert lower[0][2][0][3] == -bval
    assert lower[0][3][0][2] == -bval
    records.append({"A":str(aval),"B":str(bval),"Ricci_zero":True,
                    "R_uxux":str(lower[0][2][0][2]),
                    "R_uyuy":str(lower[0][3][0][3]),
                    "R_uxuy":str(lower[0][2][0][3])})
print(json.dumps({"python":platform.python_version(),"candidate_imports":False,
                  "evidence_kind":"three exact metric-jet Christoffel reconstructions",
                  "records":records},indent=2,sort_keys=True))
