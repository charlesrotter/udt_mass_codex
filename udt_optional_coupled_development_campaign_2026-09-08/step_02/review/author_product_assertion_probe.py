"""Expose a vacuous author diagnostic without mutating the frozen checker."""
import ast
from fractions import Fraction as F
import hashlib
import json
import pathlib
import platform
import sympy as S

path = pathlib.Path('udt_optional_coupled_development_campaign_2026-09-08/step_02/check_joint_reduction.py')
raw = path.read_bytes()
assert hashlib.sha256(raw).hexdigest() == 'b6866f1d624f1dcbdc7efac99699565317b78ce339d4909e7b2d3b4aacd71045'
matches = [n for n in ast.walk(ast.parse(raw)) if isinstance(n, ast.Call)
           and isinstance(n.func, ast.Name) and n.func.id == 'check'
           and ast.unparse(n.args[0]).startswith("'initial_independent_density_product_'")]
assert len(matches) == 1
expression = ast.Expression(matches[0].args[1])
code = compile(expression, str(path), 'eval')
rho,a,E = S.symbols('rho a E')
generic = S.simplify(eval(code, {'__builtins__': {}}, dict(rho=rho,a=a,E=E)))
assert generic == 0
env = dict(rho=F(9,4),a=F(2,3),E=F(5,3))
reported_guard = eval(code, {'__builtins__': {}}, env)
declared_s0 = F(2)
actual_residual = env['rho']*env['a']**2*env['E']-declared_s0*env['E']
assert reported_guard == 0
try:
    assert actual_residual == 0
except AssertionError:
    status = 'ACTUAL_FIXED_PRODUCT_GUARD_RED'
else:
    raise AssertionError('nonmatching supplied product unexpectedly accepted')
print(json.dumps({'python':platform.python_version(),'sympy':S.__version__,
                  'extracted_expression':ast.unparse(expression.body),
                  'generic_author_residual':str(generic),
                  'mutated_declared_s0':str(declared_s0),
                  'author_guard_still_passes':reported_guard==0,
                  'actual_fixed_product_residual':str(actual_residual),'status':status,
                  'ceiling':'three author groups are vacuous; CD1/proof product result is not refuted'},
                 indent=2,sort_keys=True))
