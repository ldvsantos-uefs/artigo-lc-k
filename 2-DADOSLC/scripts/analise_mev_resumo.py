import pandas as pd

df = pd.read_csv('2-DADOSLC/mev_fraturas_temporal.csv')

print("\n" + "="*70)
print("ANÁLISE RESUMIDA DE MORFOMETRIA MEV POR TRATAMENTO")
print("="*70)

for trat in ['ST', 'DC']:
    subset = df[df['Tratamento'] == trat]
    print(f"\n=== {trat} (N={len(subset)} imagens) ===")
    print(f"Densidade fraturas (mm⁻²): {subset['densidade_fraturas_mm2'].mean():.2f} ± {subset['densidade_fraturas_mm2'].std():.2f}")
    print(f"Severidade (%): {subset['severidade_percent'].mean():.2f} ± {subset['severidade_percent'].std():.2f}")
    print(f"Porosidade (%): {subset['porosidade_percent'].mean():.2f} ± {subset['porosidade_percent'].std():.2f}")
    print(f"Rugosidade (µm): {subset['rugosidade_um'].mean():.2f} ± {subset['rugosidade_um'].std():.2f}")

# Comparação entre tempos
print("\n" + "="*70)
print("EVOLUÇÃO TEMPORAL")
print("="*70)

for tempo in sorted(df['Tempo_dias'].unique()):
    print(f"\n--- TEMPO: {tempo} dias ---")
    for trat in ['ST', 'DC']:
        subset = df[(df['Tratamento'] == trat) & (df['Tempo_dias'] == tempo)]
        if len(subset) > 0:
            print(f"  {trat}: Densidade={subset['densidade_fraturas_mm2'].mean():.1f}, Severidade={subset['severidade_percent'].mean():.1f}%, Porosidade={subset['porosidade_percent'].mean():.1f}%, Rugosidade={subset['rugosidade_um'].mean():.1f}")

# Variações relativas
print("\n" + "="*70)
print("DIFERENÇAS RELATIVAS (DC - ST) / ST * 100%")
print("="*70)

st_overall = df[df['Tratamento'] == 'ST']
dc_overall = df[df['Tratamento'] == 'DC']

for metrica in ['densidade_fraturas_mm2', 'severidade_percent', 'porosidade_percent', 'rugosidade_um']:
    st_mean = st_overall[metrica].mean()
    dc_mean = dc_overall[metrica].mean()
    diff_pct = ((dc_mean - st_mean) / st_mean) * 100
    print(f"{metrica:30s}: ST={st_mean:8.2f}, DC={dc_mean:8.2f}, Diferença={diff_pct:+7.1f}%")
