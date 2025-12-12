---
title: "Material Suplementar: Modelo Preditivo de Degradação de Geotêxteis Naturais Baseado em *Typha domingensis*"
subtitle: "Dados Complementares, Análises Estatísticas Estendidas e Protocolos Experimentais"
author: "Luiz Diego Vidal Santos, Francisco Sandro Rodrigues Holanda, et al."
lang: pt-br
geometry: margin=2.5cm
fontsize: 11pt
---

# Material Suplementar

## S1. Protocolo Experimental Detalhado

### S1.1 Caracterização Química e Física das Fibras Brutas

**Tabela S1.** Composição química média das fibras de *Typha domingensis* in natura (% massa seca).

| Componente | Teor (%) | Desvio Padrão | Método Analítico |
|:-----------|:--------:|:-------------:|:-----------------|
| Celulose | 42,5 | ± 2,1 | Van Soest modificado |
| Hemicelulose | 28,3 | ± 1,8 | Van Soest modificado |
| Lignina | 18,7 | ± 1,4 | Klason modificado |
| Extrativos | 7,2 | ± 0,9 | Soxhlet (etanol/tolueno) |
| Cinzas | 3,3 | ± 0,4 | Calcinação 550°C |
| Razão L/C | 0,44 | ± 0,03 | Calculada |
| Índice de Cristalinidade | 48,5 | ± 3,2 | DRX (método Segal) |

**Tabela S2.** Propriedades físicas das fibras não tratadas.

| Propriedade | Valor | Unidade | Método |
|:-----------|:-----:|:-------:|:-------|
| Diâmetro médio | 6,2 ± 1,3 | mm | Paquímetro digital |
| Densidade aparente | 0,87 ± 0,05 | g/cm³ | Picnometria |
| Absorção de água (24h) | 185 ± 22 | % | ASTM D570 |
| Umidade de equilíbrio | 11,2 ± 1,1 | % | Gravimetria (105°C) |
| Porosidade | 68,4 ± 4,2 | % | Calculada |

### S1.2 Condições de Tratamento Alcalino

**Tabela S3.** Parâmetros operacionais do tratamento de mercerização.

| Parâmetro | T0 (Controle) | T1 (3%) | T2 (6%) | T3 (9%) |
|:----------|:-------------:|:-------:|:-------:|:-------:|
| Concentração NaOH (w/v) | 0% | 3% | 6% | 9% |
| Molaridade (mol/L) | - | 0,75 | 1,5 | 2,25 |
| Temperatura (°C) | - | 25 ± 2 | 25 ± 2 | 25 ± 2 |
| Tempo de imersão (h) | - | 24 | 24 | 24 |
| Razão banho (L/kg) | - | 20:1 | 20:1 | 20:1 |
| pH final | - | 12,8 | 13,1 | 13,4 |
| Lavagens (ciclos) | - | 5 | 5 | 5 |
| Tempo de secagem (h) | - | 192 | 192 | 192 |

### S1.3 Protocolo de Envelhecimento Acelerado

**Tabela S4.** Parâmetros de exposição UV e condições ambientais durante ensaio de campo.

| Parâmetro | Média | Mín-Máx | Desvio Padrão |
|:----------|:-----:|:-------:|:-------------:|
| Irradiância UV (W/m²/nm, 340 nm) | 0,68 | 0,52-0,89 | ± 0,12 |
| Temperatura do ar (°C) | 28,4 | 21,2-36,7 | ± 3,8 |
| Umidade relativa (%) | 72,1 | 48-92 | ± 11,4 |
| Precipitação acumulada (mm/mês) | 87,3 | 12-186 | ± 52,1 |
| Índice UV médio | 8,2 | 6-11 | ± 1,3 |
| Velocidade do vento (m/s) | 2,1 | 0,8-4,5 | ± 0,9 |

**Figura S1.** Variação temporal das condições ambientais durante o período experimental (180 dias).

![Condições Ambientais](../3-IMAGENS/grafico_tratamentos_ggplot.png){width="85%"}

### S1.4 Calibração da Energia de Ativação

A determinação experimental da energia de ativação ($E_a$) para degradação de *Typha domingensis* foi conduzida mediante análise comparativa entre taxas de degradação em condições aceleradas (câmara UV) e condições naturais de campo, utilizando a relação de Arrhenius (Equação S1):

$$
\ln\left(\frac{k_{\text{câmara}}}{k_{\text{campo}}}\right) = \frac{E_a}{R} \left( \frac{1}{T_{\text{campo}}} - \frac{1}{T_{\text{câmara}}} \right) \tag{S1}
$$

onde $k$ representa a taxa de degradação, $R$ é a constante universal dos gases (8,314 J mol⁻¹ K⁻¹), e $T$ as temperaturas absolutas (K). O método consistiu em:

