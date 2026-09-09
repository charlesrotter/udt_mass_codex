"""Execute one real source mutation without modifying any frozen source file."""
import pathlib
import sys

root=pathlib.Path(__file__).resolve().parents[1]
mutants={
    'omit_curl': ('check_geometry.py','dE-local-curlB','dE-local'),
    'omit_inverse': ('check_geometry.py','dRm = simp(dhi*Ric+hi*dRic)','dRm = simp(hi*dRic)'),
    'undefined_probe': ('check_matched_data.py','probe=S.Rational(1,6)','probe=S.Rational(2,3)'),
    'wrong_bianchi_curl': ('review/bianchi_components.py','edot+curl(db)-local(E)','edot-curl(db)-local(E)'),
}
name=sys.argv[1]
rel,old,new=mutants[name]
path=root/rel
text=path.read_text()
assert text.count(old)==1,('mutation_target_count',name)
print('Executing real mutation:',name,rel,repr(old),'->',repr(new),flush=True)
exec(compile(text.replace(old,new),str(path)+'::'+name,'exec'),{'__file__':str(path),'__name__':'__main__'})
