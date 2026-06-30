#!/usr/bin/env python3
"""
galerkin_basis.py -- BC-recombined spectral-Galerkin RADIAL basis for the UDT
DETERMINED static solve (category-A conditioning ONLY; the physics/residual is
UNCHANGED).

WHY (D1_FIX_DESIGN.md "CONDITIONING INVESTIGATION" + LIVE.md frontier):
the determined posing `residual_vector_p1(..., determined=True)` imposes the PDE at
all interior radial layers + DERIVED endpoint BCs on a Chebyshev collocation grid.
It will not floor below ~2e-3 because the residual, though ~99.9% linearly reducible,
lives in small-singular-value directions concentrated at the STIFF near-edge Chebyshev
nodes (d_r ~ O(N^2) endpoint amplification, smax~7e6). Uniform LM over-damps those
directions; a full SVD step overshoots them nonlinearly.

THE FIX (Shen, "Efficient Spectral-Galerkin Method I," SIAM J Sci Comput 15(6):1489,
1994; Boyd; Olver-Townsend): represent each metric/dilaton field in a RECOMBINED
Chebyshev basis whose functions satisfy that field's homogeneous boundary conditions
BY CONSTRUCTION. Then the homogeneous BC rows + stiff near-edge modes are eliminated and
the Newton step stays inside the smooth BC-satisfying subspace.

THIS IS A PURE CHANGE OF VARIABLES. We build a fixed matrix B_full mapping coefficients
-> nodal field-UPDATE, with recombined-basis blocks for the LINEAR-BC fields
(a,b,c,d,phi,e_rt,e_rp,e_tp) and IDENTITY blocks for the NONLINEAR-constraint matter
fields (n1,n2,n3, which carry |n|=1 and cannot use a linear recombined basis). The
Newton step solves in coefficient space:  J_a = J @ B_full ; solve LS for da ;
du = B_full @ da.  `residual_vector_p1` is byte-UNCHANGED.

CONSTRUCTION.  Each recombined basis spans the (Nr-2)-dim space of degree<=Nr-1
polynomials satisfying the field's two HOMOGENEOUS boundary functionals (this is
exactly the space Shen's T_n - T_{n+2} (Dirichlet) / analogous (Neumann/Robin)
recombinations span -- see `shen_recombination_field` for the explicit 3-term form,
cross-checked to span the identical column space).  We realise it as the ORTHONORMAL
null space of the two functional rows in NODAL space (SVD): this handles Dirichlet,
Neumann, the metric-component (Robin-in-warp) and the mixed cases UNIFORMLY, and an
orthonormal B (cond(B)=1) gives the cleanest possible cond(J@B).  NON-homogeneous BCs
(b core = -p ; the c,d metric-component seal -> c'(ri)=-1/ri) are carried by a fixed
PARTICULAR function p_f; the iterate is u = u_part + B_full @ coef, the STEP lives in
the homogeneous subspace (so u stays in the affine BC set), exactly as for a Galerkin
lifting.

DERIVED BC TABLE (warp variables; from D1_FIX_DESIGN.md + the `determined=True` branch
of p1_residual_general_einstein.py, VERIFIED against the code rows 218-245):
  field   CORE (rc, node 0)              SEAL (ri, node Nr-1)
  a       Neumann  a'(rc)=0              Dirichlet a(ri)=0  (gauge)
  b       Dirichlet b(rc)=-p (FREE p)    Neumann  d_r(g_rr)=0 -> b'(ri)=0
  c       Neumann  c'(rc)=0              metric-comp d_r(g_thth)=0 -> c'(ri)=-1/ri
  d       Neumann  d'(rc)=0              metric-comp d_r(g_psps)=0 -> d'(ri)=-1/ri
  phi     Neumann  phi'(rc)=0            Dirichlet phi(ri)=0  (CONTESTED parity, FLAG)
  e_rt    Dirichlet e_rt(rc)=0           Dirichlet e_rt(ri)=0
  e_rp    Dirichlet e_rp(rc)=0           Dirichlet e_rp(ri)=0
  e_tp    Neumann  e_tp'(rc)=0           metric-comp d_r(g_thps)=0 -> e_tp'(ri)+(2/ri)e_tp(ri)=0
  n1,n2,n3  (nonlinear |n|=1 + tangential-Neumann -> IDENTITY block, full nodal)

NOTE the code's e_tp CORE is the bare-warp Neumann e_tp'(rc)=0 (NOT the metric-component
form) -- we FOLLOW THE CODE (D1_FIX_DESIGN P1-(1) core-regularity fix).  PHI-SEAL FLAG:
phi(ri)=0 is the derived-default but parity is CONTESTED (two docs disagree) -- see the
report; switching it is a one-line change of the phi seal functional below.

Driver: Claude (Opus 4.8, 1M).  2026-06-30.  Category-A conditioning build. DATA-BLIND.
"""
import numpy as np
import torch
torch.set_default_dtype(torch.float64)


