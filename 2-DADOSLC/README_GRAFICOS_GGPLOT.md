# 📊 Geração de Gráficos Acadêmicos - Geotêxteis de Typha

## Visão Geral

Este script R gera **6 gráficos individuais** e **1 painel composto** em alta resolução (300 DPI) utilizando ggplot2, adequados para publicação acadêmica.

---

## ✅ Pré-requisitos

### Dependências R
Instale os pacotes necessários:

```r
install.packages(c(
  "ggplot2",
  "dplyr", 
  "tidyr",
  "scales",
  "gridExtra",
  "ggpubr",
  "readr"
))
```

### Arquivos de Dados Necessários
- ✅ `dados_resumo_extraidos.csv` - Dados experimentais da Typha
- ✅ `validacao_modelo_uv.csv` - Resultados das simulações UV (gerado pelo Python)

---

## 🚀 Execução

### Opção 1: RStudio (Recomendado)
1. Abra `gerar_graficos_ggplot.R` no RStudio
2. Certifique-se de que o diretório de trabalho está correto:
   ```r
   setwd("c:/Users/vidal/.../1-ARTIGO_LC_K/2-DADOSLC")
   ```
3. Execute o script completo: **Ctrl+Shift+Enter** ou **Source**

### Opção 2: Linha de Comando
```bash
cd "c:\Users\vidal\...\1-ARTIGO_LC_K\2-DADOSLC"
Rscript gerar_graficos_ggplot.R
```

### Opção 3: PowerShell (Windows)
```powershell
cd "c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\revisao-sistematica\1-ARTIGO_LC_K\2-DADOSLC"
Rscript.exe gerar_graficos_ggplot.R
```

---

## 📈 Gráficos Gerados

### Individuais (PNG + PDF)

| # | Arquivo | Descrição | Figura no Manuscrito |
|---|---------|-----------|---------------------|
| 1 | `grafico_degradacao_strain_ggplot` | Cinética temporal de degradação com ajuste exponencial | Figura 1 |
| 2 | `grafico_tratamentos_ggplot` | Comparação de tratamentos (duplo eixo Y) | Figura 2 |
| 3 | `grafico_validacao_uv_ggplot` | Erro relativo da validação UV | Figura 3 |
| 4 | `grafico_weibull_confiabilidade_ggplot` | Curvas de confiabilidade de Weibull | Figura 4 |
| 5 | `grafico_bootstrap_distribuicoes_ggplot` | Distribuições bootstrap de k e S₀ | Figura 5 |
| 6 | `grafico_analise_poder_ggplot` | Análise de poder estatístico | Figura 6 |

### Painel Composto
- `painel_completo_analises_ggplot.png/pdf` - 4 subplots (A-D) em layout 2×2

---

## 🎨 Características dos Gráficos

### Qualidade de Publicação
- ✅ **Resolução:** 300 DPI (PNG) + Vetorial (PDF)
- ✅ **Tema:** Acadêmico com fundo branco
- ✅ **Fontes:** Serif, tamanhos otimizados (10-14pt)
- ✅ **Cores:** Paletas academicamente apropriadas

### Elementos Visuais
- **Barras de erro:** Desvio padrão (validação UV)
- **Intervalos de confiança:** Linhas tracejadas (bootstrap)
- **Anotações:** Equações e valores-chave in-plot
- **Legendas:** Posicionamento inteligente

### Conformidade
- ✅ Segue diretrizes da **APA** e **Nature**
- ✅ Colorblind-friendly (opção viridis disponível)
- ✅ Adequado para impressão em escala de cinza

---

## 🔧 Personalização

### Alterar Resolução
```r
ggsave("grafico.png", plot, dpi = 600)  # Alta resolução
```

### Alterar Dimensões
```r
ggsave("grafico.png", plot, width = 12, height = 8, units = "in")
```

### Alterar Tema
```r
theme_set(theme_minimal())  # Minimalista
theme_set(theme_classic())  # Clássico (sem grid)
```

### Paleta de Cores Alternativa
```r
scale_color_brewer(palette = "Set1")  # ColorBrewer
scale_color_viridis_d()              # Viridis (colorblind-safe)
```

---

## 📊 Detalhes Técnicos por Gráfico

