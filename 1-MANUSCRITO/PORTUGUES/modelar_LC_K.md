---
title: "Modelo Preditivo de Degradação de Geotêxteis Naturais Baseada na Recalcitrância Química<b>Predictive Model for the Degradation of Natural Geotextiles Based on Chemical Recalcitrance"
author: "Diego Vidal"
bibliography: referencias_lc.bib
csl: apa.csl
reference-doc: modelo_formatacao.docx
fig-align: center
table-align: center
lang: pt-br
---
## Resumo

A substituição de geossintéticos petroquímicos por materiais biodegradáveis constitui imperativo para mitigar a poluição por microplásticos em ecossistemas terrestres e aquáticos. Embora o tratamento alcalino seja amplamente empregado para ampliar a durabilidade de geotêxteis de fibras naturais, a definição de um protocolo otimizado para bioengenharia de solos carece de consenso. A presente investigação validou um modelo hierárquico que conecta a composição química fundamental, especificamente a razão lignina/celulose, à Vida Útil Funcional (VUF) em 10% de probabilidade de falha, avaliando a resistência à degradação de geotêxteis manufaturados com fibras de *Typha domingensis* submetidas a modificações alcalinas. Ensaios de resistência à tração conduzidos ao longo de 180 dias permitiram parametrizar a cinética de degradação de fibras tratadas com NaOH (3%, 6% e 9%). A integração de imagens de Microscopia Eletrônica de Varredura (MEV) e análises espectroscópicas demonstrou que o tratamento alcalino modula a recalcitrância química mediante a remoção seletiva de hemicelulose. Os resultados indicam que o tratamento com NaOH 6% estabeleceu um ponto de equilíbrio operacional, conciliando ganho de VUF (95 dias, +127% sobre o controle) com a preservação de ductilidade (ε_máx = 2,8%), ao passo que a concentração de 9% induziu fragilização excessiva. A análise temporal revelou que o modelo exponencial de decaimento descreve adequadamente a cinética de fragilização, evidenciando que a razão lignina/celulose governa a taxa de degradação através de uma relação exponencial inversa. A principal contribuição metodológica reside na confirmação de que o modelo ajustado permite estimar a confiabilidade temporal a partir de ensaios composicionais rápidos, reduzindo a dependência de testes de campo prolongados e consolidando as fibras de *Typha* tratadas com 6% NaOH como alternativa sustentável para o controle de erosão em taludes tropicais, em consonância com os princípios da economia circular e da redução da pegada ecológica na geotecnia.

**Palavras-chave**: Modelagem de degradação; Razão Lignina/Celulose; Vida útil funcional; Geotêxteis naturais; Bioengenharia de solos.

## Graphical Abstract

![](../3-IMAGENS/abstract_grafico.png){width="80%"}

## 1. Introdução

A intensificação das mudanças climáticas globais e o aumento da frequência de eventos extremos impulsionam a busca por soluções resilientes e ambientalmente responsáveis para o controle da erosão, desafio central nas agendas científica, tecnológica e de gestão ambiental contemporâneas [@Pazhanivelan2025]. A predominância de materiais petroquímicos em geossintéticos tradicionais revela, contudo, uma contradição intrínseca: ao mesmo tempo em que mitigam processos erosivos, esses materiais contribuem para a poluição plástica persistente e para o aumento das emissões de gases de efeito estufa, dada a elevada energia incorporada e sua longa permanência no ambiente [@Koerner2016; @Sanjay2019].

A bioengenharia de solos promove essa transição mediante o emprego de materiais renováveis cuja degradabilidade controlada e baixo impacto ambiental confrontam a persistência petroquímica. Biocompósitos reforçados com fibras lignocelulósicas materializam essa ruptura, pois sua baixa densidade, resistência específica elevada, biodegradabilidade programável e disponibilidade territorial ampla convergem com os princípios da economia circular e da infraestrutura verde [@Karimah2021]. Paralelamente, a interação entre raízes e geotêxteis naturais potencializa a estabilidade do solo e a resistência à erosão hídrica, mimetizando processos naturais de sucessão ecológica [@Niu2017; @Vannoppen2017].

A arquitetura dessas fibras combina celulose cristalina, hemiceluloses amorfas e lignina aromática. A razão lignina/celulose (L/C) atua como determinante da durabilidade e resistência à degradação [@Reinhardt2022; @Rowell1998], definindo a recalcitrância química da matriz através da proporção entre a fase aromática e a fração cristalina.

