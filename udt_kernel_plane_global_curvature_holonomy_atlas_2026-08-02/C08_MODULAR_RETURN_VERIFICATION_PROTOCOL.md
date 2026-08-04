# C08 modular-return independent verification protocol

Date: 2026-08-03
Status: post-return protocol, frozen before verification

## Disclosed machine return

The production driver returned in about ten seconds and reported an exactness-one modular basis
with `verifyGB=1`, six zero input reductions, algebraic dimension zero, quotient dimension 124, and
nine basis elements. These values are disclosed before this verification and are not themselves
accepted by this protocol.

The post-return artifacts are frozen for this verification by these SHA-256 values:

```text
production input   8079b60cbe573ffefe0557a92b0c35f35b2e6a6a413bc26c5f99a85fc7c96ec0
production stdout  a785441f0bb6fc5bb8f631861a84336660f8508e729780a6e40459868070479b
production stderr  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
resource monitor   1626a6e646e179d3602c4b19c577c9a9352dcc044affb833075af99a44edda1e
process record     139b9789d31ba2ad903d8d770644d5483374ba9cc0f6dc2860f6ce67fd8cbb62
```

## Adversarial question

Does the saved basis independently satisfy all algebra needed to be an exact basis of the unchanged
six-generator ideal, or did the production path admit a false pass, parse error, strict containing
ideal, ordering mismatch, or corrupted artifact?

## Independent checks

The verifier must not import production functions. It must reconstruct the six generators directly
from the committed `A_i,B_i` files and parse the returned basis directly from raw stdout.

1. Recompute all 36 Buchberger S-polynomial reductions over `QQ[z,y]` in SymPy with graded reverse
   lexicographic order. Every remainder must vanish.
2. Reduce all six original generators by the returned basis in SymPy. Every remainder must vanish.
3. Derive the quotient dimension independently from the returned leading-monomial ideal, including
   explicit pure-power bounds and a complete standard-monomial count.
4. In a separate one-CPU Singular invocation, compute `lift(I,G)` and require the exact matrix
   identity `matrix(I)*lift(I,G)=matrix(G)`. This tests the otherwise missing containment
   `<G> subset <I>`; `verifyGB(G)` and input reduction alone do not establish it.
5. Recheck `verifyGB`, dimension, quotient dimension, basis size, and all six input reductions in
   that separate invocation.
6. Exercise a mutation catch by dropping one returned basis element and require at least one
   independent algebraic gate to fail.

The Singular lift is resource-bounded to one CPU, 48 GiB address space, and 1,800 seconds. A timeout,
resource failure, parse ambiguity, nonzero remainder, failed lift identity, or mutation false pass
returns `OPEN_VERIFICATION_INCOMPLETE` or `REFUTED_MACHINE_RETURN`, never a repaired result.

## Maximum conclusion

Passing this protocol independently verifies the saved rational ideal basis and its algebraic
dimension. It does not classify its real roots, complete the three nonzero-A charts, or prove the
global C08 curvature zero set. Fresh cold adversarial review remains required before a final package
verdict. No physical conclusion follows.

## Pre-algebra parser correction

The first verifier invocation stopped before any algebraic check because Singular prints compact
monomials such as `z13` and `z11y2`, while the independent SymPy parser initially expected explicit
powers. The correction expands only this documented output syntax (`z13 -> z**13`,
`z11y2 -> z**11*y**2`). Production hashes, equations, basis text, expected algebraic values, and
acceptance gates remain unchanged. The failed invocation supplies no mathematical outcome.

The second invocation completed the independent SymPy branch: 36/36 S-polynomial reductions and
6/6 source reductions vanished, the leading ideal supplied 124 standard monomials, and dropping one
basis element triggered 15 Buchberger plus six source-reduction failures. Its separate Singular
input, however, serialized rational coefficients after monomials (`z^11/224`). Singular rejects
that syntax, so `G` was undefined and the later displayed zero lift count was vacuous. The
internal-error gate correctly rejected the run. The correction emits every rational coefficient
first (`1/224*z^11`) without changing any polynomial. That failed Singular branch supplies no lift
or ideal-containment outcome; the already completed SymPy observations remain provisional until the
whole protocol passes.

The corrected third invocation retained every SymPy pass but reached the registered 1,800-second
timeout inside `lift(I,G)` without returning a reverse-containment matrix. Its separate Singular
path did return `verifyGB(G)=1` before the lift. The six source-reduction calls also printed
"G is no standard basis" because the independently reconstructed and verified basis had not been
tagged `isSB`; those displayed zeros are therefore not credited. Future replay code sets that
internal tag only after `verifyGB=1`. No automatic fourth replay is authorized by this correction.
The current status is `OPEN_VERIFICATION_INCOMPLETE`: the exact reverse containment and fresh cold
review remain absent.
