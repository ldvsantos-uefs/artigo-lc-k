# -*- coding: utf-8 -*-
"""
SCRIPT CORRIGIDO - LOCALIZAÇÃO POVOADO TIGRE (PACATUBA/SE)
Correção do erro de LabelPlacement
"""

from qgis.core import (
    QgsProject, QgsVectorLayer, QgsGeometry, QgsPointXY, QgsFeature, 
    QgsField, QgsPrintLayout, QgsLayoutItemMap, QgsLayoutItemLabel, 
    QgsLayoutItemLegend, QgsLayoutItemScaleBar, QgsLayoutPoint, 
    QgsLayoutSize, QgsUnitTypes, QgsCoordinateReferenceSystem,
    QgsLayoutExporter, QgsLayoutItemMapGrid, QgsPalLayerSettings, 
    QgsVectorLayerSimpleLabeling, QgsTextFormat, QgsSimpleFillSymbolLayer,
    QgsLayoutSize, QgsLayoutMeasurement
)
from qgis.PyQt.QtGui import QColor, QFont, QPageSize
from qgis.PyQt.QtCore import QVariant, Qt
import os
import sys

# === CONFIGURAÇÕES ===
OUTPUT_FOLDER = r"C:\Users\vidal\OneDrive\Documentos" 
LAT = -10.5909455
LON = -36.6691517
NOME_PONTO = "Povoado Tigre"
NOME_MUNICIPIO = "Pacatuba"

print(f"=== GERANDO MAPA PARA {NOME_MUNICIPIO} ===")

project = QgsProject.instance()

# 1. FUNÇÃO PARA ACHAR CAMADAS PELO NOME
def find_layer(name_key):
    for layer in project.mapLayers().values():
        if name_key.lower() == layer.name().lower():
            return layer
    return None

# Busca as camadas
lyr_br = find_layer("Brasil")
lyr_se = find_layer("Sergipe")
lyr_pac = find_layer("Pacatuba")

# Verificação de segurança
if not lyr_pac:
    print("ERRO: Não encontrei a camada 'Pacatuba'. Renomeie a camada na lateral para 'Pacatuba'.")
    sys.exit()
if not lyr_se:
    print("ERRO: Não encontrei a camada 'Sergipe'. Renomeie a camada na lateral para 'Sergipe'.")
    sys.exit()

# 2. CRIAR PONTO DO POVOADO (Memória)
lyr_ponto = QgsVectorLayer("Point?crs=EPSG:4326", "Localidades", "memory")
pr = lyr_ponto.dataProvider()
pr.addAttributes([QgsField("nome", QVariant.String)])
lyr_ponto.updateFields()
f = QgsFeature()
f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(LON, LAT)))
f.setAttributes([NOME_PONTO])
pr.addFeature(f)
lyr_ponto.updateExtents()
project.addMapLayer(lyr_ponto)

# 3. ESTILOS

def style_polygon(layer, fill, stroke, width=0.2):
    if layer:
        sym = layer.renderer().symbol()
        sym.setColor(QColor(fill))
        sym.symbolLayer(0).setStrokeColor(QColor(stroke))
        sym.symbolLayer(0).setStrokeWidth(width)
        layer.triggerRepaint()

style_polygon(lyr_br,  "#FFFFFF", "#888888", 0.2) # Brasil
style_polygon(lyr_se,  "#98FB98", "#228B22", 0.4) # Sergipe
style_polygon(lyr_pac, "#FFE4B5", "#8B4513", 0.8) # Pacatuba

# Estilo do Ponto
sym_pt = lyr_ponto.renderer().symbol()
sym_pt.setColor(QColor("red"))
sym_pt.setSize(4.5)
sym_pt.symbolLayer(0).setStrokeColor(QColor("white"))
sym_pt.symbolLayer(0).setStrokeWidth(0.6)

# --- CORREÇÃO DO RÓTULO (LABEL) ---
settings = QgsPalLayerSettings()
settings.fieldName = "nome"

# Usar AroundPoint que é mais compatível
settings.placement = QgsPalLayerSettings.AroundPoint

fmt = QgsTextFormat()
fmt.setFont(QFont("Arial", 10, QFont.Bold))
fmt.setColor(QColor("black"))
buffer = fmt.buffer()
buffer.setEnabled(True)
buffer.setColor(QColor("white"))
settings.setFormat(fmt)
settings.yOffset = 0 # Ajuste fino não é necessário no modo automático
settings.dist = 2 # Distância do ponto em mm

labeling = QgsVectorLayerSimpleLabeling(settings)
lyr_ponto.setLabelsEnabled(True)
lyr_ponto.setLabeling(labeling)
lyr_ponto.triggerRepaint()

# 4. MONTAGEM DO LAYOUT (ESTILO ACADÊMICO - 2 COLUNAS)
# Remove layout anterior se existir
layout_name = f"Mapa_{NOME_MUNICIPIO}_Tigre_V3_Final"
for layout_existing in project.layoutManager().layouts():
    if layout_existing.name() == layout_name:
        project.layoutManager().removeLayout(layout_existing)

layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName(layout_name)
project.layoutManager().addLayout(layout)

# Configurar Página A4 Paisagem (297mm x 210mm)
page = layout.pageCollection().pages()[0]
page.setPageSize(QgsLayoutSize(297, 210, QgsUnitTypes.LayoutMillimeters))

crs_dest = QgsCoordinateReferenceSystem("EPSG:4674") # SIRGAS 2000

# === COLUNA LATERAL (ESQUERDA) ===

