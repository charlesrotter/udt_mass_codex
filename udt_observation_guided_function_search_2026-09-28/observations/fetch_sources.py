"""Fetch fixed public method/schema sources; never overwrite evidence."""
from pathlib import Path
import datetime
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parent
SOURCES = {
    'desi_release.html': 'https://data.desi.lbl.gov/doc/releases/',
    'desi_dr2_products.html': 'https://data.desi.lbl.gov/public/papers/y3/bao-cosmo-params/README.html',
    'desi_dr2_methods.html': 'https://arxiv.org/html/2503.14738v3',
    'desi_bao_files.json': 'https://api.github.com/repos/CobayaSampler/bao_data/contents/desi_bao_dr2',
    'quasar_duration_methods.html': 'https://arxiv.org/html/2501.04171v2',
    'quasar_volatility_methods.html': 'https://arxiv.org/html/2606.01496v1',
    'quasar_code_files.json': 'https://api.github.com/repos/eggplantbren/QuasarTimeDilation2/contents/',
}

def main():
    dest = ROOT / 'sources'
    dest.mkdir(exist_ok=True)
    records = []
    for name, url in SOURCES.items():
        p = dest / name
        if p.exists():
            raise RuntimeError(f'Refuse overwrite: {p}')
        record = {'url': url, 'path': str(p.relative_to(ROOT)),
                  'requested_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'UDT-research-source-audit/1.0'})
            with urllib.request.urlopen(req, timeout=45) as response:
                body = response.read(5 * 1024 * 1024 + 1)
                if len(body) > 5 * 1024 * 1024:
                    raise ValueError('Source exceeds 5 MiB per-file cap')
                record.update(status=response.status, final_url=response.url,
                              content_type=response.headers.get('Content-Type'))
            with p.open('xb') as stream:
                stream.write(body)
            record.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
        except Exception as exc:
            record['error'] = f'{type(exc).__name__}: {exc}'
        records.append(record)
        print(json.dumps(record), flush=True)
    with (ROOT / 'SOURCE_DOWNLOAD.json').open('x') as stream:
        json.dump(records, stream, indent=2)
        stream.write('\n')
    return 0 if all('sha256' in r for r in records) else 1

if __name__ == '__main__':
    raise SystemExit(main())
