"""Sequential finite case-check queue with immutable captures, no time kill."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import check_survey as check

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest', default=str(check.BASE/'production_runtime/campaign.json'))
    ap.add_argument('--analysis', default=str(check.BASE/'production_analysis'))
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()
    if args.limit < 0:
        raise ValueError('NEGATIVE_LIMIT')
    manifest = check.manifest(args.manifest)
    rows = manifest['cases'][:args.limit] if args.limit else manifest['cases']
    for row in rows:
        name = row['id']
        output = check.HERE/'cases'/f'{name}.json'
        capture = check.HERE/'captures'/name
        if output.exists():
            result = check.read(output)
            receipt = check.read(capture.with_suffix('.json'))
            for stream in ['stdout', 'stderr']:
                if check.sha(capture.with_suffix('.'+stream)) != receipt[stream+'_sha256']:
                    raise ValueError('PRIOR_CAPTURE_CHANGED')
            if (result['status'] != 'PASS' or result['case'] != name
                    or result['method_sources'] != check.method_sources()
                    or result['manifest_sha256'] != manifest['_manifest_sha256']
                    or receipt['returncode'] != 0):
                raise ValueError('PRIOR_CHECK_REQUIRES_REVIEW')
            print(json.dumps(dict(case=name, action='REUSE_BOUND_PASS')), flush=True)
            continue
        command = [sys.executable, str(check.BASE/'capture.py'), str(capture),
                   sys.executable, str(check.HERE/'check_survey.py'), 'case',
                   '--manifest', args.manifest, '--analysis', args.analysis,
                   '--case', name, '--output', str(output)]
        code = subprocess.call(command)
        if code:
            return code
    print(json.dumps(dict(status='SELECTED_CASE_CHECKS_COMPLETE', count=len(rows))), flush=True)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