A transposição dos materiais lignocelulósicos do laboratório para aplicações de campo enfrenta limitações que a caracterização mecânica convencional não captura, uma vez que a exposição prolongada à radiação ultravioleta e a ciclos higrotérmicos acelera fotoxidação e hidrólise ácida em regime preferencial, com a ductilidade degradando antes da resistência última à tração [@Sathishkumar2022]. Essa sequência temporal define o colapso funcional do geotêxtil, pois a incapacidade de acomodar deformações do solo precede a ruptura por tensão, determinando que compreender e manipular os mecanismos de instabilidade química e estrutural seja mais relevante para a viabilidade geotecnológica do que a mera resistência inicial.

Modificações superficiais mitigam esses efeitos mediante alteração controlada da química interfacial. O tratamento alcalino reduz a hidrofilicidade, aumenta a compatibilidade interfacial, remove hemiceluloses e amplia a rugosidade superficial, modulando a compatibilidade química e a ancoragem mecânica entre fibras e matrizes [@Gurunathan2015; @Tanasa2022]. Essas transformações estruturais estendem a durabilidade e favorecem interações ecológicas desejáveis em bioengenharia, visto que geotêxteis naturais funcionam como substratos para colonização radicular, contribuindo para estabilização biológica do solo por acoplamento biomecânico.

*Typha domingensis* materializa essa convergência multifuncional por apresentar alta produtividade de biomassa [@Fontes2021], composição lignocelulósica favorável com razão L/C particularmente elevada [@Fontes2021], ampla distribuição em ambientes úmidos tropicais [@Grace1989; @Manning2018] e presença de metabólitos bioativos que conferem desempenho mecânico, hidráulico e ecológico integrado [@Manning2018]. A literatura, todavia, negligencia aspectos críticos, visto que estudos sistemáticos sobre resiliência mecânica sob intemperismo real são escassos e relações quantitativas entre parâmetros químicos fundamentais e desempenho em serviço permanecem inexploradas.

Fibras tradicionais como sisal e linho possuem literatura consolidada sobre envelhecimento e mecanismos de degradação, ao passo que *Typha domingensis* carece de investigações aprofundadas sobre sua resposta à fotodegradação e exposição ambiental prolongada. A inexistência de um modelo preditivo unificado capaz de conectar composição química básica à VUF de geotêxteis naturais configura lacuna crítica para padronização, certificação e adoção tecnológica [@Silveira2021].

A hipótese central postula que a razão lignina/celulose (L/C) determina a recalcitrância química da matriz, governando a taxa de degradação. Validar essa hierarquia preditiva na qual a composição química determina a cinética de degradação que, por sua vez, define a confiabilidade temporal permitiria estimar Vida Útil Funcional (VUF) mediante ensaios composicionais rápidos, suprimindo a dependência de testes de campo prolongados.

O objetivo deste estudo consiste em validar esse modelo hierárquico conectando composição química fundamental (razão lignina/celulose) à Vida Útil Funcional (VUF) em 10% de probabilidade de falha, mediante análise de resistência à degradação de geotêxteis produzidos com fibras de *Typha domingensis* submetidas a modificações alcalinas. O sucesso da validação reside em demonstrar que o modelo ajustado pode prever, com incerteza aceitável, se o material manterá a ductilidade necessária durante a janela crítica de longo prazo, período essencial para o estabelecimento da cobertura vegetal em projetos de bioengenharia.

## 2. Materiais e Métodos

### 2.1 Arquitetura Hierárquica do Modelo

A seleção da espécie *Typha domingensis* Pers. fundamentou-se em suas propriedades mecânicas e nos teores de celulose e lignina reportados na literatura.

Esta macrófita aquática, que tipicamente atinge entre 2 e 3 metros de altura, possui folhas longas e planas e é tradicionalmente utilizada na confecção de artesanato e coberturas. Sua robustez é atribuída ao alto teor de celulose, além de sua importância ecológica como filtro natural em áreas úmidas, a espécie possui amplo espectro de uso (Figura 1).

**Figura 1.**  Coleta de material utilizado e secagem das fibras.

![ ](../3-IMAGENS/coleta.png){width="90%"}

A coleta de folhas e brotos foi realizada no Povoado Tigre pertencente ao município de Pacatuba, Estado de Sergipe, nordeste do Brasil (Figura 2).

**Figura 2.** Localização geográfica da área de coleta de *Typha domingensis*.

![ ](../3-IMAGENS/mapa_tigre_en.png){width="90%"}

A identificação botânica formal foi realizada pelo Laboratório de Botânica do Instituto de Biologia da Universidade Federal da Bahia, com exsicatas depositadas no Herbário da Universidade Federal de Sergipe. Em conformidade com a legislação brasileira para acesso ao patrimônio genético, as atividades de coleta foram registradas no Sistema Nacional de Gestão do Patrimônio Genético e do Conhecimento Tradicional Associado (SisGen) sob o código A2B3842.

