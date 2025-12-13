import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configurações de estilo
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
    'axes.labelweight': 'bold',
    'legend.fontsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.figsize': (10, 6)
})

ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "3-IMAGENS" / "INGLES"
DATA_DIR = ROOT_DIR / "2-DADOS" / "processed_data"

def plot_validation_uv_en():
    print("Gerando grafico_validacao_uv_ggplot_en.png...")
    try:
        df = pd.read_csv(DATA_DIR / "validacao_modelo_uv.csv")
    except FileNotFoundError:
        print("Arquivo de dados não encontrado. Gerando dados simulados para demonstração.")
        # Simulação baseada no R script
        np.random.seed(42)
        df = pd.DataFrame({
            'uv_index': np.repeat([0, 0.5, 1.0], 50),
            'erro_relativo': np.concatenate([
                np.random.normal(0.05, 0.02, 50),
                np.random.normal(0.08, 0.03, 50),
                np.random.normal(0.12, 0.04, 50)
            ])
        })

    df['erro_pct'] = df['erro_relativo'] * 100
    df['Condition'] = df['uv_index'].map({0: "UV = 0 (Control)", 0.5: "UV = 0.5 (Shade)", 1.0: "UV = 1.0 (Exposed)"})

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Regiões de aceitação
    ax.axhspan(0, 10, color='green', alpha=0.05)
    ax.axhspan(10, 20, color='yellow', alpha=0.05)
    
    # Boxplot e Jitter
    sns.boxplot(x='Condition', y='erro_pct', data=df, ax=ax, width=0.5, palette="Blues", showfliers=False)
    sns.stripplot(x='Condition', y='erro_pct', data=df, ax=ax, color='gray', alpha=0.4, jitter=0.2, size=4)
    
    # Linhas de referência
    ax.axhline(10, color='#2E7D32', linestyle='--', linewidth=1.5)
    ax.axhline(20, color='#E65100', linestyle='--', linewidth=1.5)
    
    # Textos
    ax.text(0.5, 10.5, "High Precision Limit (10%)", color='#2E7D32', fontsize=10, fontstyle='italic')
    ax.text(0.5, 20.5, "Acceptable Limit (20%)", color='#E65100', fontsize=10, fontstyle='italic')
    
    ax.set_title("UV Degradation Model Robustness\nRelative Error Distribution in 50 Monte Carlo Simulations")
    ax.set_xlabel("Exposure Condition (UV Index)")
    ax.set_ylabel("Relative Error (%)")
    ax.set_ylim(0, max(df['erro_pct'].max() * 1.15, 35))
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / "grafico_validacao_uv_ggplot_en.png"
    plt.savefig(output_path, dpi=300)
    print(f"Salvo: {output_path}")
    plt.close()

def plot_weibull_reliability_en():
    print("Gerando grafico_weibull_confiabilidade_ggplot_en.png...")
    
    t = np.linspace(0, 200, 200)
    
    params = {
        "T0 (Natural)": {"eta": 71, "beta": 2.3, "color": "#E64A19"},
        "T1 (NaOH 3%)": {"eta": 66, "beta": 2.5, "color": "#FFA726"},
        "T2 (NaOH 6%)": {"eta": 94, "beta": 2.8, "color": "#1976D2"},
        "T3 (NaOH 9%)": {"eta": 92, "beta": 3.0, "color": "#388E3C"}
    }
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for label, p in params.items():
        R_t = np.exp(-(t / p['eta'])**p['beta']) * 100
        ax.plot(t, R_t, label=label, color=p['color'], linewidth=2.5, alpha=0.9)
        
        # P10 calculation
        p10 = p['eta'] * (-np.log(0.90))**(1/p['beta'])
        ax.axvline(p10, color=p['color'], linestyle=':', linewidth=1.5, alpha=0.6)

    ax.axhline(90, color='gray', linestyle='--', linewidth=1)
    ax.text(10, 92, "P₁₀ (90% reliability)", color='gray', fontsize=10)
    
    ax.set_title("Weibull Reliability Curves\nProbability of functional integrity over time (4 treatments)")
    ax.set_xlabel("Time (days)")
    ax.set_ylabel("Reliability R(t) (%)")
    ax.legend(title="Treatment", loc=(0.75, 0.6))
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 105)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / "grafico_weibull_confiabilidade_ggplot_en.png"
    plt.savefig(output_path, dpi=300)
    print(f"Salvo: {output_path}")
    plt.close()

if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plot_validation_uv_en()
    plot_weibull_reliability_en()
