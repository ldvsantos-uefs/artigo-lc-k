"""
Gerador de Tabelas para Manuscrito
===================================

Cria tabelas formatadas em LaTeX/Markdown prontas para inserir no manuscrito.
"""

import pandas as pd
from pathlib import Path

def gerar_tabela_descritiva():
    """Gera tabela de estatísticas descritivas."""
    
    dados_file = Path(__file__).parent.parent / 'processed_data' / 'dados_tracao_agregados.csv'
    df = pd.read_csv(dados_file)
    
    # Estatísticas por tratamento
    desc = df.groupby('treatment')['uts_mpa'].agg([
        ('n', 'count'),
        ('Média', 'mean'),
        ('DP', 'std'),
        ('Mediana', 'median'),
        ('Min', 'min'),
        ('Max', 'max')
    ]).reset_index()
    
    desc['CV (%)'] = (desc['DP'] / desc['Média'] * 100).round(1)
    desc['Média'] = desc['Média'].round(2)
    desc['DP'] = desc['DP'].round(2)
    desc['Mediana'] = desc['Mediana'].round(2)
    desc['Min'] = desc['Min'].round(2)
    desc['Max'] = desc['Max'].round(2)
    
    print("\n" + "="*80)
    print("TABELA 1: Estatísticas Descritivas da Resistência à Tração")
    print("="*80)
    print("\nFormato Markdown:")
    print(desc.to_markdown(index=False))
    
    print("\n" + "-"*80)
    print("Formato LaTeX (para manuscrito):")
    print("-"*80)
    
    latex_table = """
\\begin{table}[ht]
\\centering
\\caption{Estatísticas descritivas da resistência à tração (MPa) por tratamento ao longo do período experimental (30--180 dias).}
\\label{tab:descritiva}
\\begin{tabular}{lcccccccc}
\\hline
\\textbf{Tratamento} & \\textbf{n} & \\textbf{Média} & \\textbf{DP} & \\textbf{Mediana} & \\textbf{Mín} & \\textbf{Máx} & \\textbf{CV (\\%)} \\\\
\\hline
"""
    
    for _, row in desc.iterrows():
        latex_table += f"{row['treatment']} & {int(row['n'])} & {row['Média']:.2f} & {row['DP']:.2f} & {row['Mediana']:.2f} & {row['Min']:.2f} & {row['Max']:.2f} & {row['CV (%)']:.1f} \\\\\n"
    
    latex_table += """\\hline
\\end{tabular}
\\begin{tablenotes}
\\small
\\item DP = desvio padrão; CV = coeficiente de variação; T0 = controle (sem tratamento); T1 = 3\\% NaOH; T2 = 6\\% NaOH; T3 = 9\\% NaOH.
\\end{tablenotes}
\\end{table}
"""
    
    print(latex_table)
    
    return desc


def gerar_tabela_comparacoes():
    """Gera tabela de comparações múltiplas."""
    
    comp_file = Path(__file__).parent.parent / 'processed_data' / 'analise_estatistica' / 'comparacoes_multiplas.csv'
    df = pd.read_csv(comp_file)
    
    # Selecionar colunas relevantes
    df_tabela = df[['Comparação', 'Mediana1', 'Mediana2', 'p-valor', 'p-corrigido', "Cohen's d", 'Efeito', 'Significativo']].copy()
    
    # Formatar valores
    df_tabela['Mediana1'] = df_tabela['Mediana1'].round(2)
    df_tabela['Mediana2'] = df_tabela['Mediana2'].round(2)
    df_tabela['p-valor'] = df_tabela['p-valor'].apply(lambda x: f"{x:.4f}" if x >= 0.001 else "<0.001")
    df_tabela['p-corrigido'] = df_tabela['p-corrigido'].apply(lambda x: f"{x:.4f}" if x >= 0.001 else "<0.001")
    df_tabela["Cohen's d"] = df_tabela["Cohen's d"].round(2)
    
    print("\n" + "="*80)
    print("TABELA 2: Comparações Múltiplas entre Tratamentos")
    print("="*80)
    print("\nFormato Markdown:")
    print(df_tabela.to_markdown(index=False))
    
    print("\n" + "-"*80)
    print("Formato LaTeX (para manuscrito):")
    print("-"*80)
    
    latex_table = """
\\begin{table}[ht]
\\centering
\\caption{Comparações múltiplas entre tratamentos (teste de Mann-Whitney U com correção de Bonferroni).}
\\label{tab:comparacoes}
\\begin{tabular}{lcccccc}
\\hline
\\textbf{Comparação} & \\textbf{Mediana 1} & \\textbf{Mediana 2} & \\textbf{\\textit{p}-valor} & \\textbf{\\textit{p}-corrigido} & \\textbf{Cohen's \\textit{d}} & \\textbf{Significativo$^a$} \\\\
\\hline
"""
    
    for _, row in df_tabela.iterrows():
        sig_symbol = r"$\checkmark$" if row['Significativo'] == 'Sim' else "--"
        cohen_col = "Cohen's d"
        cohen_text = f"{row[cohen_col]} ({row['Efeito']})"
        latex_line = f"{row['Comparação']} & {row['Mediana1']} & {row['Mediana2']} & {row['p-valor']} & {row['p-corrigido']} & {cohen_text} & {sig_symbol} "
        latex_table += latex_line + r"\\" + "\n"
    
    latex_table += """\\hline
\\end{tabular}
\\begin{tablenotes}
\\small
\\item $^a$ Significativo ao nível $\\alpha = 0.05$ após correção de Bonferroni.
\\item Interpretação de Cohen's \\textit{d}: pequeno ($|d| < 0.5$), médio ($0.5 \\leq |d| < 0.8$), grande ($|d| \\geq 0.8$).
\\end{tablenotes}
\\end{table}
"""
    
    print(latex_table)
    
    return df_tabela


