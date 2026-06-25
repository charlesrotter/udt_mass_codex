"""P1 PURITY HARNESS -- machine-enforced solver integrity (SOLVER_INTEGRITY_UPGRADES_SPEC P1).

Each check is anchored to a REAL banked failure mode:
  - Liveness          <- the "off-diagonals built but dead" bug
  - Provenance lint   <- the smuggled kap8=0.05 constant
  - Limit recovery    <- standing correctness (flat/Schwarzschild/no-corruption)
  - Native-object     <- the imported S^3 Skyrme winding

SPINE (P1_PURITY_HARNESS_MAP.md S0): the harness REFERENCES derivations, it never RE-ASSERTS
their results.  No derived VALUE (kap8=1, a=e^phi) is hard-coded here; P1 checks the TAG is
present, P2's action file sources the value.

GUARD TARGET (Charles ruling 2026-06-23): the CURRENT live solver as-is.  The live path still
carries the import (a=-1 operator, S^3 hedgehog, Theta(0)=pi pin, untagged kap8/xi/kap).  Those
are surfaced as `documented_gap` xfail(strict=False) tests: they FAIL now (current=import) and
will XPASS the day the production path is migrated to the derived+native foundation -- the XPASS
is the self-resolving tripwire telling us to flip the guard to a hard assert.  Genuine regressions
are hard failures.

Anti-hang: ALL tests are FORWARD residual/Einstein evals on small bounded grids (Nr<=24) -- no
Newton, no jacrev, no solve.  Whole suite < 1s.  (A solve-bearing box-control test was deliberately
NOT included: the time sector is frozen in the current static solver, so omega->0 / box-control is
degenerate now -- it belongs to Stage 5.  The `slow` marker in pytest.ini is reserved for it.)
"""
import os, ast, re, inspect, math
import torch
import pytest

torch.set_default_dtype(torch.float64)

from full3d_spectral import (Grid3D, attach_coord_weight, build_metric,
                             einstein_mixed_weyl, field_n, PI, T, R, TH, PS)
from p1_residual_general_einstein import (residual_vector_p1, einstein_general_hybrid,
                                          pack6, pack9)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPERATOR_FILE = os.path.join(REPO, "p1_residual_general_einstein.py")
CALLER_FILE = os.path.join(REPO, "p1_validate.py")

PROVENANCE_TAGS = ("DERIVED", "POSTULATED", "FREE", "IMPORTED")

# Structural numerics legitimately allowed in operator code (tensor indices, zero/one,
# det-clamp).  NOT physics.  A physics constant outside this set must be tagged/registered.
# Kept MINIMAL (verifier 2026-06-23: a wide int allowlist would miss an integer-valued coupling
# kap8=2/3).  Only {0,1} actually occur in the scanned bodies today; 2 is kept as a benign
# index/exponent headroom.  3,4,5 are NOT allowlisted -> an integer coupling there is flagged.
STRUCTURAL_INTS = {0, 1, 2}
STRUCTURAL_FLOATS = {0.0, 1e-30}
# Registered known-gap CALL SITES (anchored by code substring, NOT by value -- verifier caught
# that registering the VALUE 1.0 would let a smuggled 1.0 coupling hide).  A literal on one of
# these lines is the documented xi=kap gap (surfaced by test_matter_couplings_tagged); a 1.0
# anywhere ELSE in the operator is still flagged.
REGISTERED_GAP_SITES = ("stress_tensor(",)


# ----------------------------------------------------------------------------- helpers
def _src(path):
    with open(path) as f:
        return f.read()


def _line_has_tag(line):
    if "#" not in line:
        return False
    comment = line.split("#", 1)[1]
    return any(t in comment for t in PROVENANCE_TAGS)


def _numeric_consts_in_func(path, funcname):
    """Numeric literals in a function BODY (signature defaults + docstring excluded)."""
    tree = ast.parse(_src(path))
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == funcname:
            for stmt in node.body:                      # body only -> skips arg defaults
                for sub in ast.walk(stmt):
                    if (isinstance(sub, ast.Constant)
                            and isinstance(sub.value, (int, float))
                            and not isinstance(sub.value, bool)):
                        out.append((sub.value, sub.lineno))
    return out


