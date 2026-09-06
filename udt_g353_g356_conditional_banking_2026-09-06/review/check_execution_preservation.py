"""Independent metadata check supporting the compact execution record."""
import hashlib
import json
import pathlib
import subprocess

root = pathlib.Path('/home/udt-admin/udt_mass_codex')
bank = root / 'udt_g353_g356_conditional_banking_2026-09-06'
data = json.loads((bank / 'INITIAL_CHECK_RECORDS.json').read_text())
original = set(data['original_status']['output'].splitlines())
command = ['git', '-c', 'core.preloadIndex=false', '-c', 'index.threads=1',
           'status', '--porcelain=v1', '--untracked-files=normal']
result = subprocess.run(command, cwd=root, capture_output=True, text=True, check=True)
current = set(result.stdout.splitlines())
assert len(original) == 46
assert original <= current, ('original status entries missing', original-current)
allowed = {line.split(maxsplit=1)[1] for line in
           (bank / 'INTEGRATION_CANDIDATE_SHA256SUMS').read_text().splitlines()}
allowed.add('udt_g353_g356_conditional_banking_2026-09-06/')
extra = current - original
assert all(line[3:] in allowed for line in extra), ('unexpected status', extra)
campaign = root / 'udt_g351_g352_content_bridge_campaign_2026-09-06'
paths = {line.split(maxsplit=1)[1] for step in range(1, 5)
         for line in (campaign / f'step_{step:02d}/SOURCE_SHA256SUMS').read_text().splitlines()}
assert len(paths) == 32
record = (bank / 'EXECUTION_RECORD.md').read_bytes()
assert hashlib.sha256(record).hexdigest() == 'c3b8a59f7813f26f3b18de1fb30225c7a83b1bc17e6e250fc10c63efc0e56cff'
print(json.dumps(dict(kind='metadata_and_record_pin_only', git_command=command,
                     git_returncode=result.returncode, original_status_count=46,
                     original_status_preserved=True, allowed_task_status_count=len(extra),
                     unique_campaign_source_paths=32,
                     execution_record_sha256=hashlib.sha256(record).hexdigest(),
                     parent_clean_full_audit='PENDING_NOT_REVIEWER_EXECUTED'), indent=2))