Os protótipos de geotêxteis foram manufaturados pelo Laboratório de Erosão e Sedimentação da Universidade Federal de Sergipe, seguindo um processo em quatro etapas: (i) corte e secagem das fibras; (ii) agrupamento; (iii) tecelagem; e (iv) tratamento químico alcalino. A extração das fibras utilizou ferramentas de lâmina lisa para preservar a integridade das fibras, com incisões realizadas acima do sistema radicular para permitir a rebrota.

O tratamento químico visou modificar a superfície das fibras para reduzir a hidrofilicidade e retardar a degradação. As mantas geotêxteis foram imersas em soluções de hidróxido de sódio (NaOH) nas concentrações de 3% (0,75 mol/L), 6% (1,5 mol/L) e 9% (2,25 mol/L) por um período de 24 horas, mantendo-se uma relação de banho constante.

Após a reação, o material foi lavado em água corrente até neutralização e seco ao ar. A secagem ocorreu à sombra por aproximadamente 8 dias.

Subsequentemente, as fibras foram trançadas manualmente para formar cordões com diâmetro médio de 6 mm, que constituíram a trama biaxial do geotêxtil tipo geogrid (grelha de reforço). A malha foi configurada em padrão xadrez com aberturas de 25 cm², totalizando uma área de 1,20 m² por unidade (Figura 3a). Essa configuração de geogrid permite o bloqueio e confinamento do solo enquanto proporciona drenagem adequada.

O monitoramento da degradação natural foi conduzido na Estação Experimental do Campus Rural da Universidade Federal da Sergipe (UFS), localizada no município de São Cristóvão – SE (16°55′S, 36°66′O). A área experimental consiste em um talude com inclinação de 45°, constituído por Plintossolo Háplico Distrófico (Figura 3b).

O experimento foi conduzido em delineamento em quadrado latino com parcelas de 0,60 m x 2,40 m com geotêxteis (geogrelhas) dispostos no sentido da pendente, simulando condições reais de aplicação (Figura 3c). As amostras foram expostas às variáveis ambientais locais (radiação solar, precipitação, vento) e à interação com a cobertura vegetal espontânea, cujo desenvolvimento foi registrado mensalmente.

**Figura 3.** (a) Confexão dos Geotêxteis com fibras de *Typha domingensis*; (b) Geotêxteis instalados no solo e (c) Geotêxteis expostos em taludes.

![ ](../3-IMAGENS/talude.png){width="90%"}

As amostras foram expostas ao clima subtropical úmido característico da região, cujos padrões de precipitação e irradiância solar ao longo do período experimental encontram-se documentados na Figura 4. O regime pluviométrico exibiu sazonalidade típica do litoral nordestino, com concentração de chuvas entre os meses de abril e agosto, acumulando aproximadamente 1400 mm durante os 180 dias de monitoramento. A irradiância solar global manteve-se predominantemente entre 18 e 22 MJ m⁻² dia⁻¹, com atenuação temporária durante eventos de nebulosidade associados aos períodos chuvosos.

**Figura 4.** Condições climáticas durante o período experimental de 180 dias: (a) Precipitação diária e acumulado móvel de 30 dias; (b) Irradiância solar global com média móvel de 15 dias. A região sombreada em vermelho destaca o período experimental centralizado em janela de observação de 2 anos.

![ ](../3-IMAGENS/grafico_clima_experimental.png){width="95%"}

Para avaliação da cinética de biodegradação, seções de 20 cm × 20 cm foram removidas da porção central das parcelas em intervalos programados, visando evitar efeitos de borda. Em laboratório, estas amostras foram secas em estufa a 60 °C por 24 horas antes da preparação dos corpos de prova. O período de exposição estendeu-se por 180 dias, com coletas realizadas em sete intervalos discretos: T0 (0 dias), T1 (30 dias), T2 (60 dias), T3 (90 dias), T4 (120 dias), T5 (150 dias) e T6 (180 dias), com cinco réplicas por ponto experimental para garantir robustez estatística.

### 2.2. Caracterização Físico-Química e Microestrutural

A análise dos grupos funcionais foi realizada em um espectrômetro FTIR (PerkinElmer, Spectrum Two), operando no modo de transmissão. As amostras foram preparadas pelo método de pastilha de KBr (1 mg de fibra moída para 100 mg de KBr espectroscópico). Os espectros foram adquiridos na faixa de 4000 a 400 cm⁻¹, com resolução de 4 cm⁻¹ e acúmulo de 32 varreduras.

A interpretação das bandas vibracionais baseou-se nos trabalhos seminais de @Pandey1999 e @Faix1991, focando na banda de 1735 cm⁻¹ (estiramento C=O de hemiceluloses) e 1505 cm⁻¹ (vibração do anel aromático da lignina) para avaliar a remoção seletiva de componentes amorfos.

