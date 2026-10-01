"""Exposed exact Fraction recomputation of saved observables, not a ray solve."""
import ast
import hashlib
import json
import platform
from fractions import Fraction as F
from pathlib import Path

N=5
def scalar(x): return [F(x)]+[F(0)]*(N-1)
def add(a,b): return [x+y for x,y in zip(a,b)]
def neg(a): return [-x for x in a]
def mul(a,b): return [sum(a[j]*b[i-j] for j in range(i+1)) for i in range(N)]
def parse_node(n):
    if isinstance(n,ast.Constant) and isinstance(n.value,int):return scalar(n.value)
    if isinstance(n,ast.Name) and n.id=='L':return [F(0),F(1),F(0),F(0),F(0)]
    if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return neg(parse_node(n.operand))
    if isinstance(n,ast.BinOp):
        a,b=parse_node(n.left),parse_node(n.right)
        if isinstance(n.op,ast.Add):return add(a,b)
        if isinstance(n.op,ast.Sub):return add(a,neg(b))
        if isinstance(n.op,ast.Mult):return mul(a,b)
        if isinstance(n.op,ast.Div):
            assert b[0] and not any(b[1:]);return [x/b[0] for x in a]
        if isinstance(n.op,ast.Pow):
            assert not any(b[1:]) and b[0].denominator==1 and 0<=b[0]<N
            out=scalar(1)
            for _ in range(int(b[0])):out=mul(out,a)
            return out
    raise ValueError(ast.dump(n))
def parse(s):return parse_node(ast.parse(s,mode='eval').body)

p=Path('udt_echo_consistency_2026-10-01/fidelity/exact_repaired.stdout')
data=p.read_bytes();saved=json.loads(data);assert saved['status']=='PASS'
count=0;result=[]
for row in saved['kasner_endpoint_reconstruction']:
    first,ret=parse(row['p']),parse(row['q'])
    residual=add(mul(add(scalar(2),neg(mul(first,first))),ret),neg(first))
    prior=parse(row['q_minus_discriminator'])
    assert residual==prior;count+=5
    assert residual[0:3]==[0,0,0];count+=3
    result.append({'r':row['axis_r'],'polynomial_residual':[str(x) for x in residual]})
for row in saved['rational_controls']:
    c,first,ret,echo=[F(row[k]) for k in ['C','p','q','pq']]
    assert first+1/ret==2*c;count+=1
    assert (2-first*first)*ret==first;count+=1
    assert first*ret==echo;count+=1
print(json.dumps({'status':'PASS','exact_coefficient_assertions':count,
 'saved_source':str(p),'saved_sha256':hashlib.sha256(data).hexdigest(),
 'python':platform.python_version(),'polynomial_residuals':result,
 'scope':'Independent Fraction polynomial composition on exposed saved p/q; no independent worldline or curvature proof, no finite-L certificate.'},indent=2))
