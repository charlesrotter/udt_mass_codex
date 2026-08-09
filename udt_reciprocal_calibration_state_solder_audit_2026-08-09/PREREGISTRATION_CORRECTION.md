# Preregistration correction — TSV serialization

Date: 2026-08-09  
Preregistration commit: `2dfd71ff`  
Original `SOURCE_MANIFEST.tsv` SHA-256: `c761ebdf9ba8b65ee00e9beb1f1c1af199de626720a91d38ceb70360d855c6c3`
Corrected `SOURCE_MANIFEST.tsv` SHA-256: `117a5de325a66173b3cb8fa8128fc725497f54dbc221cb306e43494550b16545`

The preregistered manifest stored the two visible characters `\\t` instead of actual tab bytes.
The first controller replay therefore failed closed before reading any source row.

This correction changes only the field separators from literal `\\t` text to tab bytes. The header,
24 source paths, 24 SHA-256 values, order, audit question, gates, and conclusion ceiling are unchanged.
The same mechanical correction is applied to newly generated TSV ledgers before their first
successful use. No candidate classification or scientific result is changed by this correction.
