# External G286 adversarial review — gpt-5.4

## Findings

- Medium: the package-level verifier is not a true replay verifier. `verify_package.py` only checks
  for bundled files and reads preexisting `DERIVATION_RESULT.json` and
  `INDEPENDENT_VERIFICATION.json`; it does not rerun the preregistered computations. This is an
  evidence-packaging issue, not a scientific refutation, but it needs repair.
- Low: the numerical artifact labels overstate what is mechanized. The production script proves
  only sampled prior zeros and a sampled future nonzero tide. The exact whole-region and all-jet
  statements are carried by the analytic derivation and must be labelled that way.
- Low: the main landing speaks in `L2`/`L3` terms even though G285 is noncanon and provisional.
  The science remains supportable if restated in G283-native metric/curvature language first.

## Verdict

`ACCEPT-WITH-REPAIRS`

The bounded scientific landing is valid. On the frozen smooth G283 family, the witnesses
`T0=0` and `T1=(1/5)b(u)diag(1,-1)` are both smooth symmetric histories. They agree on the
entire `u<=0` metric region and have identical joining-surface jets because the switch is flat at
`u=0`. Both are admitted by the inherited compatibility, Cartan, Jacobi, and carry layers.

Future curvature is a sufficient geometric separator: one witness has vanishing Riemann everywhere
while the other has nonzero `R_uiuj=T_ij` for every `u>0` on the central null relation. That is
enough to show the current owned identity/evaluator layer does not uniquely propagate this witness.

The null-join caveat is handled correctly. G286 does not support a stronger claim about hypothetical
future Cauchy or characteristic laws and does not justify “no native UDT law can exist.” The premise
ledger is clean on hidden imports: no field equation, observation, scale, source, action, or
`X_max` is brought in.

The reviewer replayed the registered package in a writable ephemeral copy. RK4 gave symplectic
defect `1.4210854715202004e-14`, implicit midpoint gave `6.721290191080698e-13`, the cross-method
difference was `3.866140740882429e-11`, and active-versus-flat transfer difference was
`3.2701305e-2`. These are corroborative; the analytic curvature split carries the conclusion.

## Required repairs

1. Make `verify_package.py` execute the registered derivation and independent verification itself,
   or compare explicitly supplied fresh replay outputs. It must not accept bundled JSON on trust.
2. Restate the primary landing in G283-native language first: the same whole prior metric region plus
   identical join jets admit geometrically inequivalent future continuations. Keep `L2`/`L3`
   language explicitly secondary and provisional under G285.
3. Rename or annotate sampled production fields so they cannot be read as proofs of whole-region or
   all-jet equality; those are analytic claims.
