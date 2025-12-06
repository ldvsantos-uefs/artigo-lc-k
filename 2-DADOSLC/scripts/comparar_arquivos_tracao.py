#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISE COMPARATIVA: TODOS OS ARQUIVOS DE TRAÇÃO
Objetivo: Identificar qual arquivo contém os dados corretos
"""

import pandas as pd
import numpy as np

print("="*100)
print("ANÁLISE COMPARATIVA: TODOS OS ARQUIVOS DE TRAÇÃO")
print("="*100)

# 1. TABELA-TRAÇÃO (Recuperado).xlsx - Original
print("\n1. TABELA-TRAÇÃO (Recuperado).xlsx - ARQUIVO ORIGINAL (raw_imports)")
print("-"*100)
df_orig = pd.read_excel('2-DADOSLC/raw_imports/TABOA/TABELA-TRAÇÃO (Recuperado).xlsx', sheet_name='Planilha1')
df_orig = df_orig[df_orig['TRATAMENTO'].isin([0.0, 0.03, 0.06, 0.09])].copy()
trat_map = {0.0: 'T0', 0.03: 'T1', 0.06: 'T2', 0.09: 'T3'}
df_orig['TRAT'] = df_orig['TRATAMENTO'].map(trat_map)

print("\nESTATÍSTICAS POR PERÍODO:")
for dias in sorted(df_orig['DIAS'].unique()):
    print(f"\n  {int(dias)} DIAS:")
    df_dia = df_orig[df_orig['DIAS'] == dias]
    for trat in ['T0', 'T1', 'T2', 'T3']:
        df_t = df_dia[df_dia['TRAT'] == trat]
        if len(df_t) > 0:
            s = df_t['ESFORÇO À TRAÇÃO (MPa)'].values
            e = df_t['DEFORMAÇÃO'].values
            print(f"    {trat}: stress={s.mean():.2f}±{s.std():.2f} MPa, strain={e.mean():.4f}±{e.std():.4f}, n={len(df_t)}")

# 2. Dados completo.xlsx
print("\n\n2. Dados completo.xlsx - ARQUIVO NA PASTA /TRACAO")
print("-"*100)
try:
    df_xlsx = pd.read_excel('2-DADOSLC/tracao/Dados completo.xlsx')
    print(f"Shape: {df_xlsx.shape}")
    print(f"Colunas: {df_xlsx.columns.tolist()}")
    
    # Tentar extrair dados
    if 'TRATAMENTO' in df_xlsx.columns:
        print(f"Valores de TRATAMENTO: {sorted(df_xlsx['TRATAMENTO'].unique())}")
        
        # Procurar coluna de stress
        stress_col = None
        for col in df_xlsx.columns:
            if 'stress' in col.lower() or 'esforço' in col.lower() or 'tração' in col.lower():
                stress_col = col
                break
        
        print(f"Coluna de stress encontrada: {stress_col}")
        
        if stress_col:
            print(f"\nPrimeiras linhas com stress:")
            print(df_xlsx[[c for c in df_xlsx.columns if c in ['TRATAMENTO', 'DIAS', stress_col, 'Deformação']]].head(10))
except Exception as e:
    print(f"ERRO: {e}")

# 3. Dados completos.sav (SPSS)
print("\n\n3. Dados completos.sav - ARQUIVO SPSS NA PASTA /TRACAO")
print("-"*100)
try:
    import pyreadstat
    df_sav, _ = pyreadstat.read_sav('2-DADOSLC/tracao/Dados completos.sav')
    df_sav_f = df_sav[df_sav['TRATAMENTO'].isin([0.0, 3.0, 6.0, 9.0])].copy()
    
    print(f"Shape original: {df_sav.shape}")
    print(f"Dados NaOH extraídos: {len(df_sav_f)} linhas")
    print(f"Períodos: {sorted(df_sav_f['DIAS'].unique())}")
    
    for dias in [30.0, 90.0]:
        print(f"\n  {int(dias)} DIAS:")
        df_d = df_sav_f[df_sav_f['DIAS'] == dias]
        for t in [0.0, 3.0, 6.0, 9.0]:
            df_t = df_d[df_d['TRATAMENTO'] == t]
            if len(df_t) > 0:
                trat_label = {0.0: 'T0', 3.0: 'T1', 6.0: 'T2', 9.0: 'T3'}[t]
                s = df_t['ESFORÇOÀTRAÇÃOMPa'].values
                e = df_t['Deformação'].values
                print(f"    {trat_label}: stress={s.mean():.2f}±{s.std():.2f} MPa, strain={e.mean():.4f}±{e.std():.4f}, n={len(df_t)}")
except Exception as e:
    print(f"ERRO: {e}")

# 4. RESUMO COMPARATIVO
print("\n\n" + "="*100)
print("RESUMO COMPARATIVO - QUAL ARQUIVO ESTÁ CORRETO?")
print("="*100)

print("\n30 DIAS - T3 (9% NaOH):")
print(f"  TABELA-TRAÇÃO.xlsx (Original):  {df_orig[df_orig['DIAS']==30][df_orig['TRAT']=='T3']['ESFORÇO À TRAÇÃO (MPa)'].mean():.2f} MPa")

try:
    import pyreadstat
    df_sav, _ = pyreadstat.read_sav('2-DADOSLC/tracao/Dados completos.sav')
    df_sav_f = df_sav[df_sav['TRATAMENTO'].isin([0.0, 3.0, 6.0, 9.0])].copy()
    val_spss = df_sav_f[(df_sav_f['DIAS']==30) & (df_sav_f['TRATAMENTO']==9.0)]['ESFORÇOÀTRAÇÃOMPa'].mean()
    print(f"  Dados completos.sav (SPSS):     {val_spss:.2f} MPa")
except:
    pass

print("\n90 DIAS - T3 (9% NaOH):")
print(f"  TABELA-TRAÇÃO.xlsx (Original):  {df_orig[df_orig['DIAS']==90][df_orig['TRAT']=='T3']['ESFORÇO À TRAÇÃO (MPa)'].mean():.2f} MPa")

try:
    val_spss = df_sav_f[(df_sav_f['DIAS']==90) & (df_sav_f['TRATAMENTO']==9.0)]['ESFORÇOÀTRAÇÃOMPa'].mean()
    print(f"  Dados completos.sav (SPSS):     {val_spss:.2f} MPa")
except:
    pass

print("\n\nCONCLUSÃO:")
print("-"*100)
print("Os dois arquivos (Excel original e SPSS) devem ter os MESMOS dados.")
print("Se diferem, um deles foi modificado ou está incompleto.")
