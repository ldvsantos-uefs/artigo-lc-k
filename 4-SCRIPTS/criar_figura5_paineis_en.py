
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from pathlib import Path
from scipy.optimize import curve_fit

# Configurações de estilo
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.figsize': (12, 10)
})

# Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "processed_data"
IMG_DIR = BASE_DIR.parent / "3-IMAGENS"
TEMP_PLOT_DIR = DATA_DIR / "plots"
TEMP_PLOT_DIR.mkdir(parents=True, exist_ok=True)

# Cores
COLORS = {
    "T0": "#1f77b4",  # azul
    "T1": "#ff7f0e",  # laranja
    "T2": "#2ca02c",  # verde
    "T3": "#d62728",  # vermelho
    "TE": "#9467bd",  # roxo
}

LABELS_EN = {
    "T0": "Control (0%)",
    "T1": "3% NaOH",
    "T2": "6% NaOH",
    "T3": "9% NaOH",
    "TE": "12% NaOH"
}

def modelo_decaimento(t, s0, k):
    return s0 * np.exp(-k * t)

def plot_degradation_curve_en():
    """Gera o painel (a) - Curva de degradação em inglês"""
    print("Gerando painel (a)...")
    
    # Carregar dados
    csv_path = DATA_DIR / "dados_tracao_agregados.csv"
    if not csv_path.exists():
        print(f"Erro: {csv_path} não encontrado.")
        return None
        
    df = pd.read_csv(csv_path)
    
    # Filtrar tratamentos relevantes (T0, T1, T2, T3)
    tratamentos = ['T0', 'T1', 'T2', 'T3']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for trat in tratamentos:
        df_trat = df[df['treatment'] == trat]
        if df_trat.empty:
            continue
            
        # Agrupar por tempo
        resumo = df_trat.groupby('dias')['uts_mpa'].agg(['mean', 'std']).reset_index()
        
        # Ajuste do modelo
        try:
            popt, _ = curve_fit(modelo_decaimento, resumo['dias'], resumo['mean'], 
                               p0=[resumo['mean'].max(), 0.01])
            s0, k = popt
            r2 = 1 - (np.sum((resumo['mean'] - modelo_decaimento(resumo['dias'], *popt))**2) / 
                      np.sum((resumo['mean'] - resumo['mean'].mean())**2))
        except:
            s0, k, r2 = 0, 0, 0
            
        # Plotar dados observados
        ax.errorbar(resumo['dias'], resumo['mean'], yerr=resumo['std'],
                   fmt='o', color=COLORS[trat], markersize=6, capsize=4,
                   label=f'{LABELS_EN[trat]} (Obs)', alpha=0.7)
                   
        # Plotar modelo
        t_plot = np.linspace(0, resumo['dias'].max()*1.1, 100)
        ax.plot(t_plot, modelo_decaimento(t_plot, s0, k), '--', 
               color=COLORS[trat], linewidth=2,
               label=f'{LABELS_EN[trat]} (Model: R²={r2:.2f})')
               
    ax.set_xlabel('Time (days)', fontweight='bold')
    ax.set_ylabel('Tensile Strength (MPa)', fontweight='bold')
    ax.set_title('Tensile Strength Degradation - Typha domingensis (NaOH)', fontweight='bold')
    ax.legend(loc='best', ncol=2)
    ax.grid(True, alpha=0.3)
    
    output_path = TEMP_PLOT_DIR / "degradacao_tracao_naoh_en.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path

def plot_stress_strain_en(days):
    """Gera painéis (b) e (c) - Curvas tensão-deformação em inglês"""
    print(f"Gerando painel para {days} dias...")
    
    csv_path = DATA_DIR / "tracao_taboa_combined.csv"
    if not csv_path.exists():
        print(f"Erro: {csv_path} não encontrado.")
        return None
        
    df = pd.read_csv(csv_path)
    
    # Converter colunas numéricas
    df['strain'] = pd.to_numeric(df['strain'], errors='coerce')
    df['stress'] = pd.to_numeric(df['stress'], errors='coerce')
    
    # Filtrar por dias
    df_day = df[df['days'] == days]
    if df_day.empty:
        print(f"Sem dados para {days} dias.")
        return None
        
    fig, ax = plt.subplots(figsize=(10, 6))
    
    tratamentos = ['T0', 'T1', 'T2', 'T3'] # TE removido para consistência com painel (a) se necessário, ou manter
    
    has_data = False
    for trat in tratamentos:
        df_trat = df_day[df_day['treatment'] == trat]
        if df_trat.empty:
            continue
            
        has_data = True
        # Plotar todas as curvas do tratamento
        # Para não poluir, vamos plotar uma linha média ou todas com alpha baixo
        # Aqui vou plotar todas com alpha baixo e uma label única
        
        # Agrupar por espécime para plotar linhas individuais
        specimens = df_trat['specimen'].unique()
        first = True
        for spec in specimens:
            df_spec = df_trat[df_trat['specimen'] == spec].sort_values('strain')
            if len(df_spec) < 2:
                continue
                
            label = LABELS_EN[trat] if first else ""
            ax.plot(df_spec['strain'], df_spec['stress'], 
                   color=COLORS[trat], alpha=0.5, linewidth=1,
                   label=label)
            if first: first = False
            
    if not has_data:
        return None
        
    ax.set_xlabel('Strain (mm/mm)', fontweight='bold')
    ax.set_ylabel('Stress (MPa)', fontweight='bold')
    ax.set_title(f'Stress vs. Strain - {days} Days', fontweight='bold')
    ax.set_ylim(0, 20) # Escala fixa conforme original
    ax.set_xlim(0, 0.15)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left')
    
    output_path = TEMP_PLOT_DIR / f"tracao_{days}dias_en.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path

def combine_panels(img_a_path, img_b_path, img_c_path):
    """Combina os 3 painéis na Figura 6 (antiga Figura 5)"""
    print("Combinando painéis...")
    
    if not all([img_a_path, img_b_path, img_c_path]):
        print("Erro: Um ou mais painéis não foram gerados.")
        return
        
    img_a = mpimg.imread(img_a_path)
    img_b = mpimg.imread(img_b_path)
    img_c = mpimg.imread(img_c_path)
    
    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])
    
    # Painel (a)
    ax0 = fig.add_subplot(gs[0, :])
    ax0.imshow(img_a)
    ax0.axis('off')
    ax0.text(0.02, 0.95, '(a)', transform=ax0.transAxes, 
             fontsize=16, fontweight='bold', va='top', ha='left',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
             
    # Painel (b)
    ax1 = fig.add_subplot(gs[1, 0])
    ax1.imshow(img_b)
    ax1.axis('off')
    ax1.text(0.02, 0.95, '(b)', transform=ax1.transAxes, 
             fontsize=16, fontweight='bold', va='top', ha='left',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
             
    # Painel (c)
    ax2 = fig.add_subplot(gs[1, 1])
    ax2.imshow(img_c)
    ax2.axis('off')
    ax2.text(0.02, 0.95, '(c)', transform=ax2.transAxes, 
             fontsize=16, fontweight='bold', va='top', ha='left',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
             
    plt.tight_layout()
    
    output_path = IMG_DIR / "figura5_paineis_ab_en.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Figura final salva em: {output_path}")
    plt.close()

def main():
    path_a = plot_degradation_curve_en()
    path_b = plot_stress_strain_en(30)
    path_c = plot_stress_strain_en(90)
    
    combine_panels(path_a, path_b, path_c)

if __name__ == "__main__":
    main()
