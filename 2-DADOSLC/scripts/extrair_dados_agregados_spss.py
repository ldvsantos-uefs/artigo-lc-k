"""
Extrai dados agregados de resistência à tração do arquivo SPSS.
Gera CSV consolidado com valores de UTS (Ultimate Tensile Strength) 
para todos os períodos: 30, 60, 90, 120, 150, 180 dias.

Este arquivo será usado para:
- Análises estatísticas
- Modelagem de Weibull
- Cálculo de VUF (Vida Útil Funcional)
- Geração de relatórios

Fonte: tracao/Dados completos.sav (72 linhas, n=3 espécimes por célula)
Output: processed_data/dados_tracao_agregados.csv
"""

import pandas as pd
import pyreadstat
from pathlib import Path
import numpy as np

# Caminhos
BASE_PATH = Path(__file__).resolve().parents[1]
SPSS_PATH = BASE_PATH / "tracao" / "Dados completos.sav"
OUTPUT_CSV = BASE_PATH / "processed_data" / "dados_tracao_agregados.csv"

print("="*80)
print("EXTRAÇÃO DE DADOS AGREGADOS DE TRAÇÃO - SPSS")
print("="*80)
print(f"\nArquivo fonte: {SPSS_PATH}")
print(f"Arquivo destino: {OUTPUT_CSV}")

# Ler arquivo SPSS
df, meta = pyreadstat.read_sav(str(SPSS_PATH))

print(f"\nDados lidos: {df.shape}")
print(f"Colunas disponíveis: {list(df.columns)}")

# Mapear nomes de colunas (SPSS pode ter nomes diferentes)
# Procurar coluna de resistência/stress
stress_col = None
for col in df.columns:
    col_lower = col.lower()
    if any(x in col_lower for x in ['esforço', 'esforco', 'tração', 'tracao', 'mpa', 'tensão', 'tensao', 'ruptura']):
        stress_col = col
        break

if stress_col is None:
    print("\n⚠️  Coluna de resistência não encontrada automaticamente.")
    print("Colunas disponíveis:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    stress_col = df.columns[5]  # Fallback: 6ª coluna geralmente é MPa
    print(f"\n→ Usando coluna: {stress_col}")
else:
    print(f"\n→ Coluna de resistência identificada: {stress_col}")

# Identificar colunas de tratamento e dias
treat_col = 'TRATAMENTO'
dias_col = 'DIAS'
rep_col = 'REPETIÇÃO'

# Renomear para padronizar
df_clean = df.rename(columns={
    treat_col: 'tratamento',
    dias_col: 'dias',
    rep_col: 'repeticao',
    stress_col: 'uts_mpa'
})

# Mapear tratamentos numéricos para códigos
# 0.0 → T0, 3.0 → T1 (3% NaOH), 6.0 → T2, 9.0 → T3
tratamento_map = {
    0.0: 'T0',
    3.0: 'T1',  # 3% NaOH
    6.0: 'T2',  # 6% NaOH
    9.0: 'T3'   # 9% NaOH
}

df_clean['tratamento_codigo'] = df_clean['tratamento'].map(tratamento_map)

# Verificar se mapeamento funcionou
print(f"\nTratamentos encontrados:")
print(df_clean.groupby('tratamento')['tratamento_codigo'].first())

# Verificar períodos disponíveis
print(f"\nPeríodos disponíveis (dias):")
print(sorted(df_clean['dias'].dropna().unique()))

# Selecionar colunas relevantes
df_final = df_clean[['tratamento_codigo', 'dias', 'repeticao', 'uts_mpa']].copy()
df_final = df_final.rename(columns={'tratamento_codigo': 'treatment'})

# Remover NaNs
df_final = df_final.dropna(subset=['treatment', 'dias', 'uts_mpa'])

# Ordenar por tratamento, dias, repetição
df_final = df_final.sort_values(['treatment', 'dias', 'repeticao']).reset_index(drop=True)

# Estatísticas por grupo
print(f"\n{'='*80}")
print("ESTATÍSTICAS POR TRATAMENTO E PERÍODO")
print(f"{'='*80}")

summary = df_final.groupby(['treatment', 'dias'])['uts_mpa'].agg([
    ('n', 'count'),
    ('media_mpa', 'mean'),
    ('desvio_mpa', 'std'),
    ('cv_%', lambda x: (x.std() / x.mean() * 100) if x.mean() > 0 else np.nan),
    ('min_mpa', 'min'),
    ('max_mpa', 'max')
]).reset_index()

print("\n" + summary.to_string(index=False))

# Salvar CSV
df_final.to_csv(OUTPUT_CSV, index=False)

print(f"\n{'='*80}")
print(f"✅ ARQUIVO SALVO: {OUTPUT_CSV}")
print(f"   Total de linhas: {len(df_final)}")
print(f"   Tratamentos: {sorted(df_final['treatment'].unique())}")
print(f"   Períodos: {sorted(df_final['dias'].unique())} dias")
print(f"   Espécimes por célula: ~{df_final.groupby(['treatment', 'dias']).size().mean():.1f}")
print(f"{'='*80}")

# Verificar integridade
print(f"\n🔍 VERIFICAÇÃO DE INTEGRIDADE:")
missing_cells = []
for treat in ['T0', 'T1', 'T2', 'T3']:
    for dias in [30, 60, 90, 120, 150, 180]:
        n = len(df_final[(df_final['treatment'] == treat) & (df_final['dias'] == dias)])
        if n == 0:
            missing_cells.append(f"{treat}@{dias}d")
        elif n < 3:
            print(f"   ⚠️  {treat}@{dias}d: apenas {n} espécimes (esperado: 3)")

if missing_cells:
    print(f"\n   ⚠️  Células sem dados: {', '.join(missing_cells)}")
else:
    print(f"   ✅ Todas as células têm dados!")

print(f"\n{'='*80}")
print("CONCLUÍDO")
print(f"{'='*80}")
