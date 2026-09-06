"""Portable independent rational reconstruction in original Brinkmann coordinates."""
import argparse, ast, json, math
from fractions import Fraction as F
from pathlib import Path

ap=argparse.ArgumentParser(); ap.add_argument("--repo",type=Path,required=True)
args=ap.parse_args()
package=args.repo/"udt_g351_g352_content_bridge_campaign_2026-09-06/step_01"
inputs=json.loads((package/"WITNESS_INPUTS.json").read_text())
saved=json.loads((package/"AUTHOR_RESULT.json").read_text())

def poly(node):
    if isinstance(node,ast.Constant) and isinstance(node.value,int): return {0:F(node.value)}
    if isinstance(node,ast.Name) and node.id=="x": return {1:F(1)}
    if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Add):
        a,b=poly(node.left),poly(node.right)
        return {k:a.get(k,F(0))+b.get(k,F(0)) for k in a.keys()|b.keys()}
    if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Pow):
        assert isinstance(node.left,ast.Name) and node.left.id=="x"
        assert isinstance(node.right,ast.Constant) and isinstance(node.right.value,int)
        assert node.right.value>=0
        return {node.right.value:F(1)}
    raise ValueError("outside this independently supported polynomial witness grammar")

def dot(a,g,b): return sum(a[i]*g[i][j]*b[j] for i in range(4) for j in range(4))
def determinant(matrix):
    m=[row[:] for row in matrix]; result=F(1)
    for i in range(len(m)):
        j=next(j for j in range(i,len(m)) if m[j][i])
        if i!=j: m[i],m[j]=m[j],m[i]; result=-result
        pivot=m[i][i]; result*=pivot
        for j in range(i+1,len(m)):
            factor=m[j][i]/pivot
            m[j]=[v-factor*w for v,w in zip(m[j],m[i])]
    return result
def root(q):
    n,d=math.isqrt(q.numerator),math.isqrt(q.denominator)
    assert n*n==q.numerator and d*d==q.denominator
    return F(n,d)

A,L,delta=map(F,[inputs["metric_branch_A"],inputs["screen_length_L"],inputs["phase_spacing"]])
b=root(2*abs(A)); lam,nu=map(F,inputs["label_point"])
x,y=L*lam,L*nu
H=A*(x*x-y*y)
# Unlike the author implementation, use (u,v,x,y), g_uv=-1,
# beta=-b du and C0=b partial_v. No candidate implementation is imported.
g=[[H,F(-1),F(0),F(0)],[F(-1),F(0),F(0),F(0)],
   [F(0),F(0),F(1),F(0)],[F(0),F(0),F(0),F(1)]]
assert determinant(g)==-1
C0=[F(0),b,F(0),F(0)]
assert dot(C0,g,C0)==0
qx,qy=map(F,inputs["cut_graph_gradient"])
E=[[F(0),b*qx,L,F(0)],[F(0),b*qy,F(0),L]]
gram=[[dot(e,g,z) for z in E] for e in E]
J=root(gram[0][0]*gram[1][1]-gram[0][1]*gram[1][0])
assert gram==[[L*L,F(0)],[F(0),L*L]]
assert J==F(saved["cut_area"])

rows=[]
for expression,author in zip(inputs["weights"],saved["weights"]):
    coeff=poly(ast.parse(expression.replace("lambda","x").replace("^","**"),mode="eval").body)
    assert all(c>=0 for c in coeff.values())
    # Stage A's independent integral of affine weights is extended here to
    # polynomial monomials: integral_0^1 x^n dx = 1/(n+1).
    integral=sum(c/F(n+1) for n,c in coeff.items())
    f=sum(c*lam**n for n,c in coeff.items())
    total=delta*L*L*integral
    assert total==F(author["amount"])
    rates=[]
    for wtext in inputs["observer_frequencies"]:
        w=F(wtext); Uu=w/b
        observer=[Uu,(1+H*Uu*Uu)/(2*Uu),F(0),F(0)]
        assert dot(observer,g,observer)==-1 and Uu>0
        assert -dot(observer,g,C0)==w
        Cf=[f*c for c in C0]
        rate=-dot(observer,g,Cf)
        assert rate==w*(delta*L*L*f)/(delta*J)
        gauge=F(inputs["phase_gauge_factor"])
        assert gauge*w*(delta*L*L*f)/(gauge*delta*J)==rate
        rates.append(rate)
    assert rates==list(map(F,author["rates_at_label_point"]))
    if integral:
        assert rates[0]>0
        ratio=rates[1]/rates[0]
        assert ratio==F(author["transfer_ratio"])
        assert not author["zero_ratio_not_formed"]
    else:
        ratio=None
        assert rates==[0,0] and author["transfer_ratio"] is None and author["zero_ratio_not_formed"]
    rows.append({"input_weight":expression,"total":str(total),"rate_values":list(map(str,rates)),
                 "ratio":None if ratio is None else str(ratio)})
assert len(rows)==len(saved["weights"])==4
assert rows[0]["total"]!=rows[1]["total"]
print(json.dumps({"status":"PASS","implementation":"stdlib Fraction, original Brinkmann coordinates",
"evidence":"saved finite witnesses independently recomputed; analytic source boundary not automated",
"original_metric_determinant":str(determinant(g)),"full_cut_gram":[list(map(str,row)) for row in gram],
"J":str(J),"rows":rows},indent=2))
