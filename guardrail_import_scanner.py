#!/usr/bin/env python3
"""Conservative static import inventory for declared Python entry points.

The scanner never imports inspected code. It distinguishes imports executed while a module is
loaded, imports added by a script's exact ``__main__`` equality path, and dependencies that may
execute only through a conditional or deferred function/method path. It follows declared local
entry-point graphs without claiming to decide arbitrary Python execution.

This is a provenance aid, not a native-physics or runtime-security verifier.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator


EXEC_IMPORT = "import_time"
EXEC_SCRIPT = "script_entry"
EXEC_DEFERRED = "potential_runtime"


@dataclass(frozen=True, order=True)
class ImportFinding:
    importer: str
    target: str
    execution: str
    syntax: str
    line: int
    resolution: str
    resolved_path: str = ""
    detail: str = ""


def _main_guard_value(test: ast.expr) -> bool | None:
    """Return the value of an exact ``__name__ ==/!= '__main__'`` comparison."""
    if not isinstance(test, ast.Compare) or len(test.ops) != 1 or len(test.comparators) != 1:
        return None
    left, right = test.left, test.comparators[0]
    name_on_left = isinstance(left, ast.Name) and left.id == "__name__"
    main_on_right = isinstance(right, ast.Constant) and right.value == "__main__"
    name_on_right = isinstance(right, ast.Name) and right.id == "__name__"
    main_on_left = isinstance(left, ast.Constant) and left.value == "__main__"
    if not ((name_on_left and main_on_right) or (name_on_right and main_on_left)):
        return None
    if isinstance(test.ops[0], ast.Eq):
        return True
    if isinstance(test.ops[0], ast.NotEq):
        return False
    return None


def _module_parts(path: Path, root: Path) -> tuple[str, ...]:
    rel = path.resolve().relative_to(root.resolve())
    if path.is_dir():
        return tuple(rel.parts)
    parts = list(rel.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts.pop()
    return tuple(parts)


def resolve_module(root: Path, module: str) -> Path | None:
    """Resolve a dotted local module, regular package, or namespace package without import."""
    if not module:
        return None
    base = root.resolve().joinpath(*module.split("."))
    file_path = base.with_suffix(".py")
    package_path = base / "__init__.py"
    if file_path.is_file():
        return file_path.resolve()
    if package_path.is_file():
        return package_path.resolve()
    if base.is_dir():
        return base.resolve()  # namespace package: no module body to scan
    return None


def _absolute_from(importer: Path, root: Path, level: int, module: str | None) -> str | None:
    if level == 0:
        return module or ""
    parts = list(_module_parts(importer, root))
    if importer.name != "__init__.py" and parts:
        parts.pop()
    climbs = level - 1
    # An empty package prefix is an attempted relative import beyond the declared root.
    if not parts or climbs >= len(parts):
        return None
    if climbs:
        parts = parts[:-climbs]
    if module:
        parts.extend(module.split("."))
    return ".".join(parts)


def _resolved(root: Path, target: str) -> tuple[str, str]:
    path = resolve_module(root, target)
    if path is None:
        return "external_or_unresolved", ""
    kind = "local_namespace" if path.is_dir() else "local"
    return kind, str(path.relative_to(root.resolve()))


def _conditional(execution: str) -> str:
    return EXEC_DEFERRED if execution in {EXEC_IMPORT, EXEC_SCRIPT} else execution


class _Collector:
    def __init__(self, path: Path, root: Path, script: bool):
        self.path = path.resolve()
        self.root = root.resolve()
        self.script = script
        self.importer = ".".join(_module_parts(self.path, self.root))
        self.findings: list[ImportFinding] = []
        self.importlib_aliases = {"importlib"}
        self.import_module_aliases: set[str] = set()

    def add(self, target: str, execution: str, syntax: str, line: int, detail: str = "") -> None:
        resolution, resolved_path = _resolved(self.root, target)
        self.findings.append(
            ImportFinding(
                self.importer, target, execution, syntax, line, resolution, resolved_path, detail
            )
        )

    def unresolved(self, execution: str, syntax: str, line: int, detail: str) -> None:
        self.findings.append(
            ImportFinding(
                self.importer,
                "<dynamic>",
                execution,
                syntax,
                line,
                "unclassified_dynamic",
                "",
                detail,
            )
        )

    def _from_targets(self, node: ast.ImportFrom, base: str, execution: str) -> None:
        if node.module:
            self.add(base, execution, "from", node.lineno)
        for alias in node.names:
            if alias.name == "*":
                if node.level:
                    self.unresolved(execution, "from", node.lineno, "relative star import")
                continue
            candidate = ".".join(part for part in (base, alias.name) if part)
            # ``from pkg import child`` executes child only when it is a real local submodule.
            if candidate and resolve_module(self.root, candidate) is not None:
                self.add(candidate, execution, "from-member", node.lineno)
            if base == "importlib" and alias.name == "import_module":
                self.import_module_aliases.add(alias.asname or alias.name)

    def _definition_expressions(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, execution: str
    ) -> None:
        for decorator in node.decorator_list:
            self.expression(decorator, execution)
        for default in list(node.args.defaults) + list(node.args.kw_defaults):
            if default is not None:
                self.expression(default, execution)
        annotations = [node.returns]
        annotations.extend(arg.annotation for arg in node.args.posonlyargs)
        annotations.extend(arg.annotation for arg in node.args.args)
        annotations.extend(arg.annotation for arg in node.args.kwonlyargs)
        if node.args.vararg:
            annotations.append(node.args.vararg.annotation)
        if node.args.kwarg:
            annotations.append(node.args.kwarg.annotation)
        for annotation in annotations:
            if annotation is not None:
                self.expression(annotation, execution)

    def statements(self, statements: Iterable[ast.stmt], execution: str) -> None:
        for node in statements:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.add(alias.name, execution, "import", node.lineno)
                    if alias.name == "importlib":
                        self.importlib_aliases.add(alias.asname or alias.name)
            elif isinstance(node, ast.ImportFrom):
                base = _absolute_from(self.path, self.root, node.level, node.module)
                if base is None:
                    self.unresolved(execution, "from", node.lineno, "relative import escapes root")
                    continue
                self._from_targets(node, base, execution)
            elif isinstance(node, ast.If):
                self.expression(node.test, execution)
                main_value = _main_guard_value(node.test)
                if main_value is None:
                    branch_execution = _conditional(execution)
                    self.statements(node.body, branch_execution)
                    self.statements(node.orelse, branch_execution)
                else:
                    condition_true = main_value if self.script else not main_value
                    selected = node.body if condition_true else node.orelse
                    selected_execution = (
                        EXEC_SCRIPT
                        if execution != EXEC_DEFERRED and self.script and condition_true == main_value
                        else execution
                    )
                    self.statements(selected, selected_execution)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._definition_expressions(node, execution)
                self.statements(node.body, EXEC_DEFERRED)
            elif isinstance(node, ast.ClassDef):
                for decorator in node.decorator_list:
                    self.expression(decorator, execution)
                for base in node.bases:
                    self.expression(base, execution)
                for keyword in node.keywords:
                    self.expression(keyword.value, execution)
                # Class bodies execute when the class statement executes; methods remain deferred.
                self.statements(node.body, execution)
            elif isinstance(node, ast.Try):
                self.statements(node.body, execution)
                for handler in node.handlers:
                    if handler.type is not None:
                        self.expression(handler.type, execution)
                    self.statements(handler.body, _conditional(execution))
                self.statements(node.orelse, _conditional(execution))
                self.statements(node.finalbody, execution)
            elif isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
                for expr in (getattr(node, "target", None), getattr(node, "iter", None), getattr(node, "test", None)):
                    if expr is not None:
                        self.expression(expr, execution)
                self.statements(node.body, _conditional(execution))
                self.statements(node.orelse, _conditional(execution))
            elif isinstance(node, (ast.With, ast.AsyncWith)):
                for item in node.items:
                    self.expression(item.context_expr, execution)
                    if item.optional_vars is not None:
                        self.expression(item.optional_vars, execution)
                self.statements(node.body, execution)
            elif isinstance(node, ast.Match):
                self.expression(node.subject, execution)
                for case in node.cases:
                    if case.guard is not None:
                        self.expression(case.guard, _conditional(execution))
                    self.statements(case.body, _conditional(execution))
            else:
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, ast.expr):
                        self.expression(child, execution)
                    elif isinstance(child, ast.stmt):
                        self.statements([child], execution)

    def expression(self, node: ast.AST, execution: str) -> None:
        for child in ast.walk(node):
            if not isinstance(child, ast.Call):
                continue
            kind = None
            if isinstance(child.func, ast.Name) and child.func.id == "__import__":
                kind = "__import__"
            elif isinstance(child.func, ast.Name) and child.func.id in self.import_module_aliases:
                kind = "importlib.import_module"
            elif (
                isinstance(child.func, ast.Attribute)
                and child.func.attr == "import_module"
                and isinstance(child.func.value, ast.Name)
                and child.func.value.id in self.importlib_aliases
            ):
                kind = "importlib.import_module"
            if kind is None:
                continue
            if child.args and isinstance(child.args[0], ast.Constant) and isinstance(child.args[0].value, str):
                target = child.args[0].value
                if target.startswith("."):
                    self.unresolved(execution, kind, child.lineno, "relative dynamic import")
                else:
                    self.add(target, execution, kind, child.lineno)
            else:
                detail = ast.unparse(child) if hasattr(ast, "unparse") else kind
                self.unresolved(execution, kind, child.lineno, detail)


def scan_file(
    path: Path,
    root: Path,
    *,
    script: bool = False,
    base_execution: str = EXEC_IMPORT,
) -> list[ImportFinding]:
    path = path.resolve()
    root = root.resolve()
    if path.is_dir():
        return []
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    collector = _Collector(path, root, script)
    collector.statements(tree.body, base_execution)
    return sorted(set(collector.findings))


def _package_initializers(root: Path, module: str) -> Iterator[str]:
    parts = module.split(".")
    for index in range(1, len(parts)):
        parent = ".".join(parts[:index])
        resolved = resolve_module(root, parent)
        if resolved is not None and resolved.name == "__init__.py":
            yield parent


def walk_graph(
    root: Path,
    entrypoints: Iterable[str],
    *,
    script_entries: bool = True,
    traverse_deferred: bool = False,
) -> tuple[set[str], list[ImportFinding]]:
    """Walk local dependencies reachable in each declared execution mode."""
    root = root.resolve()
    frontier: list[tuple[str, bool, str]] = [
        (entry, script_entries, EXEC_IMPORT) for entry in entrypoints
    ]
    seen_modes: set[tuple[str, bool, str]] = set()
    seen: set[str] = set()
    findings: list[ImportFinding] = []
    while frontier:
        module, as_script, base_execution = frontier.pop()
        path = resolve_module(root, module)
        if path is None:
            continue
        canonical = ".".join(_module_parts(path, root))
        mode_key = (canonical, as_script, base_execution)
        if mode_key in seen_modes:
            continue
        seen_modes.add(mode_key)
        seen.add(canonical)
        if path.is_dir():
            continue
        scanned = scan_file(
            path, root, script=as_script, base_execution=base_execution
        )
        findings.extend(scanned)
        for item in scanned:
            if item.resolution in {"local", "local_namespace"} and (
                traverse_deferred or item.execution != EXEC_DEFERRED
            ):
                child_execution = (
                    EXEC_DEFERRED if item.execution == EXEC_DEFERRED else EXEC_IMPORT
                )
                frontier.extend(
                    (parent, False, child_execution)
                    for parent in _package_initializers(root, item.target)
                )
                frontier.append((item.target, False, child_execution))
    return seen, sorted(set(findings))


def local_module_names(root: Path) -> Iterator[str]:
    """Yield modules only under an explicitly supplied root; never call as global discovery."""
    root = root.resolve()
    for path in sorted(root.rglob("*.py")):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        yield ".".join(_module_parts(path, root))