1. **Determinação de $k_{\text{câmara}}$**: Amostras de *Typha* não tratada (T0) foram expostas em câmara de degradação acelerada a 40°C (313,15 K) com irradiância UV de 0,89 W/m²/nm (340 nm). A perda de resistência à tração foi monitorada em intervalos de 6 horas durante 10 dias, ajustando-se modelo exponencial de primeira ordem: $\sigma(t) = \sigma_0 \exp(-k_{\text{câmara}} \cdot t)$. O ajuste por mínimos quadrados não-lineares forneceu $k_{\text{câmara}} = 0,0287$ dia⁻¹ ($R^2 = 0,94$).

2. **Determinação de $k_{\text{campo}}$**: Amostras idênticas foram expostas no Campus Rural da UFS (São Cristóvão-SE) durante 180 dias a temperatura média de 26°C (299,15 K) e irradiância UV de 0,68 W/m²/nm. O mesmo protocolo de ajuste resultou em $k_{\text{campo}} = 0,0170$ dia⁻¹ ($R^2 = 0,91$).

3. **Cálculo de $E_a$**: Substituindo os valores na Equação S1:

$$
\ln\left(\frac{0,0287}{0,0170}\right) = \frac{E_a}{8,314} \left( \frac{1}{299,15} - \frac{1}{313,15} \right)
$$

$$
0,5216 = \frac{E_a}{8,314} \times 1,5 \times 10^{-4}
$$

$$
E_a = 29,03 \text{ kJ/mol}
$$

Este valor posiciona *Typha* em patamar intermediário quando comparado com outras fibras lignocelulósicas: coco (*Coir*) apresenta $E_a = 42-48$ kJ/mol devido ao alto teor de lignina, enquanto juta exibe $E_a = 24-28$ kJ/mol devido à fração lignificada reduzida.

**Figura S2.** Calibração da Energia de Ativação via gráfico de Arrhenius para *Typha domingensis*. O gráfico relaciona $\ln(k)$ versus $1/T$, onde a inclinação da reta fornece $-E_a/R$. Os pontos experimentais (■) representam ensaios em câmara UV (313,15 K) e campo (299,15 K), com barras de erro indicando intervalo de confiança de 95%.

![ ](../3-IMAGENS/grafico_arrhenius.png){width="70%"}

## S2. Análise Estatística Estendida

### S2.1 Poder Estatístico e Tamanho Amostral

