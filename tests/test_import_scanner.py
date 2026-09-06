from pathlib import Path
import sys

from guardrail_import_scanner import (
    EXEC_DEFERRED,
    EXEC_IMPORT,
    EXEC_SCRIPT,
    scan_file,
    walk_graph,
)


def write(root: Path, relative: str, source: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def triples(findings):
    return {(item.target, item.execution, item.resolution) for item in findings}


def test_main_guard_equality_and_else_are_mode_specific(tmp_path):
    path = write(
        tmp_path,
        "entry.py",
        'if __name__ == "__main__":\n    import script_dep\nelse:\n    import import_dep\n',
    )
    write(tmp_path, "script_dep.py", "VALUE = 1\n")
    write(tmp_path, "import_dep.py", "VALUE = 2\n")
    assert triples(scan_file(path, tmp_path, script=False)) == {
        ("import_dep", EXEC_IMPORT, "local")
    }
    assert triples(scan_file(path, tmp_path, script=True)) == {
        ("script_dep", EXEC_SCRIPT, "local")
    }


def test_main_guard_inequality_and_reversed_order(tmp_path):
    path = write(
        tmp_path,
        "entry.py",
        'if __name__ != "__main__":\n    import imported\n'
        'if "__main__" == __name__:\n    import scripted\n',
    )
    write(tmp_path, "imported.py", "")
    write(tmp_path, "scripted.py", "")
    assert {item.target for item in scan_file(path, tmp_path)} == {"imported"}
    assert {item.target for item in scan_file(path, tmp_path, script=True)} == {"scripted"}


def test_nested_and_compound_conditions_are_conservative(tmp_path):
    path = write(
        tmp_path,
        "entry.py",
        'if FLAG:\n    if __name__ == "__main__":\n        import nested_a\n'
        '    else:\n        import nested_b\n'
        'if __name__ == "__main__" and FLAG:\n    import compound_a\nelse:\n    import compound_b\n',
    )
    findings = scan_file(path, tmp_path, script=True)
    assert {item.target for item in findings} == {
        "nested_a", "compound_a", "compound_b"
    }
    assert {item.execution for item in findings} == {EXEC_DEFERRED}


def test_function_local_import_is_deferred_not_import_time(tmp_path):
    path = write(tmp_path, "entry.py", "def later():\n    import deferred_dep\n")
    findings = scan_file(path, tmp_path)
    assert triples(findings) == {("deferred_dep", EXEC_DEFERRED, "external_or_unresolved")}


def test_deferred_graph_mode_propagates_to_transitive_module_imports(tmp_path):
    write(tmp_path, "entry.py", "def later():\n    import deferred_dep\n")
    write(tmp_path, "deferred_dep.py", "import transitive_dep\n")
    write(tmp_path, "transitive_dep.py", "VALUE = 1\n")
    seen, findings = walk_graph(
        tmp_path, ["entry"], script_entries=True, traverse_deferred=True
    )
    assert seen == {"entry", "deferred_dep", "transitive_dep"}
    assert ("deferred_dep", EXEC_DEFERRED, "local") in triples(findings)
    assert ("transitive_dep", EXEC_DEFERRED, "local") in triples(findings)


def test_packages_relative_imports_and_script_graph(tmp_path):
    write(tmp_path, "pkg/__init__.py", "from . import helper\n")
    write(tmp_path, "pkg/helper.py", "import decimal\n")
    write(
        tmp_path,
        "driver.py",
        'if __name__ == "__main__":\n    import pkg\n',
    )
    seen, findings = walk_graph(tmp_path, ["driver"], script_entries=True)
    assert seen == {"driver", "pkg", "pkg.helper"}
    assert ("pkg", EXEC_SCRIPT, "local") in triples(findings)
    assert ("pkg.helper", EXEC_IMPORT, "local") in triples(findings)


def test_literal_and_variable_dynamic_imports_are_visible(tmp_path):
    path = write(
        tmp_path,
        "entry.py",
        'import importlib\nimportlib.import_module("literal_dep")\n'
        'name = "unknown"\n__import__(name)\n',
    )
    findings = scan_file(path, tmp_path)
    assert ("literal_dep", EXEC_IMPORT, "external_or_unresolved") in triples(findings)
    unresolved = [item for item in findings if item.resolution == "unclassified_dynamic"]
    assert len(unresolved) == 1
    assert "__import__" in unresolved[0].detail


def test_class_body_except_and_definition_expressions_are_not_dropped(tmp_path):
    path = write(
        tmp_path,
        "entry.py",
        'import importlib as il\nfrom importlib import import_module as im\n'
        'class C(il.import_module("base_mod")):\n    import class_dep\n'
        '    def method(self, x: im("annotation_dep")):\n        import method_dep\n'
        'try:\n    import primary_dep\nexcept ImportError:\n    import fallback_dep\n',
    )
    findings = triples(scan_file(path, tmp_path))
    assert ("base_mod", EXEC_IMPORT, "external_or_unresolved") in findings
    assert ("annotation_dep", EXEC_IMPORT, "external_or_unresolved") in findings
    assert ("class_dep", EXEC_IMPORT, "external_or_unresolved") in findings
    assert ("method_dep", EXEC_DEFERRED, "external_or_unresolved") in findings
    assert ("fallback_dep", EXEC_DEFERRED, "external_or_unresolved") in findings


def test_from_package_member_and_package_initializer_are_walked(tmp_path):
    write(tmp_path, "pkg/__init__.py", "import decimal\n")
    write(tmp_path, "pkg/child.py", "import fractions\n")
    write(tmp_path, "entry.py", "from pkg import child\n")
    seen, findings = walk_graph(tmp_path, ["entry"], script_entries=True)
    assert seen == {"entry", "pkg", "pkg.child"}
    assert ("pkg.child", EXEC_IMPORT, "local") in triples(findings)


def test_identity_main_comparison_is_conservative(tmp_path):
    path = write(
        tmp_path,
        "entry.py",
        'if __name__ is "__main__":\n    import maybe_script\nelse:\n    import maybe_import\n',
    )
    findings = scan_file(path, tmp_path, script=True)
    assert {item.target for item in findings} == {"maybe_script", "maybe_import"}
    assert {item.execution for item in findings} == {EXEC_DEFERRED}


def test_multiple_entrypoints_are_order_independent(tmp_path):
    write(tmp_path, "a.py", "import b\n")
    write(tmp_path, "b.py", 'if __name__ == "__main__":\n    import script_only\n')
    first = walk_graph(tmp_path, ["a", "b"], script_entries=True)
    second = walk_graph(tmp_path, ["b", "a"], script_entries=True)
    assert first == second
    assert "script_only" in {item.target for item in first[1]}


def test_relative_import_cannot_escape_declared_root(tmp_path):
    path = write(tmp_path, "pkg/mod.py", "from .. import escaped\n")
    findings = scan_file(path, tmp_path)
    assert len(findings) == 1
    assert findings[0].resolution == "unclassified_dynamic"
    assert "escapes root" in findings[0].detail


def test_current_pair_kernel_scripts_have_no_silent_dynamic_imports():
    root = Path(__file__).resolve().parents[1]
    package = root / "udt_uncompressed_pair_kernel_reconstruction_2026-08-14"
    scripts = sorted(package.glob("*.py"))
    assert {path.name for path in scripts} == {
        "build_review_intake.py",
        "derive_uncompressed_pair_evaluator.py",
        "run_catch_proofs.py",
        "verify_independent.py",
        "verify_package.py",
    }
    entries = [
        f"udt_uncompressed_pair_kernel_reconstruction_2026-08-14.{path.stem}"
        for path in scripts
    ]
    seen, findings = walk_graph(root, entries, script_entries=True)
    assert seen == set(entries)
    assert not [item for item in findings if item.resolution == "unclassified_dynamic"]
    permitted = set(sys.stdlib_module_names) | {"sympy"}
    offenders = sorted(
        item.target for item in findings
        if item.resolution == "external_or_unresolved"
        and item.target.split(".")[0] not in permitted
    )
    assert not offenders


def test_numeric_only_fixture_remains_permitted(tmp_path):
    path = write(tmp_path, "numeric.py", "import math\nimport numpy as np\n")
    targets = {item.target.split(".")[0] for item in scan_file(path, tmp_path, script=True)}
    assert targets <= {"math", "numpy"}
