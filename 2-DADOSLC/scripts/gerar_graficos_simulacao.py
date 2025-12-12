import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# Configuração de estilo para publicação
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 16
})

# --- Gráfico 1: Plot de Arrhenius ---
def plot_arrhenius(lang='pt'):
    # Dados
    T_celsius = np.array([26, 40])
    T_kelvin = T_celsius + 273.15
    k_values = np.array([0.0118, 0.0199])
    
    inv_T = 1000 / T_kelvin
    ln_k = np.log(k_values)
    
    # Fit linear
    slope, intercept = np.polyfit(inv_T, ln_k, 1)
    x_fit = np.linspace(3.15, 3.40, 100)
    y_fit = slope * x_fit + intercept
    
    # Cálculo da Ea para conferência
    R = 8.314
    Ea_calc = -slope * 1000 * 8.314 / 1000 # kJ/mol
    
    fig, ax = plt.subplots(figsize=(7, 6))
    
    # Textos por idioma
    if lang == 'pt':
        label_exp = 'Pontos Experimentais'
        label_fit = 'Ajuste de Arrhenius'
        text_field = f'Campo (26°C)\nk={k_values[0]}'
        text_chamber = f'Câmara (40°C)\nk={k_values[1]}'
        title = 'Calibração da Energia de Ativação'
        filename = r'c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K\3-IMAGENS\grafico_arrhenius.png'
    else:
        label_exp = 'Experimental Points'
        label_fit = 'Arrhenius Fit'
        text_field = f'Field (26°C)\nk={k_values[0]}'
        text_chamber = f'Chamber (40°C)\nk={k_values[1]}'
        title = 'Activation Energy Calibration'
        filename = r'c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K\3-IMAGENS\grafico_arrhenius_en.png'

    # Pontos experimentais
    ax.plot(inv_T, ln_k, 'o', color='black', markersize=10, label=label_exp, zorder=5)
    
    # Linha de ajuste
    ax.plot(x_fit, y_fit, '--', color='#2c3e50', linewidth=2, label=label_fit)
    
    # Anotações
    ax.annotate(text_field, 
                xy=(inv_T[0], ln_k[0]), xytext=(10, -20), 
                textcoords='offset points', ha='left')
    
    ax.annotate(text_chamber, 
                xy=(inv_T[1], ln_k[1]), xytext=(-10, 10), 
                textcoords='offset points', ha='right')
    
    # Texto Ea
    ax.text(3.25, -4.2, f'\ = {Ea_calc:.2f}\$ kJ/mol', fontsize=14, 
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    
    ax.set_xlabel('\/T\$ (K\python{{-1}}\$)')
    ax.set_ylabel('\$\ln(k)\$')
    ax.set_title(title)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    
    # Inverter eixo X (temperatura aumenta para a esquerda em plots 1/T)
    ax.invert_xaxis()
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f'Gráfico Arrhenius ({lang}) gerado. Ea calculada: {Ea_calc:.2f} kJ/mol')

# --- Gráfico 2: Modelo de Dano (Paris-Erdoğan Modificado) com todas as proporções ---
def plot_damage(lang='pt'):
    # Parâmetros de Weibull para cada tratamento (dados reais)
    # T0 (Natural): β=2.3, η=68 dias, VUF=42 dias
    # T1 (3% NaOH): β=2.5, η=80 dias, VUF=60 dias (interpolado)
    # T2 (6% NaOH): β=2.8, η=94 dias, VUF=95 dias
    # T3 (9% NaOH): β=3.0, η=92 dias, VUF=108 dias
    
    treatments = {
        'T0': {'beta': 2.3, 'eta': 68, 'vuf': 42, 'color': '#e74c3c', 'label_pt': 'Natural (T0)', 'label_en': 'Natural (T0)'},
        'T1': {'beta': 2.5, 'eta': 80, 'vuf': 60, 'color': '#f39c12', 'label_pt': 'NaOH 3% (T1)', 'label_en': 'NaOH 3% (T1)'},
        'T2': {'beta': 2.8, 'eta': 94, 'vuf': 95, 'color': '#27ae60', 'label_pt': 'NaOH 6% (T2)', 'label_en': 'NaOH 6% (T2)'},
        'T3': {'beta': 3.0, 'eta': 92, 'vuf': 108, 'color': '#2980b9', 'label_pt': 'NaOH 9% (T3)', 'label_en': 'NaOH 9% (T3)'},
    }
    
    t = np.linspace(0, 150, 200)
    
    fig, ax = plt.subplots(figsize=(10, 6.5))
    
    # Textos por idioma
    if lang == 'pt':
        label_crit = r'Critério de Falha ($P_{10}$)'
        xlabel = 'Tempo de Exposição (dias)'
        ylabel = r'Dano Acumulado ($D$)'
        title = 'Evolução do Dano - Modelo Híbrido (Todas as Proporções)'
        filename = r'c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K\3-IMAGENS\grafico_dano_hibrido.png'
    else:
        label_crit = r'Failure Criterion ($P_{10}$)'
        xlabel = 'Exposure Time (days)'
        ylabel = r'Accumulated Damage ($D$)'
        title = 'Damage Evolution - Hybrid Model (All Treatment Levels)'
        filename = r'c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K\3-IMAGENS\grafico_dano_hibrido_en.png'

    # Plotar cada tratamento
    for treatment_id in ['T0', 'T1', 'T2', 'T3']:
        params = treatments[treatment_id]
        beta = params['beta']
        eta = params['eta']
        
        # Modelo de Dano: D(t) = 1 - exp(-(t/eta)^beta)
        D = 1 - np.exp(-(t/eta)**beta)
        
        # Label baseado no idioma
        label = params['label_pt'] if lang == 'pt' else params['label_en']
        
        ax.plot(t, D, '-', color=params['color'], linewidth=2.5, label=label)
        
        # Marcar o ponto VUF (10% de dano)
        vuf = params['vuf']
        D_at_vuf = 1 - np.exp(-(vuf/eta)**beta)
        ax.plot(vuf, D_at_vuf, 'o', color=params['color'], markersize=8, zorder=5)
        
        # Anotação do VUF
        if lang == 'pt':
            text_vuf = f"VUF ≈ {vuf} d"
        else:
            text_vuf = f"FSL ≈ {vuf} d"
        
        # Posicionar anotações para evitar sobreposição
        if treatment_id == 'T0':
            xytext = (-15, 25)
        elif treatment_id == 'T1':
            xytext = (-15, 5)
        elif treatment_id == 'T2':
            xytext = (10, -35)
        else:  # T3
            xytext = (15, -20)
        
        ax.annotate(text_vuf, 
                    xy=(vuf, D_at_vuf), 
                    xytext=xytext,
                    textcoords='offset points', 
                    arrowprops=dict(arrowstyle='->', color=params['color'], lw=1.5),
                    fontsize=10)
    
    # Linha de Dano Crítico (10% de falha)
    ax.axhline(y=0.1, color='gray', linestyle='--', alpha=0.8, linewidth=1.5, label=label_crit)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_ylim(0, 0.6)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper left', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f'Gráfico de Dano ({lang}) gerado com todas as proporções.')

if __name__ == '__main__':
    plot_arrhenius('pt')
    plot_arrhenius('en')
    plot_damage('pt')
    plot_damage('en')

