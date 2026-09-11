"""Authenticated path-only replay of original RD1 arm check with preserved public inputs."""
from pathlib import Path
import hashlib
import sys
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
R=D.parents[1]
p=R/'udt_gw_response_robustness_design_campaign/step_01/review/independent_arm_integral.py'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='13879315286f1ed34f719068b25ec4032a132642ca4ac19f9edaa9e08987f814'
text=p.read_text()
old='ROOT=pathlib.Path("/tmp/udt-gw-response-docs-L3JgrF")'
assert text.count(old)==1
text=text.replace(old,'ROOT=pathlib.Path('+repr(str(D/'rd1_public_definitions'))+')',1)
exec(compile(text,str(p)+' [path-only in-memory adapter]','exec'),{'__name__':'__main__','__file__':str(p)})
