"""SOLUTION-SPACE GATE -- the anti-imposition harness (Charles 2026-06-25).

Companion to the P1 purity harness.  The purity gate (`test_solver_integrity.py`) catches
*imports* of physics literals; THIS gate catches the broader drift from EXPLORING the metric's
solution space to IMPOSING the physics we expect.

*** LEGACY FROZEN PROVENANCE SCOPE -- not the current scientific program. ***
*** GOVERNING PRINCIPLE -- PROVENANCE, VALIDITY & HONESTY, NEVER AESTHETICS. ***
Every check here is PHYSICS-BLIND.  It checks only:
  - PROVENANCE: is each import a numeric technique (numpy/torch/scipy/stdlib) or a *registered*
                project module?  (An import is or isn't numeric -- decidable, no physics judgment.)
  - HONESTY:    is every pinned BC/ansatz/coupling tagged and surfaced so we can choose to free it?
                (A tag is or isn't present -- decidable, no physics judgment.)
It NEVER judges AESTHETIC OR INTERPRETIVE MERIT -- whether a solution is a lump or the expected
answer. Numerical certification may and should check original residuals, constraints, boundary
treatment, error control, and a claimed convergence test. Do NOT add a check here that throws a
valid member of its declared class away on interpretive grounds.

Anti-hang: pure AST / source scans + an import-graph walk.  No torch, no solve.  Whole file < 0.1s.
"""
import os
import sys
from pathlib import Path

import pytest

from guardrail_import_scanner import EXEC_DEFERRED, resolve_module, scan_file, walk_graph

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =============================================================================
# A.  NUMERIC-ONLY IMPORTS  -- traceability: every number is the action + arithmetic
# =============================================================================
# This dated legacy solver graph is walked transitively from p1_residual_general_einstein. It is
# retained as a regression/provenance scope only and is not the current UDT scientific program.
# NOTE (verifier 2026-06-25): solver_action.py is NOT in this runtime graph -- the live operator is
# hand-coded; its EQUALITY to the EL of solver_action is enforced SEPARATELY by
# tests/test_operator_from_action.py (P2), not by a runtime import.  So this lint governs the RUNTIME
# imports; the action-provenance is a distinct, already-wired check.
SOLVER_ENTRY = ("p1_residual_general_einstein",)

# Numeric-technique third-party libraries (the ONLY non-stdlib imports a clean solver may carry).
# These resolve intractable calculations; they carry no physics.  stdlib is auto-allowed
# (infrastructure, not physics) via sys.stdlib_module_names.
NUMERIC_THIRDPARTY = {"numpy", "torch", "scipy", "mpmath", "sympy"}

# PROJECT-MODULE REGISTRY.  Every project-local module reachable from the solver MUST appear here
# with a provenance CLASSIFICATION.  The registry does NOT certify cleanliness (that is the human
# audit, task: "Audit solver modules directly"); it certifies that someone CLASSIFIED the module.
# Allowed classification prefixes:
#   numeric-method   : pure numeric machinery (grids, quadrature, linear algebra, codegen eval).
#   action-EL-derived: realizes a term of solver_action.py via its Euler-Lagrange residual.
#   AUDIT-PENDING    : reached by the graph, classification not yet verified by the direct audit.
#   SMUGGLES:<what>  : the audit found a physics object/BC/count/mechanism NOT sourced from the
#                      action -- a cleanup target.
# The HARD test asserts every reached module is PRESENT here (forces a provenance decision).
# The documented_gap test asserts none is AUDIT-PENDING/SMUGGLES (XPASSes when the audit closes).
PROJECT_MODULE_REGISTRY = {
    "p1_residual_general_einstein": "action-EL-derived: the live residual = EL of solver_action (branch_operator E_mixed_branch/EL_phi_branch)",
    "branch_operator":              "action-EL-derived: derived G/P-switch gravity operator",
    "b1prime_3d_offround_residual": "action-EL-derived: validated derived-operator assembly (E_mixed/EL_phi/EL_Th)",
    "full3d_spectral":              "numeric-method: spectral grid, metric build, coord weights",
    "full3d_newton":                "numeric-method: vmap-safe 4x4 inverse/determinant + pack/unpack via solver_pack",
    "solver_pack":                  "numeric-method: 5-field <-> flat-vector reshape (pure torch; extracted 2026-06-25 so the live graph stops pulling full3d_solver's physics surface)",
    "whole_metric_3d_core":         "numeric-method: curvature calculus -- finite-diff, metric inverse, Christoffel, Einstein tensor (audited 2026-06-25, no physics pin)",
    "whole_metric_3d_matter":       "legacy-conditional-action-EL: matter stress/Lagrangian under the dated admitted action",
    "free_s2_matter":               "legacy-conditional-action-EL: three-component S2 carrier POSIT under this frozen historical branch, not current native UDT",
    "spectral_sph_exact":           "numeric-method: spherical-harmonic-EXACT d/dtheta (per-azimuthal-mode associated-Legendre) -- the grid fix so winding sin(theta) matter differentiates exactly",
    "einstein_3d_eval":             "numeric-method: Einstein-tensor evaluator (Weyl form)",
    "einstein_3d_weyl_gen":         "numeric-method: sympy-generated Einstein components (codegen)",
    "spectral_cheb":                "numeric-method: Chebyshev nodes + Clenshaw-Curtis weights",
    "spectral_sph":                 "numeric-method: theta/psi spectral operators (Gauss-Legendre)",
    "galerkin_basis":               "numeric-method: BC-recombined RADIAL spectral-Galerkin basis (category-A conditioning) -- a fixed change-of-variables B_full mapping coefficients->nodal update so the homogeneous BC rows + stiff near-edge Chebyshev modes are eliminated; residual physics UNCHANGED (Shen 1994 / Boyd / Olver-Townsend)",
}


