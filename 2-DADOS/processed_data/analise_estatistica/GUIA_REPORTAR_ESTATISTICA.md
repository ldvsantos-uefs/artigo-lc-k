# GUIA DEFINITIVO: Como Reportar Diferenças Estatísticas no Manuscrito

## ⚠️ DESCOBERTA CRÍTICA

A análise por tempo individual (30, 60, 90, 120, 150, 180 dias) revelou que:

**NENHUMA comparação par a par é significativa quando analisada em tempos individuais após correção de Bonferroni.**

**MAS** a análise longitudinal agregada (todos os tempos juntos) mostra diferenças significativas.

Isso significa que:
- ✅ As diferenças são **reais** quando consideramos o padrão ao longo do tempo (análise longitudinal)
- ⚠️ As diferenças em **pontos temporais isolados** não atingem significância estatística devido ao pequeno n (n=3 por grupo/tempo)

---

## COMO INTERPRETAR E REPORTAR NO MANUSCRITO

### 1. ANÁLISE LONGITUDINAL (AGREGADA) - Use Esta!

**Contexto:** Quando falar sobre diferenças gerais entre tratamentos ao longo de todo o experimento.

**Resultados Válidos:**

| Comparação | p-corrigido | Cohen's d | Status | Como Reportar |
|------------|-------------|-----------|--------|---------------|
| T0 vs T3 | <0.001 | -2.03 | ✅ SIM | "T3 apresenta resistência significativamente superior a T0 ao longo do período experimental (p<0.001, Mann-Whitney U com Bonferroni; d=-2.03)" |
| T1 vs T3 | 0.028 | -1.03 | ✅ SIM | "T3 supera T1 de forma estatisticamente significativa (p=0.028, Bonferroni-corrigido; d=-1.03)" |
| T2 vs T3 | 0.004 | -1.34 | ✅ SIM | "T3 demonstra superioridade significativa em relação a T2 (p=0.004, Bonferroni-corrigido; d=-1.34)" |
| T0 vs T1 | 0.054 | -1.02 | ⚠️ MARGINAL | "T1 sugere tendência de diferença em relação a T0 (p=0.054), com grande tamanho de efeito (d=-1.02)" |
| T0 vs T2 | 1.000 | -0.61 | ❌ NÃO | "T2 não difere significativamente de T0 (p>0.05)" |
| T1 vs T2 | 1.000 | 0.35 | ❌ NÃO | "T1 e T2 não diferem significativamente entre si (p>0.05)" |

**Modelos Estatísticos:**
- **GEE (Recomendado para longitudinal):** Todos os tratamentos T1, T2, T3 diferem significativamente de T0 (p<0.005)
- **GLM:** T1 e T3 diferem de T0 (p<0.001); T2 é marginalmente significativo (p=0.058)

---

### 2. ANÁLISE POR TEMPO ESPECÍFICO - Use Com Cautela!

**Contexto:** Quando falar sobre diferenças em momentos específicos (ex: "aos 30 dias").

**PROBLEMA:** Com n=3 por grupo/tempo, a correção de Bonferroni elimina a significância.

**Estratégias de Redação:**

#### ❌ EVITE (estatisticamente incorreto):
> "Aos 30 dias, T3 apresenta resistência significativamente superior a T0 (p<0.05)."

#### ✅ USE (descritivo + contexto longitudinal):
> "Aos 30 dias, T3 apresenta média de 28.9±4.6 MPa, enquanto T0 exibe 10.3±0.8 MPa. Embora o teste de Kruskal-Wallis indique diferenças globais neste tempo (p=0.024), as comparações par a par não atingem significância após correção para comparações múltiplas. A superioridade de T3 torna-se estatisticamente robusta quando considerado o padrão longitudinal completo (p<0.001)."

#### ✅ ALTERNATIVA (usar modelo GEE):
> "O modelo GEE confirma que T3 difere significativamente de T0 (p<0.001) quando ajustado para a estrutura longitudinal dos dados, indicando superioridade consistente ao longo do tempo."

---

## 3. FRASES MODELO POR CONTEXTO

### Para Resultados (Seção 3)

#### Ao apresentar dados descritivos:
> "O tratamento T3 apresentou resistência média à tração de 18.2±8.2 MPa (CV=45%), enquanto T0, T1 e T2 exibiram 5.5±3.3 MPa (CV=61%), 10.7±6.4 MPa (CV=60%) e 8.5±6.2 MPa (CV=73%), respectivamente."

#### Ao mencionar testes estatísticos:
> "A análise mediante teste de Kruskal-Wallis indicou diferenças significativas entre os grupos (H=25.08, p<0.001). Comparações múltiplas com correção de Bonferroni revelaram que T3 difere significativamente de T0 (p<0.001, d=-2.03), T1 (p=0.028, d=-1.03) e T2 (p=0.004, d=-1.34)."

#### Ao falar sobre padrão temporal:
> "A modelagem mediante Equações de Estimação Generalizadas (GEE) confirmou efeito significativo de todos os tratamentos em relação ao controle (p<0.005) e declínio temporal consistente (-0.091 MPa/dia, p<0.001). A interação tratamento×tempo sugere que T3 exibe taxa de degradação mais acentuada (p=0.001)."