A estrutura cristalina foi analisada em um difratômetro de raios X (Shimadzu, XRD-6000), utilizando radiação CuKα (λ = 1,5406 Å), operando a 40 kV e 30 mA. As varreduras foram realizadas no intervalo 2θ de 5° a 40°, com velocidade de 2°/min. O Índice de Cristalinidade (IC) foi calculado pelo método empírico de pico de altura proposto por @Segal1959 (Equação 1):

$$
IC (\%) = \frac{I_{002} - I_{am}}{I_{002}} \times 100
$$

Onde $I_{002}$ é a intensidade máxima do pico de difração do plano cristalino (002) em 2θ ≈ 22,5° e $I_{am}$ é a intensidade da difração do material amorfo em 2θ ≈ 18°.

A morfologia superficial e o modo de fratura foram examinados em um microscópio eletrônico de varredura (Hitachi, TM3000). As amostras foram fixadas em suportes de alumínio com fita de carbono condutiva e metalizadas com uma fina camada de ouro (Au) em um sputter coater (Denton Vacuum, Desk V) para evitar o carregamento eletrostático. As imagens foram adquiridas com tensão de aceleração de 15 kV sob alto vácuo.

A estabilidade térmica foi avaliada em um analisador termogravimétrico (Shimadzu, TGA-50). Amostras de aproximadamente 10 mg foram aquecidas de 25°C a 600°C a uma taxa de 10°C/min, sob fluxo dinâmico de nitrogênio (N₂) de 50 mL/min.

As curvas de perda de massa (TG) e suas derivadas (DTG) foram utilizadas para identificar os estágios de decomposição da hemicelulose, celulose e lignina, conforme metodologia descrita por @Popescu2011.

### 2.3. Ensaios Mecânicos de Tração

A resistência à tração e a deformação na ruptura foram determinadas em uma Máquina Universal de Ensaios (EMIC, DL-3000), equipada com uma célula de carga de 500 N. Os ensaios foram conduzidos conforme a norma ASTM D5035 (Método de Tira Larga), utilizando corpos de prova com dimensões de 200 mm x 50 mm, comprimento útil de 100 mm e velocidade de deslocamento de 20 mm/min. Foram testados no mínimo 5 corpos de prova para cada condição de tratamento e tempo de exposição.

### 2.4. Modelagem Estatística e Probabilística

#### 2.4.1. Cinética de Degradação e Confiabilidade

A degradação mecânica foi modelada assumindo cinética de primeira ordem ($P(t) = P_0 \cdot e^{-k \cdot t}$), com parâmetros estimados por regressão não-linear (Levenberg-Marquardt). A seleção do modelo exponencial foi validada comparativamente frente a modelos de potência ($P(t) = a \cdot t^b$) e logarítmicos ($P(t) = a + b \cdot \ln(t)$) utilizando o Critério de Informação de Akaike (AIC) e o Critério de Informação Bayesiano (BIC). Para as fibras tratadas (T2 e T3), o modelo exponencial apresentou o melhor ajuste (menor AIC), enquanto para as fibras naturais (T0) e levemente tratadas (T1), os resultados foram estatisticamente equivalentes ao modelo logarítmico ($\Delta AIC < 2$). Optou-se pelo modelo exponencial devido à sua fundamentação físico-química na cinética de degradação de primeira ordem, consistente com a hidrólise e oxidação de polímeros naturais.

A probabilidade de falha temporal seguiu a distribuição de Weibull de dois parâmetros (Equação 3), onde a VUF corresponde ao tempo para 10% de falha ($P_{10}$).

$$
R(t) = \exp\left[ -\left( \frac{t}{\eta} \right)^\beta \right]
$$

A incerteza dos parâmetros ($k$, $\eta$, $\beta$) foi quantificada via *bootstrap* não-paramétrico (1000 reamostragens, IC 95%).

#### 2.4.2. Análises Estatísticas

A estrutura longitudinal do experimento (4 tratamentos × 6 tempos × 3 réplicas) foi analisada mediante Equações de Estimação Generalizadas (GEE) com família Gaussiana e correlação *exchangeable*, robustas para medidas repetidas. Comparações entre grupos empregaram testes de Kruskal-Wallis e Mann-Whitney U (correção de Bonferroni), com tamanho de efeito medido pelo *d* de Cohen. A validação do modelo preditivo incluiu validação cruzada *leave-one-out* (LOOCV) e simulação de Monte Carlo (1000 iterações) sob cenários de irradiância UV variáveis. Análises foram conduzidas em Python 3.13.2 (`scipy`, `statsmodels`, `lifelines`) e R 4.3.1 (`ggplot2`).

