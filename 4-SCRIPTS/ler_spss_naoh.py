#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LEITURA E ANÁLISE DE DADOS SPSS - TRAÇÃO TABOA

Objetivo: 
- Ler arquivos .sav (SPSS) contendo dados de tração
- Consolidar dados APENAS de tratamentos com NaOH (T0, T1, T2, T3, TE)
- Validar períodos (30 e 90 dias)
- Comparar com dados já processados em tracao_taboa_combined.csv
"""

import sys
import io
import pandas as pd
import numpy as np
import os
from pathlib import Path

# Fixar encoding para evitar problemas com unicode
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import pyreadstat
    HAS_PYREADSTAT = True
except ImportError:
    HAS_PYREADSTAT = False
    print("AVISO: pyreadstat não instalado. Instale com: pip install pyreadstat")

def ler_arquivo_spss(caminho):
    """Lê arquivo SPSS .sav e retorna DataFrame"""
    if not HAS_PYREADSTAT:
        return None
    
    try:
        df, meta = pyreadstat.read_sav(caminho)
        print(f"[OK] Arquivo lido: {os.path.basename(caminho)}")
        print(f"  Linhas: {len(df)}, Colunas: {len(df.columns)}")
        print(f"  Colunas: {df.columns.tolist()}\n")
        return df
    except Exception as e:
        print(f"[ERRO] ao ler {caminho}: {e}\n")
        return None

def analisar_arquivos_spss():
    """Analisa todos os arquivos SPSS disponíveis"""
    
    spss_files = [
        '2-DADOSLC/tracao/DADOS TABOA PUNÇÃO.completo.sav',
        '2-DADOSLC/tracao/Dados completos.sav',
    ]
    
    print("="*80)
    print("LEITURA DE ARQUIVOS SPSS - TRAÇÃO TABOA")
    print("="*80 + "\n")
    
    dados_consolidados = {}
    
    for spss_file in spss_files:
        if os.path.exists(spss_file):
            print(f"\nProcessando: {spss_file}")
            print("-" * 80)
            df = ler_arquivo_spss(spss_file)
            
            if df is not None:
                dados_consolidados[spss_file] = df
                
                # Mostrar amostra
                print(f"Primeiras linhas:")
                print(df.head(10))
                print(f"\nTipos de dados:")
                print(df.dtypes)
                print(f"\nValores únicos por coluna:")
                for col in df.columns[:10]:  # Primeiras 10 colunas
                    unique_count = df[col].nunique()
                    if unique_count <= 20:
                        print(f"  {col}: {sorted(df[col].unique())}")
                    else:
                        print(f"  {col}: {unique_count} valores únicos")
                print("\n" + "="*80)
        else:
            print(f"⚠ Arquivo não encontrado: {spss_file}\n")
    
    return dados_consolidados

def extrair_dados_naoh(dfs_spss):
    """
    Extrai dados APENAS de tratamentos NaOH (T0, T1, T2, T3, TE)
    Consolida em um único DataFrame normalizado
    """
    
    print("\n" + "="*80)
    print("EXTRAÇÃO: Apenas Tratamentos NaOH")
    print("="*80 + "\n")
    
    dados_normalizados = []
    
    for arquivo, df in dfs_spss.items():
        print(f"\nArquivo: {arquivo}")
        print(f"Shape original: {df.shape}")
        
        # Verificar qual é a estrutura correta (arquivo "Dados completos.sav")
        if 'TRATAMENTO' in df.columns and 'DIAS' in df.columns:
            print("  ✓ Identificado como arquivo 'Dados completos.sav' (formato correto)")
            
            # Filtrar: TRATAMENTO em [0, 3, 6, 9] = [T0, T1, T2, T3]
            df_filtered = df[df['TRATAMENTO'].isin([0.0, 3.0, 6.0, 9.0])].copy()
            
            # Mapear tratamento
            trat_map = {0.0: 'T0', 3.0: 'T1', 6.0: 'T2', 9.0: 'T3'}
            df_filtered['treatment'] = df_filtered['TRATAMENTO'].map(trat_map)
            df_filtered['days'] = df_filtered['DIAS']
            df_filtered['specimen'] = df_filtered['REPETIÇÃO']
            df_filtered['stress'] = df_filtered['ESFORÇOÀTRAÇÃOMPa']
            df_filtered['strain'] = df_filtered['Deformação']
            
            # Selecionar apenas colunas necessárias
            df_norm = df_filtered[['treatment', 'days', 'specimen', 'stress', 'strain']].copy()
            df_norm['source'] = 'SPSS_Dados_completos'
            
            print(f"  [OK] Dados extraídos: {len(df_norm)} linhas")
            print(f"  Tratamentos: {sorted(df_norm['treatment'].unique())}")
            print(f"  Períodos (dias): {sorted(df_norm['days'].unique())}")
            print(f"  Espécimes por célula: {df_norm.groupby(['days', 'treatment']).size().values}")
            
            dados_normalizados.append(df_norm)
        else:
            print(f"  [AVISO] Estrutura de arquivo não reconhecida. Colunas: {df.columns.tolist()}")
    
    # Consolidar
    if dados_normalizados:
        df_consolidado = pd.concat(dados_normalizados, ignore_index=True)
        print(f"\n[OK] Dados consolidados: {len(df_consolidado)} linhas")
        
        # Estatísticas por tratamento e período
        print(f"\nESTATISTICAS CONSOLIDADAS:")
        for dias in sorted(df_consolidado['days'].unique()):
            print(f"\n  {int(dias)} dias:")
            df_dia = df_consolidado[df_consolidado['days'] == dias]
            for trat in sorted(df_dia['treatment'].unique()):
                df_trat = df_dia[df_dia['treatment'] == trat]
                stress_mean = df_trat['stress'].mean()
                strain_mean = df_trat['strain'].mean()
                n = len(df_trat)
                print(f"    {trat}: n={n}, stress={stress_mean:.2f} MPa, strain={strain_mean:.4f}")
        
        return df_consolidado
    else:
        print("\n[ERRO] Nenhum dado de NaOH foi extraído")
        return None

def comparar_com_csv_existente():
    """Compara dados SPSS com tracao_taboa_combined.csv"""
    
    print("\n" + "="*80)
    print("COMPARAÇÃO: Dados SPSS vs CSV existente")
    print("="*80 + "\n")
    
    csv_path = 'processed_data/tracao_taboa_combined.csv'
    if os.path.exists(csv_path):
        df_csv = pd.read_csv(csv_path)
        df_csv = df_csv[df_csv['treatment'].notna() & df_csv['days'].notna()]
        
        print(f"CSV existente: {len(df_csv)} linhas")
        print(f"Períodos: {sorted(df_csv['days'].unique())}")
        print(f"Tratamentos: {sorted(df_csv['treatment'].unique())}")
        print(f"Colunas: {df_csv.columns.tolist()}")
        
        # Estatísticas
        print(f"\nEstatísticas do CSV:")
        for dias in sorted(df_csv['days'].unique()):
            df_dia = df_csv[df_csv['days'] == dias]
            print(f"\n  {int(dias)} dias:")
            for trat in sorted(df_dia['treatment'].unique()):
                df_trat = df_dia[df_dia['treatment'] == trat]
                stress = df_trat['stress'].mean()
                strain = df_trat['strain'].mean()
                n = len(df_trat)
                print(f"    {trat}: n={n}, stress={stress:.2f} MPa, strain={strain:.2f}")
    else:
        print(f"⚠ Arquivo não encontrado: {csv_path}")

if __name__ == '__main__':
    
    # 1. Ler arquivos SPSS
    dfs_spss = analisar_arquivos_spss()
    
    # 2. Extrair dados NaOH
    if dfs_spss:
        df_naoh = extrair_dados_naoh(dfs_spss)
        
        if df_naoh is not None:
            # Salvar
            output_file = 'processed_data/dados_spss_naoh_extraidos.csv'
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            df_naoh.to_csv(output_file, index=False)
            print(f"\n[OK] Dados extraídos salvos em: {output_file}")
    
    # 3. Comparar com CSV existente
    comparar_com_csv_existente()
