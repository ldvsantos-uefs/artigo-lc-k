import pandas as pd
import os

def extrair_dados_reais():
    print("--- Extração de Dados Reais do DB.xlsx ---")
    
    arquivo_db = 'DB_original.xlsx'
    if not os.path.exists(arquivo_db):
        print(f"Erro: Arquivo {arquivo_db} não encontrado.")
        return

    try:
        # Ler o Excel
        df = pd.read_excel(arquivo_db)
        print("Colunas encontradas:", df.columns.tolist())
        
        # Tentar identificar colunas relevantes
        # Procurando por colunas que indiquem Tempo, Tratamento, Força/Tensão
        col_tempo = [c for c in df.columns if 'tempo' in c.lower() or 'dia' in c.lower() or 'ciclo' in c.lower()]
        col_tratamento = [c for c in df.columns if 'tratamento' in c.lower() or 'grupo' in c.lower() or 'amostra' in c.lower()]
        col_resistencia = [c for c in df.columns if 'tensao' in c.lower() or 'forca' in c.lower() or 'resistencia' in c.lower() or 'mpa' in c.lower() or 'tensão' in c.lower()]
        
        print(f"Possíveis colunas de Tempo/Ciclos: {col_tempo}")
        print(f"Possíveis colunas de Tratamento: {col_tratamento}")
        print(f"Possíveis colunas de Resistência: {col_resistencia}")
        
        # Se não achar coluna de tempo, tentar extrair do tratamento
        if not col_tempo and col_tratamento:
            print("Tentando extrair ciclos da coluna de tratamento...")
            # Exemplo: "Resinado_10JN" -> 10
            df['Ciclos'] = df[col_tratamento[0]].astype(str).str.extract(r'(\d+)').astype(float)
            col_tempo = ['Ciclos']
            print("Ciclos extraídos:", df['Ciclos'].unique())
            
        # Conversão consistente ciclos → dias (1 ciclo = 6 horas = 0.25 dias)
        if col_tempo:
            df['dias'] = df[col_tempo[0]] * 0.25
            print(f"Tempo convertido para dias: {df['dias'].unique()}")

        # Se conseguir identificar, mostrar um resumo dos dados agrupados
        if col_tempo and col_resistencia:
            tempo = col_tempo[0]
            resistencia = col_resistencia[0]
            tratamento = col_tratamento[0] if col_tratamento else None
            
            print(f"\nResumo dos dados usando: Tempo='{tempo}', Resistência='{resistencia}', Tratamento='{tratamento}'")
            
            if tratamento:
                # Agrupar por tratamento (limpo) e tempo
                # Criar coluna de grupo base (ex: "Resinado" de "Resinado_10JN")
                df['Grupo_Base'] = df[tratamento].astype(str).str.replace(r'\d+.*', '', regex=True).str.strip('_')
                
                # Extrair Tensão e Extensão se disponíveis
                cols_interesse = [resistencia]
                col_extensao = [c for c in df.columns if 'extensão' in c.lower() or 'deformação' in c.lower() or 'strain' in c.lower()]
                if col_extensao:
                    cols_interesse.append(col_extensao[0])
                    print(f"Incluindo coluna de extensão: {col_extensao[0]}")

                resumo = df.groupby(['Grupo_Base', tempo])[cols_interesse].mean().reset_index()
                print(resumo)
                
                # Salvar esse resumo para usar no modelo
                resumo.to_csv('dados_resumo_extraidos.csv', index=False)
                print("\nResumo salvo em 'dados_resumo_extraidos.csv'")
            else:
                resumo = df.groupby(tempo)[resistencia].mean().reset_index()
                print(resumo)
        
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")

if __name__ == "__main__":
    extrair_dados_reais()
