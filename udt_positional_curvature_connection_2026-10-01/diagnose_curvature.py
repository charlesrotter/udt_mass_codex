import runpy,json
import sympy as s
try:
 runpy.run_path('udt_positional_curvature_connection_2026-10-01/check_curvature.py',run_name='__main__')
except AssertionError as error:
 tb=error.__traceback__
 while tb.tb_next:tb=tb.tb_next
 v=tb.tb_frame.f_locals;z=v['z']
 print(json.dumps({'failure':str(error),'original_component':str(z),'expanded_trig_simplification':str(s.trigsimp(s.expand_trig(z))),'reason':'Determine whether asserted off-pattern curvature is nonzero or an unsimplified identity.'},indent=2))