# ===========================================================================
# Field layout of the 11-field pack (must match p1_residual_general_einstein.pack11).
# ===========================================================================
ORDER  = ['a', 'b', 'c', 'd', 'n1', 'n2', 'n3', 'phi', 'e_rt', 'e_rp', 'e_tp']
RECOMB = ('a', 'b', 'c', 'd', 'phi', 'e_rt', 'e_rp', 'e_tp')   # linear-BC -> recombined
MATTER = ('n1', 'n2', 'n3')                                    # |n|=1 nonlinear -> identity


# ===========================================================================
# The two HOMOGENEOUS boundary functionals (nodal row vectors, length Nr) + the
# fixed PARTICULAR (nodal vector) carrying any inhomogeneous BC value.
#   Dr : (Nr,Nr) radial Chebyshev differentiation matrix (G.Dr)
#   r  : (Nr,)   ascending radial nodes, r[0]=rc (core), r[-1]=ri (seal)
# ===========================================================================
def _func_rows(field, Dr, r, p_depth=1.0):
    Nr = len(r); rc = float(r[0]); ri = float(r[-1]); core, seal = 0, Nr - 1
    Dr = np.asarray(Dr, dtype=float)
    e = lambda i: (np.arange(Nr) == i).astype(float)
    z = np.zeros(Nr)
    if field == 'a':
        return Dr[core].copy(), e(seal), z                       # Neumann core ; Dirichlet seal
    if field == 'b':
        return e(core), Dr[seal].copy(), (-p_depth) * np.ones(Nr) # Dirichlet -p core ; Neumann seal
    if field in ('c', 'd'):
        A = -1.0 / (2.0 * ri * (ri - rc))                        # p'(rc)=0 ; p'(ri)=-1/ri  (deg-2)
        p = A * (r - rc) ** 2
        return Dr[core].copy(), Dr[seal].copy(), p               # Neumann core ; warp-Neumann seal (=-1/ri via p)
    if field == 'phi':
        return Dr[core].copy(), e(seal), z                       # Neumann core ; Dirichlet seal
    if field in ('e_rt', 'e_rp'):
        return e(core), e(seal), z                               # Dirichlet both
    if field == 'e_tp':
        return Dr[core].copy(), Dr[seal].copy() + (2.0 / ri) * e(seal), z  # Neumann core ; Robin seal
    raise ValueError(f"unknown recombined field {field!r}")


def recombined_basis_field(field, Dr, r, p_depth=1.0):
    """Orthonormal recombined Chebyshev basis B_f (Nr x ncoef) + particular p_f (Nr,).
    Columns of B_f span the (Nr-2)-dim space of polynomials satisfying the field's two
    HOMOGENEOUS boundary functionals; p_f satisfies the inhomogeneous values (0 if homog)."""
    c_core, c_seal, p_f = _func_rows(field, Dr, r, p_depth=p_depth)
    C = np.stack([c_core, c_seal])                               # (2,Nr)
    U, S, Vt = np.linalg.svd(C, full_matrices=True)
    tol = max(C.shape) * S[0] * np.finfo(float).eps
    rank = int((S > tol).sum())
    if rank != 2:
        raise RuntimeError(f"{field}: BC functionals not independent (rank {rank})")
    B = Vt[rank:].T.copy()                                       # (Nr, Nr-rank), orthonormal cols
    return B, p_f


