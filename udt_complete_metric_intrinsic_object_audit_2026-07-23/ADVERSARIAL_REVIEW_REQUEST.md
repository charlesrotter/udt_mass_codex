# Fresh adversarial review request

Use a fresh zero-context instance. Do not modify any repository file.

Review
`udt_complete_metric_intrinsic_object_audit_2026-07-23/` from the exact
`grok` checkout. Follow repository startup instructions, then independently
audit the package rather than trusting its report.

Required challenges:

1. Re-derive from scratch whether, for
   `alpha=dphi`, `v=alpha sharp`, and
   `P=v tensor alpha/g^-1(alpha,alpha)`, the induced map
   `Pi(F)(X,Y)=F(PX,Y)+F(X,PY)` is a real rank-three projector on
   two-forms for both timelike and spacelike nonnull `alpha`.
2. Check whether four-dimensional Lorentzian Hodge duality exchanges that
   projector with its complement, including every sign and orientation
   convention needed for the claim.
3. Check whether
   `D=e^phi Pi+e^-phi(I-Pi)` is real, frame-independent, CSN invariant, and
   satisfies `star D star^-1=D^-1`.
4. Try to continue the construction through null and zero `dphi`; verify or
   refute the claimed nilpotent degeneration and global obstruction.
5. Independently audit the metric-only statement that the real Lorentz
   commutant on `Lambda2` is spanned by `I` and `star`, and that the complex
   chiral reciprocal construction fails real descent.
6. Try to find any overlooked intrinsic section, reduction, holonomy
   reduction, characteristic class, or Hopf invariant within the declared
   registered scope.
7. Challenge every status boundary: derived local geometry versus compatible
   reciprocal action, metric-only versus `(g,phi)`-assisted, local versus
   global, `S2` fiber versus section, primary class versus Hopf secondary
   invariant, and exact conditional toric data versus native selection.
8. Re-run the production and independent scripts; inspect whether the
   standard-library verifier is actually independent and whether all mutation
   catches exercise the load-bearing claims.
9. Check the 58-source manifest, 30-row census, 33 production checks,
   24 independent checks, 20 catches, and the documented `70 passed,
   1 xfailed` baseline.
10. Identify any overclaim, missing premise, sign error, type mismatch,
    circular verification, or untested global inference.

Return `PASS`, `PASS-WITH-CAVEATS`, or `REFUTED`, followed by exact findings
and required corrections. Distinguish a correction required for the banked
claim from an optional future extension.
