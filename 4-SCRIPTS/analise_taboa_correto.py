#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISE CORRIGIDA: Dados de Tração de Typha domingensis (30 e 90 dias)

PROBLEMA IDENTIFICADO:
- modelar_LC_k_VUF.py estava usando 'dados_resumo_extraidos.csv' que contém 
  dados de RESINADO (compósito - experimento diferente)
- Os dados corretos estão em 'tracao_taboa_combined.csv' com períodos 30 e 90 dias

SOLUÇÃO:
- Este script lê tracao_taboa_combined.csv
- Calcula estatísticas por tratamento (T0, T1, T2, T3, TE) e período
- Gera tabelas para o manuscrito
- Valida consistência com dados de Weibull do manuscrito
"""

import pandas as pd
import numpy as np
from scipy.stats import sem
import os
from pathlib import Path

def calcular_estatisticas_taboa():
    """Calcula estatísticas corretas dos dados de tração de Typha"""
    
    # Carregar dados de tração CORRETOS
    csv_path = 'processed_data/tracao_taboa_combined.csv'
    
    if not os.path.exists(csv_path):
        print(f"ERRO: {csv_path} não encontrado")
        return None
    
    df = pd.read_csv(csv_path)
    
    # Filtrar apenas dados com tratamento e período definidos
    df = df[df['treatment'].notna() & df['days'].notna()].copy()
    
    # Mapeamento de tratamentos
    tratamento_map = {
        'T0': '0% (Controle)',
        'T1': '3% NaOH',
        'T2': '6% NaOH',
        'T3': '9% NaOH',
        'TE': '12% NaOH'
    }
    
    df['tratamento_desc'] = df['treatment'].map(tratamento_map)
    
    print("="*80)
    print("ANÁLISE CORRIGIDA: TRAÇÃO DE TYPHA DOMINGENSIS")
    print("="*80)
    print(f"\nDados carregados: {len(df)} linhas")
    print(f"Períodos únicos: {sorted(df['days'].unique())}")
    print(f"Tratamentos: {df['treatment'].unique()}\n")
    
    # Calcular estatísticas por tratamento e período
    resultados = []
    
    for dias in sorted(df['days'].unique()):
        df_periodo = df[df['days'] == dias]
        print(f"\n{'='*80}")
        print(f"PERÍODO: {int(dias)} DIAS")
        print(f"{'='*80}")
        
        for trat in ['T0', 'T1', 'T2', 'T3', 'TE']:
            df_trat = df_periodo[df_periodo['treatment'] == trat]
            
            if len(df_trat) > 0:
                # Stress (MPa) - coluna 'stress'
                stress_values = df_trat['stress'].values
                stress_mean = np.mean(stress_values)
                stress_std = np.std(stress_values, ddof=1)
                stress_cv = (stress_std / stress_mean * 100) if stress_mean > 0 else 0
                stress_min = np.min(stress_values)
                stress_max = np.max(stress_values)
                n_stress = len(stress_values)
                
                # Strain (mm/mm) - coluna 'strain'
                strain_values = df_trat['strain'].values
                strain_mean = np.mean(strain_values)
                strain_std = np.std(strain_values, ddof=1)
                strain_cv = (strain_std / strain_mean * 100) if strain_mean > 0 else 0
                n_strain = len(strain_values)
                
                print(f"\n{tratamento_map[trat]} (n={n_stress} espécimes):")
                print(f"  UTS (Stress):")
                print(f"    Média:  {stress_mean:.2f} ± {stress_std:.2f} MPa")
                print(f"    CV:     {stress_cv:.1f}%")
                print(f"    Min-Max: {stress_min:.2f} - {stress_max:.2f} MPa")
                print(f"  Strain @ ruptura:")
                print(f"    Média:  {strain_mean:.2f} ± {strain_std:.2f} mm/mm")
                print(f"    CV:     {strain_cv:.1f}%")
                
                resultados.append({
                    'dias': int(dias),
                    'tratamento': trat,
                    'tratamento_desc': tratamento_map[trat],
                    'n': n_stress,
                    'stress_mean': stress_mean,
                    'stress_std': stress_std,
                    'stress_cv': stress_cv,
                    'stress_min': stress_min,
                    'stress_max': stress_max,
                    'strain_mean': strain_mean,
                    'strain_std': strain_std,
                    'strain_cv': strain_cv,
                })
    
    # Criar DataFrame com resultados
    df_resultados = pd.DataFrame(resultados)
    
    print(f"\n\n{'='*80}")
    print("RESUMO COMPARATIVO")
    print(f"{'='*80}\n")
    
    # Tabela por período
    for dias in sorted(df_resultados['dias'].unique()):
        print(f"\n{dias} DIAS - UTS (MPa):")
        print("-" * 70)
        df_dia = df_resultados[df_resultados['dias'] == dias].sort_values('dias')
        for _, row in df_dia.iterrows():
            print(f"  {row['tratamento_desc']:20s}: {row['stress_mean']:6.2f} ± {row['stress_std']:5.2f}  "
                  f"(CV={row['stress_cv']:5.1f}%, n={row['n']})")
    
    # Identificar melhor tratamento em 90 dias
    df_90 = df_resultados[df_resultados['dias'] == 90].sort_values('stress_mean', ascending=False)
    print(f"\n\n{'='*80}")
    print("CONCLUSÃO: MELHOR TRATAMENTO")
    print(f"{'='*80}")
    print(f"\nAos 90 dias, o melhor tratamento é: {df_90.iloc[0]['tratamento_desc']}")
    print(f"  - UTS: {df_90.iloc[0]['stress_mean']:.2f} ± {df_90.iloc[0]['stress_std']:.2f} MPa")
    print(f"  - CV:  {df_90.iloc[0]['stress_cv']:.1f}%")
    print(f"  - Strain: {df_90.iloc[0]['strain_mean']:.2f} ± {df_90.iloc[0]['strain_std']:.2f} mm/mm")
    
    # Salvar resultados
    output_file = 'processed_data/analise_taboa_correto.csv'
    df_resultados.to_csv(output_file, index=False)
    print(f"\n✓ Resultados salvos em: {output_file}")
    
    return df_resultados

def validar_consistencia_manuscrito(df_resultados):
    """
    Valida se os resultados estão consistentes com o manuscrito
    O manuscrito menciona valores de UTS e VUF que devem ser validados
    """
    print(f"\n\n{'='*80}")
    print("VALIDAÇÃO: Dados vs Manuscrito")
    print(f"{'='*80}\n")
    
    # Dados esperados do manuscrito (Tabela 1)
    esperado = {
        'T3_30d': {'stress': 21.11, 'strain': 42.22},  # 9% NaOH aos 30 dias
        'T3_90d': {'stress': 25.56, 'strain': 51.12},  # 9% NaOH aos 90 dias
        'T0_30d': {'stress': 9.84, 'strain': 19.68},   # Controle aos 30 dias
        'T0_90d': {'stress': 11.09, 'strain': 22.19},  # Controle aos 90 dias
    }
    
    for chave, valores in esperado.items():
        trat, periodo = chave.split('_')
        dias = int(periodo.replace('d', ''))
        
        df_linha = df_resultados[(df_resultados['tratamento'] == trat) & 
                                  (df_resultados['dias'] == dias)]
        
        if len(df_linha) > 0:
            stress_atual = df_linha.iloc[0]['stress_mean']
            strain_atual = df_linha.iloc[0]['strain_mean']
            
            stress_diff = abs(stress_atual - valores['stress']) / valores['stress'] * 100
            strain_diff = abs(strain_atual - valores['strain']) / valores['strain'] * 100
            
            status_s = "✓" if stress_diff < 10 else "⚠"
            status_st = "✓" if strain_diff < 10 else "⚠"
            
            print(f"{status_s} {chave:12s} - UTS: {stress_atual:6.2f} MPa "
                  f"(esperado {valores['stress']:6.2f}, diff {stress_diff:5.1f}%)")
            print(f"{status_st} {' '*12s} - Strain: {strain_atual:6.2f} (esperado {valores['strain']:6.2f}, diff {strain_diff:5.1f}%)\n")

if __name__ == '__main__':
    df_resultados = calcular_estatisticas_taboa()
    if df_resultados is not None:
        validar_consistencia_manuscrito(df_resultados)
