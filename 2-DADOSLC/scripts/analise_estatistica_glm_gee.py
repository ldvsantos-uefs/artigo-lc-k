"""
Análise Estatística Rigorosa: GLM, GEE e Testes de Hipóteses
============================================================

Este script realiza análises estatísticas avançadas para validar as afirmações
do manuscrito sobre diferenças entre tratamentos, incluindo:

1. Modelos Lineares Generalizados (GLM)
2. Equações de Estimação Generalizadas (GEE) para dados longitudinais
3. Testes de hipóteses com correção para comparações múltiplas
4. Cálculo de tamanho de efeito (Cohen's d)
5. Análise de variância (ANOVA) e post-hoc
6. Verificação de pressupostos estatísticos

Autor: Script gerado para validação estatística do artigo
Data: Dezembro 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Análises estatísticas
from scipy import stats
from scipy.stats import shapiro, levene, kruskal, mannwhitneyu
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.power import FTestAnovaPower
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.genmod.generalized_estimating_equations import GEE
from statsmodels.genmod.cov_struct import (
    Exchangeable, Independence, Autoregressive
)
from statsmodels.genmod.families import Gaussian, Gamma

# Configurações
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def cohen_d(group1, group2):
    """
    Calcula o tamanho de efeito de Cohen's d entre dois grupos.
    
    Interpretação:
    - |d| < 0.2: efeito pequeno
    - 0.2 ≤ |d| < 0.5: efeito pequeno a médio
    - 0.5 ≤ |d| < 0.8: efeito médio
    - |d| ≥ 0.8: efeito grande
    """
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    
    if pooled_std == 0:
        return np.nan
    
    return (np.mean(group1) - np.mean(group2)) / pooled_std


def interpretar_cohen_d(d):
    """Interpreta o valor de Cohen's d."""
    d_abs = abs(d)
    if d_abs < 0.2:
        return "desprezível"
    elif d_abs < 0.5:
        return "pequeno"
    elif d_abs < 0.8:
        return "médio"
    else:
        return "grande"


def verificar_normalidade(data, group_col, value_col):
    """Testa normalidade por grupo usando Shapiro-Wilk."""
    print("\n" + "="*80)
    print("TESTE DE NORMALIDADE (Shapiro-Wilk)")
    print("="*80)
    
    resultados = []
    for group in data[group_col].unique():
        group_data = data[data[group_col] == group][value_col].dropna()
        
        if len(group_data) >= 3:
            stat, p_value = shapiro(group_data)
            normal = "Sim" if p_value > 0.05 else "Não"
            resultados.append({
                'Grupo': group,
                'n': len(group_data),
                'W': stat,
                'p-valor': p_value,
                'Normal (α=0.05)': normal
            })
    
    df_norm = pd.DataFrame(resultados)
    print(df_norm.to_string(index=False))
    
    return df_norm


def verificar_homogeneidade_variancia(data, group_col, value_col):
    """Testa homogeneidade de variâncias usando teste de Levene."""
    print("\n" + "="*80)
    print("TESTE DE HOMOGENEIDADE DE VARIÂNCIAS (Levene)")
    print("="*80)
    
    groups = [data[data[group_col] == g][value_col].dropna().values 
              for g in data[group_col].unique()]
    
    stat, p_value = levene(*groups)
    homogeneo = "Sim" if p_value > 0.05 else "Não"
    
    print(f"Estatística de Levene: {stat:.4f}")
    print(f"p-valor: {p_value:.4f}")
    print(f"Variâncias homogêneas (α=0.05): {homogeneo}")
    
    return p_value > 0.05