### Gráfico 1: Cinética de Degradação
- **Tipo:** Scatter + Line (modelo ajustado)
- **Modelo:** $S(t) = S_0 \cdot e^{-kt}$
- **R² in-plot:** Sim
- **Cor primária:** Verde (#2E7D32)

### Gráfico 2: Tratamentos
- **Tipo:** Barras + Linha (dual-axis)
- **Eixo Y1:** VUF (dias) - Azul
- **Eixo Y2:** UTS (MPa) - Vermelho
- **Labels:** Valores nas barras e pontos

### Gráfico 3: Validação UV
- **Tipo:** Barras com erro
- **Cores por status:**
  - Verde: Excelente (<10%)
  - Laranja: Aceitável (10-20%)
  - Vermelho: Revisar (>20%)
- **Linha de referência:** 10% (threshold)

### Gráfico 4: Weibull
- **Tipo:** Linhas suaves (confiabilidade vs. tempo)
- **3 curvas:** Natural, NaOH 6%, NaOH 9%
- **P₁₀ marcado:** Linhas verticais pontilhadas
- **Limiar 90%:** Linha horizontal

### Gráfico 5: Bootstrap
- **Tipo:** Densidade (2 painéis)
- **Painel A:** Taxa de degradação (k)
- **Painel B:** Deformação inicial (S₀)
- **ICs 95%:** Linhas pontilhadas

### Gráfico 6: Análise de Poder
- **Tipo:** Curvas múltiplas
- **6 tamanhos amostrais:** n = 10, 20, 30, 44, 60, 80
- **Ponto crítico:** n=44, d=0.6, poder=80% (destacado)
- **Gradiente de cor:** Viridis plasma

---

## 📁 Estrutura de Saída

```
2-DADOSLC/
├── grafico_degradacao_strain_ggplot.png (300 DPI)
├── grafico_degradacao_strain_ggplot.pdf (Vetorial)
├── grafico_tratamentos_ggplot.png
├── grafico_tratamentos_ggplot.pdf
├── grafico_validacao_uv_ggplot.png
├── grafico_validacao_uv_ggplot.pdf
├── grafico_weibull_confiabilidade_ggplot.png
├── grafico_weibull_confiabilidade_ggplot.pdf
├── grafico_bootstrap_distribuicoes_ggplot.png
├── grafico_bootstrap_distribuicoes_ggplot.pdf
├── grafico_analise_poder_ggplot.png
├── grafico_analise_poder_ggplot.pdf
├── painel_completo_analises_ggplot.png (16×12 in)
└── painel_completo_analises_ggplot.pdf (16×12 in)
```

---

## 🐛 Solução de Problemas

### Erro: "Package not found"
```r
install.packages("nome_do_pacote")
```

### Erro: "CSV not found"
Verifique se está no diretório correto:
```r
getwd()  # Ver diretório atual
list.files()  # Listar arquivos disponíveis
```

### Gráficos não aparecem
```r
dev.off()  # Fechar dispositivos gráficos pendentes
```

### Fontes não renderizam corretamente (PDF)
```r
# Instalar Cairo para melhor suporte a fontes
install.packages("Cairo")
ggsave("grafico.pdf", device = cairo_pdf)
```

---

## 📚 Referências de Customização

### ggplot2 Oficial
- [Documentação](https://ggplot2.tidyverse.org/)
- [Cheatsheet](https://rstudio.github.io/cheatsheets/data-visualization.pdf)

### Temas Acadêmicos
- [ggpubr](https://rpkgs.datanovia.com/ggpubr/)
- [ggthemes](https://jrnold.github.io/ggthemes/)

### Paletas de Cores
- [ColorBrewer](https://colorbrewer2.org/)
- [Viridis](https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html)

---

## ✅ Checklist de Qualidade

Antes de usar os gráficos na publicação:

- [ ] Resolução ≥ 300 DPI
- [ ] Texto legível quando reduzido a 50%
- [ ] Legendas e eixos corretamente rotulados
- [ ] Unidades de medida especificadas
- [ ] Cores distinguíveis em escala de cinza
- [ ] Anotações não sobrepõem dados
- [ ] Formato vetorial (PDF) disponível
- [ ] Consistência visual entre todos os gráficos

---

## 📄 Citação no Manuscrito

### LaTeX
```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{grafico_degradacao_strain_ggplot.pdf}
  \caption{Cinética de degradação da deformação para fibras de \textit{Typha domingensis}.}
  \label{fig:cinetica}
\end{figure}
```

### Markdown (Pandoc)
```markdown
![Cinética de degradação](grafico_degradacao_strain_ggplot.png){width=80%}
```

---

## 🤝 Suporte

Para questões técnicas sobre:
- **ggplot2:** [Stack Overflow - ggplot2](https://stackoverflow.com/questions/tagged/ggplot2)
- **R em geral:** [RStudio Community](https://community.rstudio.com/)

---

## 📝 Notas de Versão

**Versão 1.0** (2025-12-05)
- ✅ 6 gráficos individuais implementados
- ✅ Painel composto 2×2
- ✅ Tema acadêmico padronizado
- ✅ Exportação PNG + PDF
- ✅ Alta resolução (300 DPI)

---

**Desenvolvido para o projeto:** Modelagem de Degradação de Geotêxteis Naturais  
**Instituição:** Revisão Sistemática - Geotêxteis  
**Contato:** ldvsantos-uefs/revisao-sistematica-geotexteis