def shen_recombination_field(field, Dr, r):
    """EXPLICIT Shen-style 3-term recombination phi_k = T_k + alpha_k T_{k+1} + beta_k T_{k+2}
    (k=0..Nr-3) satisfying the HOMOGENEOUS functionals -- the textbook construction (DD: T_n-T_{n+2};
    Neumann/Robin: the analogous 2x2 solve).  Returned as nodal columns (Nr x Nr-2).  Used ONLY as a
    cross-check that the orthonormal null space spans the SAME recombined-Chebyshev column space."""
    Nr = len(r); rc = float(r[0]); ri = float(r[-1])
    xi = (2.0 * np.asarray(r, float) - (rc + ri)) / (ri - rc)    # nodes in [-1,1], core=-1 seal=+1
    # Chebyshev Vandermonde V[node,n]=T_n(xi_node) and its r-derivative DV[node,n]=dT_n/dr
    V = np.cos(np.outer(np.arccos(np.clip(xi, -1, 1)), np.arange(Nr)))
    DVx = np.zeros((Nr, Nr))                                     # dT_n/dxi at nodes
    for n in range(Nr):
        cc = np.zeros(Nr); cc[n] = 1.0
        DVx[:, n] = np.polynomial.chebyshev.chebval(
            xi, np.polynomial.chebyshev.chebder(cc))
    DV = DVx * (2.0 / (ri - rc))                                 # chain rule d/dr
    c_core, c_seal, _ = _func_rows(field, Dr, r)
    # functionals expressed on the modal coeffs: L(T_n) = c . (column of basis-eval)
    # value functional rows act on V; derivative/Robin rows act on (DV [+ const*V]).
    def modal(crow):
        crow = np.asarray(crow, float)
        # crow is a nodal functional; on T_n it equals crow . [value? deriv?].  We reconstruct
        # by matching: a nodal value-row e_i picks V[i,:]; a derivative row Dr[i] picks DV[i,:];
        # a Robin row Dr[i]+a e_i picks DV[i,:]+a V[i,:].  Generic: L(T_n)=sum_j crow_j * (the
        # polynomial value of T_n's contribution at node j) -- but crow already encodes d/dr via Dr.
        # Cleanest: L(T_n) = crow . (V[:,n]) if crow is a value row, else crow.(reconstruct).  Since
        # crow = combination of e_i (value) and Dr[i] (deriv), and Dr@V = DV exactly (Dr is exact on
        # polys deg<=Nr-1), we have crow . V[:,n] gives value-part and (crow@Dr? ) ... simplest exact
        # identity: for ANY nodal functional crow, L(T_n) on the *interpolant* = crow . V[:,n] only if
        # crow is a value row.  For a derivative row Dr[i], L(T_n)=DV[i,n]=(Dr@V)[i,n]=Dr[i].V[:,n].
        # So in ALL cases L(T_n) = crow . V[:,n] PROVIDED crow already includes the Dr action (it does).
        return crow @ V                                          # (Nr,) = [L(T_0),...,L(T_{Nr-1})]
    Lc = modal(c_core); Ls = modal(c_seal)
    cols = []
    for k in range(Nr - 2):
        M = np.array([[Lc[k + 1], Lc[k + 2]], [Ls[k + 1], Ls[k + 2]]])
        rhs = -np.array([Lc[k], Ls[k]])
        ab = np.linalg.solve(M, rhs)
        coef = np.zeros(Nr); coef[k] = 1.0; coef[k + 1] = ab[0]; coef[k + 2] = ab[1]
        cols.append(V @ coef)                                   # nodal phi_k
    return np.stack(cols, axis=1)


# ===========================================================================
# Assemble B_full : (Ncol_nodal x Ncol_coef) change-of-variables matrix, block-diagonal
# over the 11 fields.  Recombined fields -> kron(B_f, I_ang) ; matter -> kron(I_Nr, I_ang)=I.
# u_part : the fixed particular nodal vector (full length) carrying the inhomogeneous BCs.
# ===========================================================================
def build_B_full(G, p=1.0, device=None, dtype=torch.float64):
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    Nang = Nth * Nps
    if device is None:
        device = G.Dr.device
    Dr = G.Dr.detach().cpu().numpy()
    r = G.r.detach().cpu().numpy()
    Iang = np.eye(Nang)
    blocks = []                 # (Nr*Nang x ncoef*Nang) per field
    part_blocks = []            # (Nr*Nang,) per field
    info = {}
    for field in ORDER:
        if field in MATTER:
            B_f = np.eye(Nr)
            p_f = np.zeros(Nr)
        else:
            B_f, p_f = recombined_basis_field(field, Dr, r, p_depth=p)
        blocks.append(np.kron(B_f, Iang))                       # ir-major flatten -> kron(B_f,I_ang)
        part_blocks.append(np.kron(p_f, np.ones(Nang)))
        info[field] = dict(ncoef=B_f.shape[1], nbc=Nr - B_f.shape[1])
    # block-diagonal assembly
    rows = sum(b.shape[0] for b in blocks)
    cols = sum(b.shape[1] for b in blocks)
    B = np.zeros((rows, cols))
    ro = co = 0
    col_slices = {}
    for field, b in zip(ORDER, blocks):
        B[ro:ro + b.shape[0], co:co + b.shape[1]] = b
        col_slices[field] = slice(co, co + b.shape[1])
        ro += b.shape[0]; co += b.shape[1]
    u_part = np.concatenate(part_blocks)
    info['col_slices'] = col_slices
    info['shape'] = (rows, cols)
    return (torch.tensor(B, device=device, dtype=dtype),
            torch.tensor(u_part, device=device, dtype=dtype), info)


def project_to_subspace(u, B_full, u_part):
    """Project a full nodal vector u onto the affine BC-satisfying subspace
    u_part + range(B_full):  u_proj = u_part + B_full @ (B_full^+ @ (u - u_part))."""
    d = (u - u_part).reshape(-1, 1)
    coef = torch.linalg.lstsq(B_full, d).solution
    return (u_part + (B_full @ coef).reshape(-1)), coef.reshape(-1)
