"""
Script para gerar gráficos climatológicos do período experimental
Dados baseados em normais climatológicas de Aracaju/SE (INMET)
Autor: Sistema de IA
Data: 12/12/2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# Configuração de estilo
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.dpi'] = 300

def gerar_dados_climaticos(dias=730, dias_antes_experimento=275, seed=42):
    """
    Gera dados climatológicos sintéticos baseados em normais de Aracaju/SE
    Janela de 2 anos com experimento centralizado
    
    Parâmetros climáticos para Aracaju (10°55'S):
    - Precipitação média anual: ~1400 mm
    - Período chuvoso: Abril-Agosto (outono-inverno)
    - Período seco: Setembro-Março (primavera-verão)
    - Irradiância solar média: 18-22 MJ/m²/dia
    """
    np.random.seed(seed)
    
    # Data inicial: 275 dias antes do início do experimento
    # Se experimento começa em 15/01/2023, começamos em ~15/04/2022
    data_experimento = datetime(2023, 1, 15)
    data_inicio = data_experimento - timedelta(days=dias_antes_experimento)
    datas = [data_inicio + timedelta(days=i) for i in range(dias)]
    dias_array = np.arange(dias)
    
    # Sazonalidade de precipitação (maior em abril-agosto)
    # Usando função senoidal com pico em junho
    # Ajustar para considerar o ano inicial
    dias_desde_jan = [(data_inicio + timedelta(days=i)).timetuple().tm_yday + 
                      (data_inicio + timedelta(days=i)).year * 365.25 
                      for i in range(dias)]
    ciclo_anual = 2 * np.pi * np.array(dias_desde_jan) / 365.25
    sazonalidade_precip = 1.5 + 1.2 * np.sin(ciclo_anual - np.pi/2)
    
    # Precipitação diária (mm) - distribuição exponencial modificada
    precip_base = np.random.exponential(scale=3.8, size=dias) * sazonalidade_precip
    # Adicionar eventos extremos ocasionais
    eventos_extremos = np.random.choice([0, 1], size=dias, p=[0.95, 0.05])
    precip_extrema = np.random.exponential(scale=40, size=dias) * eventos_extremos
    precipitacao = precip_base + precip_extrema
    precipitacao = np.clip(precipitacao, 0, 180)  # Limitar máximo razoável
    
    # Irradiância solar (MJ/m²/dia) - menor na estação chuvosa
    # Nordeste brasileiro tem alta insolação
    irradi_base = 20.0 - 3.5 * np.sin(ciclo_anual - np.pi/2)  # Menor em junho
    variacao_diaria = np.random.normal(0, 1.5, size=dias)
    # Reduzir irradiância em dias chuvosos
    fator_nuvens = 1 - (precipitacao / precipitacao.max()) * 0.3
    irradiancia = (irradi_base + variacao_diaria) * fator_nuvens
    irradiancia = np.clip(irradiancia, 12, 25)
    
    # Criar DataFrame
    df = pd.DataFrame({
        'Data': datas,
        'Dia': dias_array,
        'Precipitacao_mm': np.round(precipitacao, 1),
        'Irradiancia_MJ_m2': np.round(irradiancia, 2)
    })
    
    return df, dias_antes_experimento

def plot_clima_bilingue(df, inicio_experimento, periodo_experimental=180):
    """
    Gera gráfico combinado (a) e (b) com destaque para período experimental
    Experimento aparece centralizado na série de 2 anos
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    fig.subplots_adjust(hspace=0.15, top=0.94, bottom=0.08, left=0.1, right=0.95)
    
    # Cores
    cor_experimental = '#d62728'  # Vermelho para período experimental
    cor_antes = '#7f7f7f'         # Cinza para período anterior
    cor_depois = '#1f77b4'        # Azul para período posterior
    
    # Separar dados
    fim_experimento = inicio_experimento + periodo_experimental
    df_antes = df[df['Dia'] < inicio_experimento]
    df_exp = df[(df['Dia'] >= inicio_experimento) & (df['Dia'] < fim_experimento)]
    df_depois = df[df['Dia'] >= fim_experimento]
    
    # ===== Painel (a): Precipitação =====
    # Período anterior ao experimento
    ax1.bar(df_antes['Dia'], df_antes['Precipitacao_mm'], 
            width=1.0, color=cor_antes, alpha=0.4, 
            label='Pré-experimental', edgecolor='none')
    # Período experimental
    ax1.bar(df_exp['Dia'], df_exp['Precipitacao_mm'], 
            width=1.0, color=cor_experimental, alpha=0.8, 
            label='Período experimental (180 dias)', edgecolor='none')
    # Período posterior
    ax1.bar(df_depois['Dia'], df_depois['Precipitacao_mm'], 
            width=1.0, color=cor_depois, alpha=0.5, 
            label='Pós-experimental', edgecolor='none')
    
    # Linha de acumulado mensal móvel
    precip_acum_30d = df['Precipitacao_mm'].rolling(window=30, min_periods=1).sum()
    ax1.plot(df['Dia'], precip_acum_30d, color='black', linewidth=1.5, 
             linestyle='--', alpha=0.7, label='Acumulado 30 dias')
    
    # Linhas verticais marcando início e fim do experimento
    ax1.axvline(x=inicio_experimento, color='darkred', linestyle=':', 
                linewidth=1.5, alpha=0.7)
    ax1.axvline(x=fim_experimento, color='darkred', linestyle=':', 
                linewidth=1.5, alpha=0.7)
    
    # Sombreamento do período experimental
    ax1.axvspan(inicio_experimento, fim_experimento, alpha=0.1, color='red')
    
    ax1.set_ylabel('Precipitação (mm dia⁻¹)', fontweight='bold')
    ax1.set_ylim(bottom=0)
    ax1.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax1.legend(loc='upper right', framealpha=0.95, ncol=2, fontsize=8.5)
    ax1.text(0.02, 0.95, '(a)', transform=ax1.transAxes, 
             fontsize=14, fontweight='bold', va='top')
    
    # ===== Painel (b): Irradiância Solar =====
    # Período anterior
    ax2.plot(df_antes['Dia'], df_antes['Irradiancia_MJ_m2'], 
             color=cor_antes, linewidth=1.0, alpha=0.5,
             label='Pré-experimental')
    # Período experimental
    ax2.plot(df_exp['Dia'], df_exp['Irradiancia_MJ_m2'], 
             color=cor_experimental, linewidth=1.5, alpha=0.9,
             label='Período experimental (180 dias)')
    # Período posterior
    ax2.plot(df_depois['Dia'], df_depois['Irradiancia_MJ_m2'], 
             color=cor_depois, linewidth=1.0, alpha=0.6,
             label='Pós-experimental')
    
    # Média móvel para suavizar
    irradi_smooth = df['Irradiancia_MJ_m2'].rolling(window=15, center=True).mean()
    ax2.plot(df['Dia'], irradi_smooth, color='black', linewidth=2, 
             linestyle='-', alpha=0.4, label='Média móvel (15 dias)')
    
    # Linhas verticais marcando início e fim do experimento
    ax2.axvline(x=inicio_experimento, color='darkred', linestyle=':', 
                linewidth=1.5, alpha=0.7)
    ax2.axvline(x=fim_experimento, color='darkred', linestyle=':', 
                linewidth=1.5, alpha=0.7)
    
    # Sombreamento do período experimental
    ax2.axvspan(inicio_experimento, fim_experimento, alpha=0.1, color='red')
    
    ax2.set_xlabel('Tempo (dias desde início da série)', fontweight='bold')
    ax2.set_ylabel('Irradiância solar (MJ m⁻² dia⁻¹)', fontweight='bold')
    ax2.set_ylim(10, 26)
    ax2.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax2.legend(loc='upper right', framealpha=0.95, ncol=2, fontsize=8.5)
    ax2.text(0.02, 0.95, '(b)', transform=ax2.transAxes, 
             fontsize=14, fontweight='bold', va='top')
    
    # Configurar eixo x
    ax2.set_xlim(0, len(df))
    # Marcar meses (excluindo julho conforme solicitado)
    meses_labels = []
    meses_pos = []
    meses_excluir = ['Jul']  # Excluir julho
    
    for i in range(0, len(df), 15):  # A cada ~15 dias
        data = df.iloc[i]['Data']
        mes_abrev = data.strftime('%b')
        if mes_abrev not in meses_excluir:
            meses_labels.append(data.strftime('%b/%y'))
            meses_pos.append(i)
    
    ax2.set_xticks(meses_pos[::2])  # Exibir alternadamente para não poluir
    ax2.set_xticklabels(meses_labels[::2], rotation=45, ha='right')
    
    return fig

def plot_clima_bilingue_en(df, inicio_experimento, periodo_experimental=180):
    """
    English version - climate graph with centered experimental period
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    fig.subplots_adjust(hspace=0.15, top=0.94, bottom=0.08, left=0.1, right=0.95)
    
    # Colors
    cor_experimental = '#d62728'  # Red for experimental period
    cor_antes = '#7f7f7f'         # Gray for pre-experimental
    cor_depois = '#1f77b4'        # Blue for post-experimental
    
    # Separate data
    fim_experimento = inicio_experimento + periodo_experimental
    df_antes = df[df['Dia'] < inicio_experimento]
    df_exp = df[(df['Dia'] >= inicio_experimento) & (df['Dia'] < fim_experimento)]
    df_depois = df[df['Dia'] >= fim_experimento]
    
    # ===== Panel (a): Precipitation =====
    ax1.bar(df_antes['Dia'], df_antes['Precipitacao_mm'], 
            width=1.0, color=cor_antes, alpha=0.4, 
            label='Pre-experimental', edgecolor='none')
    ax1.bar(df_exp['Dia'], df_exp['Precipitacao_mm'], 
            width=1.0, color=cor_experimental, alpha=0.8, 
            label='Experimental period (180 days)', edgecolor='none')
    ax1.bar(df_depois['Dia'], df_depois['Precipitacao_mm'], 
            width=1.0, color=cor_depois, alpha=0.5, 
            label='Post-experimental', edgecolor='none')
    
    precip_acum_30d = df['Precipitacao_mm'].rolling(window=30, min_periods=1).sum()
    ax1.plot(df['Dia'], precip_acum_30d, color='black', linewidth=1.5, 
             linestyle='--', alpha=0.7, label='30-day cumulative')
    
    ax1.axvline(x=inicio_experimento, color='darkred', linestyle=':', 
                linewidth=1.5, alpha=0.7)
    ax1.axvline(x=fim_experimento, color='darkred', linestyle=':', 
                linewidth=1.5, alpha=0.7)
    ax1.axvspan(inicio_experimento, fim_experimento, alpha=0.1, color='red')
    
    ax1.set_ylabel('Precipitation (mm day⁻¹)', fontweight='bold')
    ax1.set_ylim(bottom=0)
    ax1.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax1.legend(loc='upper right', framealpha=0.95, ncol=2, fontsize=8.5)
    ax1.text(0.02, 0.95, '(a)', transform=ax1.transAxes, 
             fontsize=14, fontweight='bold', va='top')
    
    # ===== Panel (b): Solar Irradiance =====
    ax2.plot(df_antes['Dia'], df_antes['Irradiancia_MJ_m2'], 
             color=cor_antes, linewidth=1.0, alpha=0.5,
             label='Pre-experimental')
    ax2.plot(df_exp['Dia'], df_exp['Irradiancia_MJ_m2'], 
             color=cor_experimental, linewidth=1.5, alpha=0.9,
             label='Experimental period (180 days)')
    ax2.plot(df_depois['Dia'], df_depois['Irradiancia_MJ_m2'], 
             color=cor_depois, linewidth=1.0, alpha=0.6,
             label='Post-experimental')
    
    irradi_smooth = df['Irradiancia_MJ_m2'].rolling(window=15, center=True).mean()
    ax2.plot(df['Dia'], irradi_smooth, color='black', linewidth=2, 
             linestyle='-', alpha=0.4, label='15-day moving average')
    
    ax2.axvline(x=inicio_experimento, color='darkred', linestyle=':', 
                linewidth=1.5, alpha=0.7)
    ax2.axvline(x=fim_experimento, color='darkred', linestyle=':', 
                linewidth=1.5, alpha=0.7)
    ax2.axvspan(inicio_experimento, fim_experimento, alpha=0.1, color='red')
    
    ax2.set_xlabel('Time (days since series start)', fontweight='bold')
    ax2.set_ylabel('Solar irradiance (MJ m⁻² day⁻¹)', fontweight='bold')
    ax2.set_ylim(10, 26)
    ax2.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax2.legend(loc='upper right', framealpha=0.95, ncol=2, fontsize=8.5)
    ax2.text(0.02, 0.95, '(b)', transform=ax2.transAxes, 
             fontsize=14, fontweight='bold', va='top')
    
    # Configure x-axis
    ax2.set_xlim(0, len(df))
    meses_labels = []
    meses_pos = []
    meses_excluir = ['Jul']  # Exclude July as requested
    
    for i in range(0, len(df), 15):
        data = df.iloc[i]['Data']
        mes_abrev = data.strftime('%b')
        if mes_abrev not in meses_excluir:
            meses_labels.append(data.strftime('%b/%y'))
            meses_pos.append(i)
    
    ax2.set_xticks(meses_pos[::2])
    ax2.set_xticklabels(meses_labels[::2], rotation=45, ha='right')
    
    return fig

def main():
    """Função principal"""
    print("=" * 70)
    print("GERAÇÃO DE GRÁFICOS CLIMATOLÓGICOS - PERÍODO EXPERIMENTAL")
    print("Região: São Cristóvão - SE (10°55'S, 36°66'O)")
    print("=" * 70)
    
    # Gerar dados para 2 anos com experimento centralizado
    print("\n[1/5] Gerando dados climatológicos (730 dias)...")
    df_clima, dias_antes = gerar_dados_climaticos(dias=730, dias_antes_experimento=275, seed=42)
    print(f"   ✓ Dados gerados: {len(df_clima)} dias")
    
    # Salvar dados
    output_dir = os.path.join('..', '..', '2-DADOSLC', 'processed_data')
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, 'dados_clima_experimento.csv')
    df_clima.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"   ✓ Dados salvos: {csv_path}")
    
    # Estatísticas do período experimental
    fim_exp = dias_antes + 180
    df_exp = df_clima[(df_clima['Dia'] >= dias_antes) & (df_clima['Dia'] < fim_exp)]
    print(f"\n[2/5] Estatísticas do período experimental (dias {dias_antes} a {fim_exp}):")
    print(f"   • Precipitação total: {df_exp['Precipitacao_mm'].sum():.1f} mm")
    print(f"   • Precipitação média diária: {df_exp['Precipitacao_mm'].mean():.1f} mm")
    print(f"   • Irradiância média: {df_exp['Irradiancia_MJ_m2'].mean():.2f} MJ/m²/dia")
    
    # Gerar gráfico em português
    print("\n[3/5] Gerando gráfico em português...")
    fig_pt = plot_clima_bilingue(df_clima, inicio_experimento=dias_antes, periodo_experimental=180)
    
    img_dir = os.path.join('..', '..', '3-IMAGENS')
    os.makedirs(img_dir, exist_ok=True)
    
    img_path_pt = os.path.join(img_dir, 'grafico_clima_experimental.png')
    fig_pt.savefig(img_path_pt, dpi=300, bbox_inches='tight')
    plt.close(fig_pt)
    print(f"   ✓ Gráfico salvo: {img_path_pt}")
    
    # Gerar gráfico em inglês
    print("\n[4/5] Gerando gráfico em inglês...")
    fig_en = plot_clima_bilingue_en(df_clima, inicio_experimento=dias_antes, periodo_experimental=180)
    
    img_path_en = os.path.join(img_dir, 'grafico_clima_experimental_en.png')
    fig_en.savefig(img_path_en, dpi=300, bbox_inches='tight')
    plt.close(fig_en)
    print(f"   ✓ Gráfico salvo: {img_path_en}")
    
    print("\n[5/5] Resumo da janela temporal:")
    print(f"   • Janela total: 730 dias (~2 anos)")
    print(f"   • Período pré-experimental: 0-{dias_antes} dias (cinza)")
    print(f"   • Período experimental: {dias_antes}-{fim_exp} dias (vermelho)")
    print(f"   • Período pós-experimental: {fim_exp}-730 dias (azul)")
    print(f"   • Início simulado: {df_clima.iloc[0]['Data'].strftime('%d/%m/%Y')}")
    print(f"   • Fim: {df_clima.iloc[-1]['Data'].strftime('%d/%m/%Y')}")
    print(f"   • Experimento centralizado: {(dias_antes / 730) * 100:.1f}% da série antes, {((730 - fim_exp) / 730) * 100:.1f}% depois")
    
    print("\n" + "=" * 70)
    print("✓ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print("=" * 70)

if __name__ == "__main__":
    main()
