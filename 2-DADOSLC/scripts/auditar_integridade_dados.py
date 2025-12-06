"""
Script para auditar integridade de dados de tração.
Compara 3 fontes primárias:
1. Excel Original (raw_imports/TABOA/TABELA-TRAÇÃO.xlsx)
2. Arquivo SPSS (tracao/Dados completos.sav)
3. Arquivo Excel na pasta tracao (Dados completo.xlsx)

Objetivo: Determinar qual é a FONTE CORRECTA
"""

import pandas as pd
import openpyxl
import os

# Caminho base
base_path = r"C:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K\2-DADOSLC"

print("="*80)
print("AUDITORIA DE INTEGRIDADE DE DADOS - TRAÇÃO")
print("="*80)

# 1. ANALISAR EXCEL ORIGINAL
print("\n1. ANALISANDO EXCEL ORIGINAL (raw_imports/TABOA/TABELA-TRAÇÃO)")
print("-" * 80)
excel_path = os.path.join(base_path, "raw_imports/TABOA/TABELA-TRAÇÃO (Recuperado).xlsx")
try:
    xls = pd.ExcelFile(excel_path)
    print(f"   Sheets disponíveis: {xls.sheet_names}")
    
    # Ler cada sheet para entender a estrutura
    for sheet in xls.sheet_names:
        df = pd.read_excel(excel_path, sheet_name=sheet)
        print(f"\n   Sheet '{sheet}': {df.shape}")
        print(f"   Colunas: {list(df.columns)}")
        print(f"   Primeiras 3 linhas:")
        print(df.head(3))
        
except Exception as e:
    print(f"   ERRO: {e}")

# 2. ANALISAR ARQUIVO SPSS
print("\n\n2. ANALISANDO ARQUIVO SPSS (tracao/Dados completos.sav)")
print("-" * 80)
sav_path = os.path.join(base_path, "tracao/Dados completos.sav")
try:
    import pyreadstat
    df_sav, meta = pyreadstat.read_sav(sav_path)
    print(f"   Shape: {df_sav.shape}")
    print(f"   Colunas: {list(df_sav.columns)}")
    print(f"   Primeiras 3 linhas:")
    print(df_sav.head(3))
    print(f"\n   Estatísticas por tratamento @ 30 dias:")
    if 'days' in df_sav.columns and 'treatment' in df_sav.columns:
        df_30 = df_sav[df_sav['days'] == 30]
        for treat in df_30['treatment'].unique():
            if pd.notna(treat):
                stress_val = df_30[df_30['treatment'] == treat]['stress'].mean() if 'stress' in df_sav.columns else "N/A"
                print(f"      {treat}: {stress_val}")
                
except Exception as e:
    print(f"   ERRO: {e}")
    print("   Tentando com pandas...")
    try:
        # Tenta com pandas se pyreadstat não estiver disponível
        df_sav = pd.read_stata(sav_path) if sav_path.endswith('.dta') else None
        if df_sav is not None:
            print(f"   Shape: {df_sav.shape}")
            print(f"   Colunas: {list(df_sav.columns)}")
    except:
        print("   Não foi possível ler arquivo SPSS")

# 3. ANALISAR EXCEL NA PASTA TRACAO
print("\n\n3. ANALISANDO EXCEL NA PASTA TRACAO (Dados completo.xlsx)")
print("-" * 80)
excel2_path = os.path.join(base_path, "tracao/Dados completo.xlsx")
try:
    xls2 = pd.ExcelFile(excel2_path)
    print(f"   Sheets disponíveis: {xls2.sheet_names}")
    
    for sheet in xls2.sheet_names:
        df = pd.read_excel(excel2_path, sheet_name=sheet)
        print(f"\n   Sheet '{sheet}': {df.shape}")
        print(f"   Colunas: {list(df.columns)}")
        print(f"   Primeiras 3 linhas:")
        print(df.head(3))
        
except Exception as e:
    print(f"   ERRO: {e}")

# 4. VERIFICAR ESTRUTURA DO CSV CORROMPIDO
print("\n\n4. VERIFICANDO CSV PROCESSADO (processed_data/tracao_taboa_combined.csv)")
print("-" * 80)
csv_path = os.path.join(base_path, "processed_data/tracao_taboa_combined.csv")
try:
    with open(csv_path, 'r', encoding='utf-8') as f:
        primeira_linha = f.readline()
        print(f"   Primeira linha (cabeçalho): {primeira_linha[:200]}...")
        segunda_linha = f.readline()
        print(f"   Segunda linha (amostra): {segunda_linha[:200]}...")
    
    # Tentar ler como CSV
    df_csv = pd.read_csv(csv_path)
    print(f"\n   Shape: {df_csv.shape}")
    print(f"   Colunas: {list(df_csv.columns)}")
    print(f"   Tipos de dados:")
    print(df_csv.dtypes)
    
except Exception as e:
    print(f"   ERRO ao ler: {e}")

print("\n\n" + "="*80)
print("FIM DA AUDITORIA")
print("="*80)