### 2.5. Simulação Híbrida

Para calibrar os modelos preditivos de vida útil, realizou-se um ensaio de degradação acelerada em câmara UV customizada, seguindo adaptações da norma EN 12224:2001. O sistema de irradiação combinou lâmpadas fluorescentes UV-A (315–400 nm), UV-B (280–315 nm) e visível (450–700 nm), simulando o espectro solar global com irradiância média de 6.214 W/m² (UV-A) e 2.281 W/m² (UV-B) (Figura 3).

O protocolo experimental consistiu em 120 ciclos de 6 horas, totalizando 720 horas de exposição. Cada ciclo compreendeu três etapas: (i) imersão em água por 15 min; (ii) secagem em estufa a 105°C por 1 h; e (iii) exposição à radiação UV por 4 h 45 min. A temperatura interna foi controlada por termômetro de painel negro em 40 ± 3°C, com umidade relativa mantida em aproximadamente 60%.

**Figura 5.** (a) Câmara de degradação forçada UV utilizada para calibração dos modelos cinéticos e (b) sistema de irradiação com lâmpadas fluorescentes UV-A, UV-B e visível.

![ ](../3-IMAGENS/camara.png){width="70%"}

A simulação híbrida integrou os dados cinéticos obtidos na simulação ($k_{\text{câmara}}$) com os dados de degradação natural em campo ($k_{\text{campo}}$), permitindo a determinação da Energia de Ativação ($E_a$) experimental via equação de Arrhenius. Adicionalmente, a evolução do dano foi modelada pela lei de Paris-Erdoğan modificada, onde o parâmetro de crescimento de fissuras ($m$) foi calibrado utilizando o módulo de Weibull ($\beta$), buscando estabelecer uma ponte entre a probabilidade de falha estática e a cinética de degradação dinâmica.

## 3. Resultados e Discussão

### 3.1. Modulação Química e Microestrutural

A caracterização basal das fibras *in natura* (Tabela 2) constitui a referência analítica inicial, na qual a razão lignina/celulose (L/C = 0.44) e o índice de cristalinidade de 48.5% delineiam uma matriz predominantemente amorfa e higroscópica. Essa configuração composicional é consistente com uma elevada densidade de sítios reativos e volumes livres, o que favorece a difusão de água e a suscetibilidade a mecanismos de hidrólise e foto-oxidação que antecedem a degradação mecânica [@Bouramdane2022, @Silva2009].

A espectroscopia FTIR evidencia a eficácia do tratamento alcalino pela atenuação da banda em 1735 cm⁻¹, associada ao estiramento de grupos carbonila (C=O) em hemiceluloses e pectinas. Conforme observado por @Pandey1999, a remoção seletiva desses constituintes amorfos eleva a proporção relativa da fração celulósica cristalina e do esqueleto aromático da lignina, um fenômeno também descrito por @Faix1991, o que pode reduzir a hidrofilicidade da parede celular. Conforme discutido por @Poletto2014 e @Mwaikambo2002, a supressão desses modos vibracionais sugere a transição para um estado de menor reatividade química, limitando potencialmente a iniciação de processos oxidativos.

**Tabela 2.** Composição química média das fibras de *Typha domingensis* *in natura* (% massa seca).

| Componente                | Teor (%) | Desvio Padrão | Método Analítico       |
| :------------------------ | :------: | :------------: | :----------------------- |
| Celulose                  |   42,5   |     ± 2,1     | Van Soest modificado     |
| Hemicelulose              |   28,3   |     ± 1,8     | Van Soest modificado     |
| Lignina                   |   18,7   |     ± 1,4     | Klason modificado        |
| Extrativos                |   7,2   |     ± 0,9     | Soxhlet (etanol/tolueno) |
| Cinzas                    |   3,3   |     ± 0,4     | Calcinação 550°C      |
| Razão L/C                |   0,44   |    ± 0,03    | Calculada                |
| Índice de Cristalinidade |   48,5   |     ± 3,2     | DRX (método Segal)      |

*Nota: Valores médios de três lotes independentes coletados em janeiro de 2023.*


Os dados cristalográficos (DRX) são compatíveis com essa reorganização estrutural ao registrarem aumento do índice de cristalinidade de 48.5% (Controle) para 62.3% (9% NaOH). Essa evolução reflete a remoção de regiões desordenadas e a reorientação das microfibrilas de celulose, conforme detalhado por @Chieng2017 e @Yang2024, o que pode resultar em arquitetura supramolecular mais compacta. A redução do volume amorfo tende a restringir o caminho difusivo para água e agentes oxidantes, atuando possivelmente como barreira física que retarda a cinética das reações de degradação [@Hiyama2006; @Yamane2006].

