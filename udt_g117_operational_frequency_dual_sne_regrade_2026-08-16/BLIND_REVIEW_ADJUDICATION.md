# G117 blind review adjudication

Fresh zero-context verdict: `VERIFIED_WITH_CAVEATS`.

The reviewer independently parsed both raw releases, reconstructed the P1 equivalence, used the DES
Schur-complement marginal precision, and checked the exact rational G116 witness. It reproduced:

- Pantheon+ `chi2=1260.8480887274916`, offset `22.34352850161709`;
- DES `chi2=1444.1864417504914`, offset `41.70895660296955`, lower-tail `p=0.0006144042`;
- wrong DES precision subblock `chi2=1451.0553337714514`;
- exact `Delta=337/1680000`, `phi_live=50063/1680000`, `phi_live+Delta=3/100`.

Required repairs were semantic and evidentiary: conditional release-coordinate typing, local-only
use of G116, interface-scoped non-identifiability, explicit G94 regrade, Pantheon dof provenance,
and separation of related-lineage regression evidence from the blind independent replay. All are
registered in `CORRECTION_RECORD.md`.
