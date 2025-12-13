import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da Página
st.set_page_config(
    page_title="Calculadora VUF - Geotêxteis Naturais",
    page_icon="🌿",
    layout="centered"
)

# Título e Introdução
st.title("🌿 Calculadora de Vida Útil Funcional (VUF)")
st.markdown("""
Este aplicativo implementa o **Modelo Preditivo de Degradação** para geotêxteis de *Typha domingensis*, 
baseado na recalcitrância química e parâmetros de Weibull.

**Objetivo:** Estimar a probabilidade de falha e a vida útil funcional ($P_{10}$) com base no tratamento alcalino aplicado.
""")

# Sidebar - Parâmetros de Entrada
st.sidebar.header("Parâmetros de Entrada")

modo_operacao = st.sidebar.radio(
    "Modo de Operação",
    ["Seleção de Tratamento", "Entrada Manual de Parâmetros"]
)

# Dados do Artigo (Tabela 2)
dados_base = {
    "Natural (T0)": {"beta": 2.3, "eta": 68, "LC": 0.45, "IC": 52.3},
    "NaOH 3% (T1)": {"beta": 2.5, "eta": 64, "LC": 0.52, "IC": 55.1},
    "NaOH 6% (T2)": {"beta": 2.8, "eta": 94, "LC": 0.58, "IC": 61.2},
    "NaOH 9% (T3)": {"beta": 3.0, "eta": 92, "LC": 0.62, "IC": 63.8}
}

if modo_operacao == "Seleção de Tratamento":
    tratamento = st.sidebar.selectbox(
        "Selecione o Tratamento Alcalino",
        list(dados_base.keys()),
        index=2 # Default T2
    )
    params = dados_base[tratamento]
    beta = params["beta"]
    eta = params["eta"]
    st.sidebar.info(f"**Parâmetros do Modelo:**\n\n$\\beta$ (Forma): {beta}\n\n$\\eta$ (Escala): {eta} dias")

else:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Parâmetros de Weibull")
    beta = st.sidebar.number_input("Parâmetro de Forma ($\\beta$)", min_value=1.0, max_value=5.0, value=2.8, step=0.1)
    eta = st.sidebar.number_input("Parâmetro de Escala ($\\eta$)", min_value=10.0, max_value=200.0, value=94.0, step=1.0)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Estimativa via Composição (Experimental)")
    ic_input = st.sidebar.number_input("Índice de Cristalinidade (%)", 40.0, 80.0, 61.2)
    # Equação do artigo: beta = -0.82 + 0.0521 * IC
    beta_est = -0.82 + 0.0521 * ic_input
    st.sidebar.caption(f"$\\beta$ estimado via IC: {beta_est:.2f}")

# Cálculos do Modelo
def calcular_confiabilidade(t, beta, eta):
    return np.exp(- (t / eta) ** beta)

def calcular_p10(beta, eta):
    # P10 = tempo para 10% de falha (R(t) = 0.90)
    # 0.90 = exp(-(t/eta)^beta) -> ln(0.90) = -(t/eta)^beta -> -ln(0.90) = (t/eta)^beta
    # t = eta * (-ln(0.90))^(1/beta)
    return eta * (-np.log(0.90)) ** (1/beta)

def calcular_p90(beta, eta):
    # P90 = tempo para 90% de falha (R(t) = 0.10)
    return eta * (-np.log(0.10)) ** (1/beta)

vuf_p10 = calcular_p10(beta, eta)
vida_final_p90 = calcular_p90(beta, eta)

# Exibição dos Resultados Principais
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Vida Útil Funcional ($P_{10}$)", value=f"{vuf_p10:.1f} dias", delta="Janela Crítica > 90d")
with col2:
    st.metric(label="Vida Característica ($\\eta$)", value=f"{eta:.1f} dias")
with col3:
    st.metric(label="Falha Quase Certa ($P_{90}$)", value=f"{vida_final_p90:.1f} dias")

# Gráfico de Confiabilidade
st.subheader("Curva de Confiabilidade $R(t)$")

t_max = int(vida_final_p90 * 1.2)
t = np.linspace(0, t_max, 200)
R_t = calcular_confiabilidade(t, beta, eta)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, R_t, label=f'Modelo Weibull ($\\beta$={beta}, $\\eta$={eta})', color='green', linewidth=2)

# Linhas de referência
ax.axvline(vuf_p10, color='blue', linestyle='--', alpha=0.6, label=f'VUF ($P_{{10}}$): {vuf_p10:.1f} dias')
ax.axhline(0.90, color='blue', linestyle=':', alpha=0.4)

ax.axvline(90, color='red', linestyle='-.', alpha=0.5, label='Requisito Mínimo (90 dias)')

# Formatação
ax.set_xlabel("Tempo de Exposição (dias)")
ax.set_ylabel("Confiabilidade $R(t)$")
ax.set_title("Probabilidade de Sobrevivência do Geotêxtil")
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 1.05)
ax.set_xlim(0, t_max)

st.pyplot(fig)

# Interpretação
st.subheader("Interpretação Técnica")
if vuf_p10 >= 90:
    st.success(f"""
    ✅ **Aprovado para Bioengenharia:** O material mantém confiabilidade superior a 90% por {vuf_p10:.1f} dias.
    Isso atende à janela crítica de 90-120 dias necessária para o estabelecimento da vegetação.
    """)
else:
    st.warning(f"""
    ⚠️ **Atenção:** A Vida Útil Funcional ({vuf_p10:.1f} dias) é inferior ao requisito de 90 dias.
    Recomenda-se utilizar um tratamento com maior teor de NaOH ou aumentar o Fator de Segurança.
    """)

# Rodapé
st.markdown("---")
st.caption("Desenvolvido como parte do estudo: *Modelagem Probabilística da Degradação de Geotêxteis Naturais*")
