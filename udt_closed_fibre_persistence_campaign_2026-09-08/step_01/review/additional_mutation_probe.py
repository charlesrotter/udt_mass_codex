"""Post-exposure in-memory author mutation; never changes author source bytes.

The mutation wrongly accepts regularity when EITHER axis has trivial holonomy.
Original finite fixtures do not contain a one-exceptional-axis example.
Both runs retain their output, including an actual false pass if it occurs.
"""
import hashlib
from pathlib import Path
import sys

source_path = Path(__file__).resolve().parent.parent / 'check_cf1.py'
source = source_path.read_text()
assert hashlib.sha256(source_path.read_bytes()).hexdigest() == '3272d699a432c86f4137505a99e44af18588e942fcf310d375acde35ee7367c9'
probe = sys.argv[1]
assert probe in ['original_fixtures', 'one_exceptional_axis_fixtures']
old = 'else axis_orders(r)==(1,1)'
assert source.count(old) == 1
source = source.replace(old, 'else 1 in axis_orders(r)')
if probe == 'one_exceptional_axis_fixtures':
    old_fixtures = 'fixtures=[Fraction(1),Fraction(3,2),Fraction(2,3),Fraction(7,5),Fraction(5,7)]'
    assert source.count(old_fixtures) == 1
    source = source.replace(old_fixtures, old_fixtures + '+[Fraction(2),Fraction(1,2)]')
sys.argv = [str(source_path), 'baseline']
exec(compile(source, '<review-only in-memory either-axis regularity mutant>', 'exec'),
     {'__name__': '__main__', '__file__': str(source_path)})