def calcular_coeficiente_variacao(data, group_col, value_col):
    """Calcula coeficiente de variação por grupo."""
    print("\n" + "="*80)
    print("COEFICIENTE DE VARIAÇÃO POR GRUPO")
    print("="*80)
    
    resultados = []
    for group in sorted(data[group_col].unique()):
        group_data = data[data[group_col] == group][value_col].dropna()
        
        media = group_data.mean()
        std = group_data.std()
        cv = (std / media * 100) if media != 0 else np.nan
        
        resultados.append({
            'Grupo': group,
            'n': len(group_data),
            'Média': f"{media:.3f}",
            'DP': f"{std:.3f}",
            'CV (%)': f"{cv:.2f}"
        })
    
    df_cv = pd.DataFrame(resultados)
    print(df_cv.to_string(index=False))
    
    return df_cv


# ============================================================================
# ANÁLISE GLM (MODELO LINEAR GENERALIZADO)
# ============================================================================

def ajustar_glm(data, formula, family=Gaussian()):
    """
    Ajusta um Modelo Linear Generalizado.
    
    Args:
        data: DataFrame com os dados
        formula: Fórmula no estilo R (ex: "uts_mpa ~ C(treatment) + dias")
        family: Família de distribuição (Gaussian, Gamma, etc.)
    """
    print("\n" + "="*80)
    print("MODELO LINEAR GENERALIZADO (GLM)")
    print("="*80)
    print(f"Fórmula: {formula}")
    print(f"Família: {family.__class__.__name__}")
    
    modelo = smf.glm(formula=formula, data=data, family=family).fit()
    
    print("\n" + "-"*80)
    print("RESUMO DO MODELO")
    print("-"*80)
    print(modelo.summary())
    
    return modelo


# ============================================================================
# ANÁLISE GEE (EQUAÇÕES DE ESTIMAÇÃO GENERALIZADAS)
# ============================================================================

def ajustar_gee(data, formula, groups, cov_struct=Exchangeable()):
    """
    Ajusta modelo GEE para dados longitudinais (medidas repetidas).
    
    Args:
        data: DataFrame com os dados
        formula: Fórmula no estilo R
        groups: Nome da coluna que identifica os grupos (ex: 'treatment')
        cov_struct: Estrutura de covariância (Exchangeable, Autoregressive, etc.)
    """
    print("\n" + "="*80)
    print("EQUAÇÕES DE ESTIMAÇÃO GENERALIZADAS (GEE)")
    print("="*80)
    print(f"Fórmula: {formula}")
    print(f"Grupos: {groups}")
    print(f"Estrutura de covariância: {cov_struct.__class__.__name__}")
    
    # Preparar dados
    data_sorted = data.sort_values([groups, 'dias']).copy()
    
    modelo_gee = GEE.from_formula(
        formula=formula,
        groups=data_sorted[groups],
        data=data_sorted,
        cov_struct=cov_struct,
        family=Gaussian()
    ).fit()
    
    print("\n" + "-"*80)
    print("RESUMO DO MODELO GEE")
    print("-"*80)
    print(modelo_gee.summary())
    
    return modelo_gee


# ============================================================================
# COMPARAÇÕES MÚLTIPLAS COM CORREÇÃO
# ============================================================================

