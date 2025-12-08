# RELATÓRIO DE ANÁLISE ESTATÍSTICA - ORIENTAÇÕES PARA O MANUSCRITO

## Data: 07 de Dezembro de 2025

---

## 1. RESUMO EXECUTIVO

A análise estatística rigorosa dos dados de tração revelou diferenças significativas entre tratamentos, mas **NEM TODAS as comparações que podem ter sido afirmadas no manuscrito são estatisticamente válidas** após correção para comparações múltiplas.

**PROBLEMA CRÍTICO IDENTIFICADO:**
- Pressupostos paramétricos violados (heterogeneidade de variâncias, p=0.024)
- Necessário uso de testes não-paramétricos
- Correção de Bonferroni aplicada (6 comparações múltiplas)

---

## 2. RESULTADOS PRINCIPAIS

### 2.1 Teste Global (Kruskal-Wallis)
```
H = 25.08, p < 0.001
```
**Conclusão:** Existem diferenças significativas entre pelo menos dois grupos.

### 2.2 Comparações Múltiplas (Mann-Whitney U com correção de Bonferroni)

| Comparação | p-valor original | p-corrigido | Significativo? | Cohen's d | Interpretação |
|------------|------------------|-------------|----------------|-----------|---------------|
| **T0 vs T1** | 0.009 | **0.054** | ❌ **NÃO** | -1.02 | Grande efeito, mas não significativo após correção |
| **T0 vs T2** | 0.189 | 1.000 | ❌ **NÃO** | -0.61 | Efeito médio, não significativo |
| **T0 vs T3** | <0.001 | **<0.001** | ✅ **SIM** | -2.03 | Grande efeito E significativo |
| **T1 vs T2** | 0.335 | 1.000 | ❌ **NÃO** | 0.35 | Pequeno efeito, não significativo |
| **T1 vs T3** | 0.005 | **0.028** | ✅ **SIM** | -1.03 | Grande efeito E significativo |
| **T2 vs T3** | 0.001 | **0.004** | ✅ **SIM** | -1.34 | Grande efeito E significativo |

### 2.3 Coeficiente de Variação

| Tratamento | CV (%) | Interpretação |
|------------|--------|---------------|
| T0 | 60.8 | Alta dispersão |
| T1 | 59.8 | Alta dispersão |
| T2 | 73.1 | Dispersão mais elevada |
| T3 | 45.2 | Menor dispersão relativa |

**IMPORTANTE:** O CV pode ser reportado como métrica descritiva, mas **NÃO como evidência de diferença estatística**.

---

## 3. MODELO GLM (Efeitos Principais e Interação)

### Coeficientes Significativos (p < 0.05):
- **Intercepto:** 10.76 MPa (p < 0.001)
- **T1 vs T0:** +10.72 MPa (p < 0.001) ✅
- **T3 vs T0:** +21.66 MPa (p < 0.001) ✅
- **Tempo (dias):** -0.050 MPa/dia (p = 0.004) ✅
- **T1:dias (interação):** -0.053 MPa/dia (p = 0.035) ✅
- **T3:dias (interação):** -0.085 MPa/dia (p = 0.001) ✅

### Coeficientes NÃO Significativos:
- **T2 vs T0:** +5.51 MPa (p = 0.058) ⚠️ Marginalmente significativo
- **T2:dias (interação):** -0.024 MPa/dia (p = 0.337) ❌

**INTERPRETAÇÃO:**
- T1 e T3 diferem significativamente de T0
- T2 apresenta tendência (p=0.058), mas não atinge significância estatística ao nível α=0.05
- Todos os tratamentos mostram declínio temporal, mas T3 declina mais rapidamente

---

## 4. MODELO GEE (Ajustado para Medidas Repetidas)

### Todos os coeficientes significativos (p < 0.001):
- **T1 vs T0:** +5.20 MPa (p < 0.001)
- **T2 vs T0:** +3.01 MPa (p = 0.004)
- **T3 vs T0:** +12.77 MPa (p < 0.001)
- **Tempo:** -0.091 MPa/dia (p < 0.001)

**OBSERVAÇÃO:** O GEE confirma efeitos dos três tratamentos quando ajustado para correlação temporal, inclusive T2 (que era marginal no GLM).

---

## 5. CORREÇÕES NECESSÁRIAS NO MANUSCRITO

### ❌ AFIRMAÇÕES QUE **NÃO PODEM** SER FEITAS:

1. **"T1 difere significativamente de T0"** (comparação direta)
   - p-corrigido = 0.054 > 0.05 ❌
   - **Correção sugerida:** "T1 apresenta tendência de diferença em relação a T0 (p=0.054, Mann-Whitney U), com grande tamanho de efeito (d=-1.02)"

2. **"T2 difere significativamente de T0"** (comparação direta)
   - p-corrigido = 1.000 ❌
   - **Correção sugerida:** "T2 não difere significativamente de T0 em análises de comparação direta (p>0.05), embora o modelo GLM sugira tendência (p=0.058)"

3. **"T1 e T2 apresentam diferenças significativas entre si"**
   - p-corrigido = 1.000 ❌
   - **Correção sugerida:** "T1 e T2 não diferem significativamente entre si (p>0.05, Mann-Whitney U)"