A análise morfológica (MEV) reflete essas alterações químicas em métricas geométricas de interação com o meio. As fibras tratadas exibem superfície livre de impurezas e com rugosidade ampliada (Figura 8), enquanto a morfometria (N=36) quantifica redução da porosidade média de 75.8% (Natural) para 26.3% (9% NaOH). Segundo @Carvalho2014, essa densificação pode minimizar a área superficial específica disponível para colonização microbiana e absorção de umidade, ao passo que o aumento da rugosidade (452 para 1549) indica potencial aprimoramento da ancoragem mecânica na matriz de solo [@Geremew2024; @Sinha2017].

**Figura 6.** Análise comparativa de microscopia eletrônica de varredura (MEV) das fibras naturais (*Typha domingensis*) versus fibras tratadas alcalinamente (3%, 6% e 9% NaOH).

![ ](../3-IMAGENS/figura_painel_comparativo_500x.png){width="90%"}

*Nota: Imagens em escala de 500 µm × 500 µm. A análise comparativa (N=36) indicou redução da porosidade média de 75,8% (Natural) para 26,3% (9% NaOH), contrastando com o aumento da rugosidade superficial (fibrilação) e reorganização cristalina observada nas fibras tratadas.*

### 3.2. Cinética de Degradação Mecânica

A quantificação cinética da degradação mecânica fortalece a hipótese de que a modificação química pode atuar como fator de retardo da obsolescência funcional. A Figura 7 ilustra a evolução temporal da Resistência Última à Tração (UTS) e da deformação máxima. 

A análise longitudinal evidencia o desempenho superior do tratamento T3 (9% NaOH), que sustenta resistência média de 18.2 ± 8.2 MPa, estatisticamente distinta do controle (5.5 ± 3.3 MPa; p < 0.001) conforme correções de Bonferroni e teste de Kruskal-Wallis (H = 25.08). A modelagem GEE corrobora essa distinção ao indicar declínio temporal significativo para todos os grupos (-0.091 MPa/dia, p < 0.001), mas com termo de interação que favorece a estabilidade das fibras tratadas (Figura 7).

**Figura 7.** Caracterização microestrutural e mecânica da degradação: (a) Evolução temporal da resistência à tração e padrões de fratura, (b) Curvas de tensão-deformação representativas em 30 dias e (c) em 90 dias para todos os tratamentos.

![ ](../3-IMAGENS/figura5_paineis_ab.png){width="95%"}

A ductilidade pode ser considerada um indicador sensível do estado limite funcional, antecipando a transição frágil que compromete a capacidade do geotêxtil de acomodar deformações do solo. A fibra não tratada colapsa para ductilidade inferior a 5% em 180 dias, enquanto os tratamentos alcalinos preservam deformabilidade superior a 6%, retardando a fragilização. Essa preservação apresenta associação com a remoção de hemiceluloses, que, segundo @Hatakka2011, @Santos2023_GeocompostosTypha, funcionam em estado natural como sítios preferenciais para absorção de umidade e ataque fúngico. A estabilização da capacidade de deformação pode refletir, portanto, uma consequência mecânica da redução da suscetibilidade biológica e química da matriz [@Kabir2012].

A parametrização cinética (Tabela 2) quantifica o ganho de durabilidade ao demonstrar que a mercerização reduz a constante de decaimento ($k$) e amplia a meia-vida ($t_{1/2}$). O tratamento T3 maximiza a retenção de propriedades, atingindo meia-vida de resistência de 91,2 dias contra 48,8 dias do controle. 

No contexto de projeto, essa extensão é crítica para garantir integridade mecânica durante a janela de estabelecimento da vegetação [@Veylon2015]. A redução da taxa de degradação da ductilidade ($k$ de 0,0355 para 0,0198 dia⁻¹) suporta a viabilidade das fibras tratadas para aplicações que demandam compatibilidade de deformação a longo prazo [ @Mwaikambo2002; @Rong2001].

**Tabela 2.** Constantes de degradação ($k$) e tempos de meia-vida ($t_{1/2}$) para resistência à tração e ductilidade.

| Propriedade  | Tratamento | k (dia⁻¹) |     IC 95%     | t₁/₂ (dias) | R² |
| :----------- | :--------: | :---------: | :-------------: | :-----------: | :--: |
| Resistência |     T0     |   0,0142   | [0,0128-0,0156] |     48,8     | 0,96 |
|              |     T1     |   0,0118   | [0,0105-0,0131] |     58,7     | 0,95 |
|              |     T2     |   0,0082   | [0,0074-0,0090] |     84,5     | 0,97 |
|              |     T3     |   0,0076   | [0,0068-0,0084] |     91,2     | 0,98 |
| Ductilidade  |     T0     |   0,0355   | [0,0312-0,0398] |     19,5     | 0,93 |
|              |     T1     |   0,0287   | [0,0251-0,0323] |     24,1     | 0,94 |
|              |     T2     |   0,0218   | [0,0192-0,0244] |     31,8     | 0,96 |
|              |     T3     |   0,0198   | [0,0174-0,0222] |     35,0     | 0,95 |