def comparacoes_multiplas_parametrico(data, group_col, value_col, correcao='bonferroni'):
    """
    Realiza comparações múltiplas entre grupos usando t-test com correção.
    
    Args:
        correcao: Método de correção ('bonferroni', 'holm', 'fdr_bh')
    """
    print("\n" + "="*80)
    print(f"COMPARAÇÕES MÚLTIPLAS (t-test com correção {correcao.upper()})")
    print("="*80)
    
    groups = sorted(data[group_col].unique())
    resultados = []
    
    # Realizar todos os pares de comparações
    for i, group1 in enumerate(groups):
        for group2 in groups[i+1:]:
            data1 = data[data[group_col] == group1][value_col].dropna()
            data2 = data[data[group_col] == group2][value_col].dropna()
            
            # t-test
            t_stat, p_val = stats.ttest_ind(data1, data2)
            
            # Cohen's d
            d = cohen_d(data1, data2)
            interpretacao = interpretar_cohen_d(d)
            
            resultados.append({
                'Comparação': f"{group1} vs {group2}",
                'n1': len(data1),
                'n2': len(data2),
                'Média1': data1.mean(),
                'Média2': data2.mean(),
                'Dif.': data1.mean() - data2.mean(),
                't': t_stat,
                'p-valor': p_val,
                "Cohen's d": d,
                'Efeito': interpretacao
            })
    
    df_resultados = pd.DataFrame(resultados)
    
    # Aplicar correção para comparações múltiplas
    p_valores = df_resultados['p-valor'].values
    reject, p_corrigidos, _, _ = multipletests(p_valores, method=correcao)
    
    df_resultados['p-corrigido'] = p_corrigidos
    df_resultados['Significativo'] = ['Sim' if r else 'Não' for r in reject]
    
    # Formatar para exibição
    df_display = df_resultados.copy()
    df_display['Média1'] = df_display['Média1'].apply(lambda x: f"{x:.3f}")
    df_display['Média2'] = df_display['Média2'].apply(lambda x: f"{x:.3f}")
    df_display['Dif.'] = df_display['Dif.'].apply(lambda x: f"{x:.3f}")
    df_display['t'] = df_display['t'].apply(lambda x: f"{x:.3f}")
    df_display['p-valor'] = df_display['p-valor'].apply(lambda x: f"{x:.4f}")
    df_display['p-corrigido'] = df_display['p-corrigido'].apply(lambda x: f"{x:.4f}")
    df_display["Cohen's d"] = df_display["Cohen's d"].apply(lambda x: f"{x:.3f}")
    
    print("\n" + df_display.to_string(index=False))
    
    return df_resultados


def comparacoes_multiplas_nao_parametrico(data, group_col, value_col, correcao='bonferroni'):
    """
    Realiza comparações múltiplas não-paramétricas (Mann-Whitney U).
    """
    print("\n" + "="*80)
    print(f"COMPARAÇÕES MÚLTIPLAS NÃO-PARAMÉTRICAS (Mann-Whitney U com {correcao.upper()})")
    print("="*80)
    
    groups = sorted(data[group_col].unique())
    resultados = []
    
    for i, group1 in enumerate(groups):
        for group2 in groups[i+1:]:
            data1 = data[data[group_col] == group1][value_col].dropna()
            data2 = data[data[group_col] == group2][value_col].dropna()
            
            # Mann-Whitney U test
            u_stat, p_val = mannwhitneyu(data1, data2, alternative='two-sided')
            
            # Cohen's d (ainda útil como medida de efeito)
            d = cohen_d(data1, data2)
            interpretacao = interpretar_cohen_d(d)
            
            resultados.append({
                'Comparação': f"{group1} vs {group2}",
                'n1': len(data1),
                'n2': len(data2),
                'Mediana1': data1.median(),
                'Mediana2': data2.median(),
                'U': u_stat,
                'p-valor': p_val,
                "Cohen's d": d,
                'Efeito': interpretacao
            })
    
    df_resultados = pd.DataFrame(resultados)
    
    # Aplicar correção
    p_valores = df_resultados['p-valor'].values
    reject, p_corrigidos, _, _ = multipletests(p_valores, method=correcao)
    
    df_resultados['p-corrigido'] = p_corrigidos
    df_resultados['Significativo'] = ['Sim' if r else 'Não' for r in reject]
    
    # Formatar
    df_display = df_resultados.copy()
    for col in ['Mediana1', 'Mediana2']:
        df_display[col] = df_display[col].apply(lambda x: f"{x:.3f}")
    df_display['U'] = df_display['U'].apply(lambda x: f"{x:.1f}")
    df_display['p-valor'] = df_display['p-valor'].apply(lambda x: f"{x:.4f}")
    df_display['p-corrigido'] = df_display['p-corrigido'].apply(lambda x: f"{x:.4f}")
    df_display["Cohen's d"] = df_display["Cohen's d"].apply(lambda x: f"{x:.3f}")
    
    print("\n" + df_display.to_string(index=False))
    
    return df_resultados


