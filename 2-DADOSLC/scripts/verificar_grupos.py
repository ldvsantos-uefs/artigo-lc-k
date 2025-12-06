import pandas as pd

try:
    df = pd.read_excel('DB_original.xlsx')
    print("Colunas:", df.columns.tolist())
    
    # Find treatment column
    col_tratamento = [c for c in df.columns if 'tratamento' in c.lower() or 'grupo' in c.lower() or 'amostra' in c.lower()]
    if col_tratamento:
        print(f"Coluna de tratamento: {col_tratamento[0]}")
        print("Valores únicos:", df[col_tratamento[0]].unique())
    else:
        print("Não encontrei coluna de tratamento.")
        
except Exception as e:
    print(f"Erro: {e}")