4. **Qualquer afirmação baseada APENAS em CV**
   - ❌ ERRADO: "O menor CV de T3 indica maior homogeneidade estatisticamente significativa"
   - ✅ CORRETO: "T3 apresenta menor dispersão relativa (CV=45%), enquanto T2 exibe maior variabilidade (CV=73%)"

### ✅ AFIRMAÇÕES QUE **PODEM** SER FEITAS:

1. **"T3 difere significativamente de T0"**
   - p < 0.001, d = -2.03 ✅
   - **Frase modelo:** "T3 apresenta resistência à tração significativamente superior a T0 (p<0.001, Mann-Whitney U com correção de Bonferroni; d=-2.03, efeito grande)"

2. **"T3 difere significativamente de T1"**
   - p = 0.028, d = -1.03 ✅
   - **Frase modelo:** "T3 supera T1 de forma estatisticamente significativa (p=0.028, Bonferroni-corrigido; d=-1.03)"

3. **"T3 difere significativamente de T2"**
   - p = 0.004, d = -1.34 ✅
   - **Frase modelo:** "T3 demonstra superioridade significativa em relação a T2 (p=0.004, Bonferroni-corrigido; d=-1.34, efeito grande)"

4. **Efeito do tempo (longitudinal)**
   - GLM: p = 0.004; GEE: p < 0.001 ✅
   - **Frase modelo:** "A resistência à tração declina significativamente ao longo do tempo em todos os tratamentos (p<0.001, GEE; -0.091 MPa/dia)"

5. **Interação tratamento × tempo**
   - T1:dias (p=0.035) e T3:dias (p=0.001) ✅
   - **Frase modelo:** "A taxa de degradação temporal varia entre tratamentos, com T3 exibindo declínio mais acentuado (interação significativa, p=0.001)"

---

## 6. TEMPLATE DE REDAÇÃO PARA O MANUSCRITO

### Exemplo de parágrafo correto:

> "A análise estatística mediante teste de Kruskal-Wallis indicou diferenças significativas entre os grupos (H=25.08, p<0.001). Comparações múltiplas com correção de Bonferroni revelaram que o tratamento T3 (9% NaOH) apresenta resistência à tração significativamente superior ao controle T0 (p<0.001, Cohen's d=-2.03, efeito grande), bem como aos tratamentos T1 (p=0.028, d=-1.03) e T2 (p=0.004, d=-1.34). A comparação entre T1 e T0 sugere tendência de diferença (p=0.054), com grande tamanho de efeito (d=-1.02), enquanto T2 não difere significativamente de T0 (p>0.05). O coeficiente de variação indica maior dispersão relativa em T2 (CV=73%) comparado a T3 (CV=45%), embora esta métrica descritiva deva ser interpretada em conjunto com os testes de hipótese. Modelos GEE ajustados para medidas repetidas confirmam efeito temporal significativo (p<0.001), com declínio médio de -0.091 MPa/dia, e interação significativa entre tratamento e tempo para T1 (p=0.035) e T3 (p=0.001)."

---

## 7. CHECKLIST DE REVISÃO

Antes de afirmar que dois grupos diferem significativamente, verifique:

- [ ] O p-valor **corrigido** (Bonferroni) é < 0.05?
- [ ] O tamanho de efeito (Cohen's d) foi reportado?
- [ ] O método estatístico foi mencionado? (Mann-Whitney U com Bonferroni)
- [ ] Evitou afirmações baseadas APENAS em CV sem teste de hipótese?
- [ ] Usou linguagem probabilística (sugere, indica, tende a) quando p está entre 0.05-0.10?
- [ ] Evitou termos categóricos (sempre, nunca, definitivamente) sem p<0.001?

---

## 8. ARQUIVOS GERADOS

Os seguintes arquivos CSV foram salvos para consulta:

1. `comparacoes_multiplas.csv` - Todas as comparações par a par com p-valores corrigidos
2. `coeficiente_variacao.csv` - CVs por tratamento (métrica descritiva)
3. `teste_normalidade.csv` - Resultados do teste de Shapiro-Wilk

**Local:** `2-DADOSLC/processed_data/analise_estatistica/`

---

## 9. RECOMENDAÇÃO FINAL

**PRIORIDADE MÁXIMA:** Revisar TODO o manuscrito buscando:

1. Afirmações sobre "diferença significativa" entre T0-T1, T0-T2, ou T1-T2 → **REMOVER ou SUAVIZAR**
2. Uso de CV como única evidência de diferença → **CONTEXTUALIZAR como métrica descritiva**
3. Ausência de p-valores nas comparações → **ADICIONAR com correção de Bonferroni**
4. Falta de tamanho de efeito (Cohen's d) → **ADICIONAR sempre que houver comparação**

**As únicas comparações estatisticamente válidas são:**
- ✅ T0 vs T3 (p<0.001)
- ✅ T1 vs T3 (p=0.028)
- ✅ T2 vs T3 (p=0.004)

---

**Gerado automaticamente pelo script:** `analise_estatistica_glm_gee.py`
**Data:** 07/12/2025
