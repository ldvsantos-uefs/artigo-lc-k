"""
Verificar qual é o script que gerou o CSV processado corrompido
e qual foi a fonte usada (TRAÇÃO vs PUNÇÃO)
"""

import pandas as pd
import os

base_path = r"C:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K\2-DADOSLC"

print("="*80)
print("ANÁLISE DO CSV PROCESSADO - IDENTIFICAR ORIGEM E CORRUPCAO")
print("="*80)

csv_path = os.path.join(base_path, "processed_data/tracao_taboa_combined.csv")

# Ler com diferentes interpretações
print("\n1. Tentando ler com tipos mistos...")
try:
    df = pd.read_csv(csv_path, dtype=str)  # Ler tudo como string primeiro
    print(f"   Shape: {df.shape}")
    print(f"   Colunas: {list(df.columns)}")
    print(f"\n   Amostra das primeiras 5 linhas:")
    print(df.head())
    
    print(f"\n   Verificando values únicos em 'source_file':")
    print(df['source_file'].unique()[:5])
    
    print(f"\n   Verificando se há dados PUNÇÃO (não TRAÇÃO):")
    punção_files = df[df['source_file'].str.contains('PUNÇÃO', case=False, na=False)]
    print(f"   Linhas com PUNÇÃO: {len(punção_files)} de {len(df)}")
    
    if len(punção_files) > 0:
        print(f"   Primeiras PUNÇÃO encontradas:")
        print(punção_files.head())
        
    print(f"\n   Verificando se há dados TRAÇÃO:")
    tracao_files = df[df['source_file'].str.contains('TRAÇÃO', case=False, na=False)]
    print(f"   Linhas com TRAÇÃO: {len(tracao_files)} de {len(df)}")
    
except Exception as e:
    print(f"   ERRO: {e}")

# Procurar pelos scripts que geraram este arquivo
print("\n\n2. PROCURANDO SCRIPTS QUE GERARAM O CSV PROCESSADO...")
print("-" * 80)

scripts_path = os.path.join(base_path, "scripts")
if os.path.exists(scripts_path):
    for file in os.listdir(scripts_path):
        if file.endswith('.py'):
            filepath = os.path.join(scripts_path, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if 'tracao_taboa_combined' in content:
                    print(f"\n   ENCONTRADO: {file}")
                    print(f"   Referências a 'tracao_taboa_combined':")
                    for i, line in enumerate(content.split('\n'), 1):
                        if 'tracao_taboa_combined' in line:
                            print(f"      Linha {i}: {line.strip()}")

print("\n\n" + "="*80)
