"""
Script para criar Figura 5 com painéis (a), (b) e (c)
Painel (a): degradacao_tracao_naoh.png
Painel (b): tracao_30dias_todos_tratamentos.png
Painel (c): tracao_90dias_todos_tratamentos.png
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path
import matplotlib.gridspec as gridspec

# Caminhos
base_path = Path(r"c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo-posdoc\1-ARTIGO_LC_K")
img_path = base_path / "3-IMAGENS"

# Carregar imagens
img_a = mpimg.imread(img_path / "degradacao_tracao_naoh.png")
img_b = mpimg.imread(img_path / "tracao_30dias_todos_tratamentos.png")
img_c = mpimg.imread(img_path / "tracao_90dias_todos_tratamentos.png")

# Criar figura com layout: (a) em cima, (b) e (c) embaixo
fig = plt.figure(figsize=(12, 10))
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])

# Painel (a) - Ocupa toda a largura superior
ax0 = fig.add_subplot(gs[0, :])
ax0.imshow(img_a)
ax0.axis('off')
ax0.text(0.02, 0.95, '(a)', transform=ax0.transAxes, 
         fontsize=16, fontweight='bold', va='top', ha='left',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Painel (b) - Esquerda inferior
ax1 = fig.add_subplot(gs[1, 0])
ax1.imshow(img_b)
ax1.axis('off')
ax1.text(0.02, 0.95, '(b)', transform=ax1.transAxes, 
         fontsize=16, fontweight='bold', va='top', ha='left',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Painel (c) - Direita inferior
ax2 = fig.add_subplot(gs[1, 1])
ax2.imshow(img_c)
ax2.axis('off')
ax2.text(0.02, 0.95, '(c)', transform=ax2.transAxes, 
         fontsize=16, fontweight='bold', va='top', ha='left',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Ajustar espaçamento
plt.tight_layout()

# Salvar
output_path = img_path / "figura5_paineis_ab.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Figura salva em: {output_path}")

plt.close()

