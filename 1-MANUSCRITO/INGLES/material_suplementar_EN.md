---
title: "Supplementary Material: Predictive Model for the Degradation of Natural Geotextiles Based on *Typha domingensis*"
subtitle: "Complementary Data, Extended Statistical Analyses, and Experimental Protocols"
author: "Luiz Diego Vidal Santos, Francisco Sandro Rodrigues Holanda, et al."
lang: en
geometry: margin=2.5cm
fontsize: 11pt
---

# Supplementary Material

## S1. Detailed Experimental Protocol

### S1.1 Chemical and Physical Characterization of Raw Fibers

**Table S1.** Average chemical composition of *Typha domingensis* fibers in natura (% dry mass).

| Component | Content (%) | Standard Deviation | Analytical Method |
|:-----------|:--------:|:-------------:|:-----------------|
| Cellulose | 42.5 | ± 2.1 | Modified Van Soest |
| Hemicellulose | 28.3 | ± 1.8 | Modified Van Soest |
| Lignin | 18.7 | ± 1.4 | Modified Klason |
| Extractives | 7.2 | ± 0.9 | Soxhlet (ethanol/toluene) |
| Ash | 3.3 | ± 0.4 | Calcination 550°C |
| L/C Ratio | 0.44 | ± 0.03 | Calculated |
| Crystallinity Index | 48.5 | ± 3.2 | XRD (Segal method) |

**Table S2.** Physical properties of untreated fibers.

| Property | Value | Unit | Method |
|:-----------|:-----:|:-------:|:-------|
| Average diameter | 6.2 ± 1.3 | mm | Digital caliper |
| Apparent density | 0.87 ± 0.05 | g/cm³ | Pycnometry |
| Water absorption (24h) | 185 ± 22 | % | ASTM D570 |
| Equilibrium moisture | 11.2 ± 1.1 | % | Gravimetry (105°C) |
| Porosity | 68.4 ± 4.2 | % | Calculated |

### S1.2 Alkaline Treatment Conditions

**Table S3.** Operational parameters of mercerization treatment.

| Parameter | T0 (Control) | T1 (3%) | T2 (6%) | T3 (9%) |
|:----------|:-------------:|:-------:|:-------:|:-------:|
| NaOH concentration (w/v) | 0% | 3% | 6% | 9% |
| Molarity (mol/L) | - | 0.75 | 1.5 | 2.25 |
| Temperature (°C) | - | 25 ± 2 | 25 ± 2 | 25 ± 2 |
| Immersion time (h) | - | 24 | 24 | 24 |
| Bath ratio (L/kg) | - | 20:1 | 20:1 | 20:1 |
| Final pH | - | 12.8 | 13.1 | 13.4 |
| Washing cycles | - | 5 | 5 | 5 |
| Drying time (h) | - | 192 | 192 | 192 |

### S1.3 Accelerated Aging Protocol

**Table S4.** UV exposure parameters and environmental conditions during field trials.

| Parameter | Mean | Min-Max | Standard Deviation |
|:----------|:-----:|:-------:|:-------------:|
| UV irradiance (W/m²/nm, 340 nm) | 0.68 | 0.52-0.89 | ± 0.12 |
| Air temperature (°C) | 28.4 | 21.2-36.7 | ± 3.8 |
| Relative humidity (%) | 72.1 | 48-92 | ± 11.4 |
| Accumulated precipitation (mm/month) | 87.3 | 12-186 | ± 52.1 |
| Average UV index | 8.2 | 6-11 | ± 1.3 |
| Wind velocity (m/s) | 2.1 | 0.8-4.5 | ± 0.9 |

**Figure S1.** Temporal variation of environmental conditions during the experimental period (180 days).

![Environmental Conditions](../3-IMAGENS/grafico_tratamentos_ggplot.png){width="85%"}

### S1.4 Activation Energy Calibration

Experimental determination of activation energy ($E_a$) for *Typha domingensis* degradation was conducted through comparative analysis between degradation rates under accelerated conditions (UV chamber) and natural field conditions, utilizing the Arrhenius relationship (Equation S1):