*Nota: Constantes obtidas via ajuste de decaimento exponencial de primeira ordem. IC: Intervalo de Confiança.*

A correlação entre desempenho macroscópico e dano acumulado é substanciada pela análise de densidade de fraturas (Figura 8b), que mapeia a evolução física das descontinuidades. O crescimento de fraturas no controle (45 para 185 mm⁻²) contrasta com a estabilização observada no tratamento mais agressivo (128 mm⁻²), o que é compatível com a premissa de que maior cristalinidade e menor porosidade impedem a propagação de trincas [@Dalirnasab2024; @Kabir2012].

**Figura 8.** Validação do modelo híbrido e evolução microestrutural sendo, (a) Comparação entre previsões do modelo acelerado (câmara UV) e dados de campo para resistência residual e (b) Evolução temporal da densidade de fraturas para todos os tratamentos.

![ ](../3-IMAGENS/grafico_validacao_microestrutura.png){width="95%"}

Essa evidência microestrutural conecta as escalas de análise, sugerindo que a durabilidade aprimorada resulta diretamente de uma arquitetura fibrosa menos propensa à nucleação de defeitos sob estresse ambiental [@Luchese2024; @Kwon2021].

### 3.3. Modelagem Estocástica e Preditiva

A transição de regime induzida pela mercerização parece deslocar o comportamento de falha para um padrão de maior determinismo, conforme evidenciado pela distribuição de Weibull (Figura 9). O incremento do módulo de forma ($\beta$) de 2,3 (Controle) para 3,0 (9% NaOH) é consistente com a redução da dispersão dos tempos de falha. @Rong2001 e @Luqman2023 associam esse comportamento à homogeneização microestrutural e à eliminação de defeitos críticos. Sob a ótica de projeto geotécnico, a métrica conservadora $P_{10}$ quantifica o ganho de confiabilidade: o tratamento T2 (6% NaOH) estende a vida útil funcional para 95 dias, superando os 42 dias do controle e mitigando o risco de colapso prematuro na fase de estabilização [@Sekulic2017].

**Figura 9.** Curvas de confiabilidade e estimativas de vida útil funcional (Weibull) para os diferentes tratamentos.

![ ](../3-IMAGENS/grafico_weibull_confiabilidade_ggplot.png){width="95%"}

A integração da dinâmica térmico-cinética via calibração híbrida dá suporte à previsibilidade do sistema sob variabilidade ambiental. Em que, a energia de ativação ($E_a = 29,03$ kJ/mol), determinada via equação de Arrhenius pelo confronto entre taxas de degradação em campo ($k \approx 0,0118$ dia⁻¹) e em câmara UV ($k \approx 0,0199$ dia⁻¹), sugere que o mecanismo de falha se situa na faixa de hidrólise e foto-oxidação acopladas de matrizes lignocelulósicas [@OrnaghiJr2024; @Wei2014]. Já a consistência entre projeções aceleradas e registros empíricos (Figura 8a) indica a viabilidade dos ensaios de curta duração em capturar a física da degradação, permitindo extrapolações temporais robustas [@Wei2014].

A robustez numérica dos ajustes, verificada via *bootstrap* não-paramétrico (1000 iterações), demonstra normalidade na distribuição dos parâmetros cinéticos (Kolmogorov-Smirnov: $p = 0,41$). A ausência de *overfitting* é atestada pela proximidade entre o erro de validação cruzada ($RMSE_{cv} = 0,000127$ dia⁻¹) e o erro de ajuste, resultando na razão $RMSE_{cv}/RMSE_{treino} = 1,10$, critério que, segundo @Sodagar2025, favorece a generalização do modelo para dados não observados.

Limites físicos de validade manifestam-se sob regimes de alta irradiância, onde a linearidade da resposta fotoquímica é comprometida. As previsões mantêm erro relativo inferior a 10% sob sombreamento parcial (UV ≤ 0,5), mas a exposição extrema (UV = 1,0) eleva a divergência para 28%, indicando a necessidade de correções não-lineares para ambientes de altitude ou climas áridos [@Andrady2019; @Aldosary2025; @wieser2023]. A forte correlação (r = 0,82) entre a cinética de fragilização e os marcadores de oxidação no FTIR sugere, contudo, que a degradação mecânica permanece governada pela evolução química da matriz [@Tanasa2022; @Silva2024].

