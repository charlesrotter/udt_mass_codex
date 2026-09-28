"""Presentation/precision repair using saved outcomes only; no fitting."""
import os
for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[key] = "1"
os.environ.setdefault("MPLCONFIGDIR", "/tmp/udt_reviewed_bao_mpl")
import datetime
import hashlib
import json
from pathlib import Path
import resource
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent
out = root / "comparison_reviewed"
if out.exists():
    raise RuntimeError("Refuse to overwrite a preserved result directory")
out.mkdir()
result_path = root / "comparison_checked/RESULT.json"
fits_path = root.parent / "data/results/full_fits.json"
result = json.loads(result_path.read_text())
fits = json.loads(fits_path.read_text())
z = np.array(result["z"])
inside = np.array(result["within_sne_domain"], dtype=bool)
ratios = np.array(result["ratios"])
ratio_sigma = np.sqrt(np.diag(result["ratio_covariance"]))
zmax = 2.26137
fig, ax = plt.subplots(figsize=(10, 7.4))
ax.axvspan(zmax, 2.45, color="#eeeeee", label="Outside SNe range: extrapolation")
ax.errorbar(z[inside], ratios[inside], yerr=ratio_sigma[inside],
            fmt="o", color="black", capsize=3, zorder=10,
            label="DESI ratio: local 1-sigma measurement error")
ax.errorbar(z[~inside], ratios[~inside], yerr=ratio_sigma[~inside],
            fmt="s", mfc="none", color="black", capsize=3, zorder=10)
colors = ["#808080", "#d95f02", "#2166ac", "#a444a2", "#a6761d", "#1b9e77"]
labels = ["F0", "F1", "F2: compact empirical shape", "F3",
          "F4: diagnostic curve; uncertainty withheld", "F5: external flat-Lambda-CDM"]
for family, color, label in zip(fits, colors, labels):
    rows = [r for r in result["curves"] if r["family"] == family]
    zz = np.array([r["z"] for r in rows])
    vv = np.array([r["F_AP"] for r in rows])
    assert np.all(np.isfinite(vv))
    supported = zz <= zmax
    ax.plot(zz[supported], vv[supported], color=color,
            ls="--" if family == "F4" else "-", lw=1.6, label=label)
    # Include one neighboring point so the extrapolated segment joins visibly.
    start = max(0, int(np.flatnonzero(~supported)[0]) - 1)
    ax.plot(zz[start:], vv[start:], color=color, ls=":", lw=1.5)
f2 = result["models"]["F2"]
assert f2["local_gaussian_prediction_diagnostic_pass"]
pred = np.array(f2["prediction"])
pred_sigma = np.sqrt(np.diag(f2["prediction_covariance"]))
ax.errorbar(z[inside], pred[inside], yerr=pred_sigma[inside], fmt="s", ms=4,
            mfc="white", color=colors[2], capsize=4, zorder=11,
            label="F2: local 1-sigma coefficient error at checked points")
ax.set(xlabel="Redshift z", ylabel="D_M / D_H", xlim=(0, 2.45), ylim=(0, 6.5))
ax.grid(alpha=.18)
ax.legend(fontsize=8, loc="upper left")
ax.set_title("Conditional SNe-shape comparison with galaxy clustering\n"
             "Flat homogeneous geometry + conventional optics/ruler; no BAO retuning", fontsize=11)
fig.text(.08, .055, "No shaded confidence bands. F2 bars exclude family and systematic uncertainty;\n"
                   "pointwise bars do not display cross-redshift correlations. F4's linear uncertainty check failed.\n"
                   "Dotted tails are extrapolations; no extrapolated prediction uncertainty is claimed.", fontsize=9)
fig.tight_layout(rect=(0, .13, 1, 1))
fig.savefig(out / "bao_shape_comparison.png", dpi=180)
fig.savefig(out / "bao_shape_comparison.pdf")
plt.close(fig)
table = {}
for family, f in fits.items():
    table[family] = {"k": f["p"], "chi2": f["chi2"],
                     "AIC": f["chi2"] + 2*f["p"],
                     "conventional_AICc_heuristic": f["aicc_without_common_constant"],
                     "conventional_BIC_heuristic": f["bic_without_common_constant"]}
record = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "scope": "Presentation and complexity-statistic precision repair; saved fits/predictions unchanged",
          "complexity_scores_without_common_likelihood_constant": table,
          "qualification": "AIC +2k optimism is exact for fixed-known-covariance linear Gaussian mean F0-F4; F5 is asymptotic. Conventional AICc/BIC are reported heuristics, not established exact corrections/evidence here.",
          "input_sha256": {str(p.relative_to(root.parent)): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (Path(__file__), result_path, fits_path)}}
(out / "PRECISION_REPAIR.json").write_text(json.dumps(record, indent=2)+"\n")
print(json.dumps({"status": "saved without refit", "scores": table}, indent=2))
