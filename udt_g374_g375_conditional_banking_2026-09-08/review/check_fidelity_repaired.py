"""Keep original fidelity code; restrict only Git pack window mappings."""
import hashlib
from pathlib import Path

source = Path(__file__).with_name('check_fidelity.py')
payload = source.read_bytes()
assert hashlib.sha256(payload).hexdigest() == '3d90f545baeb606f5027947d6b360e5ff19d2da7c5b6c4ead6f8833b5b5b0d80'
before = "return subprocess.check_output(['git', *args], cwd=ROOT, timeout=10)"
after = "return subprocess.check_output(['git', '-c', 'core.packedGitWindowSize=16m', '-c', 'core.packedGitLimit=64m', *args], cwd=ROOT, timeout=10)"
text = payload.decode()
assert text.count(before) == 1
exec(compile(text.replace(before, after), str(source) + ' [bounded Git mapping]', 'exec'),
     {'__name__': '__main__', '__file__': str(source)})
