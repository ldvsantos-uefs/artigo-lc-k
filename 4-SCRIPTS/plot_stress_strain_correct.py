"""
Script para plotar gráficos de tensão (stress) vs. deformação (strain)
para todos os tratamentos (T0, T1, T2, T3, TE) em 30 e 90 dias.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

# Configurações
RAW_IMPORTS = Path("2-DADOSLC/raw_imports/TABOA")
OUTPUT_DIR = Path("2-DADOSLC/processed_data/plots")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Cores para cada tratamento
COLORS = {
    "T0": "#1f77b4",  # azul
    "T1": "#ff7f0e",  # laranja
    "T2": "#2ca02c",  # verde
    "T3": "#d62728",  # vermelho
    "TE": "#9467bd",  # roxo
}

TREATMENTS = ["T0", "T1", "T2", "T3", "TE"]

# Mapeamento de rótulos descritivos
TREATMENT_LABELS = {
    "T0": "Controle (0%)",
    "T1": "3% NaOH",
    "T2": "6% NaOH",
    "T3": "9% NaOH",
    "TE": "12% NaOH",
}


def extract_metadata(file_path):
    """Extrai dias e tratamento do caminho do arquivo."""
    parts = file_path.parts
    
    # Buscar dias a partir do nome da pasta (ex: "30 DIAS")
    days = None
    for part in parts:
        if "DIAS" in part.upper():
            # Extract number from "30 DIAS", "90 DIAS", etc.
            try:
                days = int(part.split()[0])
                break
            except (ValueError, IndexError):
                pass
    
    # Buscar tratamento a partir do nome do arquivo
    treatment = None
    filename = file_path.name
    for t in TREATMENTS:
        if f"-{t}-" in filename:
            treatment = t
            break
    
    return days, treatment


def read_specimen_data(csv_path):
    """Lê arquivo CSV de espécime individual, extraindo strain e stress."""
    try:
        # Ler arquivo com encoding latin1 (padrão para esses arquivos)
        with open(csv_path, "r", encoding="latin1") as f:
            lines = f.readlines()
        
        # Encontrar linha do header (contém "Deformação" e "Esforço")
        header_idx = None
        for i, line in enumerate(lines):
            if "Deforma" in line and "Esfor" in line:
                header_idx = i
                break
        
        if header_idx is None:
            print(f"  ⚠ Header não encontrado em {csv_path.name}")
            return None
        
        # Ler CSV a partir do header (pular 2 linhas: cabeçalho + unidades)
        df = pd.read_csv(
            csv_path,
            sep=";",
            decimal=",",
            skiprows=header_idx + 1,  # +1 para pular linha de unidades
            encoding="latin1"
        )
        
        # Coluna de strain é sempre a 4ª coluna (índice 3): "Deformação à tracção"
        # Coluna de stress é sempre a 5ª coluna (índice 4): "Esforço à tracção"
        if df.shape[1] < 5:
            print(f"  ⚠ Arquivo {csv_path.name} tem menos de 5 colunas")
            return None
        
        # Usar índices de coluna (strain=col 3, stress=col 4)
        strain = pd.to_numeric(df.iloc[:, 3], errors="coerce").dropna()
        stress = pd.to_numeric(df.iloc[:, 4], errors="coerce").dropna()
        
        if len(strain) == 0 or len(stress) == 0:
            print(f"  ⚠ Nenhum dado válido em {csv_path.name}")
            return None
        
        # Garantir mesmo comprimento
        min_len = min(len(strain), len(stress))
        return {
            "strain": strain.iloc[:min_len].values,
            "stress": stress.iloc[:min_len].values
        }
    
    except Exception as e:
        print(f"  ✗ Erro ao ler {csv_path.name}: {e}")
        return None


def main():
    """Função principal."""
    # Dicionário para armazenar dados: {(days, treatment): [(strain, stress), ...]}
    data_by_group = {}
    
    print("🔍 Lendo arquivos de dados brutos...")
    
    # Varrer todas as pastas de dias
    for days_folder in sorted(RAW_IMPORTS.glob("*DIAS")):
        if not days_folder.is_dir():
            continue
        
        # Extrair número de dias
        try:
            days = int(days_folder.name.split()[0])
        except (ValueError, IndexError):
            continue
        
        print(f"\n📅 Processando {days} DIAS")
        
        # Varrer todas as pastas de tratamento
        for treatment_folder in sorted(days_folder.glob("*")):
            if not treatment_folder.is_dir():
                continue
            
            # Extrair tratamento
            treatment = None
            for t in TREATMENTS:
                if f"-{t}-" in treatment_folder.name:
                    treatment = t
                    break
            
            if treatment is None:
                continue
            
            print(f"  📦 {treatment}")
            
            # Ler todos os espécimes dessa combinação (dias, tratamento)
            specimen_count = 0
            for specimen_file in sorted(treatment_folder.glob("Specimen_DadosEmBruto_*.csv")):
                data = read_specimen_data(specimen_file)
                if data is not None:
                    key = (days, treatment)
                    if key not in data_by_group:
                        data_by_group[key] = []
                    data_by_group[key].append(data)
                    specimen_count += 1
            
            print(f"    ✓ {specimen_count} espécimes lidos")
    
    print(f"\n📊 Total de grupos encontrados: {len(data_by_group)}")
    
    # Plotar gráficos para 30 e 90 dias
    for target_days in [30, 90]:
        print(f"\n📈 Gerando gráfico para {target_days} dias...")
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        has_data = False
        for treatment in TREATMENTS:
            key = (target_days, treatment)
            if key not in data_by_group:
                continue
            
            has_data = True
            data_list = data_by_group[key]
            print(f"  {treatment}: {len(data_list)} espécimes")
            
            # Plotar cada espécime dessa combinação
            for idx, data in enumerate(data_list):
                label = TREATMENT_LABELS[treatment] if idx == 0 else ""  # Label apenas primeira vez
                ax.plot(
                    data["strain"],
                    data["stress"],
                    color=COLORS[treatment],
                    alpha=0.7,
                    linewidth=1.5,
                    label=label
                )
        
        if not has_data:
            print(f"  ⚠ Nenhum dado para {target_days} dias")
            continue
        
        # Formatação do gráfico
        ax.set_xlabel("Deformação (mm/mm)", fontsize=12, fontweight="bold")
        ax.set_ylabel("Tensão (MPa)", fontsize=12, fontweight="bold")
        ax.set_title(f"Tensão vs. Deformação - {target_days} Dias", fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3, linestyle="--")
        
        # Definir escala fixa para facilitar comparação visual entre 30 e 90 dias
        # O usuário relatou que 30 dias vai até ~14 MPa. Definindo 20 MPa para garantir cobertura de todos os tratamentos (ex: T3 ~18 MPa)
        ax.set_ylim(0, 20)
        ax.set_xlim(0, 0.15) # Fixar também o x para comparação justa, se necessário. Mas o usuário pediu escala de tensão.
        
        # Remover duplicatas de labels
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), fontsize=11, loc="best")
        
        # Salvar figura
        output_path = OUTPUT_DIR / f"tracao_{target_days}dias_todos_tratamentos.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"  ✓ Salvo em: {output_path}")
        plt.close()
    
    print("\n✅ Pipeline concluído!")


if __name__ == "__main__":
    main()
