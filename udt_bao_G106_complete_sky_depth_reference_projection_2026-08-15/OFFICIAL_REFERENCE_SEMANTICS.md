# Official BOSS random-reference semantics used by G106

Date checked: 2026-08-15

Primary documentation:

- <https://www.sdss4.org/dr17/spectro/lss/>
- <https://data.sdss.org/datamodel/files/BOSS_LSS_REDUX/randomN_DRX_SAMPLE_NS.html>

The SDSS documentation states that the random angular points sample the survey footprint with
density proportional to completeness. The DR12 random-catalog data model states that each random
`Z` is obtained by randomly drawing from the observed galaxy redshifts and provides `ZINDX`, the
index of the contributing galaxy.

G106 uses only the following idealized implication within each sample/cap stratum:

```text
q(zeta,n)=p_zeta(zeta) s(n),
integral_S2 s(n) dOmega=1.
```

Here `s` is the registered angular footprint/completeness reference and `p_zeta` is the observed
depth marginal represented by the random redshift draw. This does not assert exact finite-catalog
factorization, remove shot noise, or derive a physical UDT response. FKP and `NZ` remain excluded.