#### Ao reportar coeficiente de variação:
> "O coeficiente de variação indica maior dispersão relativa em T2 (CV=73%) comparado a T3 (CV=45%), refletindo maior homogeneidade nas respostas do tratamento mais concentrado. Esta métrica descritiva alinha-se aos resultados dos testes de hipótese, que confirmam diferença significativa entre estes grupos (p=0.004)."

### Para Discussão (Seção 4)

#### Ao interpretar diferenças:
> "A superioridade estatisticamente significativa de T3 (p<0.001, d=-2.03) sugere que concentrações elevadas de NaOH (9%) podem promover modificações estruturais favoráveis à resistência mecânica, embora à custa de maior taxa de degradação temporal (interação p=0.001)."

#### Ao mencionar ausência de diferença:
> "A ausência de diferença significativa entre T1 e T2 (p>0.05) indica que incrementos de 3% para 6% na concentração de NaOH podem não resultar em ganhos mecânicos substanciais, possivelmente devido à saturação de sítios reativos ou competição entre mecanismos de reticulação e degradação."

#### Ao abordar tendências:
> "Embora T1 apresente tendência de superioridade em relação a T0 (p=0.054, d=-1.02), a interpretação desta diferença marginal deve ser cautelosa, considerando o tamanho amostral e a variabilidade inerente aos materiais naturais."

---

## 4. CHECKLIST FINAL ANTES DE SUBMETER

### Para cada afirmação de diferença estatística, verifique:

- [ ] **p-valor reportado?** (com indicação de correção se for comparação múltipla)
- [ ] **Cohen's d reportado?** (com interpretação: pequeno/médio/grande)
- [ ] **Método estatístico mencionado?** (Mann-Whitney U, GEE, GLM)
- [ ] **Contexto longitudinal vs pontual claro?** (agregado vs tempo específico)
- [ ] **CV usado como descritivo, não como teste?** (acompanhado de teste de hipótese)
- [ ] **Linguagem probabilística?** (sugere, indica, pode) ao invés de categórica
- [ ] **Tamanho amostral mencionado?** (especialmente se for pequeno)

### Para afirmações sobre tempo específico:

- [ ] **Evitou afirmar "significativo" em análise pontual?** (a menos que use modelo GEE)
- [ ] **Descreveu padrão descritivamente?** (médias, CV, dispersão)
- [ ] **Remeteu à análise longitudinal para significância?** ("confirmado pelo modelo GEE")

---

## 5. EXEMPLO DE PARÁGRAFO COMPLETO E CORRETO

> "A resistência à tração variou significativamente entre os tratamentos ao longo do período experimental (Kruskal-Wallis, H=25.08, p<0.001). O tratamento T3 (9% NaOH) apresentou resistência média de 18.2±8.2 MPa, significativamente superior ao controle T0 (5.5±3.3 MPa; p<0.001, Mann-Whitney U com correção de Bonferroni; Cohen's d=-2.03, efeito grande), bem como aos tratamentos T1 (10.7±6.4 MPa; p=0.028, d=-1.03) e T2 (8.5±6.2 MPa; p=0.004, d=-1.34). Modelos GEE ajustados para a estrutura longitudinal dos dados confirmaram estes efeitos (p<0.001 para todos os tratamentos vs T0) e revelaram declínio temporal significativo em todos os grupos (-0.091 MPa/dia, p<0.001), com interação significativa para T3 (p=0.001), indicando taxa de degradação mais acentuada. O coeficiente de variação foi menor em T3 (CV=45%) comparado aos demais tratamentos (T0=61%, T1=60%, T2=73%), sugerindo maior homogeneidade de resposta. Embora T1 apresente tendência de diferença em relação a T0 (p=0.054), esta não atinge significância estatística ao nível convencional de 5%. Não foram detectadas diferenças significativas entre T0 e T2 (p>0.05) nem entre T1 e T2 (p>0.05), sugerindo que incrementos na concentração de NaOH de 3% para 6% podem não resultar em ganhos mecânicos substanciais na faixa avaliada."

---

## 6. RESUMO EXECUTIVO PARA REVISÃO RÁPIDA

### ✅ PODE AFIRMAR:
- T3 > T0 (p<0.001) ✅
- T3 > T1 (p=0.028) ✅
- T3 > T2 (p=0.004) ✅
- Efeito temporal (p<0.001) ✅
- Interação T3×tempo (p=0.001) ✅
- GEE: todos tratamentos vs T0 (p<0.005) ✅

### ⚠️ PODE MENCIONAR (com ressalva):
- T1 vs T0 (p=0.054) - "tendência", "marginal", "sugere"
- T2 vs T0 no GLM (p=0.058) - "marginalmente"

### ❌ NÃO PODE AFIRMAR:
- T2 > T0 (comparação direta, p>0.05) ❌
- T1 vs T2 (p>0.05) ❌
- Diferenças significativas em tempos pontuais sem GEE ❌
- "Significativo" baseado apenas em CV ❌

---

**Arquivo:** `GUIA_REPORTAR_ESTATISTICA.md`  
**Gerado:** 07/12/2025  
**Baseado em:** `analise_estatistica_glm_gee.py` + `analise_por_tempo.py`
