import json
import sympy as S
lam=S.Symbol("lambda",real=True)
expression="1+lambda^2"
try:
    S.sympify(expression.replace("^","**"),locals={"lambda":lam})
except S.SympifyError as error:
    original_error=str(error)
else:
    raise AssertionError("expected original reserved-keyword parse failure")
corrected=S.sympify(expression.replace("^","**").replace("lambda","ell"),locals={"ell":lam})
assert corrected==1+lam**2 and corrected.free_symbols=={lam}
print(json.dumps({"status":"PASS","sympy":S.__version__,"original_error":original_error,
"corrected_expression":str(corrected),"same_original_coordinate":True},indent=2))
