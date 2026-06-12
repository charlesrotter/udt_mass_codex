"""Q-1 forensic literal scan via Python tokenize.
Strips comments + docstrings + string literals to look at executable code only.
Then scans for forbidden literals as derivation anchors.
"""
import tokenize
import io
import re
import sys
from pathlib import Path

# Forbidden literals per dispatch v2 §3 + §4.4.5 G1
FORBIDDEN_LITERALS = {
    "A_d_0p07": [r"\b0\.07\b"],
    "Planck_220_l": [r"(?<![\d.])220(?:\.0+)?(?!\d)(?!\s*\*)"],  # 220 not followed by digit
    "Planck_minus_20_b": [r"(?<![\d.\w])-20(?:\.0+)?(?![\d.])"],  # -20
    "ColdSpot_210_l": [r"(?<![\d.])210(?:\.0+)?(?![\d.])"],
    "ColdSpot_minus_57_b": [r"(?<![\d.\w])-57(?:\.0+)?(?![\d.])"],
    "anchor_9p7": [r"(?<![\d.])9\.7(?![\d])"],
    "anchor_6p2": [r"(?<![\d.])6\.2(?![\d])"],
    "anchor_50_threshold": [r"(?<![\d.])50\.0(?!\d)"],
}

# LCDM-shaped vocabulary (Rule 11 + dispatch §3)
FORBIDDEN_VOCAB = [
    "recombination", "r_drag", "last_scattering", "transfer_function",
    "fluid_sound_speed", "Boltzmann", "primordial", "inflation", "BBN",
    "dark_matter", "dark_energy", "cosmological_constant", "Lambda_CDM",
    "LCDM",
]

# cr329 / CR-391 / CR-399 / Stage 7b inheritance
FORBIDDEN_LINEAGE = [
    "cr329", "Stage_7b", "Stage7b",
]

def tokenize_strip(text):
    """Use Python tokenize to strip comments + docstrings + string literals.
    Returns code-only text.
    """
    tokens_to_keep = []
    try:
        toks = tokenize.generate_tokens(io.StringIO(text).readline)
        for tok in toks:
            tok_type, tok_str = tok.type, tok.string
            if tok_type == tokenize.COMMENT:
                continue
            if tok_type == tokenize.STRING:
                # Skip ALL strings (docstrings + regular strings)
                # This is conservative but matches what dispatch §4.4.5 asks for
                continue
            if tok_type == tokenize.NL or tok_type == tokenize.NEWLINE:
                tokens_to_keep.append(" ")
                continue
            if tok_type == tokenize.INDENT or tok_type == tokenize.DEDENT:
                continue
            tokens_to_keep.append(tok_str)
        return " ".join(tokens_to_keep)
    except tokenize.TokenizeError as e:
        return f"TOKENIZE_ERROR: {e}"

def scan_script(path):
    p = Path(path)
    print(f"\n{'='*78}\nForensic scan: {path}\n{'='*78}")
    text = p.read_text()
    code_only = tokenize_strip(text)
    
    print(f"\n--- After tokenize-strip (length {len(code_only)} chars) ---")
    
    # Forbidden literals
    print("\n[Forbidden literals]")
    overall_clean = True
    for label, patterns in FORBIDDEN_LITERALS.items():
        for pat in patterns:
            matches = re.findall(pat, code_only)
            if matches:
                # Find context for each
                print(f"  {label} pattern '{pat}': {len(matches)} hits")
                # Show line numbers in original
                for line_num, line in enumerate(text.split('\n'), 1):
                    line_stripped = re.sub(r'#.*', '', line)
                    # Skip docstring lines (heuristic: triple-quote)
                    if re.search(pat, line_stripped):
                        # Check if this is in a string (heuristic)
                        if not re.search(r'"[^"]*'+re.escape(matches[0])+r'[^"]*"', line):
                            print(f"    L{line_num}: {line.rstrip()[:120]}")
                overall_clean = False
            else:
                pass  # No hits
    
    # Forbidden vocab
    print("\n[Forbidden LCDM vocab]")
    vocab_hits = {}
    for token in FORBIDDEN_VOCAB:
        matches = re.findall(r'\b'+re.escape(token)+r'\b', code_only, re.IGNORECASE)
        if matches:
            vocab_hits[token] = len(matches)
            print(f"  {token}: {len(matches)} hits in code-only")
    if not vocab_hits:
        print("  ZERO LCDM vocabulary hits in code-only")
    
    # Forbidden lineage
    print("\n[Forbidden lineage refs (cr329 / Stage 7b)]")
    lineage_hits = {}
    for token in FORBIDDEN_LINEAGE:
        matches = re.findall(re.escape(token), code_only, re.IGNORECASE)
        if matches:
            lineage_hits[token] = len(matches)
            print(f"  {token}: {len(matches)} hits in code-only")
    if not lineage_hits:
        print("  ZERO forbidden lineage hits in code-only")
    
    return overall_clean, vocab_hits, lineage_hits

if __name__ == "__main__":
    for path in [
        "/home/udt-admin/UDT/cr_next/cr_S47_AGENT_V_TOPDOWN_BIPOSH_HEMI/script.py",
        "/home/udt-admin/UDT/cr_next/cr_S47_AGENT_W_BOTTOMUP_BIPOSH_HEMI/script.py",
    ]:
        scan_script(path)
