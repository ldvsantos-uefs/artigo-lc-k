import pandas as pd
from pathlib import Path

P = Path(__file__).resolve().parents[1] / 'processed_data' / 'tracao_taboa_combined.csv'
print('Arquivo:', P)
if not P.exists():
    print('Arquivo não encontrado. Saindo.')
    raise SystemExit(1)

df = pd.read_csv(P)
print('Linhas:', len(df))
print('Colunas:', df.columns.tolist())

if 'days' in df.columns:
    uniq = pd.unique(df['days'])
    print('Dias únicos (amostra 50):', uniq[:50])
    print('Tipo da coluna days:', df['days'].dtype)
    # show value counts for first 20
    print('\nContagem por days (top 20):')
    print(df['days'].astype(str).value_counts().head(20).to_string())
else:
    print('Coluna days ausente')

if 'treatment' in df.columns:
    print('\nTratamentos únicos:', pd.unique(df['treatment'])[:50])

print('\nExemplo (head):')
print(df.head(20).to_string())
