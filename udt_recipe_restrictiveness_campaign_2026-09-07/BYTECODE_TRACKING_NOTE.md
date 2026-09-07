# Generated-bytecode tracking correction

The f5d95618 inventory-based staging inadvertently included generated
__pycache__/tensor_geometry.cpython-310.pyc, outside every scientific manifest.
It is not scientific evidence or a dependency. The exact bytecode path was
removed from Git tracking only; local bytes and prior commit history remain.
Subsequent staging excludes __pycache__ and uses inspected artifact inventories.
No scientific source, candidate/review hash, ignore rule or protected file changes.
The earlier PACKAGING_DIAGNOSTIC.md is sealed by the RC1 review and is unchanged;
an attempted append was immediately withdrawn before any commit/downstream use.