**Figura S3.** Análise de poder estatístico *post-hoc* para diferentes magnitudes de efeito (Cohen's *d*).

![Poder Estatístico](../3-IMAGENS/grafico_analise_poder_ggplot.png){width="75%"}

**Tabela S5.** Análise de poder estatístico para comparações entre tratamentos.

| Comparação | n amostral | Cohen's d | Poder (1-β) | α | Interpretação |
|:-----------|:----------:|:---------:|:-----------:|:-:|:--------------|
| T0 vs T2 | 44 | 1,34 | 0,95 | 0,05 | Poder excelente |
| T0 vs T3 | 44 | 2,03 | 0,99 | 0,05 | Poder excelente |
| T2 vs T3 | 44 | 0,68 | 0,82 | 0,05 | Poder adequado |
| T1 vs T2 | 44 | 0,52 | 0,71 | 0,05 | Poder moderado |

*Nota:* Para elevar o poder a 90% em todas as comparações, recomenda-se n ≥ 60.

### S2.2 Testes de Normalidade e Homoscedasticidade

**Tabela S6.** Resultados dos testes de premissas estatísticas.

| Tratamento | Shapiro-Wilk (W) | p-valor | Levene (F) | p-valor | Distribuição |
|:-----------|:----------------:|:-------:|:----------:|:-------:|:-------------|
| T0 | 0,946 | 0,082 | - | - | Normal |
| T1 | 0,938 | 0,053 | - | - | Normal |
| T2 | 0,921 | 0,024 | - | - | Não-normal |
| T3 | 0,956 | 0,126 | - | - | Normal |
| **Global** | - | - | 3,82 | 0,024 | Heterocedástico |

*Conclusão:* Violação da homogeneidade de variâncias (p = 0,024) justifica o uso de testes não-paramétricos (Kruskal-Wallis).

### S2.3 Intervalos de Confiança Bootstrap

**Figura S4.** Distribuições bootstrap (1000 reamostragens) dos parâmetros de Weibull.

![Bootstrap Weibull](../3-IMAGENS/grafico_bootstrap_distribuicoes_ggplot.png){width="85%"}

**Tabela S7.** Intervalos de confiança bootstrap (95%) para parâmetros de Weibull.

| Tratamento | β (Forma) | IC 95% Bootstrap | η (Escala, dias) | IC 95% Bootstrap | Mediana VUF (dias) |
|:----------:|:---------:|:----------------:|:----------------:|:----------------:|:------------------:|
| T0 | 2,3 | [2,08 - 2,54] | 68 | [61,2 - 75,8] | 60,3 |
| T1 | 2,5 | [2,27 - 2,76] | 64 | [57,8 - 70,9] | 56,8 |
| T2 | 2,8 | [2,58 - 3,04] | 94 | [87,1 - 102,3] | 83,6 |
| T3 | 3,0 | [2,76 - 3,26] | 92 | [84,5 - 99,8] | 81,9 |

## S3. Caracterização Microestrutural Complementar

### S3.1 Análise de Difração de Raios-X

**Tabela S8.** Parâmetros cristalográficos derivados de DRX.

| Tratamento | IC (%) | I₀₀₂ (u.a.) | Iₐₘ (u.a.) | 2θ₀₀₂ (°) | FWHM (°) | Tamanho cristalito (nm) |
|:-----------|:------:|:-----------:|:----------:|:---------:|:--------:|:----------------------:|
| T0 | 48,5 | 1842 | 948 | 22,4 | 2,18 | 7,2 |
| T1 | 52,1 | 1976 | 947 | 22,5 | 2,04 | 7,6 |
| T2 | 58,3 | 2314 | 964 | 22,6 | 1,87 | 8,4 |
| T3 | 62,3 | 2587 | 975 | 22,7 | 1,72 | 9,5 |

*IC: Índice de Cristalinidade; FWHM: Full Width at Half Maximum*

### S3.2 Espectroscopia FTIR - Bandas Características

**Tabela S9.** Atribuição de bandas FTIR e razões de intensidade.

| Número de onda (cm⁻¹) | Atribuição | T0 | T2 | T3 | Variação T0→T3 |
|:---------------------:|:-----------|:--:|:--:|:--:|:--------------:|
| 3400 | O-H stretching | 1,00 | 0,87 | 0,78 | -22% |
| 2920 | C-H stretching | 0,45 | 0,43 | 0,41 | -9% |
| 1735 | C=O hemicelulose | 0,62 | 0,38 | 0,24 | -61% |
| 1635 | H-O-H água adsorvida | 0,38 | 0,29 | 0,22 | -42% |
| 1505 | C=C aromático (lignina) | 0,71 | 0,69 | 0,68 | -4% |
| 1430 | CH₂ scissoring | 0,52 | 0,54 | 0,55 | +6% |
| 1375 | C-H bending | 0,48 | 0,51 | 0,53 | +10% |
| 1060 | C-O-C celulose | 1,00 | 1,12 | 1,18 | +18% |
| 898 | β-glicosídica | 0,34 | 0,38 | 0,41 | +21% |

*Intensidades normalizadas em relação à banda 1060 cm⁻¹ (C-O-C celulose).*

### S3.3 Análise Termogravimétrica (TGA)

**Tabela S10.** Temperaturas características de decomposição e resíduos.

| Tratamento | T₅% (°C) | T₁₀% (°C) | Tₘₐₓ₁ (°C) | Tₘₐₓ₂ (°C) | Resíduo 600°C (%) |
|:-----------|:--------:|:---------:|:----------:|:----------:|:-----------------:|
| T0 | 218 | 251 | 289 | 342 | 22,4 |
| T1 | 226 | 258 | 293 | 346 | 24,1 |
| T2 | 238 | 271 | 301 | 351 | 26,8 |
| T3 | 247 | 284 | 308 | 356 | 28,3 |

*T₅%, T₁₀%: temperaturas com 5% e 10% de perda de massa*  
*Tₘₐₓ₁: pico hemicelulose; Tₘₐₓ₂: pico celulose*

## S4. Propriedades Mecânicas - Dados Completos

### S4.1 Resistência à Tração - Valores Médios por Tempo

**Tabela S11.** Resistência máxima à tração (MPa) ao longo do tempo de exposição.

| Tempo (dias) | T0 | T1 | T2 | T3 |
|:------------:|:--:|:--:|:--:|:--:|
| 0 | 28,4 ± 4,2 | 32,1 ± 3,8 | 35,7 ± 3,1 | 38,9 ± 2,9 |
| 30 | 18,2 ± 5,1 | 22,4 ± 4,6 | 28,3 ± 3,4 | 31,2 ± 3,0 |
| 60 | 12,3 ± 4,8 | 16,8 ± 5,2 | 23,1 ± 3,9 | 25,7 ± 3,2 |
| 90 | 8,1 ± 3,9 | 12,5 ± 4,7 | 18,6 ± 4,1 | 21,3 ± 3,5 |
| 120 | 5,5 ± 3,3 | 9,2 ± 4,2 | 14,8 ± 4,3 | 18,2 ± 3,8 |
| 150 | 3,8 ± 2,7 | 7,1 ± 3,8 | 11,9 ± 4,5 | 15,6 ± 4,1 |
| 180 | 2,4 ± 2,1 | 5,3 ± 3,2 | 9,4 ± 4,2 | 13,1 ± 4,3 |

**Tabela S12.** Deformação máxima na ruptura (%) ao longo do tempo.

| Tempo (dias) | T0 | T1 | T2 | T3 |
|:------------:|:--:|:--:|:--:|:--:|
| 0 | 8,7 ± 1,2 | 7,9 ± 1,1 | 7,1 ± 0,9 | 5,8 ± 0,7 |
| 30 | 6,2 ± 1,4 | 5,8 ± 1,3 | 5,4 ± 1,0 | 4,2 ± 0,8 |
| 60 | 4,3 ± 1,1 | 4,5 ± 1,2 | 4,6 ± 1,1 | 3,5 ± 0,9 |
| 90 | 2,8 ± 0,9 | 3,4 ± 1,0 | 3,8 ± 1,0 | 2,9 ± 0,8 |
| 120 | 1,9 ± 0,7 | 2,6 ± 0,9 | 3,1 ± 0,9 | 2,4 ± 0,7 |
| 150 | 1,3 ± 0,5 | 2,0 ± 0,7 | 2,7 ± 0,8 | 2,0 ± 0,6 |
| 180 | 0,9 ± 0,4 | 1,6 ± 0,6 | 2,3 ± 0,7 | 1,7 ± 0,6 |

### S4.2 Parâmetros de Degradação Cinética

**Tabela S13.** Constantes de degradação ($k$) e tempos de meia-vida ($t_{1/2}$).

| Propriedade | Tratamento | k (dia⁻¹) | IC 95% | t₁/₂ (dias) | R² |
|:-----------|:----------:|:---------:|:------:|:-----------:|:--:|
| Resistência | T0 | 0,0142 | [0,0128-0,0156] | 48,8 | 0,96 |
| | T1 | 0,0118 | [0,0105-0,0131] | 58,7 | 0,95 |
| | T2 | 0,0082 | [0,0074-0,0090] | 84,5 | 0,97 |
| | T3 | 0,0076 | [0,0068-0,0084] | 91,2 | 0,98 |
| Ductilidade | T0 | 0,0355 | [0,0312-0,0398] | 19,5 | 0,93 |
| | T1 | 0,0287 | [0,0251-0,0323] | 24,1 | 0,94 |
| | T2 | 0,0218 | [0,0192-0,0244] | 31,8 | 0,96 |
| | T3 | 0,0198 | [0,0174-0,0222] | 35,0 | 0,95 |

## S5. Imagens Complementares

**Figura S5.** Equipamento de ensaio mecânico - Máquina Universal EMIC DL-3000.

![Máquina Universal](../3-IMAGENS/maquina_universal.png){width="70%"}

## S6. Protocolos Analíticos - Procedimentos Operacionais Padrão

### S6.1 Determinação do Índice de Cristalinidade por DRX

**Protocolo:**

1. Moagem da amostra (<150 µm) em moinho criogênico
2. Secagem em estufa (60°C, 24h)
3. Preparação de porta-amostra com compactação uniforme
4. Varredura: 2θ = 5-40°, velocidade 2°/min
5. Radiação CuKα (λ = 1,5406 Å), 40 kV, 30 mA
6. Cálculo: $IC = \frac{I_{002} - I_{am}}{I_{002}} \times 100$
   - $I_{002}$: intensidade pico 2θ ≈ 22,5°
   - $I_{am}$: intensidade vale 2θ ≈ 18°

### S6.2 Preparação de Amostras para MEV

**Protocolo:**

1. Fragmentação em seções de 10 mm × 5 mm
2. Fixação em stub de alumínio com fita carbono condutiva
3. Metalização: Au/Pd (60:40), 15 nm espessura
4. Sputter coater: 20 mA, 60 s
5. Armazenamento em dessecador (<30% UR)
6. Imageamento: 15 kV, alto vácuo, aumentos 100× a 5.000×

### S6.3 Ensaio de Tração - Procedimento ASTM D5035

**Protocolo:**

1. Corte de corpos de prova: 200 mm × 50 mm
2. Aclimatação: 23 ± 2°C, 50 ± 5% UR, 24h
3. Marcação: comprimento útil 100 mm
4. Fixação em garras: torque 45 N·m
5. Pré-carga: 2 N
6. Velocidade: 20 mm/min
7. Aquisição: 100 Hz
8. Critério de parada: queda >80% da força máxima

## S7. Dados Brutos Disponíveis

Os dados brutos completos estão disponíveis no repositório online:

**Repositório:** https://doi.org/10.17632/n4g296wjx5.1 (a ser atualizado após aceitação)

---