# 1. Título Principal
title = QgsLayoutItemLabel(layout)
title.setText(f"LOCALIZAÇÃO\n{NOME_MUNICIPIO.upper()} - SE")
title.setFont(QFont("Arial", 16, QFont.Bold))
title.setHAlign(Qt.AlignHCenter)
title.setVAlign(Qt.AlignVCenter)
title.setRect(10, 10, 75, 20)
title.setFrameEnabled(True)
title.setFrameStrokeWidth(QgsLayoutMeasurement(0.5, QgsUnitTypes.LayoutMillimeters))
title.setBackgroundColor(QColor("white"))
title.setBackgroundEnabled(True)
layout.addLayoutItem(title)

# 2. Inset Brasil (Destaque Sergipe)
map_br = QgsLayoutItemMap(layout)
map_br.setRect(10, 35, 75, 75)
map_br.setCrs(crs_dest)
if lyr_br:
    map_br.setExtent(lyr_br.extent())
    map_br.setLayers([lyr_se, lyr_br]) # Ordem: Sergipe em cima do Brasil
else:
    map_br.setExtent(lyr_se.extent())
map_br.setFrameEnabled(True)
map_br.setBackgroundColor(QColor("#F0F8FF")) # AliceBlue
layout.addLayoutItem(map_br)

lbl_br = QgsLayoutItemLabel(layout)
lbl_br.setText("Brasil")
lbl_br.setFont(QFont("Arial", 10, QFont.Bold))
lbl_br.adjustSizeToText()
lbl_br.setPos(12, 37)
layout.addLayoutItem(lbl_br)

# 3. Inset Sergipe (Destaque Município)
map_se = QgsLayoutItemMap(layout)
map_se.setRect(10, 115, 75, 75)
map_se.setCrs(crs_dest)
ext_se = lyr_se.extent()
ext_se.scale(1.05)
map_se.setExtent(ext_se)
map_se.setLayers([lyr_pac, lyr_se]) # Ordem: Município em cima de Sergipe
map_se.setFrameEnabled(True)
map_se.setBackgroundColor(QColor("white"))
layout.addLayoutItem(map_se)

lbl_se = QgsLayoutItemLabel(layout)
lbl_se.setText("Sergipe")
lbl_se.setFont(QFont("Arial", 10, QFont.Bold))
lbl_se.adjustSizeToText()
lbl_se.setPos(12, 117)
layout.addLayoutItem(lbl_se)

# === MAPA PRINCIPAL (DIREITA) ===
map_main = QgsLayoutItemMap(layout)
map_main.setRect(90, 10, 197, 190) # Ocupa o resto da página
map_main.setCrs(crs_dest)

# Ajustar Extensão para focar no Município com margem
ext_pac = lyr_pac.extent()
ext_pac.scale(1.2) # Zoom out leve para contexto
map_main.setExtent(ext_pac)

# Camadas: Ponto em cima, Município, Sergipe (fundo)
layers_main = [lyr_ponto, lyr_pac, lyr_se]
map_main.setLayers(layers_main) 
map_main.setFrameEnabled(True)
map_main.setFrameStrokeWidth(QgsLayoutMeasurement(1.5, QgsUnitTypes.LayoutMillimeters)) # Borda mais grossa
map_main.setBackgroundColor(QColor("#E0FFFF")) # LightCyan (água/fundo)

# Grade de Coordenadas
grid = map_main.grid()
grid.setEnabled(True)
grid.setIntervalX(0.04)
grid.setIntervalY(0.04)
grid.setAnnotationEnabled(True)
grid.setFrameStyle(QgsLayoutItemMapGrid.Zebra)
grid.setAnnotationFont(QFont("Arial", 8))
grid.setAnnotationPrecision(2)
grid.setAnnotationPosition(QgsLayoutItemMapGrid.OutsideMapFrame, QgsLayoutItemMapGrid.Left | QgsLayoutItemMapGrid.Bottom | QgsLayoutItemMapGrid.Right | QgsLayoutItemMapGrid.Top)
layout.addLayoutItem(map_main)

# === ELEMENTOS FINAIS ===

# Seta Norte (Canto Superior Direito do Mapa Principal)
norte = QgsLayoutItemLabel(layout)
norte.setText("N")
norte.setFont(QFont("Arial", 24, QFont.Bold))
norte.adjustSizeToText()
# Posiciona relativo ao mapa principal
norte.setPos(270, 20)
layout.addLayoutItem(norte)

# Barra de Escala (Canto Inferior Esquerdo do Mapa Principal)
scale = QgsLayoutItemScaleBar(layout)
scale.setLinkedMap(map_main)
scale.applyDefaultSize()
scale.setNumberOfSegments(4)
scale.setUnits(QgsUnitTypes.DistanceKilometers)
scale.setUnitLabel("km")
scale.setFont(QFont("Arial", 9))
scale.setPos(100, 185)
layout.addLayoutItem(scale)

# Fonte e Informações (Rodapé da Coluna Lateral)
info_text = f"""
LOCALIDADE:
{NOME_PONTO}
Lat: {LAT}
Lon: {LON}

DATUM: SIRGAS 2000
FONTE: IBGE (2022)
ELABORAÇÃO: AUTOR (2025)
"""
info = QgsLayoutItemLabel(layout)
info.setText(info_text)
info.setFont(QFont("Arial", 9))
info.setVAlign(Qt.AlignTop)
info.setRect(10, 195, 75, 40)
layout.addLayoutItem(info)

print("✓ SUCESSO! Layout V3 (Estilo Acadêmico) gerado.")

exporter = QgsLayoutExporter(layout)
img_path = os.path.join(OUTPUT_FOLDER, f"Mapa_{NOME_MUNICIPIO}_Tigre_FINAL.png")
res = exporter.exportToImage(img_path, QgsLayoutExporter.ImageExportSettings())
if res == QgsLayoutExporter.Success:
    print(f"Imagem salva em: {img_path}")
    try:
        os.startfile(img_path)
    except:
        pass