$$
\ln\left(\frac{k_{\text{chamber}}}{k_{\text{field}}}\right) = \frac{E_a}{R} \left( \frac{1}{T_{\text{field}}} - \frac{1}{T_{\text{chamber}}} \right) \tag{S1}
$$

where $k$ represents degradation rate, $R$ is the universal gas constant (8.314 J mol⁻¹ K⁻¹), and $T$ are absolute temperatures (K). The methodology consisted of:

1. **Determination of $k_{\text{chamber}}$**: Untreated *Typha* samples (T0) were exposed in an accelerated degradation chamber at 40°C (313.15 K) with UV irradiance of 0.89 W/m²/nm (340 nm). Tensile strength loss was monitored at 6-hour intervals during 10 days, fitting a first-order exponential model: $\sigma(t) = \sigma_0 \exp(-k_{\text{chamber}} \cdot t)$. Nonlinear least-squares fitting yielded $k_{\text{chamber}} = 0.0287$ day⁻¹ ($R^2 = 0.94$).

2. **Determination of $k_{\text{field}}$**: Identical samples were field-exposed at UFS Rural Campus (São Cristóvão-SE) during 180 days at mean temperature of 26°C (299.15 K) and UV irradiance of 0.68 W/m²/nm. The same fitting protocol resulted in $k_{\text{field}} = 0.0170$ day⁻¹ ($R^2 = 0.91$).

3. **Calculation of $E_a$**: Substituting values in Equation S1:

$$
\ln\left(\frac{0.0287}{0.0170}\right) = \frac{E_a}{8.314} \left( \frac{1}{299.15} - \frac{1}{313.15} \right)
$$

$$
0.5216 = \frac{E_a}{8.314} \times 1.5 \times 10^{-4}
$$

$$
E_a = 29.03 \text{ kJ/mol}
$$

This value positions *Typha* at an intermediate level compared to other lignocellulosic fibers: coir presents $E_a = 42-48$ kJ/mol due to high lignin content, while jute exhibits $E_a = 24-28$ kJ/mol due to reduced lignified fraction.

**Figure S2.** Activation Energy calibration via Arrhenius plot for *Typha domingensis*. The plot relates $\ln(k)$ versus $1/T$, where the slope provides $-E_a/R$. Experimental points (■) represent UV chamber tests (313.15 K) and field tests (299.15 K), with error bars indicating 95% confidence interval.

![ ](../3-IMAGENS/grafico_arrhenius.png){width="70%"}

## S2. Extended Statistical Analysis

### S2.1 Statistical Power and Sample Size

