# M3 V-SNe RESULTS (prereg 523f4aca; all leads until blind results-verifier + Charles)

Anchor (mode B only): M_B = -19.253 +/- 0.027 (SH0ES ladder; F-ANCHOR premise travels with every absolute number).

## A:zCMB:P1
- chi2/dof = 1260.85/1365
- inv_n = 0.947 [0.9284, 0.9658]

## A:zCMB:P2
- chi2/dof = 4412.17/1366

## A:zCMB:P3
- chi2/dof = 4412.90/1365
- inv_alpha = 0.0001 [0.0001, 0.0002364] (ONE-SIDED OPEN interval, honestly marked)

## B:zCMB:P1
- chi2/dof = 1260.85/1365
- inv_n = 0.947 [0.9284, 0.9658]
- X_eff = 2086.0 Mpc [2059.1, 2113.2] (anchor premise attached; F-ANCHOR)
- R_w at best n: 2202.6 Mpc (pair-quote per D1; never marginal-only)

## B:zCMB:P2
- chi2/dof = 4412.17/1366
- X_eff = 1761.9 Mpc [1739.8, 1784.2] (anchor premise attached; F-ANCHOR)

## B:zCMB:P3
- chi2/dof = 4412.90/1365
- inv_alpha = 0.0001 [0.0001, 0.0002364] (ONE-SIDED OPEN interval, honestly marked)
- X_eff = 1761.8 Mpc [1739.8, 1784.2] (anchor premise attached; F-ANCHOR)

## C:zCMB:P1
- chi2/dof = 2281.47/1363
- inv_n = 0.9426 [0.9317, 0.9536]
- Tripp alpha=0.131 beta=2.676

## C:zCMB:P2
- chi2/dof = 8183.62/1364
- Tripp alpha=0.170 beta=3.159

## C:zCMB:P3
- chi2/dof = 8184.85/1363
- inv_alpha = 0.0001 [0.0001, 0.0001668] (ONE-SIDED OPEN interval, honestly marked)
- Tripp alpha=0.170 beta=3.159

## D:zCMB:P1
- chi2/dof = 1260.85/1365
- inv_n = 0.947 [0.9284, 0.9658]

## D:zCMB:P2
- chi2/dof = 4412.17/1366

## D:zCMB:P3
- chi2/dof = 4412.90/1365
- inv_alpha = 0.0001 [0.0001, 0.0002364] (ONE-SIDED OPEN interval, honestly marked)

## D:zHD:P1
- chi2/dof = 1246.59/1369
- inv_n = 0.9272 [0.9087, 0.9458]

## D:zHD:P2
- chi2/dof = 4296.69/1370

## D:zHD:P3
- chi2/dof = 4297.41/1369
- inv_alpha = 0.0001 [0.0001, 0.0002383] (ONE-SIDED OPEN interval, honestly marked)

## D:zHEL:P1
- chi2/dof = 1258.18/1362
- inv_n = 0.9468 [0.9281, 0.9656]

## D:zHEL:P2
- chi2/dof = 4399.35/1363

## D:zHEL:P3
- chi2/dof = 4400.08/1362
- inv_alpha = 0.0001 [0.0001, 0.0002368] (ONE-SIDED OPEN interval, honestly marked)

## Headline sensitivity deliverables (prereg SS3)
```json
{
 "C_minus_A_shape": {
  "P1": {
   "A": 0.9470295666076658,
   "C": 0.9426452288556275,
   "abs_shift": 0.004384337752038281,
   "note": "quantified BBC-contamination estimate (prereg SS3); also the point-of-use note on the banked 0.91"
  },
  "P3": {
   "A": 0.0001,
   "C": 0.0001,
   "abs_shift": 0.0,
   "note": "quantified BBC-contamination estimate (prereg SS3); also the point-of-use note on the banked 0.91"
  }
 },
 "D_shifts_shape": {
  "P1": {
   "zHD": {
    "zCMB": 0.9470295666076658,
    "zHD": 0.9272079586981833,
    "abs_shift": 0.019821607909482508
   },
   "zHEL": {
    "zCMB": 0.9470295666076658,
    "zHEL": 0.9468253612518177,
    "abs_shift": 0.00020420535584808608
   }
  },
  "P3": {
   "zHD": {
    "zCMB": 0.0001,
    "zHD": 0.0001,
    "abs_shift": 0.0
   },
   "zHEL": {
    "zCMB": 0.0001,
    "zHEL": 0.0001,
    "abs_shift": 0.0
   }
  }
 }
}
```