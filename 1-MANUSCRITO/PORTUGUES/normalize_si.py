#!/usr/bin/env python3
"""
normalize_si.py

Converte separadores decimais de vírgula para ponto e formata números com 3 casas decimais
em um arquivo Markdown, preservando blocos de código, trechos inline de código, equações
em LaTeX ($...$ / $$...$$), URLs e DOIs.

Uso: python normalize_si.py modelar_LC_K.md
Cria backup `modelar_LC_K.md.bak` e escreve o arquivo modificado.
Gera um relatório simples no stdout com amostras antes/depois.
"""
import argparse
import re
import sys
from pathlib import Path


EXCLUDE_PATTERNS = [
    re.compile(r"```[\s\S]*?```"),      # fenced code blocks
    re.compile(r"\$\$[\s\S]*?\$\$"), # display math
    re.compile(r"\$[^$\n]+\$"),         # inline math (simple)
    re.compile(r"`[^`]*`"),                # inline code
    re.compile(r"https?://[^)\s]+"),      # URLs
    re.compile(r"doi:\s*[^)\s]+", re.IGNORECASE), # DOI
]


def build_mask(text):
    mask = [True] * len(text)
    for pat in EXCLUDE_PATTERNS:
        for m in pat.finditer(text):
            for i in range(m.start(), m.end()):
                mask[i] = False
    return mask


NUMBER_RE = re.compile(r"\d+[.,]\d+")


def normalize_number(s: str, sigfigs: int = 3) -> str:
    """Convert number string to float and format with 3 decimal places.

    Handles cases like '1.234,56' (thousands '.' and decimal ',') and
    '1234,56' or '1234.56'.
    """
    orig = s
    if "." in s and "," in s:
        # assume '.' is thousands separator and ',' decimal
        s = s.replace('.', '').replace(',', '.')
    elif "," in s:
        s = s.replace(',', '.')
    # else keep '.' as decimal
    try:
        val = float(s)
    except ValueError:
        return orig
    # Use scientific notation for very small magnitudes, otherwise fixed 3 decimals
    if val != 0 and abs(val) < 0.001:
        # use uppercase 'E' and configurable significant figures, e.g., 6.200E-04
        fmt = f"{{val:.{sigfigs}E}}"
        return fmt.format(val=val)
    return f"{val:.3f}"


def process_text(text: str, sigfigs: int = 3):
    mask = build_mask(text)
    out = []
    last = 0
    replacements = []

    for m in NUMBER_RE.finditer(text):
        i, j = m.start(), m.end()
        if not all(mask[k] for k in range(i, j)):
            continue
        num_text = m.group(0)
        new_num = normalize_number(num_text, sigfigs=sigfigs)
        if new_num != num_text:
            replacements.append((num_text, new_num, i))
    # apply replacements from end to start to not invalidate indices
    res = text
    for old, new, pos in reversed(replacements):
        # replace only at the specific position to avoid accidental other matches
        before = res[:pos]
        after = res[pos:]
        assert after.startswith(old)
        res = before + new + after[len(old):]
    # Additionally, normalize lowercase scientific 'e' to uppercase 'E'
    # but only when appearing between digits (to avoid altering words)
    sci_lower_re = re.compile(r"(\d\.\d+)[eE]([+-]?\d+)")
    sci_changes = []
    for m in sci_lower_re.finditer(res):
        old = m.group(0)
        exp = int(m.group(2))
        sign = '+' if exp >= 0 else '-'
        new = f"{m.group(1)}E{sign}{abs(exp):02d}"
        sci_changes.append((old, new, m.start()))
    if sci_changes:
        def _upper_e(m):
            exp = int(m.group(2))
            sign = '+' if exp >= 0 else '-'
            return f"{m.group(1)}E{sign}{abs(exp):02d}"
        res = sci_lower_re.sub(_upper_e, res)
    return res, replacements + sci_changes


def main():
    p = argparse.ArgumentParser(description='Normalize decimals to SI style in a Markdown file')
    p.add_argument('file', help='Markdown file to process')
    p.add_argument('--sigfigs', type=int, default=3, help='significant figures for scientific notation (default 3)')
    args = p.parse_args()
    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)
    text = path.read_text(encoding='utf-8')
    backup = path.with_suffix(path.suffix + '.bak')
    backup.write_text(text, encoding='utf-8')
    new_text, replacements = process_text(text, sigfigs=args.sigfigs)
    if replacements:
        path.write_text(new_text, encoding='utf-8')
        print(f"Arquivo processado: {path}\nBackup criado: {backup}\nReplacos realizados: {len(replacements)}\nAmostras (antes -> depois):")
        for old, new, pos in replacements[:50]:
            print(f"  {old} -> {new}")
    else:
        print("Nenhuma substituição necessária.")


if __name__ == '__main__':
    main()