def _is_project_module(name):
    return resolve_module(Path(REPO), name) is not None


def _walk_solver_graph():
    """Transitive closure of project-local modules reachable from the solver entries, plus the
    set of every (importer, imported) edge so an offender can be located."""
    # Potential-runtime imports remain part of this conservative provenance inventory, while the
    # scanner records that they are not guaranteed import-time execution.
    seen, findings = walk_graph(
        Path(REPO), SOLVER_ENTRY, script_entries=False, traverse_deferred=True
    )
    edges = [(item.importer, item.target) for item in findings]
    return seen, edges


def test_solver_imports_are_numeric_or_registered():
    """HARD (provenance).  Every import reachable from the live solver is either a numeric
    technique (numpy/torch/scipy/...), benign stdlib, or a REGISTERED project module.  An
    unknown third-party import, or an unregistered project module, fails -- it forces a
    provenance decision (numeric method, or smuggled physics?)."""
    _, edges = _walk_solver_graph()
    stdlib = sys.stdlib_module_names
    offenders = []
    for importer, imp in edges:
        root_name = imp.split(".")[0]
        if root_name in stdlib or root_name in NUMERIC_THIRDPARTY:
            continue
        if _is_project_module(imp):
            if imp not in PROJECT_MODULE_REGISTRY:
                offenders.append((importer, imp, "UNREGISTERED project module"))
            continue
        offenders.append((importer, imp, "UNKNOWN third-party import (not a numeric technique)"))
    assert not offenders, (
        "non-numeric / unregistered import(s) in the solver graph -- classify each as a numeric "
        "technique or register it in PROJECT_MODULE_REGISTRY:\n  " +
        "\n  ".join(f"{i} -> {m}  [{why}]" for i, m, why in offenders))


def test_no_unaudited_or_smuggling_modules():
    """HARD (provenance).  No reached project module is left AUDIT-PENDING or found to SMUGGLE
    physics not sourced from the action.  Was an xfail documented_gap; the direct audit
    (2026-06-25) classified every reached module to numeric-method / action-EL-derived, so this
    is now a live assert -- it REDs if a new unaudited/smuggling module enters the solver graph."""
    seen, _ = _walk_solver_graph()
    open_items = {m: PROJECT_MODULE_REGISTRY[m] for m in sorted(seen)
                  if PROJECT_MODULE_REGISTRY.get(m, "").startswith(("AUDIT-PENDING", "SMUGGLES"))}
    assert not open_items, "unaudited/smuggling modules: " + "; ".join(
        f"{m}: {c}" for m, c in open_items.items())


def test_every_reached_module_is_registered_structurally():
    """HARD (honesty).  The registry stays SYNCED to the code: every project module the graph
    reaches has a registry entry (catches a new module added to the solver without classifying
    it).  Mirror of the import test, asserted on the closure rather than the edges."""
    seen, _ = _walk_solver_graph()
    missing = sorted(m for m in seen if m not in PROJECT_MODULE_REGISTRY)
    assert not missing, f"reached project modules missing from PROJECT_MODULE_REGISTRY: {missing}"