# ============================================================================
# ANÁLISE PRINCIPAL
# ============================================================================

def main():
    """Função principal de análise."""
    
    print("\n" + "="*80)
    print("ANÁLISE ESTATÍSTICA RIGOROSA - DADOS DE TRAÇÃO")
    print("="*80)
    
    # Carregar dados
    dados_file = Path(__file__).parent.parent / 'processed_data' / 'dados_tracao_agregados.csv'
    
    if not dados_file.exists():
        print(f"\nERRO: Arquivo não encontrado: {dados_file}")
        return
    
    df = pd.read_csv(dados_file)
    
    print(f"\nDados carregados: {len(df)} observações")
    print(f"Tratamentos: {sorted(df['treatment'].unique())}")
    print(f"Tempos (dias): {sorted(df['dias'].unique())}")
    
    # ========================================================================
    # 1. ESTATÍSTICAS DESCRITIVAS
    # ========================================================================
    
    print("\n" + "="*80)
    print("ESTATÍSTICAS DESCRITIVAS POR TRATAMENTO")
    print("="*80)
    
    desc = df.groupby('treatment')['uts_mpa'].agg([
        ('n', 'count'),
        ('Média', 'mean'),
        ('DP', 'std'),
        ('Mediana', 'median'),
        ('Mín', 'min'),
        ('Máx', 'max')
    ]).reset_index()
    
    desc['CV (%)'] = (desc['DP'] / desc['Média'] * 100)
    
    print("\n" + desc.to_string(index=False))
    
    # ========================================================================
    # 2. VERIFICAÇÃO DE PRESSUPOSTOS
    # ========================================================================
    
    # Normalidade
    df_normalidade = verificar_normalidade(df, 'treatment', 'uts_mpa')
    
    # Homogeneidade de variâncias
    homogeneo = verificar_homogeneidade_variancia(df, 'treatment', 'uts_mpa')
    
    # Coeficiente de variação
    df_cv = calcular_coeficiente_variacao(df, 'treatment', 'uts_mpa')
    
    # ========================================================================
    # 3. TESTE DE HIPÓTESES GLOBAL
    # ========================================================================
    
    print("\n" + "="*80)
    print("TESTE GLOBAL: KRUSKAL-WALLIS (não-paramétrico)")
    print("="*80)
    print("H0: As medianas de todos os grupos são iguais")
    print("H1: Pelo menos uma mediana é diferente")
    
    groups_data = [df[df['treatment'] == g]['uts_mpa'].dropna().values 
                   for g in sorted(df['treatment'].unique())]
    
    h_stat, p_val_kw = kruskal(*groups_data)
    
    print(f"\nEstatística H: {h_stat:.4f}")
    print(f"p-valor: {p_val_kw:.6f}")
    print(f"Conclusão (α=0.05): {'Rejeitar H0' if p_val_kw < 0.05 else 'Não rejeitar H0'}")
    
    if p_val_kw < 0.05:
        print("⚠️  Existem diferenças significativas entre os grupos.")
    
    # ========================================================================
    # 4. COMPARAÇÕES MÚLTIPLAS
    # ========================================================================
    
    # Decidir qual teste usar baseado na normalidade
    normal_count = (df_normalidade['Normal (α=0.05)'] == 'Sim').sum()
    usar_parametrico = normal_count >= len(df_normalidade) * 0.7 and homogeneo
    
    if usar_parametrico:
        print("\n✓ Pressupostos satisfeitos: usando testes paramétricos")
        df_comparacoes = comparacoes_multiplas_parametrico(
            df, 'treatment', 'uts_mpa', correcao='bonferroni'
        )
    else:
        print("\n⚠️  Pressupostos violados: usando testes não-paramétricos")
        df_comparacoes = comparacoes_multiplas_nao_parametrico(
            df, 'treatment', 'uts_mpa', correcao='bonferroni'
        )
    
    # ========================================================================
    # 5. MODELO GLM
    # ========================================================================
    
    try:
        modelo_glm = ajustar_glm(
            df,
            formula="uts_mpa ~ C(treatment) + dias + C(treatment):dias",
            family=Gaussian()
        )
        
        print("\n" + "-"*80)
        print("INTERPRETAÇÃO DO GLM:")
        print("-"*80)
        print("- Coeficientes significativos (p < 0.05) indicam efeito do tratamento")
        print("- Interação treatment:dias mostra se o efeito varia com o tempo")
        
    except Exception as e:
        print(f"\n⚠️  Erro ao ajustar GLM: {e}")
    
    # ========================================================================
    # 6. MODELO GEE (para estrutura longitudinal)
    # ========================================================================
    
    try:
        # Criar ID único para cada réplica
        df['id'] = df['treatment'].astype(str) + '_' + df['repeticao'].astype(str)
        
        modelo_gee = ajustar_gee(
            df,
            formula="uts_mpa ~ C(treatment) + dias",
            groups='id',
            cov_struct=Exchangeable()
        )
        
        print("\n" + "-"*80)
        print("INTERPRETAÇÃO DO GEE:")
        print("-"*80)
        print("- GEE ajusta para correlação entre medidas repetidas")
        print("- Coeficientes robustos a violações de normalidade")
        
    except Exception as e:
        print(f"\n⚠️  Erro ao ajustar GEE: {e}")
    
    # ========================================================================
    # 7. SALVAR RESULTADOS
    # ========================================================================
    
    output_dir = Path(__file__).parent.parent / 'processed_data' / 'analise_estatistica'
    output_dir.mkdir(exist_ok=True)
    
    # Salvar comparações
    df_comparacoes.to_csv(output_dir / 'comparacoes_multiplas.csv', index=False)
    df_cv.to_csv(output_dir / 'coeficiente_variacao.csv', index=False)
    df_normalidade.to_csv(output_dir / 'teste_normalidade.csv', index=False)
    
    print("\n" + "="*80)
    print("ANÁLISE CONCLUÍDA")
    print("="*80)
    print(f"\nResultados salvos em: {output_dir}")
    print("\nArquivos gerados:")
    print("  - comparacoes_multiplas.csv")
    print("  - coeficiente_variacao.csv")
    print("  - teste_normalidade.csv")
    
    # ========================================================================
    # 8. RECOMENDAÇÕES PARA O MANUSCRITO
    # ========================================================================
    
    print("\n" + "="*80)
    print("RECOMENDAÇÕES PARA O MANUSCRITO")
    print("="*80)
    
    print("\n1. REPORTAR P-VALORES:")
    print("   - Usar p-valores corrigidos para comparações múltiplas")
    print("   - Exemplo: 'T2 vs T0 (p < 0.001, Bonferroni-corrigido)'")
    
    print("\n2. REPORTAR TAMANHO DE EFEITO:")
    print("   - Sempre incluir Cohen's d com interpretação")
    print("   - Exemplo: 'diferença com grande tamanho de efeito (d = 1.2)'")
    
    print("\n3. MENCIONAR MÉTODO ESTATÍSTICO:")
    if usar_parametrico:
        print("   - 't-test independente com correção de Bonferroni'")
    else:
        print("   - 'teste de Mann-Whitney U com correção de Bonferroni'")
    
    print("\n4. REPORTAR COEFICIENTE DE VARIAÇÃO:")
    print("   - Mencionar CV como medida de dispersão relativa")
    print("   - Exemplo: 'CV de 15% para T0 e 10% para T2'")


if __name__ == "__main__":
    main()