def gerar_tabela_modelos():
    """Gera tabela resumindo resultados dos modelos GLM e GEE."""
    
    print("\n" + "="*80)
    print("TABELA 3: Resumo dos Modelos Estatísticos (GLM e GEE)")
    print("="*80)
    
    # Dados dos modelos (extraídos da saída anterior)
    modelo_data = {
        'Variável': [
            'Intercepto',
            'T1 vs T0',
            'T2 vs T0',
            'T3 vs T0',
            'Tempo (dias)',
            'T1 × Tempo',
            'T2 × Tempo',
            'T3 × Tempo'
        ],
        'GLM Coef.': [10.76, 10.72, 5.51, 21.66, -0.050, -0.053, -0.024, -0.085],
        'GLM p': ['<0.001', '<0.001', '0.058', '<0.001', '0.004', '0.035', '0.337', '0.001'],
        'GEE Coef.': [14.99, 5.20, 3.01, 12.77, -0.091, '--', '--', '--'],
        'GEE p': ['<0.001', '<0.001', '0.004', '<0.001', '<0.001', '--', '--', '--']
    }
    
    df_modelos = pd.DataFrame(modelo_data)
    
    print("\nFormato Markdown:")
    print(df_modelos.to_markdown(index=False))
    
    print("\n" + "-"*80)
    print("Formato LaTeX (para manuscrito):")
    print("-"*80)
    
    latex_table = """
\\begin{table}[ht]
\\centering
\\caption{Coeficientes e significância dos modelos GLM (com interação) e GEE (longitudinal).}
\\label{tab:modelos}
\\begin{tabular}{lcccc}
\\hline
\\textbf{Variável} & \\textbf{GLM Coef.} & \\textbf{GLM \\textit{p}} & \\textbf{GEE Coef.} & \\textbf{GEE \\textit{p}} \\\\
\\hline
Intercepto          & 10.76  & <0.001 & 14.99  & <0.001 \\\\
T1 vs T0            & 10.72  & <0.001 &  5.20  & <0.001 \\\\
T2 vs T0            &  5.51  & 0.058  &  3.01  & 0.004  \\\\
T3 vs T0            & 21.66  & <0.001 & 12.77  & <0.001 \\\\
Tempo (dias)        & -0.050 & 0.004  & -0.091 & <0.001 \\\\
T1 $\\times$ Tempo  & -0.053 & 0.035  & --     & --     \\\\
T2 $\\times$ Tempo  & -0.024 & 0.337  & --     & --     \\\\
T3 $\\times$ Tempo  & -0.085 & 0.001  & --     & --     \\\\
\\hline
\\end{tabular}
\\begin{tablenotes}
\\small
\\item GLM = Modelo Linear Generalizado (família Gaussiana); GEE = Equações de Estimação Generalizadas (estrutura de covariância exchangeable).
\\item O modelo GEE não inclui termos de interação (análise de efeitos principais).
\\item Coeficientes em MPa; Tempo em dias.
\\end{tablenotes}
\\end{table}
"""
    
    print(latex_table)
    
    return df_modelos


def salvar_tabelas():
    """Salva todas as tabelas em arquivos."""
    
    output_dir = Path(__file__).parent.parent / 'processed_data' / 'analise_estatistica'
    
    # Gerar e salvar tabelas
    desc = gerar_tabela_descritiva()
    comp = gerar_tabela_comparacoes()
    modelos = gerar_tabela_modelos()
    
    # Salvar versões Markdown
    with open(output_dir / 'tabela1_descritiva.md', 'w', encoding='utf-8') as f:
        f.write("# Tabela 1: Estatísticas Descritivas\n\n")
        f.write(desc.to_markdown(index=False))
    
    with open(output_dir / 'tabela2_comparacoes.md', 'w', encoding='utf-8') as f:
        f.write("# Tabela 2: Comparações Múltiplas\n\n")
        f.write(comp.to_markdown(index=False))
    
    with open(output_dir / 'tabela3_modelos.md', 'w', encoding='utf-8') as f:
        f.write("# Tabela 3: Modelos Estatísticos\n\n")
        f.write(modelos.to_markdown(index=False))
    
    print("\n" + "="*80)
    print("TABELAS SALVAS")
    print("="*80)
    print(f"\nLocal: {output_dir}")
    print("\nArquivos gerados:")
    print("  - tabela1_descritiva.md")
    print("  - tabela2_comparacoes.md")
    print("  - tabela3_modelos.md")


if __name__ == "__main__":
    salvar_tabelas()