def test_registry_has_no_dead_entries():
    """HARD (honesty).  The registry stays SYNCED the OTHER direction too: every registered module
    is actually REACHED by the solver graph.  A dead entry is inert -- it could be mis-classified
    or lie with no test effect (verifier 2026-06-25 caught an inert `solver_action` entry this
    way).  Forces the registry to describe the REAL runtime graph, nothing more."""
    seen, _ = _walk_solver_graph()
    dead = sorted(m for m in PROJECT_MODULE_REGISTRY if m not in seen)
    assert not dead, (f"registry entries for modules NOT reached by the solver graph (inert/lying "
                      f"-- remove them or fix the entry point): {dead}")


# =============================================================================
# B.  PREMISE LEDGER  -- every pinned BC/ansatz/coupling is tagged and surfaced
# =============================================================================
# Each pinned premise of the live solver, tagged for provenance.  Tags:
#   FREE          : a scanned/explored degree of freedom, not pinned to a physics value.
#   THEORY:<cite> : fixed WITH a derivation/canon citation (no citation => not THEORY).
#   HABIT         : fixed with no theory behind it = a DRIFT FLAG; free it or justify it.
# `token` must appear in the live solver source so the ledger cannot go stale / lie (honesty).
# This ledger is SURFACING, not forbidding: it makes every pin visible so we can choose to free
# it.  It makes NO judgment about whether a pin is physically right (that is merit -> with Charles).
PREMISE_LEDGER = (
    # token,        tag,                                                          source file
    ("kap8",       "THEORY: round-gate derivation kap8=1 (solver_action / F2; native_dilation_weight)", "p1_residual_general_einstein.py"),
    ("X",          "FREE: kinetic/curvature ratio, ghost+Cassini-bounded large negative (branch_operator X_PROD)", "p1_residual_general_einstein.py"),
    ("xi",         "FREE: matter coupling (scale-breaker; value provenance open, F2)",                  "p1_residual_general_einstein.py"),
    ("kap",        "FREE: matter coupling (value provenance open, F2)",                                 "p1_residual_general_einstein.py"),
    ("branch",     "HABIT: curvature G/P fork -- the residual DEFAULT is 'G' (gauges the angular obstruction away); a choice to surface and SCAN both (the kap8 characterization runs both G and P; the core matter Theta-pin is now RETIRED -- the matter core is FREE, winding from seed)", "p1_residual_general_einstein.py"),
    ("wbc",        "FREE: boundary-penalty weight (numeric BC enforcement strength)",                   "p1_residual_general_einstein.py"),
    ("p",          "FREE: depth dial b(core)=p (the dilation depth we scan)",                           "p1_residual_general_einstein.py"),
)

ALLOWED_TAGS = ("FREE", "THEORY", "HABIT")


def test_premise_ledger_tagged_and_synced():
    """HARD (honesty).  Every premise carries an allowed provenance tag AND its token still
    appears in the named solver source (the ledger cannot silently go stale or lie)."""
    bad_tag, stale = [], []
    for token, tag, srcfile in PREMISE_LEDGER:
        if not tag.startswith(ALLOWED_TAGS):
            bad_tag.append((token, tag))
        path = os.path.join(REPO, srcfile)
        with open(path) as f:
            if token not in f.read():
                stale.append((token, srcfile))
    assert not bad_tag, f"premise(s) with no allowed provenance tag {ALLOWED_TAGS}: {bad_tag}"
    assert not stale, f"premise ledger out of sync -- token not found in source: {stale}"


@pytest.mark.documented_gap
@pytest.mark.xfail(reason="known HABIT pin (silent G/P fork) is not yet freed or justified to "
                          "THEORY; XPASSes when that branch choice is resolved.",
                   strict=False)
def test_no_habit_pins():
    """CLEAN target (honesty).  No premise is left tagged HABIT (an unjustified pin = drift).
    XPASSes when every habit-pin is either freed (FREE) or justified to THEORY."""
    habits = [(t, tag) for t, tag, _ in PREMISE_LEDGER if tag.startswith("HABIT")]
    assert not habits, f"unjustified HABIT pins (free them or justify to THEORY): {habits}"