def _untagged_literal_assignments(path, varname):
    """Lines that SET varname to a numeric literal without a provenance tag."""
    pat = re.compile(r"\b%s\s*=\s*[-+]?[0-9][0-9.eE+-]*" % re.escape(varname))
    bad = []
    for i, line in enumerate(_src(path).splitlines(), 1):
        s = line.strip()
        if s.startswith("#"):
            continue
        if pat.search(line) and not _line_has_tag(line):
            bad.append((i, s))
    return bad


def _grid(Nr=12, Nth=8, Nps=8, rc=0.05, cell=14.0):
    return attach_coord_weight(Grid3D(Nr=Nr, Nth=Nth, Nps=Nps, rc=rc, cell=cell))


# =============================================================================
# 1. LIVENESS  -- every live DOF must move the residual (off-diagonals not dead)
# =============================================================================
def test_all_dofs_live(grid, offround_fields):
    """Perturb each of the 9 live fields (a,b,c,d,Th,phi + the 3 spatial off-diagonals
    e_rt,e_rp,e_tp) at an interior body node on a GENERIC OFF-ROUND background; the residual
    MUST change.  An unmoved residual = a dead DOF / a secretly degenerate operator.  (The
    off-diagonal sector was completed 2026-06-25 -- gate #7; the e_* DOF are now live and the
    residual carries their 3 off-diagonal Einstein rows.)"""
    a, b, c, d, Th = [f.clone() for f in offround_fields[:5]]
    e_rt, e_rp, e_tp = [f.clone() for f in offround_fields[5:8]]   # generic off-round off-diagonals
    # phi: a generic nonzero off-round dilation field (so no DOF is symmetry-decoupled)
    R, TH, PS = grid.Rg, grid.THg, grid.PSg
    rmid = 0.5 * (grid.rc + grid.ri)
    phi = 0.03 * torch.exp(-((R - rmid) / 2.0) ** 2) * (1.0 + 0.2 * torch.cos(TH) * torch.cos(PS))
    fields = [a, b, c, d, Th, phi, e_rt, e_rp, e_tp]
    F0 = residual_vector_p1(pack9(*fields), grid, p=0.4, kap8=0.05)
    ir, it, ip = grid.Nr // 2, grid.Nth // 2, grid.Nps // 2
    names = ["a", "b", "c", "d", "Th", "phi", "e_rt", "e_rp", "e_tp"]
    moved = {}
    for k, name in enumerate(names):
        pert = [f.clone() for f in fields]
        pert[k][ir, it, ip] += 1e-3
        F1 = residual_vector_p1(pack9(*pert), grid, p=0.4, kap8=0.05)
        moved[name] = float((F1 - F0).norm())
    dead = {n: v for n, v in moved.items() if v < 1e-9}
    assert not dead, f"DEAD DOF(s) -- residual unmoved by perturbation: {dead}\n all: {moved}"
    # the derived dilation field phi specifically must be live
    assert moved["phi"] > 1e-9, f"phi DOF is DEAD ({moved['phi']:.2e})"


def test_time_row_is_frozen_static(grid, offround_fields):
    """STAGE-5 TODO, documented NOT silent (BOUND-not-FREEZE): the live metric has NO
    time-row off-diagonals (g_tr=g_tth=g_tps=0).  Stage 5 unfreezes them; this test then
    gets updated to a liveness check."""
    a, b, c, d, Th, e_rt, e_rp, e_tp = offround_fields
    g = build_metric(grid, a, b, c, d, e_rt, e_rp, e_tp)
    assert float(g[..., T, R].abs().max()) == 0.0
    assert float(g[..., T, TH].abs().max()) == 0.0
    assert float(g[..., T, PS].abs().max()) == 0.0


test_time_row_is_frozen_static = pytest.mark.documented_gap(test_time_row_is_frozen_static)


