#!/usr/bin/env python3
"""Download only the frozen public products; retain exact release bytes in gzip."""
from pathlib import Path
import datetime as dt
import gzip
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'raw'
COMMIT = 'c447f0fea703fcd0fff57de5000947b5ca81286b'
BASE = f'https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/{COMMIT}/Pantheon%2B_Data/'
FILES = [
    ('4_DISTANCES_AND_COVAR/README', 'README.txt', False),
    ('5_COSMOLOGY/cosmosis_likelihoods/Pantheon%2BSH0ES_cosmosis_likelihood.py', 'release_likelihood.py', False),
    ('4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat', 'Pantheon+SH0ES.dat', False),
    ('4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES_STAT%2BSYS.cov', 'Pantheon+SH0ES_STAT+SYS.cov.gz', True),
]


def main():
    RAW.mkdir(exist_ok=True)
    seal = ROOT / 'FREEZE_SEAL.json'
    freeze = ROOT / 'FREEZE.md'
    if seal.exists():
        raise RuntimeError('Refusing to replace existing freeze seal/download evidence')
    seal.write_text(json.dumps({
        'sealed_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'freeze_sha256': hashlib.sha256(freeze.read_bytes()).hexdigest(),
        'status': 'sealed before downloading observational rows',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }, indent=2)+'\n')
    records, total = [], 0
    for path, name, compress in FILES:
        target = RAW/name
        if target.exists():
            raise RuntimeError(f'Refusing to overwrite {target}')
        request = urllib.request.Request(BASE+path, headers={'User-Agent': 'UDT-bounded-observation-reconstruction'})
        with urllib.request.urlopen(request, timeout=90) as response:
            blob = response.read(512*1024*1024-total+1)
            total += len(blob)
            if total > 512*1024*1024:
                raise RuntimeError('Download allocation exceeded')
            if compress:
                with target.open('xb') as fd:
                    with gzip.GzipFile(filename='', fileobj=fd, mode='wb', mtime=0) as zf:
                        zf.write(blob)
            else:
                target.write_bytes(blob)
        records.append({'url': BASE+path, 'path': str(target.relative_to(ROOT)),
                        'source_bytes': len(blob), 'source_sha256': hashlib.sha256(blob).hexdigest(),
                        'saved_bytes': target.stat().st_size,
                        'saved_sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
        print(json.dumps(records[-1]), flush=True)
    sources = ['AGENTS.md', 'CURRENT_RESEARCH_PROGRAM.md', 'CURRENT_SCIENTIFIC_PREMISES.tsv',
        'udt_g277_observational_scale_anchor_ownership_2026-08-26/LAY_REPORT.md',
        'udt_g279_native_kernel_observational_interface_provenance_audit_2026-08-27/LAY_REPORT.md',
        'udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/LAY_REPORT.md',
        'udt_redshift_distance_readiness_2026-09-12/DECISION_BRIEF.md']
    manifest = {'completed_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                'release_commit': COMMIT, 'download_bytes': total, 'downloads': records,
                'local_source_sha256': {p:hashlib.sha256((ROOT.parent.parent/p).read_bytes()).hexdigest() for p in sources}}
    (ROOT/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')


if __name__ == '__main__':
    main()
