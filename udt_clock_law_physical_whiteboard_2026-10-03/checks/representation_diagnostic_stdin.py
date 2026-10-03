from pathlib import Path
src=Path('udt_clock_law_physical_whiteboard_2026-10-03/check_conformal_bookkeeping.py').read_text()
exec(src.split('assert wrong==')[0])
diff=(wrong+O*go*kb).applyfunc(s.expand)
assert diff==s.zeros(4,1)
control=wrong.subs(dict(zip(grad,[1,0,0,0]))).subs(O,1)
assert control==s.Matrix([-25,-15,-20,0])
print({'computed':str(wrong),'expected':str(-O*go*kb),'expanded_difference':str(diff),'nonzero_countercontrol':str(control)})
