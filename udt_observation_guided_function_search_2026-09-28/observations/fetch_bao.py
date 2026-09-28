"""Pin and fetch the two small published BAO likelihood files; no analysis."""
from pathlib import Path
import datetime
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parent

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'UDT-research-source-audit/1.0'})
    with urllib.request.urlopen(req, timeout=45) as response:
        body = response.read(5 * 1024 * 1024 + 1)
    if len(body) > 5 * 1024 * 1024:
        raise ValueError('Source exceeds per-file cap')
    return body

def main():
    dest = ROOT / 'bao'
    dest.mkdir(exist_ok=True)
    commit_url = 'https://api.github.com/repos/CobayaSampler/bao_data/commits/master'
    commit_bytes = fetch(commit_url)
    commit = json.loads(commit_bytes)['sha']
    with (dest / 'UPSTREAM_COMMIT.json').open('xb') as stream:
        stream.write(commit_bytes)
    records = []
    for name in ['desi_gaussian_bao_ALL_GCcomb_mean.txt', 'desi_gaussian_bao_ALL_GCcomb_cov.txt']:
        url = f'https://raw.githubusercontent.com/CobayaSampler/bao_data/{commit}/desi_bao_dr2/{name}'
        body = fetch(url)
        with (dest / name).open('xb') as stream:
            stream.write(body)
        records.append({'url': url, 'file': name, 'bytes': len(body),
                        'sha256': hashlib.sha256(body).hexdigest()})
    record = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'commit': commit, 'commit_url': commit_url,
              'commit_response_sha256': hashlib.sha256(commit_bytes).hexdigest(),
              'files': records}
    with (dest / 'DOWNLOAD.json').open('x') as stream:
        json.dump(record, stream, indent=2)
        stream.write('\n')
    print(json.dumps(record, indent=2))

if __name__ == '__main__':
    main()
