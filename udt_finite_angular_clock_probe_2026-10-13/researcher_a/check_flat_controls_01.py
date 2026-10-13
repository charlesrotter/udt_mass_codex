"""Regression of unchanged author series machinery in two genuinely flat metrics."""
import hashlib
import importlib.util
import json
from pathlib import Path
import time
import sympy as s


def main():
    started=time.monotonic()
    source=Path(__file__).with_name('formal_kasner_01.py')
    spec=importlib.util.spec_from_file_location('author_series',source)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    result={'kind':'shared-code regression, not independent derivation',
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'check_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'cases':{}}
    for name,exponents in [('Cartesian',[s.S.Zero,s.S.Zero]),('flat_Milne_product',[s.S.One,s.S.Zero])]:
        case={}
        for branch in ['forward','reverse']:
            case[branch]=module.solve_branch(exponents,branch)
            assert all(s.sympify(value)==0 for value in case[branch]['log_ratio']),case[branch]
        result['cases'][name]=case
    result['duration_seconds']=time.monotonic()-started
    target=Path(__file__).with_name('flat_controls_01_result.json')
    with target.open('x') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
