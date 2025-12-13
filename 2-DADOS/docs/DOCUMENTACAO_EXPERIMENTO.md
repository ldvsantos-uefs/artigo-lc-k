# Documentação do Experimento e Origem dos Dados

## 1. Origem dos Arquivos

A estrutura de arquivos deste projeto organiza os dados brutos, scripts de processamento e o manuscrito final.

*   **`2-DADOSLC/DB_original.xlsx`**: Arquivo Excel contendo os dados experimentais brutos. Inclui medições de força (N), tensão (MPa), extensão (mm) e deformação (%) para amostras de *Typha domingensis* submetidas a diferentes tempos de exposição.
*   **`1-MANUSCRITOLC/modelar_LC_K.md`**: O manuscrito principal do artigo, escrito em Markdown, contendo a introdução, metodologia, resultados e discussão.
*   **`1-MANUSCRITOLC/referencias.bib`** e **`library.bib`**: Arquivos de bibliografia no formato BibTeX, contendo as referências citadas no manuscrito (artigos, normas, livros).
*   **Scripts Python (`.py`)**:
    *   `extrair_dados.py`: Script responsável por ler o `DB_original.xlsx`, limpar os dados e extrair as colunas relevantes (Ciclos, Tensão, Extensão) para um formato intermediário (`dados_resumo_extraidos.csv`).
    *   `modelar_LC_k_VUF.py`: Script de modelagem que calcula a taxa de degradação ($k$), ajusta curvas exponenciais e gera os gráficos de resultados.

## 2. Fontes Utilizadas

### Dados Primários
Os dados primários provêm de ensaios experimentais realizados com fibras de **Taboa (*Typha domingensis*)**.
*   **Amostragem**: Fibras extraídas e processadas, submetidas ou não a tratamentos superficiais (ex: Resina).
*   **Envelhecimento**: As amostras foram expostas a ciclos de envelhecimento acelerado (UV + Umidade) em câmara de intemperismo.
*   **Ensaios Mecânicos**: Testes de tração uniaxial realizados em máquina universal de ensaios para determinar Tensão Máxima e Extensão na Ruptura ao longo do tempo.

### Dados Secundários
Dados comparativos de outras fibras (como Juta, Sisal, Coco, e anteriormente Syagrus) e suas respectivas razões Lignina/Celulose (L/C) foram obtidos da literatura científica, conforme referenciado nos arquivos `.bib`.

## 3. Lógica do Experimento e Análise

### Objetivo
Validar a hipótese de que a razão **Lignina/Celulose (L/C)** é um preditor confiável da taxa de degradação ($k$) e, consequentemente, da Vida Útil Funcional (VUF) de geotêxteis naturais.

### Metodologia de Análise
1.  **Definição da Unidade de Tempo**: O tempo de exposição foi medido em "Ciclos", onde **1 Ciclo = 6 horas** de exposição real.
2.  **Extração de Parâmetros**:
    *   A partir dos dados brutos, calculou-se a média das propriedades mecânicas para cada intervalo de tempo.
3.  **Pivô na Estratégia de Modelagem**:
    *   Inicialmente, analisou-se a **Resistência à Tração (Tensão)**. Observou-se que a tensão se manteve estável ou teve queda insignificante ($k \approx 0$) durante o período de teste, indicando que as fibras mantinham sua capacidade de carga.
    *   Em contrapartida, a **Ductilidade (Extensão/Strain)** apresentou uma degradação acentuada e consistente.
    *   **Decisão**: O foco da modelagem foi alterado para a **Perda de Ductilidade**, pois o "embrittlement" (fragilização) foi identificado como o modo de falha crítico que precede a ruptura mecânica.

### Modelagem Matemática
*   **Modelo de Decaimento**: Aplicou-se um modelo de decaimento exponencial de primeira ordem:
    $$S(t) = S_0 \cdot e^{-k \cdot t}$$
    Onde:
    *   $S(t)$: Propriedade (Deformação) no tempo $t$.
    *   $S_0$: Propriedade inicial.
    *   $k$: Taxa de degradação ($h^{-1}$ ou $dia^{-1}$).

*   **Vida Útil Funcional (VUF)**:
    *   Calculada como o tempo necessário para a propriedade atingir 50% ($t_{50}$) ou 90% ($t_{90}$) do valor inicial, ou baseada em probabilidade de falha ($P_{10}$) usando distribuição de Weibull.

*   **Correlação L/C vs $k$**:
    *   Estabeleceu-se uma relação inversa onde maior teor de lignina (maior L/C) resulta em menor taxa de degradação ($k$), conferindo maior durabilidade.

---
*Documento gerado automaticamente pelo Assistente de IA em 05/12/2025.*
