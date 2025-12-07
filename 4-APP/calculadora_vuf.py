import math
import argparse

def calcular_vuf(cristalinidade, tratamento_naoh, uv_index=0.5):
    """
    Calcula a Vida Útil Funcional (VUF) estimada para geotêxteis de Typha domingensis.
    
    Baseado no modelo:
    beta = -0.82 + 0.0521 * IC
    eta = f(tratamento) # Simplificado para valores tabelados do estudo
    P10 = eta * [-ln(0.90)]^(1/beta)
    
    Correção UV:
    k_efetivo = k_base * (1 + alpha * UV^gamma) -> Impacta eta inversamente
    """
    
    # Parâmetros do modelo (Tabela 2 e Regressão)
    # Beta estimado pela cristalinidade
    beta = -0.82 + 0.0521 * cristalinidade
    
    # Eta base (dias) para condições de laboratório (UV controlado)
    # Valores interpolados dos resultados experimentais
    if tratamento_naoh < 1.5: # ~0%
        eta_base = 68
    elif tratamento_naoh < 4.5: # ~3%
        eta_base = 64
    elif tratamento_naoh < 7.5: # ~6%
        eta_base = 94
    else: # ~9%
        eta_base = 92
        
    # Fator de correção ambiental (Proposto na Seção 3.4)
    # k_efetivo aumenta com UV, logo eta (vida útil) diminui
    # Assumindo eta_efetivo = eta_base / (1 + 0.2 * UV^1.5) como exemplo conservador
    fator_uv = 1 + 0.2 * (uv_index ** 1.5)
    eta_efetivo = eta_base / fator_uv
    
    # Cálculo do P10 (VUF)
    # P10 = eta * (-ln(0.9))^(1/beta)
    term = -math.log(0.90)
    p10 = eta_efetivo * (term ** (1/beta))
    
    return p10, beta, eta_efetivo

def main():
    print("=== Calculadora de VUF para Geotêxteis de Typha ===")
    print("Modelo baseado em Vidal et al. (2025)")
    print("---------------------------------------------------")
    
    try:
        ic_input = float(input("Insira o Índice de Cristalinidade (IC %) [ex: 61.2]: "))
        naoh_input = float(input("Insira a concentração de NaOH (%) [0, 3, 6, 9]: "))
        uv_input = float(input("Insira o Índice UV médio local normalizado [0.0 - 1.0]: "))
        
        vuf, beta, eta = calcular_vuf(ic_input, naoh_input, uv_input)
        
        print("\n--- Resultados Estimados ---")
        print(f"Parâmetro de Forma (Beta): {beta:.2f}")
        print(f"Vida Característica (Eta): {eta:.1f} dias")
        print(f"Vida Útil Funcional (P10): {vuf:.1f} dias")
        print("----------------------------")
        
        if vuf < 90:
            print("ALERTA: VUF inferior a 90 dias. Recomenda-se revisar o tratamento.")
        else:
            print("SUCESSO: VUF atende aos requisitos mínimos de estabelecimento vegetal.")
            
    except ValueError:
        print("Erro: Por favor, insira valores numéricos válidos.")

if __name__ == "__main__":
    main()
