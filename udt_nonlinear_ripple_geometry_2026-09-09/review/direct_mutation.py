"""Execute an exact source mutation in memory; author files remain unchanged."""
from pathlib import Path
import sys
package=Path(__file__).resolve().parent.parent
mode=sys.argv[1]
if mode=='initial_K':
    path=package/'check_original_metric.py'
    old='s.diff(a,t):-s.Rational(1,4)+9*q**2/16'
    new='s.diff(a,t):-s.Rational(1,4)'
elif mode=='spatial_response':
    path=package/'check_profile.py'
    old='lam=e*e*(L+t*f*df*s.cos(2*k*x)/2)'
    new='lam=e*e*L'
else:
    raise ValueError(mode)
source=path.read_text()
assert source.count(old)==1
print('MUTATION '+mode+': '+old+' -> '+new,flush=True)
exec(compile(source.replace(old,new),str(path)+'['+mode+']','exec'),{'__file__':str(path)})