# =============================================================================
# 2. PROVENANCE LINT  -- physics constants carry a tag; no smuggled literals
# =============================================================================
def test_no_smuggled_literal_in_operator():
    """HARD: the operator body contains no UN-allowlisted, UN-registered numeric literal.
    Catches a re-introduced smuggled coupling (e.g. kap8=0.05 hardcoded into the operator)."""
    offenders = []
    src_lines = _src(OPERATOR_FILE).splitlines()
    # every function in the operator file that carries residual/Einstein PHYSICS (the body is
    # duplicated across the residual + its diagnostic recompute -- scan them all).
    for fn in ("einstein_general_hybrid", "residual_vector_p1", "component_residuals_p1"):
        for val, ln in _numeric_consts_in_func(OPERATOR_FILE, fn):
            line = src_lines[ln - 1] if 0 < ln <= len(src_lines) else ""
            ok = ((isinstance(val, int) and val in STRUCTURAL_INTS)
                  or (isinstance(val, float) and val in STRUCTURAL_FLOATS)
                  or any(site in line for site in REGISTERED_GAP_SITES))  # registered gap line
            if not ok:
                offenders.append((fn, val, ln))
    assert not offenders, (
        "untagged/unregistered physics literal(s) in operator body "
        "(tag with # DERIVED|POSTULATED|FREE|IMPORTED or register): %s" % offenders)


@pytest.mark.documented_gap
@pytest.mark.xfail(reason="kap8=1 is DERIVED (round-gate) but has not propagated; live callers "
                          "pass kap8=0.05 untagged. Value to be SOURCED at P2's action file.",
                   strict=False)
def test_kap8_callers_tagged():
    """CLEAN target: every kap8 literal in a production caller carries a provenance tag."""
    bad = _untagged_literal_assignments(CALLER_FILE, "kap8")
    assert not bad, f"untagged kap8 literals in {os.path.basename(CALLER_FILE)}: {bad}"


@pytest.mark.documented_gap
@pytest.mark.xfail(reason="matter couplings xi=kap=1.0 are hardcoded UNTAGGED in the operator "
                          "body (stress_tensor call). FREE per F2; value to be sourced at P2.",
                   strict=False)
def test_matter_couplings_tagged():
    """CLEAN target: the xi,kap couplings at the stress_tensor call carry a provenance tag."""
    line = next((l for l in _src(OPERATOR_FILE).splitlines() if "stress_tensor(" in l), "")
    assert _line_has_tag(line), f"untagged xi/kap at stress call: {line.strip()!r}"


def test_derived_a_phi_in_operator():
    """The production residual is migrated to the DERIVED scalar-tensor operator (M1):
    it no longer reads the a=-1 GR baseline; the field equations come from the audited
    branch_operator (E_mixed_branch / EL_phi_branch).  Was an xfail documented_gap; now
    XPASSes after the M1 migration, flipped to a hard assert."""
    src = _src(OPERATOR_FILE)
    assert "import branch_operator" in src, "operator residual does not import branch_operator"
    rv = inspect.getsource(residual_vector_p1)
    assert "E_mixed_branch" in rv, "residual does not use the derived E_mixed_branch operator"
    assert "a=-1" not in rv and "a = -1" not in rv, "residual still on the a=-1 baseline"


# =============================================================================
# 3. LIMIT RECOVERY  -- flat/Schwarzschild vacuum; hybrid does not corrupt the diagonal
# =============================================================================
def test_flat_limit_zero():
    """a=b=c=d=0, no off-diagonals -> Minkowski -> Einstein == 0."""
    G = _grid()
    z = torch.zeros(G.Nr, G.Nth, G.Nps, device=G.dev)
    Gmix, _ = einstein_general_hybrid(G, z, z, z, z, z, z, z)
    assert float(Gmix[G.body].abs().max()) < 1e-8


def test_schwarzschild_vacuum_N_convergent():
    """Exact Schwarzschild (f=1-2M/r) is vacuum -> G==0, and the error must NOT grow with Nr."""
    norms = []
    for Nr in (12, 16, 20):
        G = _grid(Nr=Nr, rc=1.0, cell=14.0)
        f = 1.0 - 2 * 0.3 / G.Rg
        aS = 0.5 * torch.log(f)
        bS = -0.5 * torch.log(f)
        z = torch.zeros_like(aS)
        Gmix, _ = einstein_general_hybrid(G, aS, bS, z, z, z, z, z)
        norms.append(float(Gmix[G.body].abs().max()))
    assert norms[-1] < 1e-3, f"Schwarzschild residual too large: {norms}"
    assert norms[-1] <= norms[0] + 1e-12, f"NOT N-convergent (residual grows with Nr): {norms}"