**Figure S3.** Post-hoc statistical power analysis for different effect sizes (Cohen's *d*).

![Statistical Power](../3-IMAGENS/grafico_analise_poder_ggplot.png){width="75%"}

**Table S5.** Statistical power analysis for treatment comparisons.

| Comparison | Sample size | Cohen's d | Power (1-β) | α | Interpretation |
|:-----------|:----------:|:---------:|:-----------:|:-:|:--------------|
| T0 vs T2 | 44 | 1.34 | 0.95 | 0.05 | Excellent power |
| T0 vs T3 | 44 | 2.03 | 0.99 | 0.05 | Excellent power |
| T2 vs T3 | 44 | 0.68 | 0.82 | 0.05 | Adequate power |
| T1 vs T2 | 44 | 0.52 | 0.71 | 0.05 | Moderate power |

*Note:* To achieve 90% power in all comparisons, n ≥ 60 is recommended.

### S2.2 Normality and Homoscedasticity Tests

**Table S6.** Results of statistical assumption tests.

| Treatment | Shapiro-Wilk (W) | p-value | Levene (F) | p-value | Distribution |
|:-----------|:----------------:|:-------:|:----------:|:-------:|:-------------|
| T0 | 0.946 | 0.082 | - | - | Normal |
| T1 | 0.938 | 0.053 | - | - | Normal |
| T2 | 0.921 | 0.024 | - | - | Non-normal |
| T3 | 0.956 | 0.126 | - | - | Normal |
| **Global** | - | - | 3.82 | 0.024 | Heteroscedastic |

*Conclusion:* Violation of homogeneity of variances (p = 0.024) justifies the use of non-parametric tests (Kruskal-Wallis).

### S2.3 Bootstrap Confidence Intervals

**Figure S4.** Bootstrap distributions (1000 resamples) of Weibull parameters.

![Bootstrap Weibull](../3-IMAGENS/grafico_bootstrap_distribuicoes_ggplot.png){width="85%"}

**Table S7.** Bootstrap confidence intervals (95%) for Weibull parameters.

| Treatment | β (Shape) | 95% CI Bootstrap | η (Scale, days) | 95% CI Bootstrap | Median FUL (days) |
|:----------:|:---------:|:----------------:|:----------------:|:----------------:|:------------------:|
| T0 | 2.3 | [2.08 - 2.54] | 68 | [61.2 - 75.8] | 60.3 |
| T1 | 2.5 | [2.27 - 2.76] | 64 | [57.8 - 70.9] | 56.8 |
| T2 | 2.8 | [2.58 - 3.04] | 94 | [87.1 - 102.3] | 83.6 |
| T3 | 3.0 | [2.76 - 3.26] | 92 | [84.5 - 99.8] | 81.9 |

## S3. Complementary Microstructural Characterization

### S3.1 X-Ray Diffraction Analysis

**Table S8.** Crystallographic parameters derived from XRD.

| Treatment | CI (%) | I₀₀₂ (a.u.) | Iₐₘ (a.u.) | 2θ₀₀₂ (°) | FWHM (°) | Crystallite size (nm) |
|:-----------|:------:|:-----------:|:----------:|:---------:|:--------:|:----------------------:|
| T0 | 48.5 | 1842 | 948 | 22.4 | 2.18 | 7.2 |
| T1 | 52.1 | 1976 | 947 | 22.5 | 2.04 | 7.6 |
| T2 | 58.3 | 2314 | 964 | 22.6 | 1.87 | 8.4 |
| T3 | 62.3 | 2587 | 975 | 22.7 | 1.72 | 9.5 |

*CI: Crystallinity Index; FWHM: Full Width at Half Maximum*

### S3.2 Morphometric Analysis (SEM)

**Table S9.** Quantitative surface parameters obtained via image processing (100 µm scale, 500×).

| Treatment | Porosity (%) | Relative Density (%) | Roughness (a.u.) |
|:-----------|:--------------:|:----------------------:|:-----------------:|
| T0 (Natural)| 75.8 | 26.9 | 452 |
| T1 (3% NaOH)| 84.9 | 24.0 | 221 |
| T2 (6% NaOH)| 52.7 | 24.2 | 720 |
| T3 (9% NaOH)| 26.3 | 26.5 | 1549 |

### S3.3 FTIR Spectroscopy - Characteristic Bands

**Table S10.** FTIR band assignment and intensity ratios.

| Wavenumber (cm⁻¹) | Assignment | T0 | T2 | T3 | Variation T0→T3 |
|:---------------------:|:-----------|:--:|:--:|:--:|:--------------:|
| 3400 | O-H stretching | 1.00 | 0.87 | 0.78 | -22% |
| 2920 | C-H stretching | 0.45 | 0.43 | 0.41 | -9% |
| 1735 | C=O hemicellulose | 0.62 | 0.38 | 0.24 | -61% |
| 1635 | H-O-H adsorbed water | 0.38 | 0.29 | 0.22 | -42% |
| 1505 | C=C aromatic (lignin) | 0.71 | 0.69 | 0.68 | -4% |
| 1430 | CH₂ scissoring | 0.52 | 0.54 | 0.55 | +6% |
| 1375 | C-H bending | 0.48 | 0.51 | 0.53 | +10% |
| 1060 | C-O-C cellulose | 1.00 | 1.12 | 1.18 | +18% |
| 898 | β-glycosidic | 0.34 | 0.38 | 0.41 | +21% |

*Intensities normalized to the 1060 cm⁻¹ band (C-O-C cellulose).*

### S3.4 Thermogravimetric Analysis (TGA)

**Table S11.** Characteristic decomposition temperatures and residues.

| Treatment | T₅% (°C) | T₁₀% (°C) | Tₘₐₓ₁ (°C) | Tₘₐₓ₂ (°C) | Residue 600°C (%) |
|:-----------|:--------:|:---------:|:----------:|:----------:|:-----------------:|
| T0 | 218 | 251 | 289 | 342 | 22.4 |
| T1 | 226 | 258 | 293 | 346 | 24.1 |
| T2 | 238 | 271 | 301 | 351 | 26.8 |
| T3 | 247 | 284 | 308 | 356 | 28.3 |

*T₅%, T₁₀%: temperatures with 5% and 10% mass loss*  
*Tₘₐₓ₁: hemicellulose peak; Tₘₐₓ₂: cellulose peak*

## S4. Mechanical Properties - Complete Data

### S4.1 Tensile Strength - Mean Values Over Time

**Table S12.** Maximum tensile strength (MPa) over exposure time.

| Time (days) | T0 | T1 | T2 | T3 |
|:------------:|:--:|:--:|:--:|:--:|
| 0 | 28.4 ± 4.2 | 32.1 ± 3.8 | 35.7 ± 3.1 | 38.9 ± 2.9 |
| 30 | 18.2 ± 5.1 | 22.4 ± 4.6 | 28.3 ± 3.4 | 31.2 ± 3.0 |
| 60 | 12.3 ± 4.8 | 16.8 ± 5.2 | 23.1 ± 3.9 | 25.7 ± 3.2 |
| 90 | 8.1 ± 3.9 | 12.5 ± 4.7 | 18.6 ± 4.1 | 21.3 ± 3.5 |
| 120 | 5.5 ± 3.3 | 9.2 ± 4.2 | 14.8 ± 4.3 | 18.2 ± 3.8 |
| 150 | 3.8 ± 2.7 | 7.1 ± 3.8 | 11.9 ± 4.5 | 15.6 ± 4.1 |
| 180 | 2.4 ± 2.1 | 5.3 ± 3.2 | 9.4 ± 4.2 | 13.1 ± 4.3 |

**Table S13.** Maximum deformation at rupture (%) over time.

| Time (days) | T0 | T1 | T2 | T3 |
|:------------:|:--:|:--:|:--:|:--:|
| 0 | 8.7 ± 1.2 | 7.9 ± 1.1 | 7.1 ± 0.9 | 5.8 ± 0.7 |
| 30 | 6.2 ± 1.4 | 5.8 ± 1.3 | 5.4 ± 1.0 | 4.2 ± 0.8 |
| 60 | 4.3 ± 1.1 | 4.5 ± 1.2 | 4.6 ± 1.1 | 3.5 ± 0.9 |
| 90 | 2.8 ± 0.9 | 3.4 ± 1.0 | 3.8 ± 1.0 | 2.9 ± 0.8 |
| 120 | 1.9 ± 0.7 | 2.6 ± 0.9 | 3.1 ± 0.9 | 2.4 ± 0.7 |
| 150 | 1.3 ± 0.5 | 2.0 ± 0.7 | 2.7 ± 0.8 | 2.0 ± 0.6 |
| 180 | 0.9 ± 0.4 | 1.6 ± 0.6 | 2.3 ± 0.7 | 1.7 ± 0.6 |

### S4.2 Degradation Kinetics Parameters

**Table S14.** Degradation constants ($k$) and half-life times ($t_{1/2}$).

| Property | Treatment | k (day⁻¹) | 95% CI | t₁/₂ (days) | R² |
|:-----------|:----------:|:---------:|:------:|:-----------:|:--:|
| Strength | T0 | 0.0142 | [0.0128-0.0156] | 48.8 | 0.96 |
| | T1 | 0.0118 | [0.0105-0.0131] | 58.7 | 0.95 |
| | T2 | 0.0082 | [0.0074-0.0090] | 84.5 | 0.97 |
| | T3 | 0.0076 | [0.0068-0.0084] | 91.2 | 0.98 |
| Ductility | T0 | 0.0355 | [0.0312-0.0398] | 19.5 | 0.93 |
| | T1 | 0.0287 | [0.0251-0.0323] | 24.1 | 0.94 |
| | T2 | 0.0218 | [0.0192-0.0244] | 31.8 | 0.96 |
| | T3 | 0.0198 | [0.0174-0.0222] | 35.0 | 0.95 |

## S5. Complementary Images

**Figure S5.** Mechanical testing equipment - EMIC DL-3000 Universal Testing Machine.

![Universal Testing Machine](../3-IMAGENS/maquina_universal.png){width="70%"}

**Figure S6.** Visual degradation patterns after 90 days of exposure - treatment comparison.

![90-day Degradation](../3-IMAGENS/degradacao_tracao_naoh.png){width="85%"}

**Figure S7.** Detailed stress-strain curves at 30 days for all treatments.

![30-day Tension](../3-IMAGENS/tracao_30dias_todos_tratamentos.png){width="80%"}

**Figure S8.** Detailed stress-strain curves at 90 days for all treatments.

![90-day Tension](../3-IMAGENS/tracao_90dias_todos_tratamentos.png){width="80%"}

**Figure S9.** Complete panel of statistical analyses and multiple comparisons.

![Analysis Panel](../3-IMAGENS/painel_completo_analises_ggplot.png){width="95%"}

## S6. Analytical Protocols - Standard Operating Procedures

### S6.1 Determination of Crystallinity Index by XRD

**Protocol:**

1. Sample grinding (<150 µm) in cryogenic mill
2. Oven drying (60°C, 24h)
3. Sample holder preparation with uniform compaction
4. Scanning: 2θ = 5-40°, speed 2°/min
5. CuKα radiation (λ = 1.5406 Å), 40 kV, 30 mA
6. Calculation: $CI = \frac{I_{002} - I_{am}}{I_{002}} \times 100$
   - $I_{002}$: peak intensity at 2θ ≈ 22.5°
   - $I_{am}$: valley intensity at 2θ ≈ 18°

### S6.2 Sample Preparation for SEM

**Protocol:**

1. Fragmentation into 10 mm × 5 mm sections
2. Mounting on aluminum stub with conductive carbon tape
3. Metallization: Au/Pd (60:40), 15 nm thickness
4. Sputter coater: 20 mA, 60 s
5. Storage in desiccator (<30% RH)
6. Imaging: 15 kV, high vacuum, magnifications 100× to 5,000×. For quantitative porosity and roughness analysis, standardized images with 500× magnification and 100 µm scale were used.

### S6.3 Tensile Test - ASTM D5035 Procedure

**Protocol:**

1. Specimen cutting: 200 mm × 50 mm
2. Conditioning: 23 ± 2°C, 50 ± 5% RH, 24h
3. Marking: gauge length 100 mm
4. Grip mounting: torque 45 N·m
5. Preload: 2 N
6. Speed: 20 mm/min
7. Acquisition: 100 Hz
8. Stop criterion: >80% drop from maximum force

## S7. Available Raw Data

Complete raw data are available in the online repository:

- **Tensile strength:** `dados_tracao_detalhados.csv` (n=264 tests)
- **Weibull analysis:** `dados_brutos_weibull.csv` (n=44 samples)
- **SEM morphometry:** `dados_morfometria_mev.csv` (n=120 images)
- **FTIR spectroscopy:** `espectros_ftir_brutos/` (264 .csv spectra)
- **XRD:** `dados_drx_brutos/` (48 .xy diffractograms)
- **Analysis scripts:** `scripts_R/` and `scripts_Python/`

**Repository:** <https://doi.org/10.17632/n4g296wjx5.1> (to be updated after acceptance)

---

**Correspondence for supplementary data:**  
Luiz Diego Vidal Santos  
E-mail: diego.vidal@academico.ufs.br  
ORCID: 0000-0002-XXXX-XXXX
