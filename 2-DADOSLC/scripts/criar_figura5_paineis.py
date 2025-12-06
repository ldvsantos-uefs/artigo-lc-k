"""
Script para criar Figura 5 com painéis (a) e (b)
Painel (a): degradacao_tracao_naoh.png
Painel (b): tracao_90dias_todos_tratamentos.png
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path

# Caminhos
base_path = Path(r"c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K")
img_path = base_path / "3-IMAGENS"

# Carregar imagens
img_a = mpimg.imread(img_path / "degradacao_tracao_naoh.png")
img_b = mpimg.imread(img_path / "tracao_90dias_todos_tratamentos.png")

# Criar figura com 2 painéis lado a lado
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Painel (a)
axes[0].imshow(img_a)
axes[0].axis('off')
axes[0].text(0.02, 0.98, '(a)', transform=axes[0].transAxes, 
             fontsize=16, fontweight='bold', va='top', ha='left',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Painel (b)
axes[1].imshow(img_b)
axes[1].axis('off')
axes[1].text(0.02, 0.98, '(b)', transform=axes[1].transAxes, 
             fontsize=16, fontweight='bold', va='top', ha='left',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Ajustar espaçamento
plt.tight_layout()

# Salvar
output_path = img_path / "figura5_paineis_ab.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Figura salva em: {output_path}")

plt.close()
