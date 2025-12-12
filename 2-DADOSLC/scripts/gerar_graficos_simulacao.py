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

# --- Gráfico 2: Modelo de Dano (Paris-Erdoğan Modificado) ---
def plot_damage(lang='pt'):
    # Parâmetros
    beta = 3.40
    # VUF (D=0.1)
    vuf_nat = 42 # dias
    vuf_trat = 95 # dias
    
    # Calcular eta característico para cada condição
    factor = (-np.log(0.9))**(1/beta)
    eta_nat = vuf_nat / factor
    eta_trat = vuf_trat / factor
    
    t = np.linspace(0, 150, 200)
    
    # Modelo de Dano: D(t) = 1 - exp(-(t/eta)^beta)
    D_nat = 1 - np.exp(-(t/eta_nat)**beta)
    D_trat = 1 - np.exp(-(t/eta_trat)**beta)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Textos por idioma
    if lang == 'pt':
        label_nat = 'Natural (T0)'
        label_trat = 'Tratado NaOH 6% (T2)'
        label_crit = 'Critério de Falha (\{{10}}\$)'
        label_gain = 'Ganho de Vida Útil'
        text_vuf_nat = f'VUF $\\approx$ {vuf_nat} dias'
        text_vuf_trat = f'VUF $\\approx$ {vuf_trat} dias'
        xlabel = 'Tempo de Exposição (dias)'
        ylabel = 'Dano Acumulado (\\$)'
        title = 'Evolução do Dano - Modelo Híbrido'
        filename = r'c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K\3-IMAGENS\grafico_dano_hibrido.png'
    else:
        label_nat = 'Natural (T0)'
        label_trat = 'Treated NaOH 6% (T2)'
        label_crit = 'Failure Criterion (\{{10}}\$)'
        label_gain = 'Service Life Gain'
        text_vuf_nat = f'FSL $\\approx$ {vuf_nat} days'
        text_vuf_trat = f'FSL $\\approx$ {vuf_trat} days'
        xlabel = 'Exposure Time (days)'
        ylabel = 'Accumulated Damage (\\$)'
        title = 'Damage Evolution - Hybrid Model'
        filename = r'c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K\3-IMAGENS\grafico_dano_hibrido_en.png'

    ax.plot(t, D_nat, '-', color='#e74c3c', linewidth=2.5, label=label_nat)
    ax.plot(t, D_trat, '-', color='#27ae60', linewidth=2.5, label=label_trat)
    
    # Linha de Dano Crítico (VUF - 10% de falha/dano)
    ax.axhline(y=0.1, color='gray', linestyle='--', alpha=0.8, label=label_crit)
    
    # Anotações VUF
    # Interseção Natural
    idx_nat = np.abs(D_nat - 0.1).argmin()
    ax.plot(t[idx_nat], D_nat[idx_nat], 'o', color='#c0392b')
    ax.annotate(text_vuf_nat, 
                xy=(t[idx_nat], D_nat[idx_nat]), xytext=(-20, 40), 
                textcoords='offset points', arrowprops=dict(arrowstyle='->'))
    
    # Interseção Tratado
    idx_trat = np.abs(D_trat - 0.1).argmin()
    ax.plot(t[idx_trat], D_trat[idx_trat], 'o', color='#2ecc71')
    ax.annotate(text_vuf_trat, 
                xy=(t[idx_trat], D_trat[idx_trat]), xytext=(10, -40), 
                textcoords='offset points', arrowprops=dict(arrowstyle='->'))
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_ylim(0, 0.6) # Focar na região de interesse
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper left')
    
    # Preencher área de ganho
    ax.fill_between(t, D_nat, D_trat, where=(t > 10), color='gray', alpha=0.1, label=label_gain)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f'Gráfico de Dano ({lang}) gerado.')

if __name__ == '__main__':
    plot_arrhenius('pt')
    plot_arrhenius('en')
    plot_damage('pt')
    plot_damage('en')