def test_de_sitter_operator_normalization():
    """NON-VACUUM normalization anchor (verifier 2026-06-23: flat+Schwarzschild are both G=0, so
    a constant RESCALE of the gravity operator -- e.g. a wrong 8pi normalization -- would pass
    them).  de Sitter static patch f=1-Lam r^2/3 has the ANALYTIC value G^mu_nu = -Lam delta^mu_nu.
    The operator must hit -Lam (not c*Lam) on all diagonal components -> pins the normalization."""
    Lam = 0.5
    G = _grid(Nr=16, rc=0.1, cell=1.0)
    f = 1.0 - Lam * G.Rg ** 2 / 3.0
    a = 0.5 * torch.log(f)
    b = -0.5 * torch.log(f)
    z = torch.zeros_like(a)
    Gmix, _ = einstein_general_hybrid(G, a, b, z, z, z, z, z)
    body = G.body
    for comp, name in ((T, "G^t_t"), (R, "G^r_r"), (TH, "G^th_th"), (PS, "G^ps_ps")):
        err = float((Gmix[..., comp, comp][body] + Lam).abs().max())
        assert err < 1e-9, f"{name} = {-Lam} expected (de Sitter); normalization off by {err:.2e}"


def test_offdiag_zero_hybrid_equals_weyl(grid, offround_fields):
    """The pole-stable HYBRID must equal the analytic diagonal Weyl Einstein EXACTLY when the
    off-diagonals are zero (the bracket is identically zero) -- proves no diagonal corruption."""
    a, b, c, d, Th, _, _, _ = offround_fields
    z = torch.zeros_like(a)
    Ghyb, _ = einstein_general_hybrid(grid, a, b, c, d, z, z, z)
    Gweyl = einstein_mixed_weyl(grid, a, b, c, d)
    assert float((Ghyb - Gweyl).abs().max()) < 1e-12


# =============================================================================
# 4. NATIVE-OBJECT GUARD  -- characterize the import; hard-fail only the m*pi control leak
# =============================================================================
def test_default_bc_is_not_skyrme_control():
    """HARD: the production default must NOT be the labeled Skyrme-twist negative control."""
    sig = inspect.signature(residual_vector_p1)
    assert sig.parameters["node_core"].default is True, "default flipped to the Skyrme control!"


def test_skyrme_mpi_ladder_is_control_only():
    """HARD: the m*pi Skyrme ladder appears ONLY in the clearly-labeled negative-control branch
    (node_core=False); the production node BCs use the single-node pi / 0, not the m*pi ladder."""
    src = inspect.getsource(residual_vector_p1)
    ladder = re.findall(r"m\s*\*\s*PI", src)
    assert len(ladder) == 1, f"m*pi ladder appears {len(ladder)}x (expected 1, the control)"
    assert "negative-control" in src, "the m*pi ladder is not labeled as the negative control"


@pytest.mark.documented_gap
@pytest.mark.xfail(reason="production matter uses the 4-component S^3 hedgehog (field_n returns a "
                          "cosTheta 4th component); the native S^2 winding n=x/r is not in the "
                          "production path. Live-frontier (time-live native S^2) migration.",
                   strict=False)
def test_matter_winding_is_native_S2(grid):
    """CLEAN target: native S^2/pi_2 carrier is a 3-vector (no cosTheta 4th component)."""
    Th = torch.full((grid.Nr, grid.Nth, grid.Nps), 0.7, device=grid.dev)
    n = field_n(grid, Th)
    assert n.shape[-1] == 3, f"matter carrier is {n.shape[-1]}-component (S^3 hedgehog), not S^2"


@pytest.mark.documented_gap
@pytest.mark.xfail(reason="default core_mode='deg1' pins Theta(0)=pi (imported-flavored BC that "
                          "HOLDS the soliton body); the native value-free node is 'free'. The "
                          "native migration flips the default.",
                   strict=False)
def test_default_core_mode_is_native_free():
    """CLEAN target: the default core BC is the maximally-agnostic value-free node."""
    sig = inspect.signature(residual_vector_p1)
    assert sig.parameters["core_mode"].default == "free", \
        "default core_mode pins the node value (deg1: Theta(0)=pi)"
