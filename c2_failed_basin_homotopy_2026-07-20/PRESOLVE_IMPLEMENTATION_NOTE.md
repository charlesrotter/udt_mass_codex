# Presolve Implementation Note

Date: 2026-07-20

This note was committed before the official 51-path outcome was generated.  It records category-A
numerical implementation choices exposed by disposable `/tmp` software pilots; it does not change
the metric, action, homotopy equation, registered inputs, endpoint gates, or conclusion ceiling.

1. Four CPU worker processes will trace interleaved paths.  Each PyTorch worker is restricted to one
   thread.  This changes throughput only; paths share no numerical state.
2. The exact automatic-differentiation Hessian is refreshed every two accepted steps, stricter than
   the registered requirement of at least every eight.  Disposable pilots showed that an
   eight-step interval caused the arclength step to collapse while the corrector repaired stale
   secants.
3. The direct Bach implementation uses scalar forward automatic differentiation through the full
   coordinate Weyl divergence.  The fixed toric chart degenerates at the two primitive caps, whose
   physical completion is explicitly `OPEN_NOT_TESTED`.  Float64 evaluation of the exact round
   metric becomes cancellation-dominated inside about `0.02` radians of those coordinate caps.
   Therefore the registered *interior* 32/64-node Bach gate is evaluated on
   `[0.02, pi/2 - 0.02]`.  This is a bulk all-component gate only and cannot certify a boundary
   completion.  The `1e-6` raw component threshold is unchanged.
4. Disposable pilots are not part of the official census and cannot support a scientific verdict.
   They tested syntax, tensor cancellation, step refresh, and process isolation only.

If these controls still fail to trace a path, it remains unresolved.  No solver failure becomes a
no-branch statement.