### 3.4. Protocolo e Implicações Geotécnicas

A especificação técnica de geotêxteis naturais recomenda a substituição de médias determinísticas por margens probabilísticas de segurança, alinhando-se a práticas de confiabilidade estrutural via adoção do percentil $P_{10}$, conforme preconizado por @ISO2394 e @Phoon2021. A evidência empírica embasa a definição de limiares de desempenho baseados em resistência inicial mínima de 20 kN/m, VUF ≥ 90 dias e índice de cristalinidade superior a 60%, estabelecendo a redução da deformação máxima ($\varepsilon_{\text{max}}$) para 2,0% como critério terminal de funcionalidade.

A seleção do tratamento (Figura 10) baseia-se na integração de ensaios de caracterização rápida (L/C, IC, FTIR) com estimativas de VUF ponderadas pela agressividade ambiental e requisitos de ductilidade. O material não tratado restringe-se a intervenções provisórias em cenários de baixa agressividade (30–60 dias) [@Pritchard2000; @Methacanon2010], enquanto o tratamento com NaOH 6% (T2) apresenta-se como ponto de equilíbrio técnico-econômico para taludes tropicais. Esta concentração estende a VUF para 95 dias (+127%) preservando ductilidade funcional (2,8%), diferentemente da concentração de 9% (T3) que, embora maximize a durabilidade, induz fragilização ($\varepsilon_{\text{max}} < 2,0%$) compatível apenas com aplicações de reforço rígido ou contenção de base [@Syed2021; @Kafodya2020; @Holanda2024].

**Figura 10.** Fluxograma decisório para seleção de tratamento de fibras de *Typha domingensis* (critério $P_{10}$ e protocolo de qualificação acelerada).

![ ](../3-IMAGENS/fluxograma_decisorio.png){width="90%"}

A viabilidade da adoção em larga escala apoia-se na vantagem ambiental e econômica frente aos geossintéticos convencionais. A pegada de carbono reduzida em 60–70% em relação ao polipropileno [@Shamsuddoha2025; @Soares2023] combina-se à eficiência operacional em obras de grande porte (10.000 m²), onde o custo incremental do tratamento (R$ 180–220/ton) é absorvido pela extensão da vida útil e consequente redução na frequência de manutenções, gerando economia estimada entre R$ 50.000 e R$ 70.000 anuais.

A aplicabilidade do protocolo subordina-se ao regime de irradiância local, visto que a não-linearidade da resposta fotoquímica sob UV extremo (índice 1,0) introduz desvios preditivos que exigem validação *in situ* ou correção paramétrica para evitar subestimação de risco [@Andrady2019]. Sob as condições de taludes tropicais úmidos, entretanto, a cadeia causal validada — da modulação química à confiabilidade mecânica — oferece base quantitativa robusta para a engenharia de soluções baseadas na natureza.

## 4. Conclusão

A validação do modelo hierárquico que conecta a recalcitrância química à vida útil funcional representa a contribuição central deste estudo, indicando que a durabilidade de geotêxteis naturais não é um artefato estocástico, mas uma resposta determinística à arquitetura composicional. A trajetória experimental evidenciou que a remoção de hemiceluloses e a consequente reorganização cristalina induzida pela mercerização podem atuar como mecanismo governante do retardo da degradação mecânica.

A identificação do tratamento com 6% de NaOH como ponto ótimo técnico-econômico transcende a mera otimização de parâmetros, delimitando uma condição de contorno onde o ganho de confiabilidade não compromete a deformabilidade essencial para a interação solo-geotêxtil. Enquanto a concentração de 9% maximiza a resistência à tração, a fragilização resultante viola os requisitos de ductilidade para estabilização de taludes, exemplificando o compromisso entre recalcitrância química e compliância mecânica. 

A adoção da métrica de confiabilidade $P_{10}$ converte esse entendimento em especificação de engenharia, permitindo que fibras de *Typha domingensis* sejam prescritas com margens de segurança comparáveis às de contrapartes sintéticas, desde que o regime de irradiância permaneça dentro do envelope validado.

Esta investigação reposiciona os geotêxteis naturais de materiais alternativos para soluções de engenharia, fundamentadas em um arcabouço preditivo que integra evidência microestrutural e design probabilístico. 

A capacidade demonstrada de estimar o desempenho de longo prazo mediante ensaios composicionais rápidos reduz a dependência de testes de campo prolongados, acelerando a transferência tecnológica de soluções de bioengenharia. A perspectiva futura envolve a expansão do modelo para outras espécies fibrosas e a incorporação de variáveis ambientais adicionais, como umidade relativa e temperatura, visando ampliar a aplicabilidade do protocolo decisório em contextos geográficos diversos.