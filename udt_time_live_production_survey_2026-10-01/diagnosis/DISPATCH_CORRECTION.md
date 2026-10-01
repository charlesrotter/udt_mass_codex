# Prelaunch resource-prose correction

Both separate reviewers found that the first dispatch description incorrectly
called N32’s inherited per-case cap512MiB. Actual original and generated N32
specs use256MiB. The original dispatch, manifest and case map are preserved
in initial_dispatch/. Before any GPU launch, corrected the prose and rebound
only the dispatch source hash and resulting manifest hash. No spec, equation,
threshold, initial field, time control or output cap changed. Actual total
per-case caps are6.5GiB; compressed output remains required on N32, with the
unchanged resource stop. The first9.75GiB estimate was conservative, but its
description as the actual sum was wrong.
