"""
Análise Estatística por Tempo de Exposição
===========================================

Este script complementar analisa as diferenças entre tratamentos
em cada ponto temporal específico (30, 60, 90, 120, 150, 180 dias).

Útil para identificar quando as diferenças se tornam significativas.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import mannwhitneyu, kruskal
from statsmodels.stats.multitest import multipletests

def cohen_d(group1, group2):
    """Calcula Cohen's d."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    
    if pooled_std == 0:
        return np.nan
    
    return (np.mean(group1) - np.mean(group2)) / pooled_std


def analisar_por_tempo(df):
    """Analisa diferenças entre tratamentos em cada tempo."""
    
    print("\n" + "="*80)
    print("ANÁLISE POR TEMPO DE EXPOSIÇÃO")
    print("="*80)
    
    tempos = sorted(df['dias'].unique())
    
    resultados_completos = []
    
    for tempo in tempos:
        print(f"\n{'='*80}")
        print(f"TEMPO: {int(tempo)} DIAS")
        print(f"{'='*80}")
        
        # Filtrar dados para este tempo
        df_tempo = df[df['dias'] == tempo].copy()
        
        # Estatísticas descritivas
        print("\nEstatísticas Descritivas:")
        desc = df_tempo.groupby('treatment')['uts_mpa'].agg([
            ('n', 'count'),
            ('Média', 'mean'),
            ('DP', 'std'),
            ('CV%', lambda x: (x.std() / x.mean() * 100) if x.mean() != 0 else np.nan)
        ])
        print(desc.to_string())
        
        # Teste de Kruskal-Wallis
        groups = [df_tempo[df_tempo['treatment'] == t]['uts_mpa'].values 
                  for t in sorted(df_tempo['treatment'].unique())]
        
        if len(groups) >= 2 and all(len(g) > 0 for g in groups):
            h_stat, p_kw = kruskal(*groups)
            print(f"\nKruskal-Wallis: H={h_stat:.3f}, p={p_kw:.4f}")
            
            if p_kw < 0.05:
                print("✅ Diferenças significativas detectadas entre grupos")
                
                # Comparações múltiplas
                treatments = sorted(df_tempo['treatment'].unique())
                comparacoes_tempo = []
                
                for i, t1 in enumerate(treatments):
                    for t2 in treatments[i+1:]:
                        data1 = df_tempo[df_tempo['treatment'] == t1]['uts_mpa'].values
                        data2 = df_tempo[df_tempo['treatment'] == t2]['uts_mpa'].values
                        
                        if len(data1) > 0 and len(data2) > 0:
                            u_stat, p_val = mannwhitneyu(data1, data2, alternative='two-sided')
                            d = cohen_d(data1, data2)
                            
                            comparacoes_tempo.append({
                                'Tempo (dias)': int(tempo),
                                'Comparação': f"{t1} vs {t2}",
                                'Média1': data1.mean(),
                                'Média2': data2.mean(),
                                'p-valor': p_val,
                                "Cohen's d": d
                            })
                
                if comparacoes_tempo:
                    df_comp = pd.DataFrame(comparacoes_tempo)
                    
                    # Correção de Bonferroni
                    p_valores = df_comp['p-valor'].values
                    reject, p_corr, _, _ = multipletests(p_valores, method='bonferroni')
                    df_comp['p-corrigido'] = p_corr
                    df_comp['Significativo'] = ['Sim' if r else 'Não' for r in reject]
                    
                    print("\nComparações Múltiplas (Bonferroni):")
                    print(df_comp.to_string(index=False))
                    
                    resultados_completos.extend(df_comp.to_dict('records'))
            else:
                print("❌ Sem diferenças significativas entre grupos neste tempo")
    
    # Salvar resultados completos
    if resultados_completos:
        df_final = pd.DataFrame(resultados_completos)
        output_dir = Path(__file__).parent.parent / 'processed_data' / 'analise_estatistica'
        df_final.to_csv(output_dir / 'analise_por_tempo.csv', index=False)
        
        print("\n" + "="*80)
        print("RESUMO: QUANDO AS DIFERENÇAS SÃO SIGNIFICATIVAS?")
        print("="*80)
        
        # Agrupar por comparação
        for comp in df_final['Comparação'].unique():
            df_comp = df_final[df_final['Comparação'] == comp]
            tempos_sig = df_comp[df_comp['Significativo'] == 'Sim']['Tempo (dias)'].values
            
            if len(tempos_sig) > 0:
                print(f"\n{comp}:")
                print(f"  Significativo em: {', '.join(map(str, tempos_sig))} dias")
            else:
                print(f"\n{comp}:")
                print(f"  Não significativo em nenhum tempo")


def main():
    """Função principal."""
    
    # Carregar dados
    dados_file = Path(__file__).parent.parent / 'processed_data' / 'dados_tracao_agregados.csv'
    
    if not dados_file.exists():
        print(f"ERRO: Arquivo não encontrado: {dados_file}")
        return
    
    df = pd.read_csv(dados_file)
    
    analisar_por_tempo(df)
    
    print("\n" + "="*80)
    print("ANÁLISE POR TEMPO CONCLUÍDA")
    print("="*80)


if __name__ == "__main__":
    main()
