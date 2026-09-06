# Bounded review of preserved pre-freeze parser defect

Question: did the one-line alias correction preserve the registered nonconstant weight?
Read the original script, corrected script and retained failure. Run one exact parser check and
retain their exact diff. This checks syntax/representation only; no omitted physical sector,
equation, numerical tolerance, support or free variable is changed. CPU, 60 seconds and 512 MiB.
Stop after the direct equivalence/failure checks; failure would require reporting a precise
implementation objection. Maximum conclusion: preserved parser-only repair, not scientific repair.

The earlier direct diff exited 1 because a difference exists; its chained second read therefore
did not execute. No diagnostic evidence was overwritten. The retained rerun records that expected
diff exit separately. Original script execution is not claimed from its archived diagnostics
location, where its neighboring input path would differ.
