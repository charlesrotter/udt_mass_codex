"""More targeted scan for paired (l, b) direction literals in code only."""
import tokenize
import io
import re
from pathlib import Path

def tokenize_strip(text):
    tokens_to_keep = []
    try:
        toks = tokenize.generate_tokens(io.StringIO(text).readline)
        for tok in toks:
            tok_type, tok_str = tok.type, tok.string
            if tok_type == tokenize.COMMENT:
                continue
            if tok_type == tokenize.STRING:
                continue
            if tok_type == tokenize.NL or tok_type == tokenize.NEWLINE:
                tokens_to_keep.append("\n")
                continue
            if tok_type == tokenize.INDENT or tok_type == tokenize.DEDENT:
                continue
            tokens_to_keep.append(tok_str)
        return " ".join(tokens_to_keep)
    except tokenize.TokenizeError as e:
        return f"TOKENIZE_ERROR: {e}"

# Paired (l, b) direction literal patterns - with the negative latitude pattern
# which would only appear if injected as direction
PAIRED_LITERAL_PATTERNS = [
    # (220, -20) Planck dipole
    (r"220[\s,]+\-20", "Planck dipole (220, -20)"),
    (r"220\.0[\s,]+\-20\.0", "Planck dipole (220.0, -20.0)"),
    # (210, -57) Cold Spot
    (r"210[\s,]+\-57", "Cold Spot (210, -57)"),
    (r"210\.0[\s,]+\-57\.0", "Cold Spot (210.0, -57.0)"),
    # 0.07 amplitude
    (r"\b0\.07\b", "A_d ~ 0.07"),
    # 9.7° as literal
    (r"\b9\.7\b", "9.7° literal"),
    # 6.2% as literal (would be 0.062)
    (r"\b6\.2\b", "6.2% literal"),
    (r"\b0\.062\b", "0.062 frac"),
    # 50° threshold literal
    (r"\b50\.0\b", "50.0 threshold"),
    # standalone -20 latitude
    (r"(?<![\d.])\-20\b(?![\d])", "-20 standalone"),
    (r"(?<![\d.])\-57\b(?![\d])", "-57 standalone"),
]

def scan(path):
    p = Path(path)
    print(f"\n--- {path} ---")
    text = p.read_text()
    code_only = tokenize_strip(text)
    
    for pat, label in PAIRED_LITERAL_PATTERNS:
        matches = list(re.finditer(pat, code_only))
        if matches:
            print(f"  HIT: {label} ({pat}) — {len(matches)} times")
            # Show context
            for m in matches[:5]:
                start = max(0, m.start() - 50)
                end = min(len(code_only), m.end() + 50)
                print(f"    Context: ...{code_only[start:end]}...")
        else:
            print(f"  CLEAN: {label}")

for path in [
    "/home/udt-admin/UDT/cr_next/cr_S47_AGENT_V_TOPDOWN_BIPOSH_HEMI/script.py",
    "/home/udt-admin/UDT/cr_next/cr_S47_AGENT_W_BOTTOMUP_BIPOSH_HEMI/script.py",
]:
    scan(path)
