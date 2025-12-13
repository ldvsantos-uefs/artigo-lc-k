#!/usr/bin/env python3
"""
Importador de dados de tração (TABOA / GEOTÊXTIL-NaOH).
Gera um CSV combinado em `../processed_data/tracao_taboa_combined.csv`.

Comportamento:
- Procura recursivamente por arquivos em `../raw_imports`.
- Tenta ler com separador `;` e decimal `,` (fallbacks implementados).
- Extrai metadata (treatment, days, specimen) do nome do arquivo.
- Normaliza colunas para `strain` e `stress` quando possível.
"""
import re
import sys
from pathlib import Path
import warnings

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "raw_imports"
OUT_DIR = ROOT / "processed_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "tracao_taboa_combined.csv"

COL_CANDIDATES_STRAIN = [r'deform', r'exten', r'strain']
COL_CANDIDATES_STRESS = [r'esforc', r'tens', r'forc', r'carga', r'stress']


def find_column(columns, candidates):
    cols = [c for c in columns]
    for pat in candidates:
        for c in cols:
            if re.search(pat, c, re.IGNORECASE):
                return c
    return None


def try_read(filepath: Path):
    # Attempt Excel first for .xls/.xlsx
    suffix = filepath.suffix.lower()
    if suffix in ('.xls', '.xlsx'):
        try:
            return pd.read_excel(filepath)
        except Exception as e:
            warnings.warn(f"Falha ao ler Excel {filepath}: {e}")

    # Try to detect header row in text files (many files contain metadata before the CSV header)
    encodings = ['utf-8', 'latin1', 'cp1252']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc, errors='replace') as f:
                lines = [next(f) for _ in range(200)]
        except StopIteration:
            # file shorter than 200 lines
            with open(filepath, 'r', encoding=enc, errors='replace') as f:
                lines = f.readlines()
        except Exception:
            continue

        header_idx = None
        for i, L in enumerate(lines):
            if re.search(r'\bTempo\b', L, re.IGNORECASE) and re.search(r'\bExten|Deform|Esforc|Carga|Strain\b', L, re.IGNORECASE):
                header_idx = i
                break

        if header_idx is not None:
            try:
                df = pd.read_csv(filepath, sep=';', decimal=',', header=header_idx, encoding=enc, engine='python')
                return df
            except Exception:
                # fallthrough to generic attempts
                pass

    # Generic fallback attempts
    seps = [';', ',', '\t']
    for enc in encodings:
        for sep in seps:
            try:
                df = pd.read_csv(filepath, sep=sep, decimal=',' if sep == ';' else '.', encoding=enc, engine='python')
                return df
            except Exception:
                continue

    # last resort: try whitespace split utf-8
    try:
        df = pd.read_csv(filepath, sep='\s+', engine='python', encoding='utf-8')
        return df
    except Exception as e:
        warnings.warn(f"Não foi possível ler {filepath}: {e}")
        return None


def extract_meta(filepath: Path):
    rel = str(filepath.relative_to(RAW_DIR))
    # days: search in the full relative path for '30 DIAS' or '30DIAS' etc
    mday = re.search(r'(\d{1,3})\s*DIAS', rel, re.IGNORECASE)
    if not mday:
        mday = re.search(r'(\d{1,3})DIAS', rel, re.IGNORECASE)
    days = int(mday.group(1)) if mday else None

    # treatment: search for T0/T1/T2/T3/TE anywhere in path or filename
    mt = re.search(r'\bT([0-3E])\b', rel)
    treatment = None
    if mt:
        treatment = 'T' + mt.group(1)
    else:
        m2 = re.search(r'-T([0-3E])[-_]', rel)
        if m2:
            treatment = 'T' + m2.group(1)

    # specimen: try to get a specimen id from filename or parent folder
    name = filepath.name
    ms = re.search(r'Specimen[_-]?(\w+)|_(S\d+)|spec[_-]?(\w+)', name, re.IGNORECASE)
    specimen = None
    if ms:
        for g in ms.groups():
            if g:
                specimen = g
                break
    if specimen is None:
        # try parent folder name
        parent = filepath.parent.name
        if parent and parent.strip():
            specimen = re.sub(r'[^A-Za-z0-9\-_]', '_', parent)

    if specimen is None:
        specimen = re.sub(r'[^A-Za-z0-9\-_]', '_', name)

    return days, treatment, specimen


def normalize_df(df: pd.DataFrame, filepath: Path):
    df = df.copy()
    cols = list(df.columns)
    col_strain = find_column(cols, COL_CANDIDATES_STRAIN)
    col_stress = find_column(cols, COL_CANDIDATES_STRESS)

    # If found, rename
    if col_strain:
        df = df.rename(columns={col_strain: 'strain'})
    if col_stress:
        df = df.rename(columns={col_stress: 'stress'})

    # If values are strings with comma decimals, convert
    for c in df.columns:
        if df[c].dtype == object:
            # try to coerce with comma replacement
            sample = df[c].dropna().astype(str).head(10)
            if sample.str.contains(',').any():
                try:
                    df[c] = df[c].astype(str).str.replace(',', '.').astype(float)
                except Exception:
                    pass
    return df


def main():
    all_rows = []
    files = list(RAW_DIR.rglob('*'))
    files = [f for f in files if f.is_file()]
    print(f"Arquivos encontrados em raw_imports: {len(files)}")
    for f in files:
        df = try_read(f)
        if df is None:
            continue
        days, treatment, specimen = extract_meta(f)
        df = normalize_df(df, f)

        # Identify strain and stress columns
        if 'strain' not in df.columns or 'stress' not in df.columns:
            # try to find numeric columns heuristically
            numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
            if len(numeric_cols) >= 2:
                # assume first numeric is strain, second stress
                if 'strain' not in df.columns:
                    df = df.rename(columns={numeric_cols[0]: 'strain'})
                if 'stress' not in df.columns:
                    df = df.rename(columns={numeric_cols[1]: 'stress'})
            else:
                print(f"Pulando {f} — colunas strain/stress não identificadas")
                continue

        # keep only needed columns
        out = df[['strain', 'stress']].copy()
        out['treatment'] = treatment
        out['days'] = days
        out['specimen'] = specimen
        out['source_file'] = str(f.relative_to(RAW_DIR))
        # drop NaNs
        out = out.dropna(subset=['strain', 'stress'])
        all_rows.append(out)

    if not all_rows:
        print("Nenhum dado válido encontrado para consolidar.")
        return

    combined = pd.concat(all_rows, ignore_index=True)
    combined.to_csv(OUT_FILE, index=False)
    print(f"Arquivo combinado salvo em: {OUT_FILE} — linhas: {len(combined)}")


if __name__ == '__main__':
    main()
