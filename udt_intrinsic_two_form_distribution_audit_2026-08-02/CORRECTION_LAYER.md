# Post-bank wording correction — kernel dimension

Date: 2026-08-02  
Parent evidence commit: `04e1d9a9`

The first banked `AUDIT_REPORT.md` and the first navigation commit used the phrase
“four-dimensional kernel” once. The exact derivation, machine result, candidate atlas, verifier,
fresh cold review, and all algebra correctly gave:

```text
W != 0: ker(W)=span(T,N), dimension 2 inside the four-dimensional tangent space;
W  = 0: ker(W)=the full tangent space, dimension 4.
```

The report and LIVE wording are corrected to make that distinction explicit. No formula, atlas
row, candidate classification, cold-review result, or maximum conclusion changes. The parent Git
commit and its original package manifest remain historical evidence; the rebuilt current package
manifest and `PACKAGE_VERIFICATION.json` are the authoritative corrected package identities.
